# Template: Declaração de SKILL de IA (SKILL.md)

## 📌 Ótica: O que é este documento e por que ele existe?
Inspirado na padronização do ecossistema `skillsmp.com`, este documento ensina a **como codificar e organizar instruções para um Agente Autônomo de IA** (como Claude Code, Cursor, Flowgrammers ou ECC Agents).
Em vez de depender de prompts amadores dispersos em chats, um `SKILL.md` define uma competência modular e reprodutível que o Agente lê antes de começar uma tarefa complexa. Ele existe para garantir que a IA assuma um papel claro, entenda restrições do projeto e execute passos de maneira padronizada, reduzindo alucinações.

---

## 🛡️ Guard Rails (Limites e Direcionamentos)
- **Determinação e Foco (Scope):** A Skill deve fazer *uma única coisa excepcionalmente bem* (ex: "Otimizar Consultas SQL", "Escrever Testes E2E com Cypress"). Skills generalistas ("Resolver problemas gerais") geram péssimos resultados nas IAs.
- **Engenharia de Prompt Baseada em Arquitetura:** Use YAML Frontmatter para metadados e tags XML (`<instrucoes>`, `<exemplos>`) no conteúdo Markdown, pois a maioria dos LLMs analisa melhor essa estrutura.
- **Passos Concretos (Chain of Thought):** Sempre exija que a IA crie um planejamento ("Planning Mode") em um arquivo de rascunho temporário e apresente para aprovação antes de alterar códigos reais.

---

## 🚫 Políticas Não Negociáveis
1. **Gatilhos (Triggers) Declarados:** Todo `SKILL.md` deve listar comandos (ex: `/qa-check`, `/lint-fix`) para ativação clara da intenção.
2. **Não Burlar o Framework do Projeto:** A Skill da IA é expressamente proibida de recomendar ou adicionar bibliotecas de terceiros se o repositório possuir ferramentas equivalentes já instaladas.
3. **Limitação Delimitada:** A IA deve ser instruída a parar se não souber resolver algo, exigindo input humano em vez de guess-work cego.

---

*(Modelo Abaixo - Use isso ao criar novas Skills de IA para a equipe)*

```markdown
---
name: "Nome da Skill de IA"
description: "Descrição concisa de 1 linha sobre a habilidade do agente."
version: "1.0"
triggers: ["/ativar-skill", "/acao-especifica"]
dependencies: ["skill-secundaria.md"]
---

# 🤖 Propósito da Skill
(Defina a persona da IA)
"Você é um Especialista Sênior em [Tecnologia X]. Seu papel é receber [Entrada Y] e transformá-la em [Saída Z] dentro dos nossos padrões."

# 📍 Contexto e Base de Conhecimento
(Onde a IA deve buscar informações)
Quando ativado, pesquise imediatamente nos seguintes arquivos para entender o contexto antes de responder:
1. `src/core/types.ts`
2. `config/app_settings.json`

# 🛠️ Regras de Atuação (O que a IA deve ou NÃO deve fazer)
- **NUNCA** modifique arquivos na pasta `/legacy`.
- Sempre retorne código formatado usando a biblioteca interna `AppLogger`, não utilize `console.log`.
- Se você encontrar código sem testes e for instruído a refatorar, recuse-se a alterar sem antes criar uma suíte unitária de segurança.

# 📋 Fluxo de Execução (Chain of Thought)
Siga ESTRITAMENTE estes passos para resolver as tarefas desta skill:
1. **Compreensão:** Liste os arquivos analisados e o problema entendido.
2. **Planejamento:** Exponha seu plano de implementação. (Pare e espere aprovação do usuário).
3. **Execução:** Gere o código focado estritamente na melhoria requisitada, usando blocos Diff.
4. **Validação:** Descreva como você testaria (ou efetivamente rode comandos de teste, se tiver acesso ao terminal) para provar que a alteração funciona.

# 💡 Exemplos Esperados (One-Shot / Few-Shot Learning)
**Input do Usuário:** `/ativar-skill refatorar funcXYZ`
**Seu Comportamento Esperado:** "Analisei o arquivo... O plano é... [código gerado com os padrões internos]."
```
