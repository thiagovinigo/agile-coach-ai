# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "whisperx",
#   "torch",
# ]
# ///
# -*- coding: utf-8 -*-
"""Transcricao local e gratuita: WhisperX na sua maquina, via uv.

E a rota alternativa. Nao custa nada e nao manda seu video para lugar nenhum,
mas na primeira vez baixa cerca de 1,5 GB (o WhisperX, o torch e o modelo) e,
em maquina sem placa de video, e lenta: transcrever uma hora de aula pode levar
mais de uma hora.

Uso (sempre com uv, que monta o ambiente sozinho):

    uv run local.py --entrada minha-aula.mp4 --projeto projetos/minha-aula

Se a sua maquina tem placa NVIDIA:

    uv run local.py --entrada aula.mp4 --projeto projetos/aula --dispositivo cuda

Saida: os tres arquivos do contrato, gravados pelo normalizar.py. A saida crua
fica em materiais-de-trabalho/transcricao/bruto-local.json, dentro da pasta do video.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import normalizar as nz  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


MODELOS = ["tiny", "base", "small", "medium", "large-v3"]
MARCA_DE_DOWNLOAD = Path.home() / ".cache" / "fabrica-de-cortes" / "whisperx-baixado"

# Quanto tempo de maquina cada tamanho costuma gastar por minuto de audio, em CPU.
# Sao ordens de grandeza para voce decidir se vale esperar, nao promessa.
CUSTO_DE_TEMPO = {
    "tiny": "cerca de 10 segundos por minuto de áudio",
    "base": "cerca de 20 segundos por minuto de áudio",
    "small": "cerca de 40 segundos por minuto de áudio",
    "medium": "cerca de 2 minutos por minuto de áudio",
    "large-v3": "cerca de 4 minutos por minuto de áudio",
}


def avisar_do_download(modelo):
    """Na primeira vez o download e grande. Melhor a pessoa saber antes."""
    if MARCA_DE_DOWNLOAD.exists():
        return
    print("")
    print("Primeira vez rodando a transcrição local nesta máquina.")
    print("  O uv vai baixar o WhisperX, o torch e o modelo %s." % modelo)
    print("  Isso dá cerca de 1,5 GB e acontece uma vez só. Da segunda em diante começa direto.")
    print("  Se a sua internet estiver lenta, prefira a rota da nuvem:")
    print("  flow-reels transcrever/replicate --entrada <seu vídeo> --projeto <pasta do projeto>")
    print("")


def marcar_download():
    try:
        MARCA_DE_DOWNLOAD.parent.mkdir(parents=True, exist_ok=True)
        MARCA_DE_DOWNLOAD.write_text("ok", encoding="utf-8")
    except Exception:
        pass


def transcrever(caminho_audio, modelo, idioma, dispositivo, lote):
    try:
        import whisperx
    except ImportError:
        nz.erro(
            "o WhisperX não está disponível neste ambiente.\n\n"
            "  Este script foi feito para rodar pelo uv, que instala tudo sozinho:\n"
            "  uv run local.py --entrada <seu vídeo> --projeto <pasta do projeto>\n\n"
            "  Se você não tem o uv, instale em https://docs.astral.sh/uv/ ou use a\n"
            "  rota da nuvem, que não precisa instalar nada:\n"
            "  flow-reels transcrever/replicate --entrada <seu vídeo> --projeto <pasta do projeto>",
            codigo=3,
        )

    tipo_de_calculo = "float16" if dispositivo == "cuda" else "int8"

    print("  [1 de 3] Carregando o modelo %s em %s..." % (modelo, dispositivo))
    argumentos = {"compute_type": tipo_de_calculo}
    if idioma:
        argumentos["language"] = idioma
    try:
        motor = whisperx.load_model(modelo, dispositivo, **argumentos)
    except Exception as e:
        if dispositivo == "cuda":
            nz.erro("não consegui usar a placa de vídeo (%s).\n"
                    "  Rode de novo com --dispositivo cpu." % e, 4)
        nz.erro("não consegui carregar o modelo (%s)." % e, 4)
    marcar_download()

    audio = whisperx.load_audio(str(caminho_audio))

    print("  [2 de 3] Transcrevendo. Em CPU isso demora, pode deixar rodando.")
    argumentos_fala = {"batch_size": lote}
    if idioma:
        argumentos_fala["language"] = idioma
    try:
        resultado = motor.transcribe(audio, **argumentos_fala)
    except Exception as e:
        nz.erro("a transcrição parou no meio (%s).\n"
                "  Se foi falta de memória, tente um modelo menor: --modelo small\n"
                "  ou um lote menor: --lote 4" % e, 4)

    detectado = resultado.get("language", idioma or "pt")

    print("  [3 de 3] Alinhando palavra a palavra (idioma: %s)..." % detectado)
    try:
        alinhador, dados_do_alinhador = whisperx.load_align_model(
            language_code=detectado, device=dispositivo
        )
        resultado = whisperx.align(
            resultado["segments"], alinhador, dados_do_alinhador, audio, dispositivo
        )
        alinhado = True
    except Exception as e:
        # sem alinhamento ainda da para ler e escolher o gancho, mas o corte
        # precisa ser conferido na onda do audio. O meta registra isso.
        nz.aviso("o alinhamento falhou (%s). Seguindo com tempo por trecho." % e)
        alinhado = False

    return {"segments": resultado["segments"]}, detectado, alinhado


def main():
    parser = argparse.ArgumentParser(
        description="Transcreve com WhisperX na sua máquina e grava os três arquivos do contrato.",
        epilog="Exemplo: uv run local.py --entrada aula.mp4 --projeto projetos/aula",
    )
    parser.add_argument("--entrada", required=True, help="arquivo de vídeo ou áudio local")
    parser.add_argument("--projeto", required=True,
                        help="diretório do projeto, onde os três arquivos vão cair")
    parser.add_argument("--modelo", default="large-v3", choices=MODELOS,
                        help="tamanho do modelo (padrão: large-v3). Em CPU, small resolve e é bem mais rápido")
    parser.add_argument("--idioma", default="pt",
                        help="idioma da fala (padrão: pt). Use vazio para deixar detectar")
    parser.add_argument("--dispositivo", default="cpu", choices=["cpu", "cuda"],
                        help="cpu (padrão) ou cuda, se você tem placa NVIDIA")
    parser.add_argument("--lote", type=int, default=8, help="batch size (padrão: 8)")
    parser.add_argument("--sem-audio", action="store_true", help="não extrair o audio16k.wav")

    if len(sys.argv) == 1:
        parser.print_help()
        print("\nEsta é a rota gratuita, que roda na sua máquina. Na primeira vez ela baixa\n"
              "cerca de 1,5 GB e em CPU é lenta. A rota rápida é o replicate.py, na mesma pasta.\n")
        sys.exit(2)

    args = parser.parse_args()

    entrada = Path(args.entrada)
    if not entrada.exists():
        nz.erro("não encontrei o arquivo %s.\n"
                "  Se o vídeo está no YouTube ou no Drive, baixe primeiro:\n"
                "  flow-reels transcrever/baixar --url <link> --projeto %s" % (entrada, args.projeto))

    projeto = Path(args.projeto)
    projeto.mkdir(parents=True, exist_ok=True)

    # O audio e a saida crua sao material de trabalho: moram debaixo do teto de
    # materiais-de-trabalho/, nunca na raiz da pasta do video.
    pasta_transcricao = nz.pasta_transcricao(projeto)
    pasta_transcricao.mkdir(parents=True, exist_ok=True)

    avisar_do_download(args.modelo)

    duracao = nz.duracao_do_arquivo(entrada)
    print("Transcrição local, WhisperX %s em %s." % (args.modelo, args.dispositivo))
    if duracao:
        print("  duração do áudio ....... %s" % nz.mmss(duracao))
    if args.dispositivo == "cpu":
        print("  ritmo esperado ......... %s" % CUSTO_DE_TEMPO.get(args.modelo, "depende da máquina"))
    print("  custo .................. zero, roda aqui mesmo")
    print("")

    # o audio16k.wav faz parte do contrato e ainda acelera o WhisperX, que
    # converte para 16 kHz de qualquer jeito. Melhor converter uma vez so.
    caminho_audio = None
    if not args.sem_audio:
        caminho_audio = nz.extrair_audio(entrada, pasta_transcricao / "audio16k.wav")

    fonte_da_fala = caminho_audio or entrada
    cru, idioma, alinhado = transcrever(
        fonte_da_fala, args.modelo, args.idioma, args.dispositivo, args.lote
    )

    bruto = pasta_transcricao / "bruto-local.json"
    bruto.write_text(json.dumps(cru, ensure_ascii=False, indent=1), encoding="utf-8")
    print("  Saída crua guardada em %s" % bruto)

    nz.normalizar(
        cru, projeto=projeto,
        meta_extra={
            "fonte": str(entrada),
            "idioma": idioma,
            "motor": "whisperx %s local%s" % (args.modelo, " (alinhado)" if alinhado else ""),
            "alinhado": alinhado,
            "audio": nz.caminho_relativo_ao_projeto(caminho_audio, projeto)
                     if caminho_audio else None,
        },
        video=entrada,
        gerar_audio=False,
    )
    if caminho_audio:
        print("  audio16k.wav    %s" % caminho_audio)


if __name__ == "__main__":
    main()
