# Demos — Dados: Supabase, pgvector e RAG

Código pronto-pra-rodar das demos do tema. Setup escrito para **macOS**.

> Se for a primeira vez que você usa Python no Mac e o `python3` não responder: `brew install python`.

---

## Os 2 arquivos e quando usar cada um

| Arquivo | Quando rodar | Precisa de |
|---|---|---|
| **`rag_local_warmup.py`** | Warmup — antes da gravação, pra entender o ciclo RAG (ingest/retrieve/augment) sem cloud | Apenas `ANTHROPIC_API_KEY` |
| **`rag_supabase_voyage.py`** | **Demo principal da aula** — RAG completo com Supabase + voyage-3 | Conta Supabase + Voyage + Anthropic |

Tem também:

- `supabase_setup.sql` — SQL para criar tabela `documents` e função `match_documents` no Supabase
- `CLAUDE.md` — exemplo de arquivo de contexto (Vídeo 3 explica)

---

## Setup base (5 minutos)

```bash
# 1. Crie um ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# 2. Instale as dependências
pip3 install -r requirements.txt

# 3. Configure as chaves (apenas as que for usar)
export ANTHROPIC_API_KEY="sk-ant-..."
export VOYAGE_API_KEY="pa-..."         # apenas para o exemplo principal
export SUPABASE_URL="https://xxx.supabase.co"
export SUPABASE_KEY="seu_anon_key"
```

> 💡 Persista as chaves entre sessões adicionando ao `~/.zshrc` e rodando `source ~/.zshrc`.

---

## Warmup — `rag_local_warmup.py` 🧠

Use **antes** de gravar. Roda 100% local: ChromaDB com modelo de embeddings padrão (sentence-transformers) + Claude Haiku para gerar a resposta. Zero Supabase, zero Voyage.

```bash
python3 rag_local_warmup.py
```

Roda 3 perguntas exercitando o ciclo completo de RAG:
1. "Esqueci minha senha, o que faço?" → recupera doc sobre reset de senha
2. "Quanto custa o plano com requisições ilimitadas?" → recupera doc sobre planos
3. "Vocês têm relatórios mais detalhados?" → recupera doc sobre roadmap

**Vantagens:**
- ✅ Zero cloud, zero conta, zero API de embeddings
- ✅ Roda offline depois do `pip install`
- ✅ Mesmos conceitos do exemplo principal

---

## Demo principal — `rag_supabase_voyage.py` 🚀

**Este é o exemplo gravado na aula.** Mostra Claude Code integrado ao Supabase com pgvector, gerando embeddings com voyage-3 — stack real de produção.

### Setup do Supabase (uma vez só, ~3 minutos)

1. **Crie uma conta** em https://supabase.com (free tier basta)
2. **Crie um projeto** (escolha região São Paulo se possível)
3. **Pegue suas credenciais** em Project Settings > API:
   - `Project URL` → `SUPABASE_URL`
   - `anon public` ou `service_role` → `SUPABASE_KEY`
4. **Rode o SQL setup** em SQL Editor (cole o conteúdo de `supabase_setup.sql`)
5. **Confirme** que a tabela `documents` foi criada em Table Editor

### Setup do Voyage AI

1. Crie uma conta em https://www.voyageai.com/
2. Pegue sua API key em https://dash.voyageai.com/
3. Tem 50 milhões de tokens grátis pra começar (mais que suficiente)

### Rodando

```bash
python3 rag_supabase_voyage.py
```

A primeira execução faz a ingestão dos docs (gera embeddings com voyage-3 e insere no Supabase). Depois roda 3 perguntas de exemplo.

⚠️ Cada execução re-ingere os documentos. Para evitar duplicatas, comente a linha `ingest(SAMPLE_DOCS)` no `if __name__ == "__main__":` depois da primeira rodada.

---

## CLAUDE.md como camada de contexto (Vídeo 3) 📄

O arquivo `CLAUDE.md` neste diretório serve como exemplo do padrão discutido no Vídeo 3: **um arquivo de contexto que o Claude Code lê automaticamente**.

Quando você abre o Claude Code na pasta `demos/`, ele já carrega o conteúdo do `CLAUDE.md` e entende o projeto sem precisar de busca vetorial.

Use CLAUDE.md quando:
- O contexto cabe num arquivo (~200 linhas no max)
- O conteúdo é estável (decisões de arquitetura, padrões)
- Você quer que TODO conversa com Claude Code já tenha esse contexto

Use RAG (Supabase + voyage) quando:
- A base é grande (centenas/milhares de documentos)
- Pesquisa semântica genuína é necessária
- O conteúdo muda frequentemente (precisa indexar continuamente)

---

## Variações se sobrar tempo na demo (até 20 min)

- **Chunking inteligente** — quebrar docs longos em pedaços antes de embedar
- **Filtros por metadata** — buscar apenas docs da categoria "api" (use `metadata @> '{"category":"api"}'`)
- **Re-ranking** — usar `voyage-rerank-2` para reordenar os resultados após a busca cosseno
- **Persistência local** — trocar `chromadb.Client()` por `chromadb.PersistentClient(path=".chromadb")`

---

## Troubleshooting macOS

- **`command not found: python3`** → `brew install python`
- **Apple Silicon (M1/M2/M3)** → tudo aqui é compatível
- **Erro `pgvector` não encontrado no Supabase** → certifique-se de rodar `create extension vector;` no SQL Editor (linha 1 do `supabase_setup.sql`)
- **HTTP 429 mesmo com Haiku + retry** → confirme sua tier em [console.anthropic.com](https://console.anthropic.com/) (Settings → Rate Limits)
- **Voyage 429** → o free tier do Voyage permite 3 RPM. Espere 30s entre execuções ou pegue uma chave paga
