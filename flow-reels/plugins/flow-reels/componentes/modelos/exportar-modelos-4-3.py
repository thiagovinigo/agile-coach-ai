#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
exportar-modelos-4-3.py  ·  como os três ONNX da visão 4.3 foram feitos (para refazer, não para rodar sempre)

O pacote não tem torch, e não há ONNX oficial destes modelos no tamanho que o visao.py usa. Eles foram
exportados uma vez, num venv separado e temporário, e só os .onnx ficam em componentes/modelos/:

  vda-small-codificador.onnx  Video Depth Anything Small (Apache-2.0), o DINOv2-S quadro a quadro:
                              pixel [N, 3, H, W] (H e W múltiplos de 14, livres) -> c1..c4 [N, 384, H/14, W/14]
  vda-small-cabeca.onnx       a cabeça DPT temporal do mesmo modelo, numa janela de 32 quadros:
                              c1..c4 [32, 384, h, w] -> profundidade [32, 14h, 14w] (maior = mais perto)
  birefnet-lite-640.onnx      BiRefNet lite (MIT), recorte fino de cabelo, entrada fixa de 640:
                              imagem [1, 3, 640, 640] (ImageNet) -> alfa [1, 1, 640, 640] (0 a 1, já com sigmoide)

Os três guardam os pesos grandes em float16 com um Cast para float32 na frente (o arquivo cai à metade e
fica abaixo de 100 MB; o onnxruntime dobra o Cast ao abrir a sessão, então a conta continua em float32).

Como refazer (em torno de 2 GB de download, uns 10 minutos):

    uv venv --python 3.12 /tmp/exportar/venv
    VIRTUAL_ENV=/tmp/exportar/venv uv pip install torch torchvision onnx onnxruntime numpy einops easydict \
        opencv-python-headless tqdm timm transformers safetensors kornia
    # Video Depth Anything: o código (zip do main de github.com/DepthAnything/Video-Depth-Anything) e o peso
    #   huggingface.co/depth-anything/Video-Depth-Anything-Small/resolve/main/video_depth_anything_vits.pth
    #   (SÓ o Small: o Base e o Large são CC-BY-NC, não comerciais)
    # BiRefNet lite: birefnet.py, BiRefNet_config.py e model.safetensors de huggingface.co/ZhengPeng7/BiRefNet_lite
    /tmp/exportar/venv/bin/python exportar-modelos-4-3.py vda --src <pasta do Video-Depth-Anything> \
        --peso video_depth_anything_vits.pth --saida . --conferir
    /tmp/exportar/venv/bin/python exportar-modelos-4-3.py birefnet --hf <pasta do BiRefNet_lite> --lado 640 --saida .

O que muda em relação ao código original (só para o ONNX sair com tamanho livre e rodar no onnxruntime):
  - VDA: o interpolate_pos_encoding do DINOv2 usa o tamanho de saída em vez do fator com o deslocamento de
    0,1 (o fator em float prendia o ONNX no tamanho do traçado); a atenção temporal usa matmul no lugar do
    baddbmm sobre um torch.empty (que virava uma constante do tamanho da janela); o unflatten do lote vira
    unsqueeze (o Reshape dele quebrava o otimizador do onnxruntime 1.30). Medido no --conferir contra o
    torch original: erro máximo de 0,6% (364 x 210) e 1,0% (280 x 504) do valor máximo, quase todo da
    posição interpolada.
  - BiRefNet: a convolução deformável do torchvision vira o DeformConv do ONNX (opset 19), nativo no
    onnxruntime. O ONNX do rembg (birefnet-general-lite.onnx, 1024) faz a mesma conta com Gather/Scatter
    e levava ~15 s por quadro na CPU; este, em 640, leva ~0,5 a 0,7 s.
"""

import argparse
import importlib.util
import math
import sys
import types
from pathlib import Path


def pesos_em_meia(origem, destino):
    """Os pesos float32 com 4096 valores ou mais vão em float16, com um Cast para float32 na frente."""
    import numpy as np
    import onnx
    from onnx import TensorProto, helper, numpy_helper
    m = onnx.load(str(origem))
    g = m.graph
    novos, casts = [], []
    for t in list(g.initializer):
        if t.data_type == TensorProto.FLOAT and int(np.prod(t.dims)) >= 4096:
            nome16 = t.name + "__f16"
            novos.append(numpy_helper.from_array(numpy_helper.to_array(t).astype(np.float16), nome16))
            casts.append(helper.make_node("Cast", [nome16], [t.name], to=TensorProto.FLOAT, name=t.name + "__cast"))
            g.initializer.remove(t)
    g.initializer.extend(novos)
    nos = casts + list(g.node)
    del g.node[:]
    g.node.extend(nos)
    onnx.save(m, str(destino))
    print("  %s: %d pesos em float16" % (Path(destino).name, len(casts)))


# ---------------------------------------------------------------------------
# Video Depth Anything Small
# ---------------------------------------------------------------------------

def exportar_vda(a):
    import torch
    import torch.nn as nn
    import torch.nn.functional as F

    T = 32
    CAMADAS = [2, 5, 8, 11]
    sys.path.insert(0, str(Path(a.src).resolve()))
    from video_depth_anything.video_depth import VideoDepthAnything
    from video_depth_anything.motion_module.attention import CrossAttention

    def posicao_por_tamanho(self, x, w, h):
        N = self.pos_embed.shape[1] - 1
        pos = self.pos_embed.float()
        cls_pos, patch_pos = pos[:, 0], pos[:, 1:]
        dim = x.shape[-1]
        lado = int(math.sqrt(N))
        patch_pos = F.interpolate(patch_pos.reshape(1, lado, lado, dim).permute(0, 3, 1, 2),
                                  size=(w // self.patch_size, h // self.patch_size), mode="bicubic",
                                  antialias=self.interpolate_antialias, align_corners=False)
        patch_pos = patch_pos.permute(0, 2, 3, 1).reshape(1, -1, dim)
        return torch.cat((cls_pos.unsqueeze(0), patch_pos), dim=1).to(x.dtype)

    def atencao_sem_vazio(self, query, key, value, attention_mask=None):
        s = torch.matmul(query, key.transpose(-1, -2)) * self.scale
        return self.reshape_batch_dim_to_heads(torch.matmul(s.softmax(dim=-1), value))

    class Codificador(nn.Module):
        def __init__(self, m):
            super().__init__()
            self.p = m.pretrained
            self.p.interpolate_pos_encoding = types.MethodType(posicao_por_tamanho, self.p)

        def forward(self, x):
            n, _, h, w = x.shape
            feats = self.p.get_intermediate_layers(x, CAMADAS, return_class_token=True)
            return tuple(f[0].permute(0, 2, 1).reshape(n, f[0].shape[-1], h // 14, w // 14) for f in feats)

    class Cabeca(nn.Module):
        def __init__(self, m):
            super().__init__()
            self.h = m.head

        def forward(self, c1, c2, c3, c4):
            hd = self.h
            out = []
            for i, x in enumerate((c1, c2, c3, c4)):
                out.append(hd.resize_layers[i](hd.projects[i](x)))
            l1, l2, l3, l4 = out

            def tempo(mod, x):
                y, _ = mod(x.unsqueeze(0).permute(0, 2, 1, 3, 4), None, None, None)
                return y.permute(0, 2, 1, 3, 4).squeeze(0)

            l3 = tempo(hd.motion_modules[0], l3)
            l4 = tempo(hd.motion_modules[1], l4)
            r1, r2 = hd.scratch.layer1_rn(l1), hd.scratch.layer2_rn(l2)
            r3, r4 = hd.scratch.layer3_rn(l3), hd.scratch.layer4_rn(l4)
            p4 = tempo(hd.motion_modules[2], hd.scratch.refinenet4(r4, size=r3.shape[2:]))
            p3 = tempo(hd.motion_modules[3], hd.scratch.refinenet3(p4, r3, size=r2.shape[2:]))
            p2 = hd.scratch.refinenet2(p3, r2, size=r1.shape[2:])
            o = hd.scratch.output_conv1(hd.scratch.refinenet1(p2, r1))
            o = F.interpolate(o, size=(c1.shape[2] * 14, c1.shape[3] * 14), mode="bilinear", align_corners=True)
            return F.relu(hd.scratch.output_conv2(o)).squeeze(1)

    def carregar():
        m = VideoDepthAnything(encoder="vits", features=64, out_channels=[48, 96, 192, 384])
        m.load_state_dict(torch.load(a.peso, map_location="cpu"), strict=True)
        return m.eval()

    original = CrossAttention._attention
    m = carregar()
    CrossAttention._attention = atencao_sem_vazio
    cod, cab = Codificador(m).eval(), Cabeca(m).eval()
    saida = Path(a.saida)
    tmp_c, tmp_h = saida / "vda-codificador-f32.onnx", saida / "vda-cabeca-f32.onnx"
    h, w = 364, 210
    with torch.no_grad():
        torch.onnx.export(cod, (torch.randn(2, 3, h, w),), str(tmp_c), dynamo=False, opset_version=17,
                          input_names=["pixel"], output_names=["c1", "c2", "c3", "c4"],
                          dynamic_axes={"pixel": {0: "n", 2: "altura", 3: "largura"},
                                        **{c: {0: "n", 2: "h", 3: "w"} for c in ("c1", "c2", "c3", "c4")}})
        torch.onnx.export(cab, tuple(torch.randn(T, 384, h // 14, w // 14) for _ in range(4)), str(tmp_h),
                          dynamo=False, opset_version=17, input_names=["c1", "c2", "c3", "c4"],
                          output_names=["profundidade"],
                          dynamic_axes={**{c: {2: "h", 3: "w"} for c in ("c1", "c2", "c3", "c4")},
                                        "profundidade": {1: "altura", 2: "largura"}})
    pesos_em_meia(tmp_c, saida / "vda-small-codificador.onnx")
    pesos_em_meia(tmp_h, saida / "vda-small-cabeca.onnx")
    if a.conferir:
        import numpy as np
        import onnxruntime as ort
        CrossAttention._attention = original
        ref_m = carregar()
        sc = ort.InferenceSession(str(saida / "vda-small-codificador.onnx"), providers=["CPUExecutionProvider"])
        sh = ort.InferenceSession(str(saida / "vda-small-cabeca.onnx"), providers=["CPUExecutionProvider"])
        for hh, ww in ((364, 210), (280, 504)):
            x = torch.randn(T, 3, hh, ww)
            with torch.no_grad():
                ref = ref_m.forward(x[None])[0].numpy()
            d = sh.run(None, dict(zip(["c1", "c2", "c3", "c4"], sc.run(None, {"pixel": x.numpy()}))))[0]
            print("  conferência %dx%d: erro máximo %.2f%% do valor máximo"
                  % (hh, ww, 100.0 * float(np.abs(d - ref).max() / (np.abs(ref).max() + 1e-6))))
    tmp_c.unlink()
    tmp_h.unlink()


# ---------------------------------------------------------------------------
# BiRefNet lite
# ---------------------------------------------------------------------------

def exportar_birefnet(a):
    import torch
    from torch.onnx import symbolic_helper as sh

    @sh.parse_args("v", "v", "v", "v", "v", "i", "i", "i", "i", "i", "i", "i", "i", "b")
    def deform_conv2d(g, x, w, offset, mask, bias, s_h, s_w, p_h, p_w, d_h, d_w, grupos, grupos_off, usa_mascara):
        entradas = [x, w, offset, bias] + ([mask] if usa_mascara else [])
        return g.op("DeformConv", *entradas, dilations_i=[d_h, d_w], group_i=grupos, offset_group_i=grupos_off,
                    pads_i=[p_h, p_w, p_h, p_w], strides_i=[s_h, s_w])

    torch.onnx.register_custom_op_symbolic("torchvision::deform_conv2d", deform_conv2d, 19)
    hf = Path(a.hf).resolve()
    saida = Path(a.saida)
    local = saida / "_birefnet_local.py"
    local.write_text((hf / "birefnet.py").read_text(encoding="utf-8").replace(
        "from .BiRefNet_config import", "from BiRefNet_config import"), encoding="utf-8")
    sys.path.insert(0, str(hf))
    spec = importlib.util.spec_from_file_location("_birefnet_local", local)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    from BiRefNet_config import BiRefNetConfig
    from safetensors.torch import load_file
    m = mod.BiRefNet(BiRefNetConfig(bb_pretrained=False))
    m.load_state_dict(load_file(str(hf / "model.safetensors")), strict=True)

    class Embrulho(torch.nn.Module):
        def __init__(self, m):
            super().__init__()
            self.m = m

        def forward(self, x):
            return torch.sigmoid(self.m(x)[-1])

    e = Embrulho(m.eval()).eval()
    tmp = saida / "birefnet-f32.onnx"
    with torch.no_grad():
        torch.onnx.export(e, (torch.randn(1, 3, a.lado, a.lado),), str(tmp), opset_version=19, dynamo=False,
                          input_names=["imagem"], output_names=["alfa"])
    pesos_em_meia(tmp, saida / ("birefnet-lite-%d.onnx" % a.lado))
    tmp.unlink()
    local.unlink()


def principal():
    ap = argparse.ArgumentParser(description="exporta os ONNX da visão 4.3 (rode num venv com torch)")
    sub = ap.add_subparsers(dest="qual", required=True)
    v = sub.add_parser("vda")
    v.add_argument("--src", required=True)
    v.add_argument("--peso", required=True)
    v.add_argument("--saida", default=".")
    v.add_argument("--conferir", action="store_true")
    b = sub.add_parser("birefnet")
    b.add_argument("--hf", required=True)
    b.add_argument("--lado", type=int, default=640)
    b.add_argument("--saida", default=".")
    a = ap.parse_args()
    exportar_vda(a) if a.qual == "vda" else exportar_birefnet(a)


if __name__ == "__main__":
    principal()
