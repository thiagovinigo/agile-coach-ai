# Changelog

Todas as mudanças notáveis deste projeto estão documentadas aqui.

O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/)
e o versionamento [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [2.2.1] — 2026-05-29

### Adicionado — Skill de Cibersegurança

- `seguranca-mvs` — CISO Virtual Sênior com análise 360° de Segurança Mínima Viável (MVS)
  - 10 domínios técnicos: Conformidade/LGPD, Dados, IAM, Hardening, AppSec, SecOps, Pentest, IR, DevSecOps, Cloud Security
  - `references/lgpd.md` — artigos LGPD, prazos ANPD (Resolução 15/2024), bases legais
  - `references/dominios.md` — detalhamento técnico completo dos 10 domínios
  - `references/playbooks-ir.md` — playbooks de IR para Ransomware, Data Breach, DDoS, Credencial Comprometida, Insider Threat, Supply Chain Attack
  - Metodologia MVS com roadmap em 3 ondas (0–30d / 30–90d / 90–180d) e KPIs mensuráveis

---

## [2.2.0] — 2026-05-28

### Adicionado — 13 novos domínios com 130 sub-skills

**Conteúdo & Copy (`conteudo-copy/`) — 10 sub-skills**
- `gerador-de-headlines`, `criador-de-hooks`, `copy-de-anuncio`, `escritor-de-emails`
- `escritor-de-artigos`, `posts-sociais`, `copy-de-vendas`, `reaproveitamento-de-conteudo`
- `storytelling`, `descricao-de-produto`

**Marketing, Vendas & Publicidade (`marketing-vendas/`) — 10 sub-skills**
- `funil-vendas`, `proposta-comercial`, `objecoes-vendas`, `voz-da-marca`, `deck-de-pitch`
- `follow-up`, `script-vendas`, `estudo-de-caso`, `estrategia-promocional`, `analise-competitiva`

**Financeiro, Jurídico & Compliance (`financeiro-compliance/`) — 10 sub-skills**
- `fluxo-caixa`, `dre-balanco`, `impostos-br`, `conformidade-lgpd`, `contratos-br`
- `gestao-riscos`, `cobranca`, `kpis-financeiros`, `due-diligence`, `open-finance-pix`

**Operações, RH & Gestão (`operacoes-rh/`) — 10 sub-skills**
- `criador-de-sop`, `descricao-de-vagas`, `onboarding`, `gestao-de-okrs`, `avaliacao-desempenho`
- `politicas-rh`, `automacao-processos`, `facilitador-de-reunioes`, `cultura-empresa`, `clt-pj-mei`

**Produto, E-commerce & SaaS (`produto-ecommerce/`) — 10 sub-skills**
- `lancamento-produto`, `estrategia-plg`, `analise-de-churn`, `operacoes-ecommerce`
- `precificacao-saas`, `roadmap-de-produto`, `upsell-e-crosssell`, `estrategia-marketplace`
- `abandono-de-carrinho`, `analitica-de-produto`

**Código, Dev & Automação (`codigo-automacao/`) — 10 sub-skills**
- `especialista-em-debug`, `construtor-de-api`, `docker-compose`, `automacao-de-testes`
- `banco-de-dados-ops`, `implementacao-de-auth`, `no-code-automacao`, `integrador-de-webhooks`
- `especialista-claude-code`, `engenheiro-de-prompts`

**Carreira, Educação & Marca Pessoal (`carreira-educacao/`) — 10 sub-skills**
- `perfil-linkedin`, `curriculo-e-cv`, `criador-de-portfolio`, `criador-de-cursos`
- `palestra-preparacao`, `estrutura-freelancer`, `framework-de-mentoria`, `busca-de-emprego`
- `marca-pessoal`, `negociacao-salarial`

**Rotina, Tarefas & Organização (`rotina-organizacao/`) — 10 sub-skills**
- `sistema-gtd`, `bloqueio-de-tempo`, `criador-de-checklists`, `delegacao`, `revisao-semanal`
- `prioridades`, `caixa-de-entrada-zero`, `habitos`, `foco-e-trabalho-profundo`, `equilibrio-vida`

**Design & Branding (`design-branding/`) — 10 sub-skills**
- `identidade-visual`, `design-de-pitch`, `materiais-vendas`, `assets-redes-sociais`
- `feedback-de-design`, `briefing-de-logo`, `manual-de-marca`, `producao-no-figma`
- `apresentacao-slides`, `briefing-de-video`

**Jurídico & Advocacia (`juridico-advocacia/`) — 10 sub-skills**
- `peticao-inicial`, `contrato-servicos`, `captacao-clientes`, `honorarios`, `lgpd-juridico`
- `trabalhista`, `empresarial`, `consumidor`, `rotina-escritorio`, `marketing-juridico`

**Direção Criativa (`direcao-criativa/`) — 10 sub-skills**
- `conceito-criativo`, `direcao-arte`, `naming`, `tagline`, `campanha-360`
- `narrativa-visual`, `moodboard`, `roteiro-video`, `ideacao`, `ativacao-de-marca`

**Liderança & Equipes (`lideranca-equipes/`) — 10 sub-skills**
- `feedback-estruturado`, `reuniao-individual`, `gestao-conflitos`, `cultura-psicologica`
- `reconhecimento`, `desenvolvimento-time`, `remoto-hibrido`, `reuniao-eficaz`
- `lider-tecnico`, `time-pequeno`

**SEO, Analítica & Dados (`seo-analitica/`) — 10 sub-skills**
- `seo-tecnico`, `pesquisa-de-palavras-chave`, `google-analytics`, `google-search-console`
- `relatorio-dados`, `bi-indicadores`, `rastreamento-utm`, `analise-de-coortes`
- `testes-ab`, `dados-lgpd`

### Adicionado — Skills de Desenvolvimento de Produto
- `prd-generator` — Gerador de PRD completo a partir de Product Brief (9 seções + Mermaid + SQL)
- `sdd-generator` — Gerador de SDD / specs executáveis para subagentes paralelos

### Alterado
- Suporte multi-plataforma adicionado a todos os novos domínios: Claude Code, Cursor, Codex, Windsurf, OpenClaw
- Seção "Configuração de Harness" em cada domínio com trechos prontos de CLAUDE.md, .cursorrules e AGENTS.md
- Todas as pastas de sub-skills renomeadas para português do Brasil
- Atribuições de autor removidas dos arquivos de skill

---

## [2.1.0] — 2026-04-23

### Adicionado — 12 novas skills cobrindo gaps estratégicos

**C-Level Advisor (+3)**
- `cdo-advisor` — Chief Data Officer (dados, governança, LGPD, monetização)
- `caio-advisor` — Chief AI Officer (estratégia de IA, responsible AI, ROI)
- `clo-advisor` — Chief Legal Officer / General Counsel (jurídico BR, M&A, LGPD)

**Engineering Team (+3)**
- `senior-mobile-ios` — Swift 6, SwiftUI, Xcode Cloud, App Store
- `senior-mobile-android` — Kotlin, Jetpack Compose, Play Store, KMP
- `senior-sre` — SLO, error budget, postmortems, chaos engineering

**Business Growth (+2)**
- `account-manager` — Account Plan, QBR, renovação, upsell/cross-sell
- `partnerships-manager` — Canais, resellers, SIs, marketplaces, MDF

**Finance (+2)**
- `controller-contador` — Contabilidade BR (NF-e, SPED, ECD, regimes tributários)
- `fpa-analyst` — Budget, forecast, variance analysis, unit economics, 3-statements

**Product Team (+1)**
- `growth-product-manager` — NSM, AARRR, growth loops, PLG, experimentação

**Project Management (+1)**
- `program-manager` — Programa multi-projeto, RAID log, steering committee

### Adicionado — Documentação institucional
- `SKILLS-portavel.html` — apresentação HTML com 14 slides cobrindo todas as skills (estilo cyberpunk neon, portável, responsivo, print-friendly)
- `LICENSE` — arquivo MIT formal na raiz
- `CONTRIBUTING.md` — guia de contribuição

### Corrigido
- Auditoria confirmou 100% das 251 skills em português do Brasil
- Frontmatter YAML padronizado em 240/241 arquivos (1 intencional: fixture do skill-tester)

## [2.0.0] — 2026-03-05

### Adicionado
- Catálogo inicial com 241 skills em 9 domínios
- Comandos slash em `commands/` (29 comandos)
- `install.sh` automatizado para `~/.claude/skills/` e `~/.claude/commands/`
- `MASTERCLASS-portavel.html` institucional

---

**Legenda:**
- `Adicionado` — funcionalidades novas
- `Alterado` — mudanças em funcionalidades existentes
- `Depreciado` — funcionalidades que serão removidas
- `Removido` — funcionalidades removidas
- `Corrigido` — bug fixes
- `Segurança` — correções relacionadas a segurança
