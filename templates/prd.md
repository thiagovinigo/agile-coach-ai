# Template: Documento de Requisitos de Produto (PRD)

## 📌 Ótica: O que é este documento e por que ele existe?
O PRD (Product Requirements Document) é o ponto de partida de qualquer nova iniciativa ou feature. Ele não é um documento técnico, mas sim a tradução de um **problema de negócio/usuário** para uma **visão de solução**. 
Ele existe para garantir que **Engenharia, Design, QA e Negócios** estejam alinhados sobre **o que** estamos construindo, **para quem** e **como mediremos o sucesso**. Sem um PRD, construímos software às cegas.

---

## 🛡️ Guard Rails (Limites e Direcionamentos)
- **Foco no Problema, Não na Solução Técnica:** O PRD define o *O Que* e o *Por Quê*. O *Como* (banco de dados, arquitetura) pertence ao documento de Especificação (SPEC).
- **Métricas antes do Código:** Se não sabemos como medir o sucesso de uma feature, ela não está pronta para desenvolvimento.
- **Escopo Fechado (MVP):** Tudo que não for essencial para validar a hipótese principal deve ir para a seção "Out of Scope" (Fora de Escopo).

---

## 🚫 Políticas Não Negociáveis
1. **Aprovação Obrigatória:** Nenhum PRD vai para desenvolvimento (Sprint Backlog) sem o de-acordo formal de Produto, Design e Engenharia (Tech Lead).
2. **Definição de Audiência:** O documento deve identificar claramente qual segmento de usuário será impactado. Construir "para todos" é proibido.
3. **Casos de Uso Bem Definidos:** Casos de uso de borda (edge cases) e cenários de erro devem estar mapeados.

---

## 1. Problema e Oportunidade
- **O Problema (1 frase):** [Resumo claro do problema do usuário].
- **Contexto:** Por que estamos resolvendo isso agora? Qual a dor?
- **Impacto no Negócio:** Qual métrica da empresa isso move? (Ex: Churn, Receita, Custo Operacional).

## 2. Audiência (Personas)
- **Quem vai usar:** [Persona Primária - Ex: Gestor de RH].
- **Cenário atual:** Como eles resolvem esse problema hoje (workaround)?
- **Valor entregue:** O que melhora na vida deles com essa feature?

## 3. Escopo da Solução
- **In Scope (Dentro do Escopo):** O que será entregue na Fase 1 (MVP)?
  - Funcionalidade A: [Breve descrição].
  - Funcionalidade B: [Breve descrição].
- **Out of Scope (Fora do Escopo):** O que NÃO vamos fazer agora? (Evitar escopo oculto).

## 4. Métricas de Sucesso
- **Métrica Primária:** [Ex: Aumentar a conversão em 15%].
- **Health Metrics (Métricas de Saúde):** O que NÃO podemos piorar? [Ex: O tempo de carregamento da página não pode subir].

## 5. Casos de Uso e Experiência do Usuário (UX)
- Resumo dos fluxos que o usuário deve percorrer. Referenciar mockups ou protótipos de design.
- O que acontece se houver um erro de conexão? (Unhappy paths).

## 6. Riscos e Dependências
- **Dependência Técnica:** Precisamos da API de parceiros? Precisamos que outra equipe entregue algo?
- **Risco de Negócio:** Se atrasarmos, perdemos um cliente importante?
- **Plano de Mitigação:** Como vamos lidar com esses riscos.

## 7. Assinaturas (Aprovação)
| Papel | Nome | Status |
|---|---|---|
| Product Manager | [Nome] | ⏳ Pendente |
| Tech Lead | [Nome] | ⏳ Pendente |
| Design Lead | [Nome] | ⏳ Pendente |
