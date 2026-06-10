---
name: a11y-audit
description: Varre um projeto frontend em busca de violações de acessibilidade WCAG 2.2 e as corrige. Uso: /a11y-audit [caminho]
---

# /a11y-audit

Varre um projeto frontend em busca de problemas de acessibilidade WCAG 2.2, exibe correções e verifica contraste de cores.

## Uso

```bash
/a11y-audit                     # Varre o projeto atual
/a11y-audit ./src               # Varre um diretório específico
/a11y-audit ./src --fix         # Varre e aplica correções automáticas
```

## O que faz

### Etapa 1: Varredura

Executa o scanner de acessibilidade no diretório alvo:

```bash
python3 {skill_path}/scripts/a11y_scanner.py {path} --json
```

Agrupa os achados por severidade (crítico → sério → moderado → leve).

Exibe um resumo:
```
Auditoria A11y: ./src
  Crítico: 3 | Sério: 7 | Moderado: 12 | Leve: 5
  Arquivos varridos: 42 | Arquivos com problemas: 15
```

### Etapa 2: Correção

Para cada achado (começando pelos críticos):

1. Lê o arquivo afetado
2. Exibe a violação com contexto (antes)
3. Aplica a correção de `references/framework-a11y-patterns.md`
4. Exibe o resultado (depois)

**Correções automáticas** (aplicadas sem perguntar):
- `alt=""` ausente em imagens decorativas
- Atributo `lang` ausente no `<html>`
- Valores de `tabindex` > 0 → definidos como 0
- `type="button"` ausente em botões não-submit
- Remoção de outline sem substituto → adiciona estilos `:focus-visible`

**Problemas que exigem decisão do usuário** (exibe a correção e pergunta):
- Texto alternativo ausente (requer descrição do usuário)
- Labels de formulário ausentes (requer texto do label)
- Reestruturação de headings (pode afetar layout)
- Alterações de papel ARIA (pode afetar funcionalidade)

### Etapa 3: Verificação de Contraste

Se houver arquivos CSS, executa o verificador de contraste:

```bash
python3 {skill_path}/scripts/contrast_checker.py --batch {path}
```

Para cada par de cores com falha, sugere alternativas acessíveis.

### Etapa 4: Relatório

Gera um relatório markdown em `a11y-report.md`:
- Resumo executivo (aprovado/reprovado, contagem de problemas)
- Achados por arquivo com diffs antes/depois
- Itens pendentes de revisão manual
- Cobertura de critérios WCAG

## Referência de Skill

- `engineering-team/a11y-audit/SKILL.md`
- `engineering-team/a11y-audit/scripts/a11y_scanner.py`
- `engineering-team/a11y-audit/scripts/contrast_checker.py`
- `engineering-team/a11y-audit/references/wcag-quick-ref.md`
- `engineering-team/a11y-audit/references/aria-patterns.md`
- `engineering-team/a11y-audit/references/framework-a11y-patterns.md`
