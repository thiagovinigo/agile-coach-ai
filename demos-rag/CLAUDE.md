# Contexto do projeto — Demo RAG (Tema 2)

> Este arquivo é lido automaticamente pelo Claude Code. Serve como
> **camada de contexto** para o modelo entender o projeto sem precisar
> de busca vetorial — exatamente o padrão discutido no Vídeo 3.

## O que é este projeto

Demo do Tema 2 (Dados: Supabase, pgvector e RAG) da Etapa 5 da Formação
Claude Code Engineering. Mostra como Claude Code interage com bancos
vetoriais para implementar RAG.

## Estrutura

- `rag_local_warmup.py` — warmup local com ChromaDB (sem cloud, sem voyage)
- `rag_supabase_voyage.py` — demo principal: Supabase + pgvector + voyage-3
- `supabase_setup.sql` — SQL para criar tabela e função de busca no Supabase
- `requirements.txt` — dependências
- `README.md` — passo-a-passo de setup

## Decisões de arquitetura

- **Modelo do Claude:** `claude-haiku-4-5` (rate limit alto, custo baixo, ideal para demos)
- **Modelo de embeddings:** `voyage-3` (1024 dimensões, recomendado pela Anthropic)
- **Banco vetorial:** Supabase com pgvector (Postgres + extensão vector)
- **Tipo de índice:** HNSW com `vector_cosine_ops` (similaridade de cosseno)
- **Tamanho do top-k:** 3 documentos por busca (suficiente para perguntas curtas)
- **Distinção document vs query:** voyage-3 aceita `input_type` distinto, melhora a qualidade

## Padrões de código

- Toda chamada à API do Claude passa pelo wrapper `call_claude()` com retry exponencial
- Variáveis de ambiente são lidas via `os.environ[]` (falha rápido se faltar) ou `os.getenv()` (opcional)
- Documentação inline em cada bloco (1. State, 2. Cliente, 3. Nodes, etc)

## Como o Claude Code deve atuar neste repo

- Manter o estilo enxuto e didático (cada bloco numerado e comentado)
- Não introduzir frameworks pesados (FastAPI, etc) sem necessidade — esta demo é focada em RAG
- Sugerir migração para o exemplo principal só depois que o warmup local estiver funcionando

## Exemplo: ler este CLAUDE.md como contexto

Quando você abrir o Claude Code nesta pasta, ele já carrega este arquivo automaticamente.
Pode pedir coisas como:

- "Adicione um novo doc à base de conhecimento"
- "Mude o modelo de embeddings para voyage-3-lite"
- "Crie uma função para deletar documentos pelo metadata.category"

E o Claude já saberá o contexto sem precisar perguntar.
