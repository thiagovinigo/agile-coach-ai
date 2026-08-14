# Template: Especificação Técnica (SPEC)

## 📌 Ótica: O que é este documento e por que ele existe?
A Especificação Técnica (SPEC ou Tech Spec) é a resposta da Engenharia ao documento de Produto (PRD). O PRD diz *o que* precisa ser feito e *por quê*; a SPEC dita exatamente **COMO** a solução será arquitetada, quais ferramentas serão usadas e qual o impacto no ecossistema atual.
Este documento existe para **evitar surpresas durante o desenvolvimento**. Ele promove alinhamento técnico entre os engenheiros, permite feedback estruturado antes de escrever código e garante que segurança, performance e escalabilidade não sejam esquecidas.

---

## 🛡️ Guard Rails (Limites e Direcionamentos)
- **Não Reescreva o PRD:** Faça referência aos requisitos de negócio, mas foque nas decisões técnicas.
- **Design de Contratos Primeiro (API-First):** Antes de codificar o backend ou frontend, o contrato (JSON/OpenAPI) deve estar documentado e acordado na SPEC.
- **Pense na Falha:** Descreva explicitamente como o sistema se comporta quando o banco de dados falha, a rede cai ou um serviço de terceiros fica indisponível.

---

## 🚫 Políticas Não Negociáveis
1. **Revisão de Pares:** SPECs de alta complexidade precisam ser revisadas por pelo menos um Engenheiro Sênior ou Tech Lead antes da execução.
2. **Avaliação de Segurança:** Toda SPEC que altera fluxos de autenticação, permissões ou adiciona coleta de PII (Dados Pessoais Identificáveis) deve passar por revisão do time de InfoSec.
3. **Plano de Rollback:** Toda SPEC deve incluir como desfazer as mudanças em produção de forma segura caso ocorra um incidente crítico no deploy.

---

## 1. Visão Geral da Arquitetura
*Explicação de alto nível de como a solução técnica resolve o problema descrito no PRD.*
- **Abordagem:** [Breve explicação, ex: "Criaremos um novo microserviço em Go que assina os eventos do RabbitMQ..."]
- **Diagrama (Opcional, mas recomendado):** Mermaid.js, draw.io ou link para a arquitetura.

## 2. Modelagem de Dados
*Como os dados serão armazenados?*
- **Tabelas / Coleções Novas:** [Esquemas, tipos de dados, chaves primárias e estrangeiras].
- **Índices necessários:** [Para garantir performance em queries pesadas].

## 3. Contratos de API
*Endpoints criados ou modificados.*
```json
// Exemplo: POST /api/v1/users
// Request Body:
{
  "email": "string",
  "role_id": "integer"
}
// Response (201 Created):
{
  "id": "uuid",
  "status": "active"
}
```

## 4. Requisitos Não-Funcionais e Restrições
- **Performance:** Tempo de resposta (p95 < 200ms).
- **Escalabilidade:** Como o design lida com um pico de 10x no tráfego.
- **Observabilidade:** Quais métricas de negócio e logs técnicos precisaremos emitir? (Datadog, Prometheus).

## 5. Estratégia de Migração e Rollout
- Serão necessárias migrações de dados retroativas?
- Como será o Feature Flag / Canary Release?
- **Plano de Rollback:** Passo-a-passo se algo der errado.

## 6. Testabilidade
- Quais os desafios para escrever testes automatizados? 
- Serão necessários mocks de sistemas externos complexos?

## 7. Questões Abertas (Open Questions)
*Dúvidas que precisam ser resolvidas com outras equipes antes de fechar a SPEC.*
- [ ] O serviço de notificação suporta batch processing?
