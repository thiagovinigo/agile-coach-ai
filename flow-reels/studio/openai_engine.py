#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
openai_engine.py · Motor OpenAI Universal para o Flow Reels Studio 3.0
Gera opções de ganchos virais, roteiros de 5 blocos, preview de áudio instantâneo
e executa a renderização real de vídeos 1080x1920 para QUALQUER marca, nicho ou criador.
"""

import asyncio
import edge_tts
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from openai import OpenAI

RAIZ = Path(__file__).resolve().parent.parent
STUDIO_DIR = RAIZ / "studio"
PROJETOS_DIR = RAIZ / "projetos"
CONFIG_PROJETOS_FILE = PROJETOS_DIR / "projetos_config.json"
MARCA_TOKENS_FILE = RAIZ / "marca" / "tokens.json"
ENV_FILE = RAIZ / ".env"
PYTHON_EXE = RAIZ / ".venv" / "Scripts" / "python.exe"

FFMPEG_BIN = "C:\\Users\\User\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\\ffmpeg-9.0.2-full_build\\bin"


def obter_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key and ENV_FILE.is_file():
        m = re.search(r"^OPENAI_API_KEY=(.+)$", ENV_FILE.read_text(encoding="utf-8"), re.MULTILINE)
        if m:
            api_key = m.group(1).strip()
    if not api_key:
        raise ValueError("Chave OPENAI_API_KEY não encontrada no .env")
    return OpenAI(api_key=api_key)


# ==============================================================================
# Gerenciamento Dinâmico de Projetos (Para Qualquer Pessoa / Marca)
# ==============================================================================

def carregar_config_projetos():
    if not CONFIG_PROJETOS_FILE.is_file():
        padrao = {
            "projeto_ativo": "nutrivvo",
            "projetos": [
                {
                    "id": "nutrivvo",
                    "nome": "Nutrivvo",
                    "nicho": "SaaS & IA para Nutricionistas e Clínicas",
                    "proposta": "Secretária virtual no Telegram, radar de abandono de pacientes e dietas com IA",
                    "publico": "Nutricionistas clínicos e donos de consultório",
                    "palavra_cta": "RETENCAO",
                    "cor_destaque": "#8B5CF6",
                    "tipo_formato": "narrado",
                    "voz_padrao": "pt-BR-AntonioNeural",
                    "video_base": "projetos/nutrivvo-retencao-pacientes/materiais-de-trabalho/fonte/video-base.mp4"
                }
            ]
        }
        CONFIG_PROJETOS_FILE.write_text(json.dumps(padrao, indent=2, ensure_ascii=False), encoding="utf-8")
        return padrao
    try:
        return json.loads(CONFIG_PROJETOS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {"projeto_ativo": "nutrivvo", "projetos": []}


def salvar_config_projetos(dados):
    CONFIG_PROJETOS_FILE.write_text(json.dumps(dados, indent=2, ensure_ascii=False), encoding="utf-8")


def obter_projeto_ativo(projeto_id=None):
    cfg = carregar_config_projetos()
    pid = projeto_id or cfg.get("projeto_ativo")
    projetos = cfg.get("projetos", [])
    for p in projetos:
        if p.get("id") == pid:
            return p
    if projetos:
        return projetos[0]
    return {
        "id": "universal",
        "nome": "Minha Marca",
        "nicho": "Negócios & Conteúdo",
        "proposta": "Soluções práticas e alta conversão",
        "publico": "Clientes e seguidores",
        "palavra_cta": "ACESSO",
        "cor_destaque": "#8B5CF6",
        "tipo_formato": "narrado",
        "voz_padrao": "pt-BR-AntonioNeural"
    }


def atualizar_tokens_marca(projeto):
    """Atualiza marca/tokens.json com as cores e nome do projeto ativo"""
    if not MARCA_TOKENS_FILE.is_file():
        return
    try:
        tokens = json.loads(MARCA_TOKENS_FILE.read_text(encoding="utf-8"))
        tokens["nome"] = projeto.get("nome", "Flow Reels")
        cor_destaque = projeto.get("cor_destaque", "#8B5CF6")
        tokens["cores"]["destaque"] = cor_destaque
        MARCA_TOKENS_FILE.write_text(json.dumps(tokens, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception as e:
        print(f"[AVISO] Falha ao sincronizar tokens de marca: {e}")


def ativar_projeto(projeto_id):
    cfg = carregar_config_projetos()
    cfg["projeto_ativo"] = projeto_id
    salvar_config_projetos(cfg)
    proj = obter_projeto_ativo(projeto_id)
    atualizar_tokens_marca(proj)
    return proj


def criar_projeto(dados):
    nome = dados.get("nome", "").strip()
    if not nome:
        raise ValueError("O nome do projeto é obrigatório.")
    
    slug = re.sub(r'[^a-z0-9]+', '-', nome.lower()).strip('-') or "novo-projeto"
    cfg = carregar_config_projetos()
    
    # Garantir id único
    existentes = [p.get("id") for p in cfg.get("projetos", [])]
    novo_id = slug
    contador = 2
    while novo_id in existentes:
        novo_id = f"{slug}-{contador}"
        contador += 1
        
    novo_proj = {
        "id": novo_id,
        "nome": nome,
        "url_site": dados.get("url_site", "").strip(),
        "nicho": dados.get("nicho", "Geral").strip(),
        "proposta": dados.get("proposta", "").strip(),
        "publico": dados.get("publico", "Geral").strip(),
        "palavra_cta": dados.get("palavra_cta", "REEL").strip().upper(),
        "cor_destaque": dados.get("cor_destaque", "#8B5CF6").strip(),
        "tipo_formato": dados.get("tipo_formato", "narrado"),
        "voz_padrao": dados.get("voz_padrao", "pt-BR-AntonioNeural"),
        "video_base": dados.get("video_base") or None,
        "pautas": dados.get("pautas") or []
    }
    
    cfg.setdefault("projetos", []).append(novo_proj)
    cfg["projeto_ativo"] = novo_id
    salvar_config_projetos(cfg)
    atualizar_tokens_marca(novo_proj)
    
    # Criar pasta física do projeto
    pasta_projeto = PROJETOS_DIR / novo_id
    (pasta_projeto / "materiais-de-trabalho" / "fonte").mkdir(parents=True, exist_ok=True)
    
    return novo_proj


def extrair_texto_site(url: str):
    """Extrai título, meta descrição e texto principal de uma URL pública."""
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    )
    with urllib.request.urlopen(req, timeout=12) as response:
        html = response.read().decode("utf-8", errors="ignore")
    
    titulo = ""
    m_title = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
    if m_title:
        titulo = m_title.group(1).strip()
        
    desc = ""
    m_desc = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']', html, re.I | re.S)
    if not m_desc:
        m_desc = re.search(r'<meta[^>]*content=["\'](.*?)["\'][^>]*name=["\']description["\']', html, re.I | re.S)
    if m_desc:
        desc = m_desc.group(1).strip()
        
    headings = re.findall(r"<h[1-3][^>]*>(.*?)</h[1-3]>", html, re.I | re.S)
    headings_clean = [re.sub(r"<[^>]+>", " ", h).strip() for h in headings if h.strip()][:10]
    
    body_clean = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.I | re.S)
    body_clean = re.sub(r"<[^>]+>", " ", body_clean)
    body_clean = re.sub(r"\s+", " ", body_clean).strip()[:3000]
    
    return {
        "url": url,
        "titulo": titulo,
        "descricao": desc,
        "headings": headings_clean,
        "amostra_texto": body_clean
    }


def analisar_url_site(url: str):
    """
    Lê a página web fornecida pelo usuário, extrai a essência do negócio
    e usa GPT-4o para montar a ficha completa do projeto + 4 pautas virais sob medida.
    """
    try:
        dados_site = extrair_texto_site(url)
    except Exception as e:
        dados_site = {
            "url": url,
            "titulo": Path(url).name or url,
            "descricao": "",
            "headings": [],
            "amostra_texto": f"URL do site fornecido: {url}. Erro ao baixar HTML diretamente: {e}"
        }
        
    client = obter_openai_client()
    prompt = f"""Você é o Estrategista Viral e Especialista em Posicionamento de Marca do Flow Reels Studio 3.0.
Um usuário informou a URL do seu site/plataforma para criar um projeto de Reels:
URL: {dados_site.get('url')}
Título da página: {dados_site.get('titulo')}
Meta Descrição: {dados_site.get('descricao')}
Títulos/Headings: {', '.join(dados_site.get('headings', []))}
Amostra de Texto do Site:
{dados_site.get('amostra_texto', '')[:2500]}

Analise cuidadosamente este site e retorne uma estrutura em JSON com os campos:
1. "nome": Nome oficial da marca ou plataforma (curto e limpo, ex: 'Busca Armas', 'Nutrivvo', 'Barbearia Alfa')
2. "nicho": Ramo de atuação e posicionamento de mercado em 4 a 8 palavras
3. "proposta": Proposta de valor principal (o que o site resolve ou vende em 1 a 2 linhas impactantes)
4. "publico": Público-alvo ideal desse site
5. "palavra_cta": Palavra-chave única em maiúsculas recomendada para a chamada da DM (ex: 'PRECO', 'ARMAS', 'AGENDA', 'OFERTA')
6. "cor_destaque": Cor hexadecimal marcante sugerida para os cards e destaques da marca (ex: '#F59E0B', '#10B981', '#06B6D4')
7. "modo_cena_sugerido": Um dos modos oficiais: 'rosto-vidro', 'manchete', 'vidro-liquido', 'lado-a-lado', 'mundo', 'camadas', 'chat', 'lista'
8. "voz_sugerida": Uma das vozes neurais: 'pt-BR-AntonioNeural', 'pt-BR-FranciscaNeural', 'pt-BR-ThalitaMultilingualNeural', 'pt-PT-DuarteNeural', 'pt-PT-RaquelNeural'
9. "trilha_sugerida": Uma das faixas: 'calma-pads-01', 'tensa-atmosfera-01', 'tensa-synthwave-01', 'calma-lofi-01', 'calma-lofi-02', 'leve-lofi-03', 'tech-synthwave-02', 'animada-synthwave-01', 'animada-deephouse-01'
10. "pautas": Lista com EXATAMENTE 4 pautas/roteiros completos e virais de 5 blocos (135 a 160 palavras somadas em cada) calibrados para este produto/site:
    Cada pauta deve ter:
    - id: "pauta-1", "pauta-2", etc.
    - label: Título curto com emoji para o botão (ex: '🔫 De R$ 12 Mil por R$ 5.800')
    - titulo: Título da pauta
    - gancho: 0 a 4s (máx 15 palavras)
    - oQueE: 4 a 10s (onde o erro acontece)
    - provas: 10 a 35s (o dia a dia e dados concretos)
    - virada: 35 a 42s (apresentação da solução do site)
    - chamada: 42 a 50s ("Comenta [PALAVRA] aqui embaixo que eu te mando...")
    - palavraCta: A mesma palavra da chamada

Responda EXCLUSIVAMENTE em formato JSON com esses campos."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Você é um extrator e estrategista de marcas de alta precisão. Responda em JSON válido."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        response_format={"type": "json_object"}
    )
    
    return json.loads(response.choices[0].message.content)


def gerar_sugestao_etapa(etapa: int, contexto, projeto_id=None):
    """
    Gera auxílio da IA focado especificamente em uma etapa do Wizard:
    1: Idéias & Ângulos
    2: Refinamento de Roteiro (ou blocos individuais)
    3: Composição Visual & Modo de Cena
    4: Voz & Ambiente Acústico
    """
    projeto = obter_projeto_ativo(projeto_id)
    client = obter_openai_client()
    sys_prompt = construir_system_prompt_projeto(projeto)

    if isinstance(contexto, str):
        contexto_dict = {"texto": contexto, "foco": contexto, "duvida": contexto}
    elif isinstance(contexto, dict):
        contexto_dict = contexto
    else:
        contexto_dict = {}

    foco_usuario = contexto_dict.get("texto") or contexto_dict.get("duvida") or contexto_dict.get("foco") or ""
    
    if etapa == 1:
        user_prompt = f"""Ajude o criador a definir o melhor formato e ângulo viral para um novo vídeo do projeto '{projeto.get('nome')}' ({projeto.get('nicho')}).
Contexto/Dúvida do usuário: "{foco_usuario}"

Responda em JSON com o formato:
{{
  "formatoRecomendado": "narrado" ou "fabrica" ou "radar",
  "tituloEstrategia": "Nome chamativo da estratégia",
  "angulosSugeridos": [
    {{"angulo": "Nome do Ângulo 1", "ganchoAmostra": "Frase de abertura", "porQueFunciona": "..."}},
    {{"angulo": "Nome do Ângulo 2", "ganchoAmostra": "Frase de abertura", "porQueFunciona": "..."}},
    {{"angulo": "Nome do Ângulo 3", "ganchoAmostra": "Frase de abertura", "porQueFunciona": "..."}}
  ],
  "explicacao": "Por que esta abordagem é a ideal para este nicho"
}}"""
    elif etapa == 2:
        user_prompt = f"""Redija ou otimize um roteiro de alta retenção no formato de 5 blocos do Flow Reels 3.0 para o projeto '{projeto.get('nome')}' ({projeto.get('nicho')}).
Foco ou pedido do usuário: "{foco_usuario}"
Proposta de valor do projeto: "{projeto.get('proposta')}"
Palavra da DM: "{projeto.get('palavra_cta', 'ACESSO')}"

Regras:
- 135 a 160 palavras no total (fala de 40 a 50s).
- Gancho com menos de 15 palavras, impactante.
- Sem travessões (use apenas vírgula e ponto final).

Responda em JSON com o formato:
{{
  "gancho": "Frase de abertura forte (0 a 4s)",
  "oQueE": "O contexto e onde o erro acontece (4 a 10s)",
  "provas": "Dados, números, comparações concretas e dor real (10 a 35s)",
  "virada": "Apresentação da solução e como {projeto.get('nome')} resolve (35 a 42s)",
  "chamada": "Comenta {projeto.get('palavra_cta', 'ACESSO')} aqui embaixo que eu te envio o link direto na sua DM (42 a 48s)",
  "palavraCta": "{projeto.get('palavra_cta', 'ACESSO')}",
  "explicacao": "Breve justificativa do ritmo e da psicologia do roteiro"
}}"""
    elif etapa == 3:
        user_prompt = f"""Para o projeto '{projeto.get('nome')}' ({projeto.get('nicho')}) e contexto: "{foco_usuario}".
Qual é a melhor composição visual entre os 8 modos oficiais (rosto-vidro, manchete, vidro-liquido, lado-a-lado, mundo, camadas, chat, lista)?

Responda em JSON com o formato:
{{
  "modoCenaRecomendado": "vidro-liquido" (ou um dos outros 7 modos),
  "transicaoRecomendada": "desfoque" ou "zoom" ou "corte",
  "duracaoRecomendada": "0.36",
  "legendaRecomendada": "amarelo-ouro" ou "verde-neon" ou "violeta-marca" ou "branco-bold" ou "placa-escura",
  "orientacaoVisual": "Como posicionar o produto/gravação de tela na cena para máximo impacto",
  "justificativa": "Razão psicológica desta escolha para o nicho"
}}"""
    elif etapa == 4:
        user_prompt = f"""Recomende a combinação acústica perfeita para o projeto '{projeto.get('nome')}' ({projeto.get('nicho')}) com foco em: "{foco_usuario}".

Responda em JSON com o formato:
{{
  "vozRecomendada": "pt-BR-AntonioNeural" ou "pt-BR-FranciscaNeural" ou "pt-BR-ThalitaMultilingualNeural" ou "pt-PT-DuarteNeural",
  "trilhaRecomendada": "calma-pads-01" ou "tensa-atmosfera-01" ou "tensa-synthwave-01" ou "tech-synthwave-02" ou "animada-synthwave-01",
  "sfxHabilitado": true,
  "orientacaoMixagem": "Como equilibrar o volume da voz sobre a trilha sonora",
  "justificativa": "Justificativa da energia e autoridade transmitida por esta voz e trilha"
}}"""
    else:
        user_prompt = "Sugira melhorias gerais para o vídeo vertical."
        
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.6,
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)


def construir_system_prompt_projeto(projeto):
    nome = projeto.get("nome", "Marca")
    nicho = projeto.get("nicho", "Geral")
    proposta = projeto.get("proposta", "Solução de alta qualidade")
    publico = projeto.get("publico", "Público qualificado")
    palavra_cta = projeto.get("palavra_cta", "ACESSO")
    url_site = projeto.get("url_site") or ""
    
    site_info = f"\nWebsite Oficial: {url_site}" if url_site else ""
    
    return f"""Você é o Diretor Criativo e Estrategista Viral do Flow Reels Studio 3.0 para o projeto '{nome}'.{site_info}
Segmento / Nicho: {nicho}
Proposta de Valor / O que vende: {proposta}
Público-Alvo: {publico}
Palavra de Chamada para DM: {palavra_cta}

Sua missão é criar roteiros de retenção máxima e altíssima conversão para Reels/TikTok verticais (9:16).
Você NUNCA entrega conteúdo genérico ou vago: você usa dores viscerais do dia a dia, números concretos e contrastes fortes.

Regras Estritas de Redação:
- NUNCA use travessão (— ou –) nem hífen solto (' - ') como pausa de texto. Use apenas vírgula ou ponto final.
- O tom deve ser direto, profissional, magnético e sem enrolação."""


def gerar_opcoes_ganchos(tema_ou_pedido: str, projeto_id=None):
    """
    Gera 3 a 4 opções de ganchos com ângulos psicológicos distintos antes de redigir o roteiro completo.
    Permite ao criador escolher a melhor abordagem.
    """
    projeto = obter_projeto_ativo(projeto_id)
    client = obter_openai_client()
    sys_prompt = construir_system_prompt_projeto(projeto)
    
    prompt = f"""O criador deseja gravar/produzir um Reel sobre o seguinte tema ou ideia:
"{tema_ou_pedido}"

Gere EXATAMENTE 4 opções de ganchos virais e ângulos de abordagem diferentes e estratégicos para ele escolher:
1. Ângulo da Dor / Choque / Alerta (foco no erro que causa perda de tempo ou dinheiro)
2. Ângulo da Curiosidade / Segredo Revelado (o método pouco falado que os top 1% usam)
3. Ângulo Contra-intuitivo / Quebra de Mito ("pare de fazer X achando que vai ter Y")
4. Ângulo da Prova / Transformação Rápida (como alcançar o resultado desejado sem o obstáculo clássico)

Cada opção deve ter:
- id: número (1 a 4)
- angulo: nome do ângulo
- icone: emoji temático
- titulo: título chamativo
- gancho: a frase exata de abertura dos primeiros 0 a 4 segundos (máximo 15 palavras, impactante)
- explicacao: 1 a 2 linhas explicando por que esse gancho prende e converte
- palavraCta: palavra-chave única em maiúsculas recomendada para a chamada da DM

Responda EXCLUSIVAMENTE em formato JSON com o schema:
{{
  "opcoes": [
    {{
      "id": 1,
      "angulo": "...",
      "icone": "...",
      "titulo": "...",
      "gancho": "...",
      "explicacao": "...",
      "palavraCta": "..."
    }}
  ]
}}"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        response_format={"type": "json_object"}
    )
    
    try:
        conteudo = json.loads(response.choices[0].message.content)
        return conteudo
    except Exception as e:
        raise ValueError(f"Falha ao interpretar resposta da OpenAI: {e}")


def gerar_roteiro_ia(prompt_ou_gancho: str, projeto_id=None, palavra_cta_custom=None):
    """
    Desenvolve o roteiro completo no formato rigoroso dos 5 blocos do Flow Reels (135 a 160 palavras, 40 a 50s).
    """
    projeto = obter_projeto_ativo(projeto_id)
    client = obter_openai_client()
    sys_prompt = construir_system_prompt_projeto(projeto)
    palavra_padrao = palavra_cta_custom or projeto.get("palavra_cta", "ACESSO")
    
    user_prompt = f"""Desenvolva o roteiro viral completo (RIGOROSAMENTE entre 135 e 160 palavras somadas) para o projeto '{projeto.get("nome")}' a partir do gancho ou tema:
"{prompt_ou_gancho}"

A palavra da chamada deve ser: '{palavra_padrao}'.

ESTRUTURA OBRIGATÓRIA DOS 5 BLOCOS:
1. gancho (0 a 4s - máx 15 palavras): Frase magnética que interrompe o scroll.
2. oQueE (4 a 10s): Explicação direta da dor ou oportunidade sem rodeios.
3. provas (10 a 35s): O cerne do vídeo. Detalhe fatos do cotidiano, estatísticas, exemplos reais e a causa raiz (mínimo 65 a 85 palavras).
4. virada (35 a 42s): A quebra de padrão e apresentação da solução de {projeto.get("nome")}.
5. chamada (42 a 48s): "Comenta {palavra_padrao} aqui embaixo que eu te mando [item de valor exclusivo] na sua DM."

REGRA CRÍTICA DE PALAVRAS:
O somatório das palavras de gancho + oQueE + provas + virada + chamada DEVE ficar entre 135 e 160 palavras (calibrado para 40 a 50 segundos na velocidade de 3.7 palavras por segundo).
NUNCA use travessão (— ou –) nem hífen solto. Use apenas vírgulas e pontos.

Responda EXCLUSIVAMENTE em formato JSON com o schema:
{{
  "titulo": "Título do Reel",
  "gancho": "...",
  "oQueE": "...",
  "provas": "...",
  "virada": "...",
  "chamada": "...",
  "palavraCta": "{palavra_padrao}",
  "visual": "Rosto + Liquid Glass Cards",
  "voz": "Antônio Neural (pt-BR)",
  "analise_ia": "Explicação estratégica do porquê esse roteiro converte."
}}"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        response_format={"type": "json_object"}
    )
    
    dados = json.loads(response.choices[0].message.content)
    
    # Calcular contagem real de palavras
    texto_completo = " ".join([
        dados.get("gancho", ""),
        dados.get("oQueE", ""),
        dados.get("provas", ""),
        dados.get("virada", ""),
        dados.get("chamada", "")
    ])
    palavras = [w for w in texto_completo.split() if w]
    dados["totalPalavras"] = len(palavras)
    dados["duracaoEstimada"] = round(len(palavras) / 3.7)
    dados["projeto"] = projeto.get("nome")
    return dados


# ==============================================================================
# Pré-Visualização Instantânea de Áudio (Preview de 1.5s via Edge-TTS)
# ==============================================================================

async def sintetizar_audio_preview_async(texto: str, arquivo_saida: Path, voz: str = "pt-BR-AntonioNeural"):
    communicate = edge_tts.Communicate(texto, voz)
    await communicate.save(str(arquivo_saida))


def gerar_preview_audio(texto: str, voz: str = "pt-BR-AntonioNeural"):
    """
    Sintetiza o áudio da locução em ~1.5 segundo e salva em studio/temp-preview.mp3.
    Retorna a URL temporária para o usuário ouvir antes de renderizar o vídeo.
    """
    if not texto.strip():
        raise ValueError("O texto para o preview de áudio não pode estar vazio.")
    
    temp_dir = STUDIO_DIR / "temp-audio"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = int(time.time() * 1000)
    nome_arquivo = f"preview-{timestamp}.mp3"
    caminho_mp3 = temp_dir / nome_arquivo
    
    asyncio.run(sintetizar_audio_preview_async(texto, caminho_mp3, voz))
    
    # Limpar previews antigos com mais de 30 minutos
    agora = time.time()
    for f in temp_dir.glob("preview-*.mp3"):
        if f != caminho_mp3 and (agora - f.stat().st_mtime) > 1800:
            try:
                f.unlink()
            except Exception:
                pass
                
    return {
        "sucesso": True,
        "audioUrl": f"/temp-audio/{nome_arquivo}?t={timestamp}",
        "duracaoEstimada": round(len(texto.split()) / 3.7, 1)
    }


# ==============================================================================
# Síntese Completa com Alinhamento Palavra por Palavra
# ==============================================================================

async def sintetizar_voz_e_palavras(texto: str, voice_dir: Path, voz: str = "pt-BR-AntonioNeural"):
    voice_dir.mkdir(parents=True, exist_ok=True)
    mp3_path = voice_dir / "voz-a.mp3"
    json_path = voice_dir / "palavras-a.json"
    cru_path = voice_dir / "alinhamento-a.json"
    
    communicate = edge_tts.Communicate(texto, voz)
    sentences = []
    audio_data = bytearray()
    
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data.extend(chunk["data"])
        elif chunk["type"] == "SentenceBoundary":
            start_s = (chunk["offset"] / 10) / 1_000_000
            end_s = ((chunk["offset"] + chunk["duration"]) / 10) / 1_000_000
            sentences.append({
                "texto": chunk["text"].strip(),
                "inicio": round(start_s, 3),
                "fim": round(end_s, 3)
            })
            
    mp3_path.write_bytes(audio_data)
    
    todas_palavras = []
    for s in sentences:
        tokens = [t for t in s["texto"].split() if t]
        if not tokens:
            continue
        tot_chars = sum(len(t) for t in tokens)
        dur_total = s["fim"] - s["inicio"]
        
        t_cur = s["inicio"]
        for idx, token in enumerate(tokens):
            w_dur = (len(token) / tot_chars) * dur_total
            w_start = round(t_cur, 3)
            w_end = round(t_cur + w_dur, 3)
            t_cur += w_dur
            todas_palavras.append({
                "texto": token,
                "inicio": w_start,
                "fim": w_end
            })
            
    duracao_total = todas_palavras[-1]["fim"] if todas_palavras else 0.0
    meta = {
        "take": "a",
        "modelo": f"edge-tts:{voz}",
        "estabilidade": 0.5,
        "similaridade": 0.85,
        "palavras_no_roteiro": len(todas_palavras),
        "duracao_total": duracao_total
    }
    
    cru_data = {"frases": sentences, "meta": meta}
    cru_path.write_text(json.dumps(cru_data, indent=2, ensure_ascii=False), encoding="utf-8")
    
    payload = {"palavras": todas_palavras, "meta": meta}
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return duracao_total


def executar_comando(cmd_list, cwd=RAIZ):
    env = os.environ.copy()
    env["PATH"] = FFMPEG_BIN + ";" + env.get("PATH", "")
    res = subprocess.run(cmd_list, cwd=str(cwd), env=env, capture_output=True, text=True, check=True)
    return res.stdout


def limpar_texto(t):
    if not t:
        return ""
    t = re.sub(r"[—–]", ", ", str(t))
    t = re.sub(r"\s-\s", ", ", t)
    return t.strip()


def apontar_revisao_para_projeto(pasta_projeto):
    try:
        out = subprocess.run("netstat -ano | findstr :8790", shell=True, capture_output=True, text=True).stdout
        for line in out.strip().splitlines():
            parts = line.strip().split()
            if len(parts) >= 5 and "LISTENING" in parts:
                pid = parts[-1]
                subprocess.run(f"taskkill /F /PID {pid}", shell=True, capture_output=True)
        time.sleep(0.5)
        env = os.environ.copy()
        env["PATH"] = FFMPEG_BIN + ";" + env.get("PATH", "")
        cmd = [str(PYTHON_EXE), "plugins/flow-reels/skills/narrado/scripts/revisao_narrado.py", str(pasta_projeto)]
        subprocess.Popen(cmd, cwd=str(RAIZ), env=env)
        print(f"[REVISAO] Servidor na porta 8790 atualizado para: {pasta_projeto.name}")
    except Exception as e:
        print(f"[REVISAO] Aviso ao reiniciar servidor: {e}")


# ==============================================================================
# Renderização Final do Vídeo 1080x1920 (Universal)
# ==============================================================================

def renderizar_novo_reel(dados: dict):
    """
    Renderiza um novo reel vertical 1080x1920 a partir dos dados do formulário e do projeto ativo.
    Suporta qualquer pessoa, nicho, marca ou negócio.
    """
    projeto_id = dados.get("projetoId")
    projeto = obter_projeto_ativo(projeto_id)
    nome_marca = projeto.get("nome", "Minha Marca")
    slug_marca = re.sub(r'[^a-z0-9]+', '-', nome_marca.lower()).strip('-') or "reel"
    
    titulo = limpar_texto(dados.get("titulo", f"{nome_marca} Reel"))
    palavra = dados.get("palavraCta", projeto.get("palavra_cta", "ACESSO")).strip().upper()
    palavra = re.sub(r'[^A-Z0-9]+', '', palavra) or "ACESSO"
    slug_palavra = re.sub(r'[^a-z0-9]+', '-', palavra.lower()).strip('-') or "corte"
    
    # Criar nome único de projeto para esta renderização
    timestamp = int(time.time())
    nome_projeto = f"{slug_marca}-{slug_palavra}-{timestamp}"
    pasta_projeto = PROJETOS_DIR / nome_projeto
    pasta_projeto.mkdir(parents=True, exist_ok=True)
    
    # Pastas internas
    fonte_dir = pasta_projeto / "materiais-de-trabalho" / "fonte"
    fonte_dir.mkdir(parents=True, exist_ok=True)
    narrado_trabalho = pasta_projeto / "materiais-de-trabalho" / "narrado-01"
    narrado_trabalho.mkdir(parents=True, exist_ok=True)
    voz_dir = narrado_trabalho / "voz"
    voz_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. RESPEITAR O VÍDEO DE ORIGEM
    video_fonte_pedido = dados.get("videoFonte") or projeto.get("video_base")
    video_base_destino = fonte_dir / "video-base.mp4"
    origem_resolvida = None
    
    if video_fonte_pedido:
        cand = RAIZ / video_fonte_pedido if not Path(video_fonte_pedido).is_absolute() else Path(video_fonte_pedido)
        if cand.is_file():
            origem_resolvida = cand
            
    if not origem_resolvida:
        # Fallbacks por nicho
        if "arma" in slug_marca or "garimpo" in slug_marca:
            cand = PROJETOS_DIR / "garimpo-armas-desconto" / "materiais-de-trabalho" / "fonte" / "video-base.mp4"
            if cand.is_file():
                origem_resolvida = cand
        if not origem_resolvida:
            cand = PROJETOS_DIR / "nutrivvo-retencao-pacientes" / "materiais-de-trabalho" / "fonte" / "video-base.mp4"
            if cand.is_file():
                origem_resolvida = cand

    if origem_resolvida and origem_resolvida.is_file():
        shutil.copy2(origem_resolvida, video_base_destino)
        print(f"[VIDEO] Vídeo base configurado a partir de: {origem_resolvida}")
        
    # 2. RESPEITAR O TEXTO DO ROTEIRO
    gancho = limpar_texto(dados.get("gancho", ""))
    oQueE = limpar_texto(dados.get("oQueE", ""))
    provas = limpar_texto(dados.get("provas", ""))
    virada = limpar_texto(dados.get("virada", ""))
    chamada = limpar_texto(dados.get("chamada", ""))
    
    texto_completo = f"{gancho} {oQueE} {provas} {virada} {chamada}".strip()
    (narrado_trabalho / "roteiro-tts.txt").write_text(texto_completo, encoding="utf-8")
    (narrado_trabalho / "roteiro.md").write_text(texto_completo, encoding="utf-8")
    
    # 3. RESPEITAR A VOZ ESCOLHIDA (TODAS AS VOZES REAIS DO PACOTE)
    motor_voz = (dados.get("motorVoz") or projeto.get("voz_padrao") or "pt-BR-AntonioNeural").lower().strip()
    if "francisca" in motor_voz:
        voz_real = "pt-BR-FranciscaNeural"
    elif "thalita" in motor_voz:
        voz_real = "pt-BR-ThalitaMultilingualNeural"
    elif "duarte" in motor_voz:
        voz_real = "pt-PT-DuarteNeural"
    elif "raquel" in motor_voz:
        voz_real = "pt-PT-RaquelNeural"
    else:
        voz_real = "pt-BR-AntonioNeural"
        
    print(f"[VOZ] Sintetizando locução com voz: {voz_real}")
    duracao_s = asyncio.run(sintetizar_voz_e_palavras(texto_completo, voz_dir, voz_real))
    
    # 4. RESPEITAR AS OPÇÕES DE TRANSIÇÃO E DURAÇÃO
    transicao_escolhida = dados.get("transicao", "desfoque").lower().strip()
    if transicao_escolhida not in ["desfoque", "zoom", "corte"]:
        transicao_escolhida = "desfoque"
    duracao_transicao = 0.0 if transicao_escolhida == "corte" else float(dados.get("duracaoTransicao", 0.36))
    
    # 5. RESPEITAR O MODO DE CENA
    modo_cena = dados.get("modoCena", "rosto-vidro").lower().strip()
    tela_cheia = modo_cena in ["mundo", "camadas"]
    centro_y = 960 if tela_cheia else 815
    escurecer = 0.35 if modo_cena == "manchete" else (0.2 if modo_cena == "vidro-liquido" else 0.0)

    # 6. CONFIGURAR TOMADAS.JSON COM AS OPÇÕES ESCOLHIDAS
    destaque_candidato = None
    for w in re.findall(r"\w+", gancho):
        if w.upper() == palavra:
            destaque_candidato = w
            break
    if not destaque_candidato:
        palavras_gancho = [w for w in re.findall(r"[A-Za-z0-9%]+", gancho) if len(w) >= 3]
        destaque_candidato = palavras_gancho[0] if palavras_gancho else None

    t_cta = round(max(duracao_s * 0.82, duracao_s - 8.0), 2)
    credito = f"{nome_marca}"
    kicker = nome_marca.upper()
    
    destaques_legenda = [palavra, nome_marca]
    for w in re.findall(r"\b[A-Z][a-z]{3,}\b", gancho + " " + virada):
        if w not in destaques_legenda:
            destaques_legenda.append(w)

    tomadas = {
        "titulo": titulo,
        "palavra_chave": palavra,
        "fonte_padrao": "materiais-de-trabalho/fonte/video-base.mp4",
        "credito_padrao": credito,
        "voz": { "take": "a" },
        "abertura": {
            "titulo": gancho,
            "destaque": destaque_candidato,
            "kicker": kicker,
            "logo": None
        },
        "tomadas": [
            { "id": "t01", "entrada": 0.5, "centro_y": centro_y, "tela_cheia": tela_cheia, "escurecer": escurecer },
            { "id": "t02", "inicio": round(duracao_s * 0.15, 2), "entrada": 6.0, "transicao": transicao_escolhida, "duracao_transicao": duracao_transicao, "centro_y": centro_y, "tela_cheia": tela_cheia, "escurecer": escurecer },
            { "id": "t03", "inicio": round(duracao_s * 0.35, 2), "entrada": 14.0, "transicao": transicao_escolhida, "duracao_transicao": duracao_transicao, "centro_y": centro_y, "tela_cheia": tela_cheia, "escurecer": escurecer },
            { "id": "t04", "inicio": round(duracao_s * 0.65, 2), "entrada": 24.0, "transicao": transicao_escolhida, "duracao_transicao": duracao_transicao, "centro_y": centro_y, "tela_cheia": tela_cheia, "escurecer": escurecer },
            { "id": "t05", "inicio": t_cta, "entrada": 40.0, "transicao": transicao_escolhida, "duracao_transicao": duracao_transicao, "centro_y": centro_y, "tela_cheia": tela_cheia, "escurecer": escurecer }
        ],
        "fechamento": {
            "inicio": t_cta,
            "palavra": palavra,
            "item": "o acesso exclusivo",
            "cauda": 1.4
        },
        "legenda": {
            "destaques": destaques_legenda[:8]
        }
    }
    (narrado_trabalho / "tomadas.json").write_text(json.dumps(tomadas, indent=2, ensure_ascii=False), encoding="utf-8")
    
    # 7. RESPEITAR O ESTILO DA LEGENDA (COR DE DESTAQUE E PLACA ESCURA)
    estilo_legenda = dados.get("estiloLegenda", "amarelo-ouro").lower().strip()
    cor_destaque_legenda = "#F59E0B"
    flag_placa = []
    
    if "verde" in estilo_legenda:
        cor_destaque_legenda = "#10B981"
    elif "violeta" in estilo_legenda or "marca" in estilo_legenda:
        cor_destaque_legenda = projeto.get("cor_destaque", "#8B5CF6")
    elif "branco" in estilo_legenda:
        cor_destaque_legenda = "#FFFFFF"
    elif "amarelo" in estilo_legenda:
        cor_destaque_legenda = "#F59E0B"
        
    if "placa" in estilo_legenda:
        flag_placa = ["--placa", "sempre"]

    try:
        tokens = json.loads(MARCA_TOKENS_FILE.read_text(encoding="utf-8"))
        tokens["cores"]["destaque"] = cor_destaque_legenda
        tokens["nome"] = nome_marca
        MARCA_TOKENS_FILE.write_text(json.dumps(tokens, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[LEGENDA] Cor de destaque configurada para: {cor_destaque_legenda} (Estilo: {estilo_legenda})")
    except Exception as e:
        print(f"[AVISO] Erro ao gravar cor nos tokens: {e}")

    # 8. RESPEITAR A TRILHA SONORA ESCOLHIDA (COPIAR O MP3 REAL PARA marca/audio/leito.mp3)
    trilha_escolhida = dados.get("trilha", "calma-pads").strip()
    flags_mixar = []
    
    if trilha_escolhida == "nenhuma" or not trilha_escolhida:
        flags_mixar.append("--sem-leito")
        print("[AUDIO] Trilha desabilitada (--sem-leito)")
    else:
        nome_arquivo_trilha = trilha_escolhida if trilha_escolhida.endswith(".mp3") else f"{trilha_escolhida}.mp3"
        origem_trilha = RAIZ / "plugins" / "flow-reels" / "componentes" / "trilhas" / nome_arquivo_trilha
        if not origem_trilha.is_file():
            achados = list((RAIZ / "plugins" / "flow-reels" / "componentes" / "trilhas").glob(f"{trilha_escolhida}*.mp3"))
            if achados:
                origem_trilha = achados[0]
        if origem_trilha.is_file():
            pasta_audio_marca = RAIZ / "marca" / "audio"
            pasta_audio_marca.mkdir(parents=True, exist_ok=True)
            shutil.copy2(origem_trilha, pasta_audio_marca / "leito.mp3")
            print(f"[AUDIO] Trilha sonora ativa: {origem_trilha.name}")
        else:
            print(f"[AVISO] Trilha '{trilha_escolhida}' não encontrada no acervo, mantendo padrão.")

    # 9. RESPEITAR EFEITOS SONOROS (SFX)
    sfx_habilitado = dados.get("sfxHabilitado", True)
    if not sfx_habilitado:
        flags_mixar.append("--sem-efeitos")
        print("[AUDIO] Efeitos sonoros desabilitados (--sem-efeitos)")

    # --- EXECUÇÃO DO MOTOR COM AS OPÇÕES DO USUÁRIO ---
    # 1. Linha do Tempo
    executar_comando([
        str(PYTHON_EXE), "plugins/flow-reels/skills/narrado/scripts/linha_do_tempo.py",
        "--projeto", str(pasta_projeto), "--narrado", "01"
    ])
    
    # 2. Compor Vídeo
    executar_comando([
        str(PYTHON_EXE), "plugins/flow-reels/skills/narrado/scripts/compor_narrado.py",
        "--projeto", str(pasta_projeto)
    ])
    
    # 3. Queimar Legendas
    cmd_legenda = [
        str(PYTHON_EXE), "plugins/flow-reels/skills/narrado/scripts/legenda_narrado.py",
        "--projeto", str(pasta_projeto)
    ] + flag_placa
    executar_comando(cmd_legenda)
    
    # 4. Mixar Áudio Final
    cmd_mixar = [
        str(PYTHON_EXE), "plugins/flow-reels/skills/narrado/scripts/mixar.py",
        "--projeto", str(pasta_projeto)
    ] + flags_mixar
    executar_comando(cmd_mixar)
    
    # 5. Criar Revisão
    executar_comando([
        str(PYTHON_EXE), "plugins/flow-reels/skills/narrado/scripts/revisao_narrado.py",
        str(pasta_projeto), "--sem-servidor"
    ])
    
    # Atualizar revisao.json com detalhes
    revisao_json_path = pasta_projeto / "revisao" / "revisao.json"
    if revisao_json_path.is_file():
        try:
            rev = json.loads(revisao_json_path.read_text(encoding="utf-8"))
            if rev.get("cortes"):
                rev["cortes"][0]["porque"] = f"Roteiro estratégico produzido para '{nome_marca}' focado em '{titulo}'."
                rev["cortes"][0]["decisoes"] = [
                    f"Locução neural ({voz_real}) com autoridade e clareza.",
                    f"Transições aplicadas: '{transicao_escolhida}' ({duracao_transicao}s) no modo '{modo_cena}'.",
                    f"Legendas dinâmicas no estilo '{estilo_legenda}' com destaque ({cor_destaque_legenda}).",
                    f"Trilha sonora: '{trilha_escolhida}' masterizada em 1080x1920 a -14.2 LUFS."
                ]
                revisao_json_path.write_text(json.dumps(rev, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception:
            pass

    mp4_final = pasta_projeto / "narrado-01" / "narrado-01.mp4"
    tamanho_mb = round(mp4_final.stat().st_size / (1024 * 1024), 1) if mp4_final.is_file() else 0.0
    
    # Apontar servidor de revisão da porta 8790 para o novo projeto
    apontar_revisao_para_projeto(pasta_projeto)
    
    return {
        "sucesso": True,
        "projeto": nome_projeto,
        "marca": nome_marca,
        "titulo": titulo,
        "gancho": gancho,
        "videoUrl": f"/video/{nome_projeto}/narrado-01/narrado-01.mp4",
        "duracao": f"{round(duracao_s, 1)} s",
        "tamanhoMb": f"{tamanho_mb} MB",
        "cta": palavra,
        "caminho": f"projetos/{nome_projeto}/narrado-01/narrado-01.mp4",
        "revisaoUrl": "http://localhost:8790"
    }


if __name__ == "__main__":
    opcoes = gerar_opcoes_ganchos("Dicas de corte de cabelo e barba para homens no verão", "barbearia-alfa")
    print("Opções de Ganchos:", json.dumps(opcoes, indent=2, ensure_ascii=False))
