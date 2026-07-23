const tfsData = {
    "Fase 1: Fundações": [
        {
            "id": "passo1",
            "title": "Passo 1: Processo Herdado",
            "description": "Como criar um Processo Herdado no Azure DevOps e associá-lo ao seu Projeto.",
            "path": "contexto/tfs/passo1-processo.md"
        },
        {
            "id": "passo2",
            "title": "Passo 2: Limpeza de Estados Nativos",
            "description": "Como ocultar os estados nativos (New, Active, Closed) para abrir espaço ao nosso fluxo.",
            "path": "contexto/tfs/passo2-limpeza.md"
        }
    ],
    "Fase 2: Estruturação": [
        {
            "id": "passo3",
            "title": "Passo 3: Mapeamento de Estados",
            "description": "Criação dos novos Estados e mapeamento obrigatório para as Categorias Nativas do Azure (com exemplos visuais).",
            "path": "contexto/tfs/passo3-estados.md"
        },
        {
            "id": "passo4",
            "title": "Passo 4: Campos Customizados",
            "description": "Criação dos campos estruturais: Expedite, Blocked, Blocked Reason e Review Type.",
            "path": "contexto/tfs/passo4-campos.md"
        }
    ],
    "Fase 3: O Board Visual": [
        {
            "id": "passo5",
            "title": "Passo 5: Colunas, Split e WIP",
            "description": "Mapeamento das colunas de Upstream e Downstream no Board Kanban, configurando Doing/Done e limites (com exemplos visuais).",
            "path": "contexto/tfs/passo5-board.md"
        },
        {
            "id": "passo6",
            "title": "Passo 6: Classes de Serviço",
            "description": "Como configurar a Swimlane Urgente/Expedite para separar itens de alta prioridade.",
            "path": "contexto/tfs/passo6-swimlanes.md"
        }
    ],
    "Fase 4: Automações": [
        {
            "id": "passo7",
            "title": "Passo 7: Ciclo de Vida (Epic/Feature)",
            "description": "Automação em cascata (R1, R2, R3) para que os pais sejam atualizados pelo progresso dos itens filhos.",
            "path": "contexto/tfs/passo7-ciclo-vida.md"
        },
        {
            "id": "passo8",
            "title": "Passo 8: Rastreador de Bloqueios",
            "description": "Regras automáticas para capturar 'Blocked Start Date' e 'Blocked End Date'.",
            "path": "contexto/tfs/passo8-blocked.md"
        },
        {
            "id": "passo9",
            "title": "Passo 9: Trava do PO",
            "description": "Regra que impede a transição para 'Pronto para Replenishment' sem a aprovação do Product Owner.",
            "path": "contexto/tfs/passo9-trava-po.md"
        }
    ],
    "Fase 5: Operação": [
        {
            "id": "passo10",
            "title": "Passo 10: Métricas e Dicas IA",
            "description": "Como as colunas se traduzem em Lead Time, WIP e Cycle Time, e prompts para recriar o board via IA.",
            "path": "contexto/tfs/passo10-metricas.md"
        }
    ]
};
