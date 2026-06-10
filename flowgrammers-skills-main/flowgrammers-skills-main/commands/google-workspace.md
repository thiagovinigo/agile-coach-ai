---
name: google-workspace
description: "Operações CLI do Google Workspace: diagnóstico de configuração, auditoria de segurança, descoberta de receitas e análise de saída. Uso: /google-workspace <setup|audit|recipe|analyze> [opções]"
---

# /google-workspace

Administração do Google Workspace via CLI `gws`. Execute diagnósticos de configuração, auditorias de segurança, navegue e execute receitas, e analise saídas de comandos.

## Uso

```
/google-workspace setup [--json]
/google-workspace audit [--services gmail,drive,calendar] [--json]
/google-workspace recipe list [--persona <cargo>] [--json]
/google-workspace recipe search <palavra-chave> [--json]
/google-workspace recipe run <nome> [--dry-run]
/google-workspace recipe describe <nome>
/google-workspace analyze [--filter <campo=valor>] [--group-by <campo>] [--stats <campo>] [--format table|csv|json]
```

## Exemplos

```
/google-workspace setup
/google-workspace audit --services gmail,drive --json
/google-workspace recipe list --persona pm
/google-workspace recipe search "email"
/google-workspace recipe run standup-report --dry-run
/google-workspace recipe describe morning-briefing
/google-workspace analyze --filter "mimeType=pdf" --select "name,size" --format table
```

## Scripts

- `engineering-team/google-workspace-cli/scripts/gws_doctor.py` — Diagnóstico pré-voo
- `engineering-team/google-workspace-cli/scripts/auth_setup_guide.py` — Guia de configuração de autenticação
- `engineering-team/google-workspace-cli/scripts/gws_recipe_runner.py` — Catálogo e executor de receitas
- `engineering-team/google-workspace-cli/scripts/workspace_audit.py` — Auditoria de segurança
- `engineering-team/google-workspace-cli/scripts/output_analyzer.py` — Analisador JSON/NDJSON

## Subcomandos

### setup
Executa diagnóstico pré-voo e validação de autenticação.
```bash
python3 engineering-team/google-workspace-cli/scripts/gws_doctor.py [--json]
python3 engineering-team/google-workspace-cli/scripts/auth_setup_guide.py --validate [--json]
```

### audit
Executa auditoria de segurança e configuração.
```bash
python3 engineering-team/google-workspace-cli/scripts/workspace_audit.py [--services gmail,drive,calendar] [--json]
```

### recipe
Navega, pesquisa e executa as 43 receitas gws integradas.
```bash
python3 engineering-team/google-workspace-cli/scripts/gws_recipe_runner.py --list [--persona <cargo>] [--json]
python3 engineering-team/google-workspace-cli/scripts/gws_recipe_runner.py --search <palavra-chave> [--json]
python3 engineering-team/google-workspace-cli/scripts/gws_recipe_runner.py --describe <nome>
python3 engineering-team/google-workspace-cli/scripts/gws_recipe_runner.py --run <nome> [--dry-run]
```

### analyze
Processa, filtra e agrega saída JSON de qualquer comando gws.
```bash
gws <comando> --json | python3 engineering-team/google-workspace-cli/scripts/output_analyzer.py [opções]
python3 engineering-team/google-workspace-cli/scripts/output_analyzer.py --demo --format table
```

## Referência de Skill
→ `engineering-team/google-workspace-cli/SKILL.md`

## Comandos Relacionados
- Sem dependências diretas (skill Google Workspace autocontida)
