"""
RAG completo com Supabase + pgvector + voyage-3 + Claude.

ESTE É O EXEMPLO PRINCIPAL DA DEMO DO TEMA — mostra Claude integrado
a uma stack real de produção: Postgres com pgvector (via Supabase) +
embeddings de alta qualidade (voyage-3) + geração com Claude Haiku.

Demonstra os conceitos centrais de RAG:
  - Ingest:    chunks de texto → embeddings (voyage-3) → tabela pgvector
  - Retrieve:  embedar pergunta → cosseno no pgvector → top k
  - Augment:   injetar trechos recuperados no prompt do Claude
  - Generate:  Claude Haiku responde com base no contexto

Pré-requisitos (descritos no README.md):
  1. Conta Supabase + projeto criado (free tier serve)
  2. Extensão `vector` ativada no projeto
  3. Tabela `documents` e função `match_documents` criadas
     (rodar supabase_setup.sql)
  4. Conta Voyage AI: https://www.voyageai.com/
  5. Variáveis de ambiente:
       export SUPABASE_URL="https://xxxxx.supabase.co"
       export SUPABASE_KEY="seu_anon_key_ou_service_role"
       export VOYAGE_API_KEY="pa-..."
       export ANTHROPIC_API_KEY="sk-..."

Como rodar (macOS):
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install -r requirements.txt
    python3 rag_supabase_voyage.py
"""

import os
import time
from typing import Iterable

import anthropic
from anthropic import Anthropic
import voyageai
import voyageai.error
from supabase import create_client


# ============================================================
# 1. CLIENTES (Supabase, Voyage, Anthropic)
# ============================================================

supabase = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_KEY"],
)
voyage = voyageai.Client()    # usa VOYAGE_API_KEY
claude = Anthropic()          # usa ANTHROPIC_API_KEY

CLAUDE_MODEL = "claude-haiku-4-5"
VOYAGE_MODEL = "voyage-3"


def call_claude(prompt: str, max_tokens: int = 200, max_retries: int = 4) -> str:
    """Chamada ao Claude com retry exponencial pra 429."""
    for attempt in range(max_retries):
        try:
            response = claude.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text.strip()
        except anthropic.RateLimitError:
            wait = 2 ** attempt
            print(f"⏳ Rate limit Claude. Aguardando {wait}s...")
            time.sleep(wait)
    raise RuntimeError("Rate limit Claude persistiu.")


# ============================================================
# 2. EMBEDDINGS COM VOYAGE-3
# ============================================================

def voyage_embed_with_retry(texts: list[str], input_type: str, max_retries: int = 4) -> list[list[float]]:
    """Chama voyage.embed com retry exponencial em rate limits.

    Free tier sem payment method tem 3 RPM e 10K TPM — fácil de estourar.
    Para destravar de vez, adicione método de pagamento em
    https://dashboard.voyageai.com/ (200M tokens grátis continuam valendo).
    """
    for attempt in range(max_retries):
        try:
            result = voyage.embed(texts, model=VOYAGE_MODEL, input_type=input_type)
            return result.embeddings
        except voyageai.error.RateLimitError:
            wait = 25 * (2 ** attempt)   # 25s, 50s, 100s, 200s — respeita 3 RPM
            print(f"⏳ Rate limit Voyage (free tier 3 RPM). Aguardando {wait}s...")
            time.sleep(wait)
    raise RuntimeError(
        "Rate limit Voyage persistiu após múltiplas tentativas. "
        "Adicione payment method em https://dashboard.voyageai.com/ "
        "para subir de 3 RPM para ~300 RPM (free tokens continuam)."
    )


def embed_documents(texts: list[str]) -> list[list[float]]:
    """Gera embeddings para vários textos (input_type='document')."""
    return voyage_embed_with_retry(texts, input_type="document")


def embed_query(text: str) -> list[float]:
    """Gera embedding para uma pergunta (input_type='query').

    Distinguir 'document' de 'query' melhora a qualidade da busca.
    """
    return voyage_embed_with_retry([text], input_type="query")[0]


# ============================================================
# 3. INGEST — popular o Supabase com docs + embeddings
# ============================================================

def ingest(docs: Iterable[dict]):
    """Cada doc = {'content': str, 'metadata': dict}.

    Os embeddings são gerados em batch pra eficiência.
    """
    docs_list = list(docs)
    contents = [d["content"] for d in docs_list]
    embeddings = embed_documents(contents)

    rows = [
        {
            "content": d["content"],
            "embedding": emb,
            "metadata": d.get("metadata", {}),
        }
        for d, emb in zip(docs_list, embeddings)
    ]

    supabase.table("documents").insert(rows).execute()
    print(f"✅ {len(rows)} documentos ingeridos no Supabase.")


# ============================================================
# 4. RETRIEVE — busca semântica via pgvector
# ============================================================

def retrieve(question: str, k: int = 3) -> list[dict]:
    """Embeda a pergunta e busca os k documentos mais similares.

    Usa a função SQL `match_documents` (vide supabase_setup.sql).
    """
    query_embedding = embed_query(question)
    response = supabase.rpc(
        "match_documents",
        {"query_embedding": query_embedding, "match_count": k},
    ).execute()
    return response.data


# ============================================================
# 5. AUGMENT + GENERATE — Claude responde com o contexto
# ============================================================

def ask(question: str):
    print("=" * 72)
    print(f"❓ Pergunta: {question}")
    print("=" * 72)

    docs = retrieve(question, k=3)
    print(f"\n📚 Top {len(docs)} documentos recuperados:")
    for i, d in enumerate(docs, 1):
        score = d.get("similarity", 0)
        snippet = d["content"][:80] + "..." if len(d["content"]) > 80 else d["content"]
        print(f"   {i}. [score={score:.3f}] {snippet}")

    context = "\n\n".join(f"- {d['content']}" for d in docs)
    prompt = (
        "Você é um agente de suporte da plataforma SaaS X. "
        "Responda a pergunta usando APENAS o contexto fornecido. "
        "Se a resposta não estiver no contexto, diga que não tem essa informação.\n\n"
        f"CONTEXTO:\n{context}\n\n"
        f"PERGUNTA: {question}\n\n"
        "RESPOSTA:"
    )
    answer = call_claude(prompt)
    print(f"\n💬 Resposta:\n   {answer}")
    print()


# ============================================================
# 6. RODANDO A DEMO
# ============================================================

# Documentação fictícia da plataforma SaaS X
SAMPLE_DOCS = [
    {"content": "Para resetar a senha, acesse Configurações > Conta > Reset de senha. "
                "O link de reset chega por email em até 5 minutos.",
     "metadata": {"category": "conta"}},
    {"content": "Plano Free: até 1.000 requisições/mês. "
                "Plano Pro: R$ 29/mês com 50.000 requisições. "
                "Plano Business: R$ 199/mês com requisições ilimitadas.",
     "metadata": {"category": "planos"}},
    {"content": "API disponível em https://api.exemplo.com/v1. "
                "Autenticação via Bearer Token no header Authorization. "
                "Endpoints: /users, /projects, /events.",
     "metadata": {"category": "api"}},
    {"content": "Tela de relatórios avançados planejada para julho de 2026. "
                "Disponibilidade primeiro para clientes Business.",
     "metadata": {"category": "roadmap"}},
    {"content": "Integração com Slack em Integrações > Slack > Conectar Workspace. "
                "Necessário ser admin do workspace.",
     "metadata": {"category": "integracoes"}},
    {"content": "Backup automático diário às 03h (São Paulo). "
                "Retenção de 30 dias no Pro e 90 dias no Business.",
     "metadata": {"category": "backup"}},
]


if __name__ == "__main__":
    required = ["SUPABASE_URL", "SUPABASE_KEY", "VOYAGE_API_KEY", "ANTHROPIC_API_KEY"]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        print(f"⚠️  Variáveis ausentes: {', '.join(missing)}")
        print("   Veja o README.md para o passo-a-passo de setup.")
        raise SystemExit(1)

    # 1. Ingestão única (rode só na primeira vez ou após mudança nos docs)
    print("\n🔧 Ingerindo documentos no Supabase (com voyage-3)...")
    ingest(SAMPLE_DOCS)

    # 2. Algumas perguntas para exercitar o RAG.
    # Pausa de 25s entre execuções porque a Voyage free tier limita 3 RPM
    # (≈ 1 chamada a cada 20s). Cada ask() faz 1 chamada à Voyage.
    # Para destravar a gravação: adicione payment method em
    # https://dashboard.voyageai.com/ (free tokens continuam, rate limit sobe).
    ask("Esqueci minha senha, o que faço?")
    time.sleep(25)
    ask("Quanto custa o plano com requisições ilimitadas?")
    time.sleep(25)
    ask("Vocês têm relatórios mais detalhados?")
