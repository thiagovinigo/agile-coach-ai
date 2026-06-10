# Comandos Slash — Guia de Referência

Todos os slash commands disponíveis no pacote Flowgrammers Skills. Cada comando é um arquivo `.md` nesta pasta que o Claude Code carrega automaticamente via `~/.claude/commands/`.

---

## Como usar

```bash
# No Claude Code, basta digitar:
/nome-do-comando [argumentos]

# Exemplos:
/prd Adicionar autenticação via SSO ao painel admin
/tdd generate src/services/pagamento.ts
/saas-health metrics --mrr 120000 --customers 350 --churned 5
```

---

## Índice de Comandos

### Engenharia & Código

| Comando | O que faz | Uso rápido |
|---------|-----------|------------|
| `/a11y-audit` | Varre um projeto frontend em busca de violações WCAG 2.2 e corrige automaticamente o que for possível | `/a11y-audit ./src --fix` |
| `/changelog` | Gera entradas de changelog no formato Keep a Changelog a partir do histórico git; valida mensagens de commit convencional | `/changelog generate --from-tag v2.0.0` |
| `/focused-fix` | Protocolo de 5 fases para reparar sistematicamente uma feature/módulo inteiro (escopo → rastreamento → diagnóstico → correção → verificação) | `/focused-fix src/features/pagamento` |
| `/karpathy-check` | Revisa alterações em stage ou o último commit com base nos 4 princípios do Karpathy: simplicidade, cirurgia, pensamento e verificação de objetivos | `/karpathy-check` |
| `/pipeline` | Detecta o stack do projeto e gera YAML de pipeline CI/CD para GitHub Actions ou GitLab CI | `/pipeline generate --platform github` |
| `/tdd` | Gera testes, analisa cobertura e valida qualidade dos testes | `/tdd generate src/auth/login.ts` |
| `/tech-debt` | Varre o codebase em busca de dívida técnica, pontua severidade e gera plano de remediação priorizado | `/tech-debt scan ./src` |

---

### Produto & UX

| Comando | O que faz | Uso rápido |
|---------|-----------|------------|
| `/code-to-prd` | Faz engenharia reversa de um codebase frontend e gera um PRD completo com inventário de páginas, APIs e enums | `/code-to-prd ./src` |
| `/competitive-matrix` | Constrói matriz competitiva com pontuação ponderada, análise de lacunas e posicionamento de mercado | `/competitive-matrix analyze competitors.json` |
| `/okr` | Gera cascata de OKRs da estratégia da empresa até os key results de cada time | `/okr generate growth` |
| `/persona` | Gera personas de usuário estruturadas com dados demográficos, objetivos e padrões comportamentais | `/persona generate` |
| `/prd` | Gera um PRD conciso para uma feature, iniciativa ou problema | `/prd Onboarding guiado para novos usuários` |
| `/rice` | Prioriza features usando pontuação RICE (Reach, Impact, Confidence, Effort) com limite de capacidade opcional | `/rice prioritize features.csv --capacity 20` |
| `/sprint-plan` | Cria um plano de sprint com stories priorizadas, escopo stretch, riscos e dependências | `/sprint-plan "Lançar módulo de relatórios" 34` |
| `/user-story` | Gera user stories estruturadas com critérios de aceite e planejamento de sprint | `/user-story generate` |

---

### Gestão de Projetos & Times

| Comando | O que faz | Uso rápido |
|---------|-----------|------------|
| `/project-health` | Gera dashboard de saúde de portfólio e análise de matriz de riscos | `/project-health dashboard portfolio-q2.json` |
| `/retro` | Analisa dados de retrospectiva de sprint para temas recorrentes, sentimento e eficácia dos itens de ação | `/retro analyze sprint-24-retro.json` |
| `/sprint-health` | Pontua a saúde do sprint em entrega, qualidade e métricas de time; analisa tendência de velocidade | `/sprint-health analyze sprint-24.json` |
| `/tc` | Rastreia mudanças técnicas com registros estruturados, máquina de estados e handoff entre sessões | `/tc create minha-feature` |

---

### Financeiro & SaaS

| Comando | O que faz | Uso rápido |
|---------|-----------|------------|
| `/financial-health` | Analisa demonstrações financeiras, constrói valuation DCF, avalia variações orçamentárias e elabora previsões | `/financial-health ratios dados.json` |
| `/saas-health` | Calcula métricas de saúde SaaS (ARR, MRR, churn, CAC, LTV, NRR) e compara com benchmarks do setor | `/saas-health metrics --mrr 80000 --customers 200 --churned 3` |

---

### Marketing & SEO

| Comando | O que faz | Uso rápido |
|---------|-----------|------------|
| `/seo-auditor` | Audita e otimiza arquivos de documentação para SEO em 7 fases: meta tags, conteúdo, palavras-chave, links, sitemap | `/seo-auditor docs/` |

---

### Infraestrutura & Operações

| Comando | O que faz | Uso rápido |
|---------|-----------|------------|
| `/google-workspace` | Administração do Google Workspace via CLI: diagnóstico, auditoria de segurança, execução de receitas e análise de saída | `/google-workspace audit --services gmail,drive` |

---

### Auditoria & Qualidade

| Comando | O que faz | Uso rápido |
|---------|-----------|------------|
| `/plugin-audit` | Auditoria completa de 8 fases para skills, plugins, agentes e comandos: estrutura, qualidade, segurança, marketplace, ecossistema e revisão de código | `/plugin-audit product-team/code-to-prd` |

---

### Wiki LLM

Conjunto de comandos para construir e consultar uma base de conhecimento pessoal estruturada (LLM Wiki).

| Comando | O que faz | Uso rápido |
|---------|-----------|------------|
| `/wiki-init` | Inicializa um novo vault LLM Wiki com estrutura em três camadas, esquemas e templates | `/wiki-init ~/vaults/pesquisa --topic "Interpretabilidade de LLMs"` |
| `/wiki-ingest` | Ingere uma fonte no wiki: lê, discute TL;DR, escreve resumo, atualiza referências cruzadas (5–15 páginas) e registra no log | `/wiki-ingest raw/papers/artigo.pdf` |
| `/wiki-query` | Consulta o wiki: lê o índice, aprofunda em páginas relevantes, sintetiza resposta com citações e oferece arquivar a resposta | `/wiki-query "compare abordagens de RAG vs fine-tuning"` |
| `/wiki-lint` | Verificação de saúde do wiki: páginas órfãs, links quebrados, contradições, frontmatter ausente e desvios estruturais | `/wiki-lint --stale-days 30` |
| `/wiki-log` | Exibe entradas recentes do log do wiki com filtros por operação e data | `/wiki-log --last 20 --op ingest` |

---

## Instalação

Os comandos são instalados automaticamente pelo script de instalação do pacote:

```bash
# Instalação completa
curl -fsSL https://raw.githubusercontent.com/ricardonevesbraga/flowgrammers-skills/main/install.sh | bash
```

Ou manualmente, copiando os arquivos `.md` desta pasta para `~/.claude/commands/`.

---

## Estrutura de um arquivo de comando

Cada arquivo segue este padrão:

```markdown
---
name: nome-do-comando
description: Descrição curta. Uso: /nome-do-comando [argumentos]
---

# /nome-do-comando

Descrição detalhada do que o comando faz.

## Uso
...

## Exemplos
...

## Referência de Skill
→ caminho/para/SKILL.md
```

O frontmatter `name` e `description` são usados pelo Claude Code para descoberta e autocompletar.
