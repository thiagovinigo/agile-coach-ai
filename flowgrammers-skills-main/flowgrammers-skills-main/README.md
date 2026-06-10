# Flowgrammers Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-e8006a.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-383-e8006a.svg)](#mapa-completo-de-skills)
[![Idioma](https://img.shields.io/badge/idioma-PT--BR-e8006a.svg)](#)
[![Plataformas](https://img.shields.io/badge/plataformas-Claude%20·%20Cursor%20·%20Codex%20·%20Windsurf-00e8d0.svg)](#como-usar)
[![Version](https://img.shields.io/badge/version-2.2.0-00e8d0.svg)](CHANGELOG.md)

> **401 skills + 30 comandos slash prontos para produção**
> Contexto 100% brasileiro · Multi-plataforma · Claude Code, Cursor, Codex, Windsurf, OpenClaw

> 📊 **Veja a apresentação visual completa:** abra [`SKILLS-portavel.html`](SKILLS-portavel.html) no navegador.

---

## O que são Skills?

Skills são arquivos de instrução que transformam qualquer AI coding assistant em especialistas sob demanda. Em vez de escrever longos prompts toda vez, você carrega uma skill e o AI assume imediatamente o papel de um especialista — com frameworks, ferramentas e contexto já configurados.

```
Sem skill:  "Me ajude com marketing..."        → resposta genérica
Com skill:  /read conteudo-copy/copy-de-anuncio/SKILL.md
            "Preciso de uma campanha no Meta Ads com orçamento de R$5k"
            → análise de segmentação, estrutura de campanha, copy de anúncio, ROAS esperado
```

---

## Instalação Rápida (1 comando)

```bash
curl -fsSL https://raw.githubusercontent.com/ricardonevesbraga/flowgrammers-skills/main/install.sh | bash
```

Isso instala tudo automaticamente em `~/.claude/skills/` e `~/.claude/commands/`.

### Ou clone e instale

```bash
git clone https://github.com/ricardonevesbraga/flowgrammers-skills.git
cd flowgrammers-skills
./install.sh
```

> ⭐ **Gostou?** Deixe uma estrela no GitHub — ajuda o projeto a crescer.

---

## Como Usar

### Claude Code
```
/read [dominio]/[sub-skill]/SKILL.md
```

### Cursor
Cole o conteúdo do SKILL.md desejado no `.cursorrules` ou em `.cursor/rules/[nome].md`.

### Codex / GitHub Copilot
Inclua o conteúdo do SKILL.md no `AGENTS.md` do projeto ou passe como contexto de sistema.

### Windsurf
Adicione nas instruções globais em **Windsurf Settings > AI Rules**.

### OpenClaw
Carregue via `/skill` ou inclua no contexto do sistema.

### Claude.ai (interface web)

Não é necessário instalar nada — basta copiar e colar o conteúdo da skill desejada.

**Opção 1 — Em um projeto Claude.ai:**
1. Acesse [claude.ai/projects](https://claude.ai/projects) e abra ou crie um projeto
2. Clique em **Project Instructions** (ícone de lápis)
3. Cole o conteúdo do  desejado nas instruções do projeto
4. Todas as conversas dentro do projeto já terão a skill ativa

**Opção 2 — Em qualquer conversa:**
1. Abra uma nova conversa em [claude.ai](https://claude.ai)
2. Cole o conteúdo do  no início da conversa como contexto de sistema
3. Continue a conversa normalmente — a skill estará ativa para toda a sessão

**Dica:** Skills menores (< 2.000 tokens) funcionam melhor em conversas únicas. Para skills com múltiplos arquivos de referência, use sempre um projeto.

### Exemplos rápidos

```
/read conteudo-copy/gerador-de-headlines/SKILL.md
Preciso de 10 headlines para landing page de curso de vendas B2B.

/read financeiro-compliance/conformidade-lgpd/SKILL.md
Temos 50k usuários e enviamos emails de marketing. Como me adequar à LGPD?

/read prd-generator/SKILL.md
[cole seu product brief aqui]

/read codigo-automacao/engenheiro-de-prompts/SKILL.md
Preciso otimizar meus prompts para o Claude Code rodar tasks complexas.
```

---

## Mapa Completo de Skills

### Novos Domínios (v2.2.0)

#### Conteúdo & Copy (`conteudo-copy/`) — 10 skills

Headlines, hooks, copy de anúncio, posts, emails e artigos.

| Skill | Pasta | O que faz |
|-------|-------|-----------|
| Gerador de Headlines | `gerador-de-headlines/` | Headlines com AIDA, PAS, 4U, Curiosity Gap |
| Criador de Hooks | `criador-de-hooks/` | Hooks para posts, vídeos, threads e stories |
| Copy de Anúncio | `copy-de-anuncio/` | Copy para Meta Ads, Google Ads, LinkedIn BR |
| Escritor de Emails | `escritor-de-emails/` | Sequências de email, newsletters, cold email |
| Escritor de Artigos | `escritor-de-artigos/` | Blog, SEO, white papers e long-form |
| Posts Sociais | `posts-sociais/` | Instagram, LinkedIn, Twitter/X, TikTok |
| Copy de Vendas | `copy-de-vendas/` | Páginas de vendas, VSL, copy de produto |
| Reaproveitamento de Conteúdo | `reaproveitamento-de-conteudo/` | Video → post → email → thread |
| Storytelling | `storytelling/` | Narrativa de marca e storytelling corporativo |
| Descrição de Produto | `descricao-de-produto/` | Descrições para e-commerce e marketplace BR |

```
/read conteudo-copy/gerador-de-headlines/SKILL.md
Preciso de 10 headlines para uma landing page de software de gestão para PMEs.
```

---

#### Marketing, Vendas & Publicidade (`marketing-vendas/`) — 10 skills

Funis, propostas, objeções, ads e brand voice.

| Skill | Pasta | O que faz |
|-------|-------|-----------|
| Funil de Vendas | `funil-vendas/` | Mapeamento e otimização TOFU/MOFU/BOFU |
| Proposta Comercial | `proposta-comercial/` | Propostas profissionais com precificação BR |
| Objeções de Vendas | `objecoes-vendas/` | Roteiros para tratar objeções comuns |
| Voz da Marca | `voz-da-marca/` | Definição e manual de tom de voz |
| Deck de Pitch | `deck-de-pitch/` | Apresentações de vendas e pitch para investidores |
| Follow-up | `follow-up/` | Sequências por e-mail, WhatsApp e telefone |
| Script de Vendas | `script-vendas/` | Scripts para cold call, discovery e fechamento |
| Estudo de Caso | `estudo-de-caso/` | Cases de sucesso, depoimentos e provas sociais |
| Estratégia Promocional | `estrategia-promocional/` | Promoções sazonais (Black Friday, etc.) |
| Análise Competitiva | `analise-competitiva/` | Posicionamento e análise de concorrentes BR |

---

#### Financeiro, Jurídico & Compliance (`financeiro-compliance/`) — 10 skills

Fluxo de caixa, contratos, LGPD, impostos e riscos.

| Skill | Pasta | O que faz |
|-------|-------|-----------|
| Fluxo de Caixa | `fluxo-caixa/` | Modelagem, projeções e gestão de capital de giro |
| DRE e Balanço | `dre-balanco/` | DRE, balanço patrimonial no padrão BR |
| Impostos BR | `impostos-br/` | Simples Nacional, Lucro Presumido, Real, MEI |
| Conformidade LGPD | `conformidade-lgpd/` | LGPD: DPIA, políticas de privacidade, DPA |
| Contratos BR | `contratos-br/` | Contratos conforme CC, CDC e CLT |
| Gestão de Riscos | `gestao-riscos/` | Matriz de riscos e planos de mitigação |
| Cobrança | `cobranca/` | Scripts e estratégias de cobrança (respeito ao CDC) |
| KPIs Financeiros | `kpis-financeiros/` | Dashboards: LTV, CAC, MRR, ARR, payback em R$ |
| Due Diligence | `due-diligence/` | Checklist para M&A, investimento e parcerias |
| Open Finance / PIX | `open-finance-pix/` | PIX, Open Finance, recorrência, split de pagamentos |

---

#### Operações, RH & Gestão (`operacoes-rh/`) — 10 skills

SOPs, vagas, OKRs, onboarding e automação.

| Skill | Pasta | O que faz |
|-------|-------|-----------|
| Criador de SOP | `criador-de-sop/` | SOPs com fluxogramas e responsabilidades |
| Descrição de Vagas | `descricao-de-vagas/` | JDs, perfis e critérios de seleção |
| Onboarding | `onboarding/` | Planos de onboarding para CLT/PJ e clientes |
| Gestão de OKRs | `gestao-de-okrs/` | Definição, cascateamento e acompanhamento |
| Avaliação de Desempenho | `avaliacao-desempenho/` | 360°, PDI, calibração e promoções |
| Políticas de RH | `politicas-rh/` | Código de conduta, handbook do colaborador |
| Automação de Processos | `automacao-processos/` | Identificação e automação com Make/Zapier/n8n |
| Facilitador de Reuniões | `facilitador-de-reunioes/` | Agenda, facilitação e ata de reuniões produtivas |
| Cultura da Empresa | `cultura-empresa/` | Valores, rituais e desenvolvimento de cultura |
| CLT / PJ / MEI | `clt-pj-mei/` | Regimes de contratação e compliance trabalhista BR |

---

#### Produto, E-commerce & SaaS (`produto-ecommerce/`) — 10 skills

Lançamentos, PLG, churn, e-commerce e vendas.

| Skill | Pasta | O que faz |
|-------|-------|-----------|
| Lançamento de Produto | `lancamento-produto/` | Playbook pré/lançamento/pós-lançamento |
| Estratégia PLG | `estrategia-plg/` | Product-Led Growth: trial, freemium, expansão |
| Análise de Churn | `analise-de-churn/` | Diagnóstico, cohort e estratégias de retenção |
| Operações E-commerce | `operacoes-ecommerce/` | Catálogo, frete, checkout, devoluções BR |
| Precificação SaaS | `precificacao-saas/` | Tiers, annual vs monthly, teste de preço em R$ |
| Roadmap de Produto | `roadmap-de-produto/` | RICE, ICE, Now/Next/Later |
| Upsell e Cross-sell | `upsell-e-crosssell/` | Estratégias de expansão de receita |
| Estratégia Marketplace | `estrategia-marketplace/` | Mercado Livre, Amazon, Shopee, Magalu BR |
| Abandono de Carrinho | `abandono-de-carrinho/` | Recuperação: email, WhatsApp e retargeting |
| Analítica de Produto | `analitica-de-produto/` | DAU, MAU, NPS, retention, feature adoption |

---

#### Código, Dev & Automação (`codigo-automacao/`) — 10 skills

Debug, APIs, Docker, testes, banco de dados e auth.

| Skill | Pasta | O que faz |
|-------|-------|-----------|
| Especialista em Debug | `especialista-em-debug/` | Diagnóstico sistemático: logs, stack traces |
| Construtor de API | `construtor-de-api/` | APIs REST e GraphQL com documentação |
| Docker Compose | `docker-compose/` | Containerização para dev e produção |
| Automação de Testes | `automacao-de-testes/` | Unitários, integração, E2E com Playwright |
| Banco de Dados Ops | `banco-de-dados-ops/` | Queries, migrations, indexação, modelagem |
| Implementação de Auth | `implementacao-de-auth/` | JWT, OAuth 2.0, Supabase Auth, Firebase |
| No-Code Automação | `no-code-automacao/` | Make, Zapier, n8n, ActivePieces |
| Integrador de Webhooks | `integrador-de-webhooks/` | Webhooks, eventos e filas de mensagens |
| Especialista Claude Code | `especialista-claude-code/` | Claude Code avançado: skills, subagentes, worktrees |
| Engenheiro de Prompts | `engenheiro-de-prompts/` | Prompt engineering para máxima produtividade |

---

#### Carreira, Educação & Marca Pessoal (`carreira-educacao/`) — 10 skills

LinkedIn, cursos, mentoria, palestras e freelancing.

| Skill | Pasta | O que faz |
|-------|-------|-----------|
| Perfil LinkedIn | `perfil-linkedin/` | Otimização para recrutadores e clientes BR |
| Currículo e CV | `curriculo-e-cv/` | Currículo no padrão ATS e visual para BR |
| Criador de Portfólio | `criador-de-portfolio/` | Portfólio profissional com cases e showcase |
| Criador de Cursos | `criador-de-cursos/` | Módulos, aulas e materiais para EaD |
| Preparação de Palestra | `palestra-preparacao/` | Palestras técnicas e apresentações em eventos |
| Estrutura Freelancer | `estrutura-freelancer/` | Negócio freelancer: MEI, PJ, precificação BR |
| Framework de Mentoria | `framework-de-mentoria/` | Programas de mentoria e planos de desenvolvimento |
| Busca de Emprego | `busca-de-emprego/` | Estratégia e preparação para entrevistas técnicas |
| Marca Pessoal | `marca-pessoal/` | Autoridade e posicionamento digital |
| Negociação Salarial | `negociacao-salarial/` | Benchmarks de mercado BR, scripts de negociação |

---

#### Rotina, Tarefas & Organização (`rotina-organizacao/`) — 10 skills

GTD, time blocking, checklists, delegação e produtividade pessoal.

| Skill | Pasta | O que faz |
|-------|-------|-----------|
| Sistema GTD | `sistema-gtd/` | Getting Things Done adaptado ao Brasil |
| Bloqueio de Tempo | `bloqueio-de-tempo/` | Time blocking, deep work e temas do dia |
| Criador de Checklists | `criador-de-checklists/` | Checklists, SOPs pessoais e rotinas |
| Delegação | `delegacao/` | Delegação eficaz para líderes e donos de negócio |
| Revisão Semanal | `revisao-semanal/` | Revisão semanal: capturas, projetos e ações |
| Prioridades | `prioridades/` | Eisenhower, RICE pessoal, princípio 80/20 |
| Caixa de Entrada Zero | `caixa-de-entrada-zero/` | Gestão de email e notificações |
| Hábitos | `habitos/` | Atomic habits, habit stacking, tracking |
| Foco e Trabalho Profundo | `foco-e-trabalho-profundo/` | Pomodoro, deep work, eliminação de distrações |
| Equilíbrio Vida | `equilibrio-vida/` | Work-life balance, prevenção de burnout |

---

#### Design & Branding (`design-branding/`) — 10 skills

Propostas visuais, decks, identidade, materiais de vendas e assets B2B.

| Skill | Pasta | O que faz |
|-------|-------|-----------|
| Identidade Visual | `identidade-visual/` | Identidade visual e brand guidelines |
| Design de Pitch | `design-de-pitch/` | Pitch decks e apresentações executivas |
| Materiais de Vendas | `materiais-vendas/` | One-pager, proposta visual, folder B2B |
| Assets Redes Sociais | `assets-redes-sociais/` | Templates: feed, stories, banners |
| Feedback de Design | `feedback-de-design/` | Feedback em projetos de UI/UX |
| Briefing de Logo | `briefing-de-logo/` | Briefing de logo para designers e agências |
| Manual de Marca | `manual-de-marca/` | Brandbook: aplicações, tipografia, cores |
| Produção no Figma | `producao-no-figma/` | Organização e produção em Figma |
| Apresentação Slides | `apresentacao-slides/` | Slides executivos: estrutura e narrativa |
| Briefing de Vídeo | `briefing-de-video/` | Briefing para vídeos institucionais e de produto |

---

#### Jurídico & Advocacia (`juridico-advocacia/`) — 10 skills

Petições, contratos, captação de clientes, precificação e rotina do advogado solo.

| Skill | Pasta | O que faz |
|-------|-------|-----------|
| Petição Inicial | `peticao-inicial/` | Petições iniciais, contestações e recursos |
| Contrato de Serviços | `contrato-servicos/` | Contratos conforme CC/CDC BR |
| Captação de Clientes | `captacao-clientes/` | Captação respeitando o Código de Ética OAB |
| Honorários | `honorarios/` | Tabela de honorários e precificação jurídica |
| LGPD Jurídico | `lgpd-juridico/` | Adequação LGPD: contratos, políticas, DPA |
| Trabalhista | `trabalhista/` | CLT, reforma, TST, dissídio e acordos |
| Empresarial | `empresarial/` | Constituição de empresa, alterações societárias |
| Consumidor | `consumidor/` | CDC, Procon, Reclame Aqui, mediação |
| Rotina do Escritório | `rotina-escritorio/` | SOP para advocacia solo e boutique |
| Marketing Jurídico | `marketing-juridico/` | Marketing permitido: LinkedIn, Instagram, WhatsApp |

---

#### Direção Criativa (`direcao-criativa/`) — 10 skills

Ideação criativa, direção de arte, conceito de campanha e storytelling visual.

| Skill | Pasta | O que faz |
|-------|-------|-----------|
| Conceito Criativo | `conceito-criativo/` | Big idea e conceito central de campanha |
| Direção de Arte | `direcao-arte/` | Briefing e referências para produção visual |
| Naming | `naming/` | Naming de produtos, marcas e campanhas |
| Tagline | `tagline/` | Taglines, slogans e brand promises |
| Campanha 360° | `campanha-360/` | Campanha integrada multi-canal |
| Narrativa Visual | `narrativa-visual/` | Storytelling visual para marcas |
| Moodboard | `moodboard/` | Moodboards e referências para produções |
| Roteiro de Vídeo | `roteiro-video/` | Roteiros para vídeos publicitários |
| Ideação | `ideacao/` | Brainstorming e sessões de ideação criativa |
| Ativação de Marca | `ativacao-de-marca/` | Ativações de marca, experiências e eventos |

---

#### Liderança & Equipes (`lideranca-equipes/`) — 10 skills

SOPs, OKRs, feedback, onboarding, delegação e gestão de times pequenos.

| Skill | Pasta | O que faz |
|-------|-------|-----------|
| Feedback Estruturado | `feedback-estruturado/` | Feedback 1:1 com SBI e feedforward |
| Reunião Individual | `reuniao-individual/` | Preparação e condução de 1:1s eficazes |
| Gestão de Conflitos | `gestao-conflitos/` | Resolução de conflitos e mediação |
| Cultura Psicológica | `cultura-psicologica/` | Segurança psicológica e inclusão |
| Reconhecimento | `reconhecimento/` | Programas de reconhecimento e engajamento |
| Desenvolvimento de Time | `desenvolvimento-time/` | PDIs, trilhas de carreira e promoções |
| Remoto e Híbrido | `remoto-hibrido/` | Gestão de times remotos e híbridos |
| Reunião Eficaz | `reuniao-eficaz/` | Facilitação de reuniões produtivas |
| Líder Técnico | `lider-tecnico/` | Transição de especialista para líder |
| Time Pequeno | `time-pequeno/` | Gestão de 2-15 pessoas em startups e PMEs BR |

---

#### SEO, Analítica & Dados (`seo-analitica/`) — 10 skills

SEO, analytics, métricas, relatórios de dados e inteligência de negócio.

| Skill | Pasta | O que faz |
|-------|-------|-----------|
| SEO Técnico | `seo-tecnico/` | Auditoria: Core Web Vitals, indexação, schema |
| Pesquisa de Palavras-chave | `pesquisa-de-palavras-chave/` | Keyword research para busca BR |
| Google Analytics | `google-analytics/` | GA4 com eventos customizados |
| Google Search Console | `google-search-console/` | GSC para diagnóstico e oportunidades |
| Relatório de Dados | `relatorio-dados/` | Relatórios e dashboards executivos |
| BI e Indicadores | `bi-indicadores/` | KPIs de negócio para PMEs: fórmulas e benchmarks |
| Rastreamento UTM | `rastreamento-utm/` | UTMs, rastreamento de campanhas e atribuição |
| Análise de Coortes | `analise-de-coortes/` | Cohort analysis, retenção e LTV |
| Testes A/B | `testes-ab/` | Planejamento e análise estatística de A/B |
| Dados e LGPD | `dados-lgpd/` | Coleta de dados em conformidade com LGPD |

---

### Skills de Produto

#### PRD Generator (`prd-generator/`)

Transforma um Product Brief em PRD completo com 9 seções, diagramas Mermaid e SQL PostgreSQL executável.

```
/read prd-generator/SKILL.md
[cole seu product brief aqui]
```

#### SDD Generator (`sdd-generator/`)

Decompõe um PRD em specs executáveis para subagentes paralelos no Claude Code.

```
/read sdd-generator/SKILL.md
[cole seu PRD aqui]
```

---

### PM Flow Skills (`pm-flow-skills/`) — 27 slash commands de Product Management

Kit completo de PM cobrindo todo o ciclo de produto: da ideia vaga ao produto escalado. Baseado nos frameworks de Teresa Torres (OST), Ash Maurya (Lean Canvas), Sean Ellis (PMF), Rob Fitzpatrick (Mom Test), Marty Cagan (Dual-Track) e Lenny Rachitsky (OKRs + Growth).

#### Jornada 0→1: Da ideia ao Product-Market Fit

```
Fase 1: Problem Discovery → /persona  /discovery  /customer-journey
Fase 2: Problem Validation → /lean-canvas  /competitive-analysis  /hypothesis
Fase 3: Solution Discovery → /opportunity-tree  /experiment-design  /hypothesis
Fase 4: Solution Validation → /ab-test-analysis  /measure-pmf
Fase 5: MVP Spec & Build → /prd  /user-stories  /pre-mortem
Fase 6: Launch & Traction → /launch-checklist  /gtm  /north-star
Fase 7: Product-Market Fit → /measure-pmf  /interview-synthesis  /stakeholder-update
```

#### Jornada 1→100: Do PMF ao scale

```
Fase 8: Growth Engine → /north-star  /okr  /experiment-design  /ab-test-analysis
Fase 9: Scaling & Expansion → /pricing  /ideal-customer-profile  /battlecard  /roadmap
Fase 10: Optimization & Moat → /strategy  /competitive-analysis  /okr  /stakeholder-update
Fase 11: Maturity & Reinvention → /strategy  /discovery  /lean-canvas  /prioritize
```

#### 27 commands por domínio

| Domínio | Commands | Quando usar |
|---------|---------|-------------|
| **Discovery** (7) | `/persona` `/discovery` `/interview-synthesis` `/competitive-analysis` `/opportunity-tree` `/hypothesis` `/customer-journey` | Entender o problema e o mercado |
| **Delivery** (3) | `/prd` `/user-stories` `/acceptance-criteria` | Especificar a solução |
| **Strategy** (7) | `/prioritize` `/strategy` `/roadmap` `/okr` `/lean-canvas` `/pricing` `/north-star` | Priorizar, planejar e alinhar |
| **Validation** (3) | `/experiment-design` `/measure-pmf` `/ab-test-analysis` | Testar e medir |
| **Execution** (2) | `/pre-mortem` `/launch-checklist` | Preparar e proteger o lançamento |
| **GTM** (5) | `/release-notes` `/stakeholder-update` `/gtm` `/battlecard` `/ideal-customer-profile` | Comunicar e ir ao mercado |

#### Workflows prontos (combos de skills)

| Workflow | Skills |
|----------|--------|
| Customer Discovery | `/persona` → `/discovery` → `/interview-synthesis` → `/opportunity-tree` |
| Feature Kickoff | `/hypothesis` → `/prd` → `/user-stories` → `/acceptance-criteria` |
| Product Strategy | `/competitive-analysis` → `/strategy` → `/okr` → `/roadmap` → `/stakeholder-update` |
| Validate & Launch | `/experiment-design` → `/pre-mortem` → `/launch-checklist` → `/gtm` |
| Pricing & GTM | `/pricing` → `/ideal-customer-profile` → `/battlecard` → `/gtm` |
| Growth Sprint | `/north-star` → `/experiment-design` → `/ab-test-analysis` → `/okr` |
| Board Update | `/measure-pmf` → `/stakeholder-update` → `/roadmap` |

Veja tutoriais completos em `pm-flow-skills/tutorial/` e templates preenchíveis em `pm-flow-skills/templates/`.

---

### Domínios Originais

#### C-Level Advisory (`c-level-advisor/`) — 37 skills

| Skill | O que faz |
|-------|-----------|
| `ceo-advisor` | Estratégia, captação, board, cultura organizacional |
| `cfo-advisor` | Modelagem financeira, runway, fundraising |
| `cto-advisor` | Arquitetura técnica, build vs buy, roadmap de eng. |
| `cmo-advisor` | Estratégia de marketing, GTM, posicionamento |
| `coo-advisor` | Operações, OKRs, eficiência organizacional |
| `cpo-advisor` | Estratégia de produto, roadmap, métricas |
| `cro-advisor` | Revenue, pipeline, quota, sales ops |
| `chro-advisor` | RH, cultura, retenção, CLT/PJ |
| `ciso-advisor` | Segurança, LGPD, ISO 27001, gestão de risco |
| `cdo-advisor` | Chief Data Officer — dados, governança, LGPD |
| `caio-advisor` | Chief AI Officer — estratégia de IA, responsible AI |
| `clo-advisor` | Chief Legal Officer — jurídico BR, M&A, LGPD |
| `chief-of-staff` | Roteador automático para o C-suite correto |
| E mais 24... | |

#### Engineering (`engineering/`) — 60 skills · Engineering Team (`engineering-team/`) — 54 skills

RAG, MCP Server Builder, CI/CD, Observabilidade, Playwright, TDD, AWS/GCP/Azure, Mobile iOS/Android, SRE.

#### Marketing (`marketing-skill/`) — 45 skills

SEO, AI SEO, CRO, Email Marketing, Paid Ads, Growth, Content Strategy.

#### Product Team (`product-team/`) — 18 skills · Business Growth (`business-growth/`) — 7 skills

PM toolkit, Growth PM, UX, UI Design System, CS Manager, RevOps.

#### Finance (`finance/`) — 6 skills · RA/QM Team (`ra-qm-team/`) — 14 skills

Controller BR, FP&A, SaaS Metrics · ISO 13485, LGPD, ANVISA/FDA, ISO 27001, SOC2.

---

## Comandos Slash Disponíveis

**54 comandos no total** — 30 originais Flowgrammers + 24 novos PM Flow Skills.

### PM Flow Skills (27 comandos de Product Management)

| Comando | O que faz |
|---------|-----------|
| `/discovery` | Ciclo de descoberta: framing → hipóteses → plano de experimentos |
| `/persona` | Personas com JTBD, behaviors, pain points e citações reais |
| `/opportunity-tree` | Opportunity Solution Tree de Teresa Torres |
| `/hypothesis` | Hipóteses testáveis com kill criteria e métricas |
| `/customer-journey` | Jornada do cliente em 7 estágios com emoções e pain points |
| `/interview-synthesis` | Síntese de entrevistas em padrões, JTBD e recomendações |
| `/competitive-analysis` | Mapa competitivo com gaps de diferenciação |
| `/prd` | PRD completo em 8 seções com exemplos detalhados |
| `/user-stories` | User stories INVEST com critérios de aceite |
| `/acceptance-criteria` | Given/When/Then para happy path + edge cases |
| `/prioritize` | RICE scoring com trade-offs e recomendação |
| `/strategy` | Strategy canvas com 9 seções |
| `/roadmap` | Roadmap trimestral com fases e dependências |
| `/okr` | OKRs cascateados (empresa → time) com 9 princípios Lenny |
| `/lean-canvas` | Lean Canvas de Ash Maurya (9 blocos) |
| `/pricing` | 7 modelos de pricing + willingness-to-pay |
| `/north-star` | North Star Metric + 3-5 input metrics |
| `/experiment-design` | Design de pretotypes e A/B tests (XYZ hypothesis) |
| `/measure-pmf` | Product-Market Fit (Sean Ellis 40% + retenção) |
| `/ab-test-analysis` | Análise estatística de resultados de A/B test |
| `/pre-mortem` | Risk analysis (Tigers / Paper Tigers / Elephants) |
| `/launch-checklist` | Checklist cross-functional para lançamento |
| `/release-notes` | Release notes orientadas a benefício |
| `/stakeholder-update` | Status executivo: situação → análise → recomendação |
| `/gtm` | Go-to-market completo com canais, mensagens e métricas |
| `/battlecard` | Battlecard competitiva para vendas |
| `/ideal-customer-profile` | ICP detalhado com demographics, behaviors e JTBD |

### Comandos Originais Flowgrammers

| Comando | O que faz |
|---------|-----------|
| `/prd` | PRD via Flowgrammers generator (9 seções + Mermaid + SQL) |
| `/tdd` | Workflow de Test-Driven Development |
| `/sprint-plan` | Planejamento de sprint com estimativas |
| `/saas-health` | Dashboard de métricas SaaS (ARR, MRR, Churn) |
| `/tech-debt` | Inventário e priorização de dívida técnica |
| `/retro` | Facilitação de retrospectiva ágil |
| `/code-to-prd` | Gera PRD a partir de código existente |
| `/financial-health` | Análise de saúde financeira |
| `/rice` | Priorização RICE de features |
| `/a11y-audit` | Auditoria de acessibilidade WCAG 2.2 |
| `/security-review` | Review de segurança de código |
| `/changelog` | Geração de changelog conventional commits |
| E mais... | `/sprint-health` `/karpathy-check` `/focused-fix` `/pipeline` `/project-health` `/user-story` `/google-workspace` `/plugin-audit` `/deep-research` `wiki-*` |

---

## Contexto Brasileiro

| Contexto | Skills Relevantes |
|----------|------------------|
| **LGPD** | `financeiro-compliance/conformidade-lgpd`, `juridico-advocacia/lgpd-juridico`, `seo-analitica/dados-lgpd` |
| **PIX / Open Finance** | `financeiro-compliance/open-finance-pix` |
| **WhatsApp Business** | `marketing-vendas/follow-up`, `marketing-vendas/script-vendas` |
| **NF-e / SPED** | `financeiro-compliance/impostos-br`, `financeiro-compliance/dre-balanco` |
| **CLT / PJ / MEI** | `operacoes-rh/clt-pj-mei`, `carreira-educacao/estrutura-freelancer` |
| **ANVISA** | `ra-qm-team/fda-consultant-specialist` |
| **Meta Ads BR** | `conteudo-copy/copy-de-anuncio`, `marketing-vendas/funil-vendas` |
| **Métricas em R$** | `financeiro-compliance/kpis-financeiros`, `produto-ecommerce/precificacao-saas` |
| **OAB** | `juridico-advocacia/` (domínio completo) |
| **CONAR** | `direcao-criativa/campanha-360` |

---

## Instalação Manual

```bash
# Clonar e instalar
git clone https://github.com/ricardonevesbraga/flowgrammers-skills.git
cd flowgrammers-skills
chmod +x install.sh
./install.sh
```

Ou passo a passo:
```bash
mkdir -p ~/.claude/skills
cp -r . ~/.claude/skills/flowgrammers-skills/
mkdir -p ~/.claude/commands
cp -r commands/* ~/.claude/commands/
```

---

## Requisitos

- **Claude Code / Cursor / Windsurf / Codex / OpenClaw** — instale via script ou manualmente
- **Claude.ai** — nenhum requisito, basta copiar e colar (veja seção *Como Usar* acima)
- macOS, Linux ou Windows (WSL2) para instalação local
- Sem outras dependências

---

## Sobre

Skills da comunidade Flowgrammers para o mercado brasileiro.

- Site: [flowgrammers.com.br](https://flowgrammers.com.br)
- Versão: 2.2.0 ([changelog](CHANGELOG.md))
- Licença: [MIT](LICENSE)
- Repositório: [github.com/ricardonevesbraga/flowgrammers-skills](https://github.com/ricardonevesbraga/flowgrammers-skills)

### Créditos

| Contribuição | Autor |
|---|---|
| Flowgrammers Skills (401 skills, domínios, install) | [@ricardonevesbraga](https://github.com/ricardonevesbraga) |
| PM Flow Skills (27 slash commands de PM) | [@lucasgaravelli](https://github.com/lucasgaravelli) |

## Contribuindo

Quer sugerir uma skill nova, corrigir algo, ou adicionar um perfil? Veja [CONTRIBUTING.md](CONTRIBUTING.md).

## Apoie o projeto

- ⭐ Dê uma estrela no GitHub
- 🔁 Compartilhe com outros devs brasileiros
- 💬 Abra uma issue com feedback ou sugestão
- 🤝 Contribua com uma skill nova via PR
