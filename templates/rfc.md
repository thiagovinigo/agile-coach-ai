# Template: Request for Comments (RFC)

## 📌 Ótica: O que é este documento e por que ele existe?
O Request for Comments (RFC) é um processo formal de proposição de uma mudança técnica, arquitetural ou de processo. 
Ele existe para **democratizar o design de software e solicitar feedback aberto**. Antes de investir semanas codificando uma solução pesada, um engenheiro escreve um RFC para colher opiniões dos pares, levantar pontos cegos e construir consenso, garantindo que o time inteiro "compre" a ideia.

---

## 🛡️ Guard Rails (Limites e Direcionamentos)
- **Foco na Investigação Aberta:** O RFC não é uma ditadura. A linguagem deve ser persuasiva, mas aberta à refutação. Use frases como "Esta é a minha proposta, onde ela falha?".
- **Comunicação Assíncrona:** A vantagem do RFC é evitar longas reuniões inúteis. O documento deve ser claro o suficiente para que qualquer desenvolvedor leia no seu próprio tempo e adicione comentários na plataforma (GitHub, Notion, Docs).
- **Time-Boxed:** Um RFC não pode ficar "aberto a comentários" para sempre. Estipule um prazo (ex: "Feedback encerra na próxima sexta-feira").

---

## 🚫 Políticas Não Negociáveis
1. **RFC antes do Código Complexo:** Nenhuma mudança de infraestrutura base (ex: migração de nuvem, mudança drástica de framework web, criação de CI/CD complexo) pode começar sem um RFC aprovado.
2. **Resolução de Comentários:** O autor não precisa acatar todas as ideias, mas tem a obrigação de responder educadamente e registrar o porquê descartou os apontamentos críticos dos colegas.

---

## 1. Visão Geral (Abstract)
**Status:** [Rascunho | Em Discussão | Aceito | Rejeitado]  
**Autor:** [Nome do autor principal]  
**Prazo para Feedback:** [Data limite]  

Um parágrafo resumindo o problema atual e qual é a direção que você propõe para resolvê-lo.
> **Ex:** Atualmente temos um monólito que leva 40 min para buildar. Proponho dividirmos a área de faturamento em um serviço separado para diminuir a carga do repositório principal e dar autonomia ao squad financeiro.

## 2. A Motivação (Por que isso é necessário?)
*Apresente dados. Dores atuais do time, impacto financeiro, riscos iminentes, gargalos de performance.*

## 3. A Solução Proposta
*Explique a sua ideia central com riqueza de detalhes técnicos suficientes para os outros avaliarem a viabilidade.*
- Etapas sugeridas de implementação.
- Diagramas e fluxos.
- Contratos (APIs) ou bibliotecas que seriam desenvolvidas.

## 4. O Custo (Trade-offs e Impactos)
*Nenhuma mudança vem de graça. Liste o que o time vai perder ao adotar sua proposta.*
- Custos financeiros (AWS, licenças).
- Tempo de desenvolvimento (man-hours).
- Curva de aprendizado.
- Sistemas antigos que vão parar de funcionar e precisam ser desligados.

## 5. Alternativas Analisadas
*A solução proposta não é a única. Quais as outras opções e por que a sua é melhor?*

## 6. Questões em Aberto
*Pergunte à equipe onde você tem dúvidas.*
- "Nós deveríamos usar gRPC em vez de REST neste gargalo?"
- "O time de segurança já tem regras definidas para esse novo tipo de banco?"
