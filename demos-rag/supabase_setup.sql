-- =====================================================================
-- Setup do Supabase para o demo RAG (Tema 2 — Etapa 5)
--
-- Cole estes comandos no SQL Editor do seu projeto Supabase:
-- https://supabase.com/dashboard/project/_/sql
-- =====================================================================

-- 1. Ativa a extensão pgvector (já vem instalada no Supabase, só precisa habilitar)
create extension if not exists vector;


-- 2. Tabela de documentos com a coluna `embedding` do tipo vector(1024)
--    1024 é a dimensão dos embeddings do voyage-3
create table if not exists documents (
  id          bigserial primary key,
  content     text not null,
  embedding   vector(1024) not null,
  metadata    jsonb default '{}'::jsonb,
  created_at  timestamptz default now()
);


-- 3. Índice HNSW para busca aproximada de vizinhos (rápida em produção)
--    Use cosine_ops para similaridade de cosseno
create index if not exists documents_embedding_idx
  on documents
  using hnsw (embedding vector_cosine_ops);


-- 4. Função para busca semântica
--    Retorna os top N documentos mais similares à query, com a similaridade.
create or replace function match_documents (
  query_embedding vector(1024),
  match_count int default 3
)
returns table (
  id bigint,
  content text,
  metadata jsonb,
  similarity float
)
language sql stable
as $$
  select
    d.id,
    d.content,
    d.metadata,
    1 - (d.embedding <=> query_embedding) as similarity
  from documents d
  order by d.embedding <=> query_embedding
  limit match_count;
$$;


-- 5. Desabilita RLS (Row-Level Security) para esta demo
--    O Supabase ativa RLS por padrão em tabelas novas, bloqueando todas
--    as operações até você criar policies. Para um projeto isolado de
--    aprendizado, desabilitar RLS é o caminho mais simples.
--
--    EM PRODUÇÃO: deixe RLS ativado e crie policies adequadas para sua
--    aplicação (autenticação, multi-tenancy, etc).
alter table documents disable row level security;


-- =====================================================================
-- Pronto! Agora rode `python3 rag_supabase_voyage.py` no terminal.
-- =====================================================================
