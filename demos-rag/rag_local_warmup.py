"""
WARMUP / ESTUDO — RAG local com ChromaDB (SEM Supabase, SEM Voyage).

Use este arquivo para SE FAMILIARIZAR com o ciclo completo do RAG
(ingest → embed → store → query → retrieve → augment) antes de
rodar o exemplo principal (rag_supabase_voyage.py).

Aqui usamos:
  - ChromaDB com modelo de embedding default (sentence-transformers,
    roda localmente, zero API)
  - Claude Haiku para gerar a resposta final (única chamada à API)

Comparação com o exemplo principal:

  rag_supabase_voyage (demo da aula):
    docs → voyage-3 → Supabase/pgvector → busca cosseno → Claude

  rag_local_warmup (este, warmup local):
    docs → sentence-transformers → ChromaDB em memória → busca → Claude

Demonstra os MESMOS conceitos do RAG:
  - Ingest:    quebrar conteúdo em chunks e gerar embeddings
  - Store:     guardar texto + vetor numa base vetorial
  - Query:    embedar a pergunta e buscar os k mais similares
  - Augment:  injetar o contexto recuperado no prompt do Claude

Como rodar (macOS):
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install -r requirements.txt
    export ANTHROPIC_API_KEY="sua_chave_aqui"
    python3 rag_local_warmup.py
"""

import os
import time
import chromadb
import anthropic
from anthropic import Anthropic


# ============================================================
# 1. BASE DE CONHECIMENTO MOCK
#    Documentação fictícia de uma plataforma SaaS.
# ============================================================

KNOWLEDGE_BASE = [
    "Para resetar a senha, acesse Configurações > Conta > Reset de senha. "
    "O link de reset chega por email em até 5 minutos.",

    "Nosso plano Free inclui até 1.000 requisições por mês. "
    "O plano Pro custa R$ 29/mês e inclui 50.000 requisições. "
    "O plano Business custa R$ 199/mês com requisições ilimitadas.",

    "A API está disponível em https://api.exemplo.com/v1. "
    "A autenticação é feita via Bearer Token no header Authorization. "
    "Endpoints principais: /users, /projects, /events.",

    "Tela de relatórios avançados está planejada para Q3 (julho de 2026). "
    "Já está sendo construída e estará disponível primeiro para clientes Business.",

    "Para integrar com Slack, vá em Integrações > Slack > Conectar Workspace. "
    "Necessário ser admin do workspace do Slack.",

    "O backup automático roda diariamente às 03h (horário de São Paulo). "
    "Backups são retidos por 30 dias para clientes Pro e 90 dias para Business.",
]


# ============================================================
# 2. CLIENTE ANTHROPIC (com retry para 429)
# ============================================================

claude = Anthropic()
MODEL = "claude-haiku-4-5"


def call_claude(prompt: str, max_tokens: int = 200, max_retries: int = 4) -> str:
    """Wrapper com retry exponencial para rate limits."""
    for attempt in range(max_retries):
        try:
            response = claude.messages.create(
                model=MODEL,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text.strip()
        except anthropic.RateLimitError:
            wait = 2 ** attempt
            print(f"⏳ Rate limit. Aguardando {wait}s...")
            time.sleep(wait)
    raise RuntimeError("Rate limit persistiu.")


# ============================================================
# 3. BASE VETORIAL (ChromaDB local, em memória)
# ============================================================

def build_vector_store():
    """Cria a coleção e ingere os documentos.

    O ChromaDB usa internamente o modelo padrão de embeddings
    (all-MiniLM-L6-v2 via sentence-transformers). Tudo local.
    """
    client = chromadb.Client()  # in-memory; some on disk: chromadb.PersistentClient(path=".chromadb")
    collection = client.create_collection(name="docs")

    collection.add(
        documents=KNOWLEDGE_BASE,
        ids=[f"doc-{i}" for i in range(len(KNOWLEDGE_BASE))],
    )
    return collection


# ============================================================
# 4. RAG — Retrieve + Augment + Generate
# ============================================================

def retrieve(collection, question: str, k: int = 3) -> list[str]:
    """Busca os k documentos mais relevantes para a pergunta."""
    results = collection.query(query_texts=[question], n_results=k)
    return results["documents"][0]


def augment_and_generate(question: str, context_docs: list[str]) -> str:
    """Monta o prompt aumentado e pede uma resposta ao Claude."""
    context = "\n\n".join(f"- {doc}" for doc in context_docs)
    prompt = (
        "Você é um agente de suporte da plataforma SaaS X. "
        "Responda a pergunta do cliente usando APENAS o contexto fornecido. "
        "Se a resposta não estiver no contexto, diga que não tem essa informação.\n\n"
        f"CONTEXTO:\n{context}\n\n"
        f"PERGUNTA: {question}\n\n"
        "RESPOSTA:"
    )
    return call_claude(prompt)


def ask(collection, question: str):
    """Pipeline RAG completo para uma pergunta."""
    print("=" * 72)
    print(f"❓ Pergunta: {question}")
    print("=" * 72)

    docs = retrieve(collection, question, k=3)
    print("\n📚 Documentos recuperados (top 3):")
    for i, d in enumerate(docs, 1):
        snippet = d[:80] + "..." if len(d) > 80 else d
        print(f"   {i}. {snippet}")

    answer = augment_and_generate(question, docs)
    print(f"\n💬 Resposta:\n   {answer}")
    print()


# ============================================================
# 5. RODANDO A DEMO
# ============================================================

if __name__ == "__main__":
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  Defina ANTHROPIC_API_KEY antes de rodar.")
        raise SystemExit(1)

    print("\n🔧 Construindo base vetorial local com ChromaDB...")
    collection = build_vector_store()
    print(f"✅ {collection.count()} documentos indexados.\n")

    # Três perguntas exercitando a busca semântica.
    # Pausa de 2s entre execuções pra espalhar as chamadas no minuto
    # e reduzir a chance de HTTP 429 (rate limit) na Tier 1.
    ask(collection, "Esqueci minha senha, o que faço?")
    time.sleep(2)
    ask(collection, "Quanto custa o plano com requisições ilimitadas?")
    time.sleep(2)
    ask(collection, "Vocês têm relatórios mais detalhados?")
