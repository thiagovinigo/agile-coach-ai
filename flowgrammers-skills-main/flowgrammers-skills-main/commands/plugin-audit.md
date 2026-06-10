---
name: plugin-audit
description: |
  Pipeline de auditoria completo para skills, plugins, agentes e comandos. Valida estrutura,
  qualidade, segurança, conformidade com o marketplace, compatibilidade multiplataforma e integração
  com o ecossistema. Executa todas as ferramentas de validação integradas, invoca agentes de revisão
  de código adequados ao domínio e produz um relatório de aprovação/reprovação. Uso: /plugin-audit <caminho-da-skill>
---

# /plugin-audit

Pipeline de auditoria completo para qualquer skill, plugin, agente ou comando neste repositório. Executa 8 fases de validação, corrige automaticamente o que for possível e só para para entrada do usuário em decisões críticas (mudanças que quebram compatibilidade, novas dependências).

## Uso

```bash
/plugin-audit product-team/code-to-prd
/plugin-audit engineering/agenthub
/plugin-audit engineering-team/playwright-pro
```

## O que faz

Executa todas as 8 fases sequencialmente. Para em falhas críticas. Corrige automaticamente problemas não críticos. Reporta resultados ao final.

---

## Fase 1: Descoberta

Identifica o conteúdo da skill e a classifica.

1. Verifica se `{skill_path}` existe e contém `SKILL.md`
2. Lê o frontmatter do `SKILL.md` — extrai `name`, `description`, `Category`, `Tier`
3. Detecta o tipo de skill: scripts Python, docs de referência, assets, outputs esperados, agentes embutidos, sub-skills, plugin standalone, registros de comandos
4. Detecta domínio pelo caminho
5. Verifica comando associado em `commands/`

Exibe resumo da descoberta antes de prosseguir:
```
Auditando: code-to-prd
  Domínio: product-team
  Tipo: skill PADRÃO com plugin standalone
  Scripts: 2 | Referências: 2 | Assets: 1 | Outputs esperados: 3
  Comando: /code-to-prd (encontrado)
  Plugin: .claude-plugin/plugin.json (encontrado)
```

---

## Fase 2: Validação de Estrutura

Executa o validador de skill-tester:

```bash
python3 engineering/skill-tester/scripts/skill_validator.py {skill_path} --tier {tier} --json
```

**Regra de aprovação:** Pontuação ≥ 75 (BOM). Abaixo de 75 → tenta correções automáticas e re-executa. Se ainda abaixo de 75, reporta como FALHA.

---

## Fase 3: Pontuação de Qualidade

```bash
python3 engineering/skill-tester/scripts/quality_scorer.py {skill_path} --detailed --json
```

**Regra de aprovação:** Pontuação ≥ 60 (C). Abaixo de 60 → reporta itens do roadmap de melhoria como ações.

---

## Fase 4: Teste de Scripts

Se a skill tiver `scripts/` com arquivos `.py`:

```bash
python3 engineering/skill-tester/scripts/script_tester.py {skill_path} --json --verbose
```

**Regra de aprovação:** Todos os scripts devem PASSAR. Qualquer FALHA é um bloqueio.

---

## Fase 5: Auditoria de Segurança

```bash
python3 engineering/skill-security-auditor/scripts/skill_security_auditor.py {skill_path} --strict --json
```

**Regra de aprovação:** Zero achados CRÍTICOS. Zero achados ALTOS. **Não corrija automaticamente problemas de segurança** — reporte e deixe o usuário decidir.

---

## Fase 6: Conformidade com Marketplace e Plugin

Valida `plugin.json` (campos permitidos, versão, nome), `settings.json` (versão, referências de comandos) e entrada no `marketplace.json`.

**Correção automática:** Atualiza versões desatualizadas. Remove campos extras.

---

## Fase 7: Integração com Ecossistema

- Verifica se a skill aparece nos índices de plataforma (Codex, Gemini)
- Valida frontmatter dos arquivos de comando associados
- Verifica se agentes embutidos têm frontmatter válido
- Verifica dependências entre skills

---

## Fase 8: Revisão de Código Adequada ao Domínio

| Domínio | Agente | Foco da Revisão |
|---------|--------|-----------------|
| `engineering/` ou `engineering-team/` | cs-senior-engineer | Arquitetura, qualidade de código, integração CI/CD |
| `product-team/` | cs-product-manager | Qualidade do PRD, cobertura de user stories, alinhamento RICE |
| `marketing-skill/` | cs-content-creator | Qualidade do conteúdo, SEO, voz da marca |
| `ra-qm-team/` | cs-quality-regulatory | Checklist de conformidade, trilha de auditoria |
| `business-growth/` | cs-growth-strategist | Métricas de crescimento, impacto na receita |
| `finance/` | cs-financial-analyst | Precisão do modelo financeiro, definições de métricas |
| Outros | cs-senior-engineer | Revisão geral de código e arquitetura |

---

## Relatório Final

```
╔══════════════════════════════════════════════════════════════╗
║  RELATÓRIO DE AUDITORIA DE PLUGIN: {skill_name}             ║
╠══════════════════════════════════════════════════════════════╣
║  Fase 1 — Descoberta          ✅ {tipo}, {domínio}           ║
║  Fase 2 — Estrutura           ✅ {score}/100 ({nível})       ║
║  Fase 3 — Qualidade           ✅ {score}/100 ({nota})        ║
║  Fase 4 — Scripts             ✅ {n}/{n} PASSOU              ║
║  Fase 5 — Segurança           ✅ PASSOU (0 crítico, 0 alto)  ║
║  Fase 6 — Marketplace         ✅ plugin.json válido           ║
║  Fase 7 — Ecossistema         ✅ Codex + Gemini sincronizados ║
║  Fase 8 — Revisão de Código   ✅ revisão de {domínio} passou ║
║                                                              ║
║  VEREDICTO: ✅ APROVADO — Pronto para merge/publicação      ║
║                                                              ║
║  Correções automáticas: {n}                                  ║
║  Avisos: {n}                                                 ║
║  Itens de ação: {n}                                          ║
╚══════════════════════════════════════════════════════════════╝
```

### Lógica do Veredicto

| Condição | Veredicto |
|----------|-----------|
| Todas as fases aprovadas | **APROVADO** — Pronto para merge/publicação |
| Apenas avisos (sem bloqueios) | **APROVADO COM AVISOS** — Revise os avisos antes do merge |
| Qualquer fase com bloqueio | **REPROVADO** — Lista de bloqueios com instruções de correção |

---

## Referências de Skill

| Ferramenta | Caminho |
|------------|---------|
| Validador de Skill | `engineering/skill-tester/scripts/skill_validator.py` |
| Pontuador de Qualidade | `engineering/skill-tester/scripts/quality_scorer.py` |
| Testador de Scripts | `engineering/skill-tester/scripts/script_tester.py` |
| Auditor de Segurança | `engineering/skill-security-auditor/scripts/skill_security_auditor.py` |
