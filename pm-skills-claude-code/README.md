# PM Skills for Claude Code

> **27 Product Management skills** ready to use as `/commands` in [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Clone, open Claude Code, start shipping.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-27-brightgreen)](.claude/commands/)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-blueviolet)](https://docs.anthropic.com/en/docs/claude-code)

---

## O que é / What is this

**pt-BR**: Um kit de 27 skills de Product Management para o Claude Code. Cobre todo o ciclo de produto — discovery, delivery, strategy, validation, execution e go-to-market. Baseado nos frameworks de Teresa Torres, Ash Maurya, Sean Ellis, Marty Cagan, Rob Fitzpatrick e outros.

**EN**: A kit of 27 Product Management skills for Claude Code. Covers the full product lifecycle — discovery, delivery, strategy, validation, execution, and go-to-market. Built on frameworks from Teresa Torres, Ash Maurya, Sean Ellis, Marty Cagan, Rob Fitzpatrick, and more.

---

## Instalação / Installation

### Opção 1: Clone direto (recomendado / recommended)

```bash
git clone https://github.com/flowgrammers/pm-skills-claude-code.git
cd pm-skills-claude-code
# Abra o Claude Code aqui / Open Claude Code here
# Todas as 27 skills estarão disponíveis como /commands
```

### Opção 2: Instalação global / Global install

Instala as skills em `~/.claude/commands/` para usar em qualquer projeto.

```bash
# Unix/macOS/WSL
chmod +x scripts/install-global.sh
./scripts/install-global.sh

# Windows PowerShell
.\scripts\install-global.ps1
```

### Opção 3: Manual

Copie os arquivos de `.claude/commands/` para `~/.claude/commands/`:

```bash
mkdir -p ~/.claude/commands
cp .claude/commands/*.md ~/.claude/commands/
```

---

## 27 Skills — Catálogo Completo / Full Catalog

### DISCOVERY (7) — Entender o problema / Understand the problem

| Comando | Descrição | When to use |
|---------|-----------|-------------|
| `/persona` | Personas com JTBD, behaviors, pain points | Project kickoff |
| `/discovery` | Ciclo de descoberta completo | Ill-defined problem |
| `/interview-synthesis` | Sintetiza entrevistas em padrões | After 3+ interviews |
| `/competitive-analysis` | Mapa competitivo | Before PRD or strategy |
| `/opportunity-tree` | OST de Teresa Torres | Deciding where to invest |
| `/hypothesis` | Hipóteses testáveis com kill criteria | Before any experiment |
| `/customer-journey` | Jornada do cliente (7 estágios) | End-to-end experience |

### DELIVERY (3) — Especificar a solução / Specify the solution

| Comando | Descrição | When to use |
|---------|-----------|-------------|
| `/prd` | PRD completo (8 seções) | Validated hypothesis |
| `/user-stories` | User stories INVEST | Break down for eng |
| `/acceptance-criteria` | Given/When/Then | Detail for QA |

### STRATEGY (7) — Priorizar e alinhar / Prioritize and align

| Comando | Descrição | When to use |
|---------|-----------|-------------|
| `/prioritize` | RICE scoring + recomendação | 5+ features to sequence |
| `/strategy` | Canvas de estratégia (9 seções) | New quarter |
| `/roadmap` | Roadmap trimestral | Communicate to team |
| `/okr` | OKRs cascateados | Quarter start |
| `/lean-canvas` | Canvas de Ash Maurya | Business model validation |
| `/pricing` | 7 modelos de pricing | Define monetization |
| `/north-star` | NSM + input metrics | Define main metric |

### VALIDATION (3) — Testar e medir / Test and measure

| Comando | Descrição | When to use |
|---------|-----------|-------------|
| `/experiment-design` | Design de pretotypes e A/B tests | Before building |
| `/measure-pmf` | Product-Market Fit (Sean Ellis) | 50+ active users |
| `/ab-test-analysis` | Análise estatística de A/B test | After experiment |

### EXECUTION (2) — Preparar o lançamento / Prepare launch

| Comando | Descrição | When to use |
|---------|-----------|-------------|
| `/pre-mortem` | Risk analysis (Tigers framework) | 2-3 weeks before launch |
| `/launch-checklist` | Checklist cross-functional | 1-2 weeks before launch |

### COMMUNICATION & GTM (5) — Comunicar e lançar / Communicate and launch

| Comando | Descrição | When to use |
|---------|-----------|-------------|
| `/release-notes` | Release notes orientadas a benefício | Feature shipped |
| `/stakeholder-update` | Status executivo | Sprint end, board meeting |
| `/gtm` | Go-to-market completo | Product/feature launch |
| `/battlecard` | Battlecard competitiva | Position vs competitor |
| `/ideal-customer-profile` | ICP detalhado | Define target audience |

---

## Workflows — Combos de Skills

Encadeie skills para fluxos completos / Chain skills for complete flows:

| Workflow | Skills | Quando usar / When |
|----------|--------|-------------------|
| **Customer Discovery** | `/persona` → `/discovery` → `/interview-synthesis` → `/opportunity-tree` | Começando do zero / Starting from scratch |
| **Feature Kickoff** | `/hypothesis` → `/prd` → `/user-stories` → `/acceptance-criteria` | Especificar feature / Spec a feature |
| **Product Strategy** | `/competitive-analysis` → `/strategy` → `/okr` → `/roadmap` → `/stakeholder-update` | Planejar trimestre / Plan the quarter |
| **Validate & Launch** | `/experiment-design` → `/pre-mortem` → `/launch-checklist` → `/gtm` | Testar e lançar / Test and launch |
| **Pricing & GTM** | `/pricing` → `/ideal-customer-profile` → `/battlecard` → `/gtm` | Monetizar / Monetize |
| **Growth Sprint** | `/north-star` → `/experiment-design` → `/ab-test-analysis` → `/okr` | Crescimento / Growth |
| **Board Update** | `/measure-pmf` → `/stakeholder-update` → `/roadmap` | Reunião com investidores / Investor meeting |

Mais detalhes em [tutorial/03-workflows.md](tutorial/03-workflows.md).

---

## Como usar / How to use

### Chamando uma skill / Calling a skill

```
/discovery
Problema: Churn alto em onboarding (35% em 7 dias)
Contexto: B2B SaaS CRM, 400 users, mid-market
Restrições: 2 semanas para decidir se faz PRD
```

### Encadeando skills / Chaining skills

```
/persona → output: Persona "Alex, Sales Rep"
     ↓
/discovery → input: Persona Alex + churn problem
     ↓
/prd → input: Validated hypothesis from discovery
     ↓
/user-stories → input: Approved PRD
```

### Regras de ouro / Golden rules

- **Contexto mínimo**: Problema + audiência + constraints
- **Quanto mais específico, melhor**: Dados > opiniões
- **Skills são independentes**: Mas muito mais poderosas encadeadas
- **Refine iterativamente**: Primeiro draft → refine → valide

---

## Jornadas / Journeys

Este kit inclui guias metodológicos completos:

| Tutorial | Conteúdo / Content |
|----------|-------------------|
| [00 — Como usar](tutorial/00-como-usar.md) | Quick start, mapa de skills |
| [01 — Jornada 0→1](tutorial/01-zero-a-um.md) | 7 fases: da ideia ao Product-Market Fit |
| [02 — Jornada 1→100](tutorial/02-um-a-cem.md) | 4 fases: do PMF ao scale |
| [03 — Workflows](tutorial/03-workflows.md) | 7 workflows prontos com exemplos |

---

## Frameworks & Fontes / Sources

| Framework | Autor / Author | Skill |
|-----------|---------------|-------|
| Opportunity Solution Tree | Teresa Torres | `/opportunity-tree` |
| Lean Canvas | Ash Maurya | `/lean-canvas` |
| Mom Test | Rob Fitzpatrick | `/discovery`, `/interview-synthesis` |
| PMF Survey (40%) | Sean Ellis | `/measure-pmf` |
| Superhuman PMF Engine | Rahul Vohra | `/measure-pmf` |
| Pretotyping / YODA | Alberto Savoia | `/experiment-design` |
| Growth Loops | Reforge | `/north-star` |
| RICE Scoring | Intercom | `/prioritize` |
| INVEST Stories | Mike Cohn | `/user-stories` |
| Gherkin/BDD | Cucumber | `/acceptance-criteria` |
| OKR Principles | 55 Product Leaders (Lenny) | `/okr` |
| Pre-mortem | Gary Klein | `/pre-mortem` |
| Value-Based Pricing | Paddle/Price Intelligently | `/pricing` |
| ICP Framework | Multiple | `/ideal-customer-profile` |

---

## Estrutura / Structure

```
pm-skills-claude-code/
├── README.md              ← Você está aqui / You are here
├── CLAUDE.md              ← Context file for Claude Code
├── LICENSE                ← MIT
├── .claude/commands/      ← 27 skills (the core)
├── tutorial/              ← 4 methodology guides
├── templates/             ← 4 fillable templates
└── scripts/               ← Global install scripts
```

---

## Requisitos / Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) instalado
- Conta Anthropic com acesso ao Claude Code

---

## Contribuindo / Contributing

PRs são bem-vindos! Para adicionar uma nova skill:

1. Crie um arquivo `.md` em `.claude/commands/`
2. Siga o formato das skills existentes (veja qualquer arquivo como referência)
3. Atualize o `CLAUDE.md` com a nova skill na tabela do domínio correspondente
4. Abra um PR com descrição do caso de uso

---

## Licença / License

[MIT](LICENSE) — use, modifique e distribua livremente.

---

Made with Claude Code by [Flowgrammers](https://github.com/flowgrammers)
