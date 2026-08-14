# Template: Root Cause Analysis (RCA / Post-mortem)

## 📌 Ótica: O que é este documento e por que ele existe?
O RCA (ou Post-mortem) é um documento focado no aprendizado corporativo após um **Incidente Crítico em Produção**. 
Ele existe para garantir que a equipe entenda *o que aconteceu*, *por que aconteceu*, e *como garantir que nunca mais aconteça*. O maior desperdício de um incidente (site fora do ar, perda de dados) é não aprender nada com ele.

---

## 🛡️ Guard Rails (Limites e Direcionamentos)
- **Cultura Blameless (Sem Culpa):** O RCA avalia os *sistemas* e os *processos*, nunca as *pessoas*. Em vez de dizer "O João deletou a tabela errada", escreva "O sistema permitiu que um desenvolvedor operasse o banco de produção sem um mecanismo de confirmação (dry-run)". Assuma que todos agiram com as melhores intenções dadas as informações e ferramentas que tinham.
- **Investigação Profunda (5 Porquês):** Não pare no primeiro erro óbvio. Vá perguntando "por quê?" até chegar na raiz estrutural do problema.
- **Planos de Ação Acionáveis:** Itens de ação não podem ser vagos como "ter mais cuidado". Eles devem ser tickets no Jira/Trello com donos e prazos claros (ex: "Configurar alerta no Datadog se a CPU passar de 90%").

---

## 🚫 Políticas Não Negociáveis
1. **Obrigatoriedade:** Todo incidente de Severidade Crítica (Sev 1 ou Sev 2) que impacta o cliente final exige a escrita de um RCA em até 48 horas após a resolução.
2. **Participação Multidisciplinar:** A reunião de RCA deve incluir quem descobriu o erro, quem corrigiu e pelo menos um líder técnico/PM.
3. **Não Encerrar Sem Ticket:** O RCA só é considerado "Concluído" se as tarefas de mitigação de longo prazo forem criadas no backlog do time de engenharia.

---

## 1. Informações Básicas
- **Data do Incidente:** [DD/MM/AAAA]
- **Severidade:** [Crítica / Alta / Média]
- **Líder do Incidente (Incident Commander):** [Nome]
- **Sistemas Afetados:** [Ex: API de Pagamentos]
- **Duração da Indisponibilidade (Downtime):** [Horas/Minutos]

## 2. Resumo Executivo
*Um parágrafo que alguém não-técnico (ex: C-Level) possa entender.*
> **Ex:** No dia 10 de maio, das 14h às 15h30, nossos clientes não conseguiram finalizar compras devido a uma falha na tabela de banco de dados do carrinho de compras. O problema foi causado por um script de migração falho, e foi resolvido revertendo o sistema para a versão anterior.

## 3. Linha do Tempo (Timeline)
*Tudo em fuso horário padrão (ex: UTC-3).*
- **14:02** - Alerta do PagerDuty: Latência na API disparou.
- **14:05** - Engenheiro A começa a investigar e nota aumento de conexões travadas.
- **14:15** - Identificado que o script v2.1 travou o banco em modo *lock*.
- **14:40** - Iniciado o processo de Rollback.
- **15:30** - Sistema estabilizado e tráfego restaurado.

## 4. Análise de Causa Raiz (Os 5 Porquês)
1. **Por que o site ficou lento?** O banco de dados chegou a 100% de uso de CPU.
2. **Por que a CPU bateu 100%?** Porque houve um gargalo (table lock) na tabela de Carrinhos.
3. **Por que ocorreu um table lock?** Porque a migração de banco executada adicionou uma coluna em uma tabela gigante sem instrução `CONCURRENTLY`.
4. **Por que a migração não tinha CONCURRENTLY?** O desenvolvedor desconhecia essa limitação e não havia validação no CI/CD.
5. **Por que não temos validação no CI/CD? (Causa Raiz):** Nossa ferramenta de deploy não bloqueia operações bloqueantes no PostgreSQL.

## 5. Como Mitigamos o Problema Imediatamente?
*O que foi feito para restaurar a paz?*
> Ex: Rollback do último commit e matamos as transações presas manualmente no banco.

## 6. Plano de Ação (Ações Preventivas)
*Para garantir que nunca mais aconteça.*
| Ação | Dono | Prazo/Ticket |
|---|---|---|
| Adicionar linter (ex: sqruff) no pipeline para vetar migrações inseguras. | João / DevOps | Jira-123 (Sexta) |
| Criar alerta se o DB Load passar de 80% por 5 minutos seguidos. | Ana / SRE | Jira-124 (Próx Sprint) |
