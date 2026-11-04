# 🛡️ Jev + Claude Code: Os 4 Caminhos de Integração

Durante o uso do **Claude Code**, o agente frequentemente precisa tomar micro-decisões operacionais:
- *"Esse comando `Bash` é seguro para rodar sem perguntar ao humano?"*
- *"Esse arquivo contém segredos ou afeta produção?"*
- *"Qual subagente especializado deve assumir essa tarefa?"*

A aula apresenta **4 padrões práticos** para acoplar o Jev (Sistema 1) ao Claude Code (Sistema 2):

---

## Caminho 1: Hook `PreToolUse` (Guardião de Segurança em <200ms) ⭐ Recomendado
Toda vez que o Claude Code tenta executar `Bash`, o hook `.claude/settings.json` intercepta o comando e chama `jev_gate.py`.
- O Jev avalia simultaneamente:
  - `acao` (`choice`): `["allow", "ask", "deny"]`
  - `risco` (`score`): `0.0` a `1.0`
  - `motivo_curto` (`noul`): elemento crítico detectado
- **Resultado**: Comandos seguros (`ls`, `git status`, `npm test`) passam no piloto automático em 150ms (`allow`), comandos duvidosos pedem confirmação (`ask`), e comandos destrutivos (`rm -rf /`, `git push --force main`, `DROP TABLE`) são bloqueados na hora (`deny`).

---

## Caminho 2: Roteador de Subagentes (`Task` Dispatcher)
Antes de invocar um subagente pesado (Opus), um script leve consulta o Jev para escolher:
- `subagent` (`choice`): `["explorer-haiku", "debugger-sonnet", "architect-opus", "security-reviewer"]`
- Evita gastar tokens de Opus em tarefas mecânicas de busca de arquivos.

---

## Caminho 3: Servidor MCP (`jev-mcp`)
Expor o endpoint `https://api.typesafe.ai/v1/systemone` como uma tool MCP (`jev_decide`) para que o próprio agente ou scripts de automação possam classificar lotes de arquivos, issues do GitHub ou logs de erro com latência mínima.

---

## Caminho 4: Hook `UserPromptSubmit` (Enriquecimento de Contexto)
Quando o desenvolvedor envia um prompt no Claude Code, o hook classifica a intenção (`bugfix`, `feature`, `refactor`, `deploy`) e injeta apenas as instruções/skills relevantes no contexto, mantendo a janela de tokens enxuta.
