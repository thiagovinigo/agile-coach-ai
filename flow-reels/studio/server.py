#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
server.py · Servidor Web do Flow Reels Studio 3.0
Serve a interface do estúdio, os vídeos renderizados com suporte a HTTP 206 (streaming)
e as APIs dinâmicas para qualquer projeto/marca, ganchos com IA e preview de áudio.
"""

import json
import os
import re
import socket
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
STUDIO_DIR = RAIZ / "studio"
PROJETOS_DIR = RAIZ / "projetos"
TEMP_AUDIO_DIR = STUDIO_DIR / "temp-audio"
PORTA_PADRAO = 8080

if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))
if str(STUDIO_DIR) not in sys.path:
    sys.path.insert(0, str(STUDIO_DIR))

import openai_engine  # noqa: E402


class StudioHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STUDIO_DIR), **kwargs)

    def do_GET(self):
        # Servir áudio temporário de preview
        if self.path.startswith("/temp-audio/"):
            rel_audio = self.path[len("/temp-audio/"):].split("?")[0]
            audio_file = TEMP_AUDIO_DIR / rel_audio
            if audio_file.is_file():
                self.send_response(200)
                self.send_header("Content-Type", "audio/mpeg")
                self.send_header("Content-Length", str(audio_file.stat().st_size))
                self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                self.end_headers()
                with open(audio_file, "rb") as f:
                    shutil_copy(f, self.wfile)
                return
        # Servir áudio de trilha sonora do acervo do pacote
        if self.path.startswith("/trilha/"):
            nome_trilha = self.path[len("/trilha/"):].split("?")[0]
            if not nome_trilha.endswith(".mp3"):
                nome_trilha += ".mp3"
            trilha_file = RAIZ / "plugins" / "flow-reels" / "componentes" / "trilhas" / nome_trilha
            if trilha_file.is_file():
                self.send_response(200)
                self.send_header("Content-Type", "audio/mpeg")
                self.send_header("Content-Length", str(trilha_file.stat().st_size))
                self.end_headers()
                with open(trilha_file, "rb") as f:
                    shutil_copy(f, self.wfile)
                return
            else:
                self.send_error(404, "Trilha sonora não encontrada no acervo")
                return

        # Servir vídeo renderizado com suporte a streaming / range request
        if self.path.startswith("/video/"):
            rel_path = self.path[len("/video/"):].split("?")[0]
            video_file = PROJETOS_DIR / rel_path
            if not video_file.is_file():
                nome_alvo = Path(rel_path).name
                partes = Path(rel_path).parts
                if len(partes) > 0:
                    pasta_projeto = PROJETOS_DIR / partes[0]
                    if pasta_projeto.is_dir():
                        achados = list(pasta_projeto.rglob(nome_alvo))
                        if achados:
                            video_file = achados[0]
            if video_file.is_file():
                return self.entregar_video(video_file)
            else:
                self.send_error(404, f"Vídeo não encontrado: {rel_path}")
                return

        # Listar projetos cadastrados
        if self.path == "/api/projetos":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            cfg = openai_engine.carregar_config_projetos()
            self.wfile.write(json.dumps(cfg, ensure_ascii=False).encode("utf-8"))
            return

        # Servir status da API
        if self.path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            payload = {
                "status": "online",
                "workspace": str(RAIZ),
                "motor": "3.0.0",
                "porta_revisao": 8790
            }
            self.wfile.write(json.dumps(payload).encode("utf-8"))
            return

        # Padrão estático
        super().do_GET()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        try:
            payload = json.loads(body)
        except Exception:
            payload = {}

        # 1. Ativar / Selecionar Projeto
        if self.path == "/api/projetos/selecionar":
            pid = payload.get("projetoId")
            try:
                proj = openai_engine.ativar_projeto(pid)
                self.responder_json({"sucesso": True, "projeto": proj})
            except Exception as e:
                self.responder_erro(str(e))
            return

        # 2. Criar Novo Projeto
        if self.path == "/api/projetos/criar":
            try:
                novo = openai_engine.criar_projeto(payload)
                self.responder_json({"sucesso": True, "projeto": novo})
            except Exception as e:
                self.responder_erro(str(e))
            return

        # 2.1 Analisar URL de Site com IA
        if self.path == "/api/projetos/analisar-url":
            url = payload.get("url", "")
            try:
                analise = openai_engine.analisar_url_site(url)
                self.responder_json({"sucesso": True, "analise": analise})
            except Exception as e:
                self.responder_erro(f"Falha ao analisar site: {e}")
            return

        # 2.2 Assistência da IA Por Etapa
        if self.path == "/api/assistente/etapa":
            etapa = int(payload.get("etapa", 1))
            contexto = payload.get("contexto", {})
            pid = payload.get("projetoId")
            try:
                sugestao = openai_engine.gerar_sugestao_etapa(etapa, contexto, pid)
                self.responder_json({"sucesso": True, "sugestao": sugestao})
            except Exception as e:
                self.responder_erro(f"Falha ao gerar sugestão de etapa: {e}")
            return

        # 3. Gerar Opções de Ganchos com IA
        if self.path == "/api/assistente/ganchos":
            tema = payload.get("tema", "")
            pid = payload.get("projetoId")
            try:
                opcoes = openai_engine.gerar_opcoes_ganchos(tema, pid)
                self.responder_json(opcoes)
            except Exception as e:
                self.responder_erro(str(e))
            return

        # 4. Gerar Roteiro Completo a partir do Gancho Escolhido
        if self.path == "/api/assistente/roteiro" or self.path == "/api/assistente":
            gancho_ou_prompt = payload.get("gancho") or payload.get("prompt", "")
            pid = payload.get("projetoId")
            palavra = payload.get("palavraCta")
            try:
                roteiro = openai_engine.gerar_roteiro_ia(gancho_ou_prompt, pid, palavra)
                self.responder_json(roteiro)
            except Exception as e:
                self.responder_erro(str(e))
            return

        # 5. Preview Instantâneo de Áudio (Edge-TTS em 1.5s)
        if self.path == "/api/preview-audio":
            texto = payload.get("texto", "")
            voz = payload.get("voz", "pt-BR-AntonioNeural")
            try:
                preview = openai_engine.gerar_preview_audio(texto, voz)
                self.responder_json(preview)
            except Exception as e:
                self.responder_erro(str(e))
            return

        # 6. Renderizar Vídeo Final 1080x1920
        if self.path == "/api/renderizar":
            try:
                resp = openai_engine.renderizar_novo_reel(payload)
                self.responder_json(resp)
            except Exception as e:
                import traceback
                traceback.print_exc()
                self.responder_erro(str(e), status=500)
            return

        self.send_error(404, "Endpoint não encontrado")

    def responder_json(self, dados, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(dados, ensure_ascii=False).encode("utf-8"))

    def responder_erro(self, msg, status=400):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps({"sucesso": False, "erro": msg}, ensure_ascii=False).encode("utf-8"))

    def entregar_video(self, caminho: Path):
        tamanho = caminho.stat().st_size
        range_header = self.headers.get("Range")

        if not range_header:
            self.send_response(200)
            self.send_header("Content-Type", "video/mp4")
            self.send_header("Content-Length", str(tamanho))
            self.send_header("Accept-Ranges", "bytes")
            self.end_headers()
            with open(caminho, "rb") as f:
                while chunk := f.read(64 * 1024):
                    try:
                        self.wfile.write(chunk)
                    except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError, OSError):
                        return
            return

        match = re.match(r"bytes=(\d+)-(\d*)", range_header)
        if not match:
            self.send_error(416, "Requested Range Not Satisfiable")
            return

        inicio = int(match.group(1))
        fim = int(match.group(2)) if match.group(2) else tamanho - 1
        fim = min(fim, tamanho - 1)

        if inicio >= tamanho or inicio > fim:
            self.send_error(416, "Requested Range Not Satisfiable")
            return

        self.send_response(206)
        self.send_header("Content-Type", "video/mp4")
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Range", f"bytes {inicio}-{fim}/{tamanho}")
        self.send_header("Content-Length", str(fim - inicio + 1))
        self.end_headers()

        restante = fim - inicio + 1
        with open(caminho, "rb") as f:
            f.seek(inicio)
            while restante > 0:
                chunk = f.read(min(64 * 1024, restante))
                if not chunk:
                    break
                try:
                    self.wfile.write(chunk)
                except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError, OSError):
                    return
                restante -= len(chunk)


def shutil_copy(fsrc, fdst, length=64*1024):
    while chunk := fsrc.read(length):
        try:
            fdst.write(chunk)
        except (BrokenPipeError, ConnectionResetError, OSError):
            break


def achar_porta_livre(porta_base=PORTA_PADRAO):
    for p in range(porta_base, porta_base + 10):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.2)
            if s.connect_ex(("127.0.0.1", p)) != 0:
                return p
    return porta_base


def main():
    porta = achar_porta_livre()
    servidor = ThreadingHTTPServer(("127.0.0.1", porta), StudioHandler)
    print(f"\n=======================================================")
    print(f"  Flow Reels Studio 3.0 Universal no ar!")
    print(f"  Acesse no navegador: http://localhost:{porta}")
    print(f"=======================================================\n")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("Servidor encerrado.")
    finally:
        servidor.server_close()


if __name__ == "__main__":
    main()
