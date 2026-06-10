# Prompt Engineering para Claude Code — Guia de Referência

> Última atualização: Mai/2026. Fontes: Anthropic Docs, Claude Code Docs, HoraDeCodar, eesel AI.

---

## Princípios Fundamentais

O Claude responde melhor quando o prompt tem:
1. **Clareza de intenção** — o que exatamente você quer
2. **Contexto suficiente** — o que existe, quais restrições
3. **Formato esperado** — como a saída deve ser estruturada
4. **Exemplos quando relevante** — few-shot para tarefas complexas

---

## Técnicas Essenciais

### 1. Zero-Shot Prompting
Instrução direta sem exemplos. Funciona bem para tarefas simples.

```
Refatore esta função Python para ser mais legível e adicione type hints:
[código]
```

### 2. Few-Shot Prompting
Forneça 2-3 exemplos do padrão desejado antes de pedir a tarefa.

```
Converta estes títulos para formato slug:
"Olá Mundo" → "ola-mundo"
"Como Aprender React" → "como-aprender-react"
"Meu Projeto #1" → "meu-projeto-1"

Agora converta: "Guia de Produtividade para Devs"
```

### 3. Chain of Thought (CoT)
Peça ao Claude para raciocinar passo a passo antes de responder.

```
Antes de implementar, pense em voz alta:
1. Quais são os casos de borda dessa função?
2. Qual a abordagem mais simples?
3. Como isso pode falhar?
Então, implemente.
```

### 4. Role Prompting (Personas)
Defina um papel específico para aumentar a qualidade da resposta.

```
Você é um engenheiro sênior de backend com 10 anos de experiência em Node.js e PostgreSQL.
Revise este código de API como faria em um code review real, apontando:
- Bugs potenciais
- Problemas de performance
- Violações de boas práticas
```

---

## Técnicas Avançadas para Claude Code

### 5. Entrevista Antes de Implementar
Para tarefas complexas, peça ao Claude para te entrevistar antes de escrever código.

```
Quero criar um sistema de autenticação para minha API Next.js.
Antes de começar a implementar, entreviste-me sobre:
- Requisitos de segurança
- Fluxo de usuário
- Integrações necessárias
- Casos de uso específicos
Faça uma pergunta de cada vez.
```

### 6. Implementação por Partes (Scaffolding)
Construa progressivamente — estrutura primeiro, detalhes depois.

```
Passo 1: Crie apenas a estrutura de arquivos e interfaces TypeScript
Passo 2: [após aprovar] Implemente as funções principais
Passo 3: [após aprovar] Adicione tratamento de erros e validações
Passo 4: [após aprovar] Escreva os testes
```

### 7. Debug Sistemático
Quando há erros, forneça contexto completo.

```
Este código está retornando erro:
[código completo]
[mensagem de erro completa com stack trace]
[o que já tentei]
[o que espero que aconteça]
Analise o problema e explique a causa raiz antes de sugerir a solução.
```

### 8. Explicação Linha a Linha
Para aprendizado ou code review profundo.

```
Explique este código linha por linha, incluindo:
- O que cada parte faz
- Por que foi escrito assim
- Possíveis alternativas
- Pontos de atenção
[código]
```

---

## Estrutura de Prompt Eficaz para Claude Code

```markdown
## Contexto
[Descreva o projeto, stack tecnológica, o que já existe]

## Objetivo
[O que precisa ser feito — seja específico]

## Restrições
[Limitações técnicas, dependências, padrões a seguir]

## Formato esperado
[Como quer a resposta: só código, com explicação, com testes, etc.]

## Exemplo (se aplicável)
[Input/output esperado ou código similar existente]
```

---

## Prompts Práticos por Caso de Uso

### Geração de Código
```
Crie uma função TypeScript que [descrição precisa].
Requisitos:
- Use apenas [bibliotecas específicas]
- Trate os erros [de forma específica]
- Inclua JSDoc
- Escreva um teste unitário com Jest

Não use [tecnologias/padrões que quer evitar].
```

### Code Review
```
Revise este código como um engenheiro sênior focando em:
1. Correctness — bugs e comportamentos inesperados
2. Performance — gargalos e otimizações
3. Maintainability — legibilidade e estrutura
4. Security — vulnerabilidades

Para cada problema, explique: o que está errado, por que é um problema, e como corrigir.
```

### Refatoração
```
Refatore este código com os objetivos:
- [Objetivo 1: ex. eliminar duplicação]
- [Objetivo 2: ex. melhorar testabilidade]
- [Objetivo 3: ex. seguir padrão SOLID]

Mantenha o comportamento externo idêntico. Explique cada mudança significativa.
```

### Debugging
```
Estou com este bug:
Comportamento esperado: [X]
Comportamento atual: [Y]
Erro: [mensagem de erro]
Já tentei: [o que já fiz]

Código relevante: [código mínimo que reproduz o problema]
```

### Documentação
```
Gere documentação completa para este módulo em português BR:
- Descrição geral e propósito
- Parâmetros e tipos (com exemplos)
- Valores de retorno
- Casos de uso comuns
- Limitações e casos de borda
[código]
```

---

## Melhores Práticas para Projetos Grandes

### Contexto via CLAUDE.md
Crie um arquivo `CLAUDE.md` na raiz do projeto com:
- Arquitetura geral
- Convenções de código do time
- Padrões de nomenclatura
- Dependências principais
- Como rodar testes

### Model Context Protocol (MCP)
Conecte Claude a ferramentas externas:
- Puppeteer/Playwright para automação de browser
- Banco de dados para consultas diretas
- APIs internas para contexto em tempo real
- Sentry/logs para debugging automático

### Prompt Caching para Contextos Grandes
Para projetos com muito código de contexto, estruture prompts para aproveitar o cache do Claude (reduções de até 90% em custo e latência).

---

## Anti-padrões a Evitar

| Anti-padrão | Problema | Solução |
|---|---|---|
| Prompt vago | "Melhore meu código" | Especifique o que melhorar e como medir |
| Contexto demais sem foco | 1000 linhas de código sem pergunta clara | Forneça só o código relevante |
| Pedido de múltiplas tarefas | "Crie, teste, documente e deploy" | Uma tarefa por vez |
| Sem formato esperado | Output inconsistente | Especifique: "retorne apenas o código, sem explicação" |
| Aceitar primeira resposta | Código pode ter bugs | Sempre peça testes e validação |

---

## Fluxo Iterativo Recomendado

```
1. Prompt inicial com contexto completo
2. Review da resposta — entenda antes de usar
3. Peça testes se não foram fornecidos
4. Execute os testes / rode o código
5. Se houver erros, retorne com o erro completo
6. Peça code review da própria solução ("que problemas você vê neste código?")
7. Itere até aprovação
```

---

## Referências

- [Melhores Práticas Claude Code — Anthropic](https://code.claude.com/docs/pt/best-practices)
- [Claude Prompting Best Practices — Anthropic API](https://platform.claude.com/docs/pt-BR/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [Claude Code Técnicas — HoraDeCodar](https://horadecodar.com.br/prompts-claude-code-tecnicas-funcionam/)
- [7 Melhores Práticas Claude Code — eesel AI](https://www.eesel.ai/pt/blog/claude-code-best-practices)
