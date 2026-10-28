const demosRagData = {
    "GUIA DE SETUP & CONTEXTO (CLAUDE CODE)": [
        {
            id: "rag-readme",
            title: "README: Passo a Passo Completo (Warmup + Produção)",
            description: "Guia oficial da demo: quando usar o Warmup Local vs Supabase Cloud, setup em 5 minutos, chaves de API, variações de aula e troubleshooting.",
            icon: "📖",
            path: "demos-rag/README.md"
        },
        {
            id: "rag-claude-md",
            title: "CLAUDE.md: Camada de Contexto Automática (Vídeo 3)",
            description: "Exemplo prático de como o Claude Code lê o contexto arquitetural do projeto automaticamente sem precisar de busca vetorial.",
            icon: "🧠",
            path: "demos-rag/CLAUDE.md"
        },
        {
            id: "rag-requirements",
            title: "requirements.txt (Stack Python)",
            description: "Dependências enxutas do projeto: anthropic, voyageai, supabase e chromadb.",
            icon: "📦",
            path: "demos-rag/requirements.txt"
        }
    ],
    "IMPLEMENTAÇÕES RAG (LOCAL VS PRODUÇÃO)": [
        {
            id: "rag-local-warmup",
            title: "1. rag_local_warmup.py (Warmup 100% Local com ChromaDB)",
            description: "Ciclo completo de RAG (Ingest → Embed → Store → Retrieve → Augment) rodando em memória com ChromaDB + sentence-transformers e Claude Haiku.",
            icon: "🏠",
            path: "demos-rag/rag_local_warmup.py"
        },
        {
            id: "rag-supabase-voyage",
            title: "2. rag_supabase_voyage.py (Demo Principal: Supabase + Voyage-3)",
            description: "Stack real de produção: embeddings de 1024 dimensões com voyage-3 (input_type document vs query), busca cosseno no pgvector e geração com retry exponencial.",
            icon: "🚀",
            path: "demos-rag/rag_supabase_voyage.py"
        }
    ],
    "BANCO VETORIAL & SCRIPTS DE DIAGNÓSTICO": [
        {
            id: "rag-supabase-sql",
            title: "supabase_setup.sql (Tabela, Índice HNSW & RPC)",
            description: "Script SQL para ativar a extensão pgvector, criar a tabela documents vector(1024), índice HNSW (vector_cosine_ops) e função match_documents.",
            icon: "🗄️",
            path: "demos-rag/supabase_setup.sql"
        },
        {
            id: "rag-test-setup",
            title: "test_setup.py (Smoke Test das 3 Nuvens)",
            description: "Script de verificação rápida que valida variáveis de ambiente, chamada ao Claude Haiku, geração de vetor na Voyage AI e leitura na tabela do Supabase.",
            icon: "✅",
            path: "demos-rag/test_setup.py"
        },
        {
            id: "rag-embedding-test",
            title: "embedding_test.py (Inspeção de Vetor Voyage-3)",
            description: "Teste mínimo para inspecionar o vetor de 1024 dimensões retornado pelo modelo voyage-3 com input_type='query'.",
            icon: "🔬",
            path: "demos-rag/embedding_test.py"
        }
    ]
};
