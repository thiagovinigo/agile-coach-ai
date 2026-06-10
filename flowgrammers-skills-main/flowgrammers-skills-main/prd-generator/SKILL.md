---
name: prd-generator
description: "Gerador de PRD (Product Requirements Document) em portugues-BR a partir de um Product Brief. Conduz entrevista guiada com 6 perguntas-chave (Nome, Overview, Persona, Objetivo, Requisitos Funcionais, Modelo de Negocio) e gera um PRD completo em Markdown com 9 secoes (Visao Geral, Funcionalidades, Fluxos, Diagrama Mermaid, Design UI, Modelo de Dados com ER e SQL, Arquitetura, Metricas, Roadmap), salvando em .prd/prd_NOME.md para uso em Claude Code. Use SEMPRE que o usuario mencionar gerar PRD, criar PRD, Product Requirements Document, documento de requisitos, transformar brief em PRD, estruturar product brief, preparar requisitos para Lovable Bolt V0, documentar produto, ou enviar um product brief pedindo estruturacao. Trigger TAMBEM quando descrever ideia de produto ou app pedindo estruturar, documentar ou preparar para desenvolvimento. Nao use para specs tecnicas de feature isolada (use sdd-generator)."
---

# PRD Generator

Skill para transformar um Product Brief curto em um PRD completo, estruturado e pronto para alimentar ferramentas de Vibe Coding (Lovable, Bolt, V0, Claude Code).

## Quando usar

Use esta skill sempre que o usuário:
- Pedir explicitamente para gerar/criar um PRD
- Enviar um product brief, lista de features ou descrição de produto pedindo estruturação
- Mencionar querer "preparar requisitos" para uma ferramenta de IA de desenvolvimento
- Descrever uma ideia de aplicação e pedir documentação técnica/produto

Não use para:
- Especificação técnica de UMA feature isolada → use `sdd-generator`
- Roadmap de produto sem detalhamento de implementação
- Análise/auditoria de PRD existente (a menos que o usuário peça reescrita)

## Workflow

### Etapa 1: Capturar contexto inicial

Verifique se o usuário já forneceu o product brief na mensagem inicial. Há três cenários:

**Cenário A — Brief completo já enviado:** o usuário colou um brief com as 6 informações principais. Vá direto para a Etapa 3.

**Cenário B — Brief parcial:** o usuário descreveu o produto mas faltam informações. Identifique o que está preenchido e pule a Etapa 2 — pergunte apenas o que falta.

**Cenário C — Pedido genérico:** o usuário pediu para "criar um PRD" sem detalhes. Vá para a Etapa 2 (entrevista completa).

### Etapa 2: Entrevista guiada (Product Brief)

Faça as 6 perguntas do Product Brief. **Faça TODAS em uma única mensagem** (não uma por vez — isso quebra o fluxo). Use formatação clara:

```
Para gerar um PRD completo, preciso entender 6 pontos sobre o produto. Pode responder em texto livre ou em tópicos — fique à vontade.

**1. Nome do Produto**
Como o produto se chama?

**2. Overview**
Em 2-3 parágrafos: o que o produto faz, qual problema resolve e como funciona em alto nível?

**3. Persona**
Quem é o público-alvo? Que tipos de usuários/perfis vão usar?

**4. Objetivo**
Qual o objetivo principal do produto? O que ele permite que o usuário alcance?

**5. Requisitos Funcionais**
Quais são as funcionalidades-chave? (Pode listar em bullets — login, dashboard, etc.)

**6. Modelo de Negócio**
Como o produto monetiza? Tem MVP gratuito? Planos pagos? Limites?
```

Após receber as respostas, faça perguntas de follow-up **apenas se** alguma informação crítica estiver faltando para construir uma seção do PRD. Exemplos de follow-ups que valem a pena:
- Stack tecnológica preferida (se houver constraints)
- Integrações externas necessárias (WhatsApp, pagamento, e-mail)
- Plataforma alvo (web, mobile, PWA)
- Tem identidade visual/cores definidas?

Se o usuário não souber algo (ex: stack), **assuma defaults sensatos** (React + Vite + TypeScript + Tailwind + Supabase) e mencione isso no PRD como "stack recomendada — ajustável".

### Etapa 3: Gerar o PRD

Antes de gerar, leia OBRIGATORIAMENTE os arquivos de referência:

1. **`references/prd_structure.md`** — estrutura completa das 9 seções com instruções detalhadas de cada uma
2. **`references/example_prd.md`** — exemplo de PRD de alta qualidade para calibrar tom, profundidade e formato

Depois, gere o PRD seguindo estas diretrizes:

**Princípios de qualidade:**
- **Idioma:** sempre português-BR. Tom profissional mas claro, sem jargão desnecessário.
- **Profundidade:** vá fundo em cada seção. Um PRD raso não serve para Vibe Coding — ferramentas como Lovable precisam de contexto rico.
- **Mermaid:** todos os diagramas (fluxo, ER, arquitetura) em Mermaid válido.
- **SQL real:** o schema na seção 6.2 deve ser SQL PostgreSQL executável (com RLS, índices, triggers), não pseudo-código.
- **Adaptação ao contexto:** se o produto é mobile-first, dê mais peso à seção mobile. Se tem coleta anônima de dados, destaque LGPD. Se tem múltiplos perfis, detalhe permissões.

**Estrutura obrigatória (9 seções):**
1. Visão Geral (4 parágrafos: o quê + como funciona + público + diferenciais)
2. Funcionalidades (perfis de usuário em tabela + módulos numerados + páginas em tabela)
3. Processos de Navegação e Fluxo (jornada de cada perfil em passos numerados)
4. Diagrama de Fluxo Completo (Mermaid graph TD)
5. Design Interface (cores, tipografia, componentes, páginas detalhadas, responsividade)
6. Modelo de Dados (ER em Mermaid + SQL completo com RLS)
7. Arquitetura (diagrama Mermaid + stack + estrutura de pastas + fluxos + segurança)
8. Métricas de Sucesso do MVP (tabela)
9. Roadmap Pós-MVP (fases futuras)

**Antes de gerar:** confirme rapidamente com o usuário o nome do arquivo final, ex: "Vou gerar o PRD e salvar em `.prd/prd_avalie_meu_atendimento.md`. Posso prosseguir?". Se o usuário já demonstrou pressa ou autonomia, pule essa confirmação e gere direto.

### Etapa 4: Salvar o arquivo

1. **Determinar o nome do arquivo:** converta o nome do produto para snake_case minúsculo, sem acentos.
   - "Avalie o Meu Atendimento" → `prd_avalie_meu_atendimento.md`
   - "FinanceFlow Pro" → `prd_financeflow_pro.md`
   - "Açaí Express" → `prd_acai_express.md`

2. **Garantir que o diretório `.prd/` existe na raiz do projeto:**
   ```bash
   mkdir -p .prd
   ```

3. **Salvar o arquivo em `.prd/prd_<nome>.md`.**

4. **Confirmar ao usuário** com o caminho final e uma sugestão de próximo passo, ex: "PRD salvo em `.prd/prd_avalie_meu_atendimento.md`. Você pode agora alimentar este arquivo no Lovable/Bolt ou usar com `sdd-generator` para quebrar em specs de feature."

### Etapa 5 (opcional): Iteração

Se o usuário pedir ajustes após ver o PRD ("aumenta a parte de segurança", "adiciona uma seção de testes", "muda o modelo de cores"), edite o arquivo diretamente com `str_replace` — não regenere tudo.

## Anti-padrões a evitar

- **Não gere PRDs genéricos.** Um PRD bom é específico ao produto. "O sistema terá autenticação" é fraco; "Autenticação via Supabase Auth com login e-mail/senha + Google OAuth, sessão persistente para reduzir atrito" é forte.
- **Não pule diagramas.** Mesmo que o produto seja simples, gere o Mermaid. Ferramentas de Vibe Coding usam isso.
- **Não invente requisitos.** Se o usuário não mencionou algo, ou pergunte ou marque explicitamente como "sugestão — confirmar".
- **Não economize na seção 6 (Modelo de Dados).** SQL completo, com tipos certos, RLS por padrão, índices estratégicos e triggers quando fizer sentido.
- **Não use tabelas onde prosa funciona melhor.** A seção Visão Geral é prosa rica; tabelas são para perfis, módulos e páginas.
- **Não force complexidade.** Se o produto não precisa de microservices, não desenhe microservices. Calibre pela persona — um PRD para SMB simples não precisa de Kubernetes.

## Formato de saída final

O arquivo deve seguir exatamente o template descrito em `references/prd_structure.md`. Use `references/example_prd.md` como espelho de qualidade — observe como cada seção tem profundidade real, não apenas listas vazias.

Após salvar, **não** despeje o conteúdo completo do PRD no chat — apenas confirme com o caminho do arquivo e ofereça resumo/próximos passos. O usuário lê o arquivo diretamente.
