---
name: tc
description: Rastreia mudanças técnicas com registros estruturados, máquina de estados e handoff entre sessões. Uso: /tc <init|create|update|status|resume|close|export|dashboard> [args]
---

# /tc — Rastreador de Mudanças Técnicas

Despacha um comando de TC (Technical Change). Argumentos: `$ARGUMENTS`.

Se `$ARGUMENTS` estiver vazio, exibe este menu e para:

```
/tc init                       Inicializa o rastreamento de TC neste projeto
/tc create <nome>              Cria um novo registro TC
/tc update <tc-id> [...]       Atualiza campos, status, arquivos, handoff
/tc status [tc-id]             Exibe um TC ou o resumo do registro
/tc resume <tc-id>             Retoma um TC de uma sessão anterior
/tc close <tc-id>              Transiciona um TC para implantado
/tc export                     Re-renderiza artefatos derivados
/tc dashboard                  Re-renderiza o resumo do registro
```

Caso contrário, analisa `$ARGUMENTS` como `<subcomando> <resto>` e despacha para o protocolo correspondente abaixo. Todos os scripts ficam em `engineering/tc-tracker/scripts/`.

## Subcomandos

### `init`

```bash
python3 engineering/tc-tracker/scripts/tc_init.py --root . --json
```

Se status for `already_initialized`, reporta estatísticas atuais e para. Caso contrário, reporta o que foi criado e sugere `/tc create <nome>` como próximo passo.

### `create <nome>`

1. Interpreta `<nome>` como slug em kebab-case. Se ausente, pede ao usuário.
2. Solicita (uma pergunta por vez):
   - Título (5–120 chars)
   - Escopo: `feature | bugfix | refactor | infrastructure | documentation | hotfix | enhancement`
   - Prioridade: `critical | high | medium | low` (padrão `medium`)
   - Resumo (10+ chars)
   - Motivação
3. Executa:
   ```bash
   python3 engineering/tc-tracker/scripts/tc_create.py --root . \
     --name "<slug>" --title "<título>" --scope <escopo> --priority <prioridade> \
     --summary "<resumo>" --motivation "<motivação>" --json
   ```
4. Reporta o ID do novo TC e o caminho para o registro.

### `update <tc-id> [intenção]`

1. Se `<tc-id>` estiver ausente, lista TCs ativos e pergunta qual.
2. Determina a intenção do usuário a partir de linguagem natural:
   - **Mudança de status** → `--set-status <estado>` com `--reason "<motivo>"`
   - **Adicionar arquivos** → `--add-file caminho[:ação]`
   - **Adicionar teste** → `--add-test "<título>" --test-procedure "<passo>" --test-expected "<resultado>"`
   - **Atualizar handoff** → `--handoff-progress`, `--handoff-next`, `--handoff-blocker`, `--handoff-context`
   - **Adicionar nota** → `--note "<texto>"`
   - **Adicionar tag** → `--tag <tag>`
3. Executa:
   ```bash
   python3 engineering/tc-tracker/scripts/tc_update.py --root . --tc-id <tc-id> [flags] --json
   ```
4. Se código de saída não for zero, exibe o erro verbatim. Não repita cegamente.

### `status [tc-id]`

```bash
# Com tc-id:
python3 engineering/tc-tracker/scripts/tc_status.py --root . --tc-id <tc-id>
# Sem tc-id:
python3 engineering/tc-tracker/scripts/tc_status.py --root . --all
```

### `resume <tc-id>`

1. Executa `tc_status.py --tc-id <tc-id> --json`
2. Exibe o bloco de handoff em destaque: `progress_summary`, `next_steps` (numerados), `blockers`, `key_context`
3. Pergunta: "Retomar <tc-id> e continuar a partir do passo 1? (s/n)"
4. Se sim, registra a retomada via `tc_update.py` e começa a executar o primeiro item de `next_steps`.

### `close <tc-id>`

1. Lê o registro via `tc_status.py --tc-id <tc-id> --json`
2. Verifica se o status atual é `tested`. Se não, recusa e informa quais transições ainda são necessárias.
3. Verifica `test_cases`: avisa se algum estiver `pending`, `fail` ou `blocked`.
4. Pergunta: aprovador, notas de aprovação, status de cobertura de teste.
5. Executa `tc_update.py --set-status deployed`
6. Reporta: "TC-NNN fechado e implantado."

### `export`

Não há exportação automática para HTML. Em vez disso:
1. Lê o registro.
2. Para cada registro, executa `tc_validator.py --record <caminho> --json`
3. Executa `tc_validator.py --registry docs/TC/tc_registry.json --json`
4. Reporta: total de registros validados, erros, caminhos de itens inválidos.

### `dashboard`

```bash
python3 engineering/tc-tracker/scripts/tc_status.py --root . --all
```

## Leis de Ferro

1. **Nunca edite `tc_record.json` manualmente.** Sempre use `tc_update.py` para que o histórico seja preservado e a validação seja executada.
2. **Nunca pule a máquina de estados.** Avance pelos estados mesmo que pareça redundante.
3. **Nunca exclua um TC.** O histórico é apenas de acréscimo — adicione uma revisão final e marque como `[CANCELADO]`.
4. **Tarefas administrativas em segundo plano.** Quando estiver no meio de uma tarefa, despache um subagente em segundo plano para atualizar o TC. Não pause a codificação para burocracia.
5. **Valide antes de reportar sucesso.** Se um script sair com código diferente de zero, exiba o erro e pare.

## Skills Relacionadas

- `engineering/tc-tracker` — SKILL.md completo com referência de esquema, diagramas de ciclo de vida e formato de handoff
- `engineering/changelog-generator` — Par com o TC tracker: TCs para trilha de auditoria por mudança, changelog para notas de lançamento voltadas ao usuário
- `engineering/tech-debt-tracker` — Para rastrear dívida de longa duração em vez de mudanças de código discretas
