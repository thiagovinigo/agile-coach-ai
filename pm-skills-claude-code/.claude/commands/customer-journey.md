# /customer-journey

## O que essa skill faz

Gera um mapa completo de jornada do cliente em 7 estágios (Awareness → Advocacy), documentando touchpoints, ações, emoções, pain points e oportunidades em cada fase. Identifica momentos críticos: Aha Moment, Moments of Truth e Churn Triggers.

Saída: **Customer Journey Map** em tabela + análise de momentos críticos + recomendações priorizadas.

---

## Quando usar

- Está mapeando a experiência completa de um segmento de usuário pela primeira vez
- Quer identificar onde usuários abandonam o produto (churn triggers)
- Precisa alinhar múltiplos times (Marketing, Produto, CS, Sales) sobre a experiência do cliente
- Quer priorizar melhorias com base em impacto na jornada, não em opinião
- Está redesenhando onboarding, retenção ou expansion e precisa do contexto completo

---

## Input esperado

**Mínimo:**
- **Produto/serviço**: O que o cliente está usando
- **Persona**: Quem está percorrendo essa jornada (cargo, contexto, objetivo)
- **Escopo**: Jornada completa ou foco em estágios específicos

**Opcional:**
- Dados de analytics (funil, retenção, NPS por estágio)
- Trechos de entrevistas com usuários
- Mapa de touchpoints existente
- Métricas de conversão entre estágios
- Tickets de suporte categorizados por estágio
- Personas já definidas (usar /persona se não existir)

---

## Processo

1. **Definir a persona** — Quem está viajando essa jornada? Se não tem persona definida, criar um perfil mínimo (nome, cargo, contexto, objetivo principal). A jornada muda drasticamente entre personas — nunca mapeie "o usuário genérico".

2. **Mapear os 7 estágios com touchpoints** — Para cada estágio (Awareness → Consideration → Acquisition → Onboarding → Engagement → Retention → Advocacy), listar os touchpoints onde o usuário interage com produto, marca ou time. Incluir touchpoints offline e de terceiros.

3. **Documentar ações, pensamentos e emoções** — Por estágio, registrar: o que o usuário FAZ (ações observáveis), o que PENSA (perguntas, dúvidas, expectativas) e o que SENTE (emoção dominante, intensidade 1-5). Basear em dados reais quando possível.

4. **Identificar momentos críticos** — Marcar três tipos:
   - **Aha Moment**: Quando o usuário experimenta o valor core pela primeira vez
   - **Moments of Truth**: Pontos onde o usuário decide continuar ou abandonar
   - **Churn Triggers**: Eventos ou fricções que causam abandono

5. **Priorizar melhorias** — Para cada pain point, avaliar: impacto na conversão/retenção × facilidade de resolver. Gerar top 5 recomendações ordenadas.

---

## Output

```markdown
# Customer Journey Map

## Persona
**Nome:** [Nome da persona]
**Cargo:** [Título]
**Objetivo:** [O que quer alcançar]
**Contexto:** [Situação que motiva a jornada]

---

## Journey Map — Visão Geral

| Estágio | Emoção Dominante | Conversão | Pain Point Principal |
|---------|-----------------|-----------|---------------------|
| Awareness | [Emoção] [1-5] | [%] → | [Dor] |
| Consideration | [Emoção] [1-5] | [%] → | [Dor] |
| Acquisition | [Emoção] [1-5] | [%] → | [Dor] |
| Onboarding | [Emoção] [1-5] | [%] → | [Dor] |
| Engagement | [Emoção] [1-5] | [%] → | [Dor] |
| Retention | [Emoção] [1-5] | [%] → | [Dor] |
| Advocacy | [Emoção] [1-5] | [%] | [Dor] |

---

## Estágio 1: Awareness

**Touchpoints:**
- [Onde o usuário descobre o produto: blog, ads, referral, evento, etc.]

**Ações do Usuário:**
- [O que faz: pesquisa, pergunta a colegas, lê review]

**Pensamentos & Perguntas:**
- "[Pergunta que tem na cabeça]"
- "[Dúvida]"

**Emoção:** [Emoção] — Intensidade: [1-5]

**Pain Points:**
- [Fricção ou barreira nesse estágio]

**Oportunidades:**
- [Como melhorar essa fase]

---

## Estágio 2: Consideration

**Touchpoints:**
- [Site, demo, trial, comparação com concorrentes]

**Ações do Usuário:**
- [Compara opções, pede demo, lê case studies]

**Pensamentos & Perguntas:**
- "[Pergunta]"
- "[Dúvida]"

**Emoção:** [Emoção] — Intensidade: [1-5]

**Pain Points:**
- [Fricção]

**Oportunidades:**
- [Melhoria]

---

## Estágio 3: Acquisition

**Touchpoints:**
- [Signup, compra, contrato, implementação inicial]

**Ações do Usuário:**
- [Cria conta, instala, configura]

**Pensamentos & Perguntas:**
- "[Pergunta]"

**Emoção:** [Emoção] — Intensidade: [1-5]

**Pain Points:**
- [Fricção]

**Oportunidades:**
- [Melhoria]

---

## Estágio 4: Onboarding

**Touchpoints:**
- [Primeiro login, tutorial, setup, primeira tarefa]

**Ações do Usuário:**
- [Configura perfil, importa dados, completa primeira ação]

**Pensamentos & Perguntas:**
- "[Pergunta]"

**Emoção:** [Emoção] — Intensidade: [1-5]

**Pain Points:**
- [Fricção]

**Oportunidades:**
- [Melhoria]

---

## Estágio 5: Engagement

**Touchpoints:**
- [Uso diário, features core, integrações, colaboração]

**Ações do Usuário:**
- [Workflow diário, features usadas, frequência]

**Pensamentos & Perguntas:**
- "[Pergunta]"

**Emoção:** [Emoção] — Intensidade: [1-5]

**Pain Points:**
- [Fricção]

**Oportunidades:**
- [Melhoria]

---

## Estágio 6: Retention

**Touchpoints:**
- [Renovação, upsell, suporte, check-ins de CS]

**Ações do Usuário:**
- [Avalia ROI, compara alternativas, expande uso]

**Pensamentos & Perguntas:**
- "[Pergunta]"

**Emoção:** [Emoção] — Intensidade: [1-5]

**Pain Points:**
- [Fricção]

**Oportunidades:**
- [Melhoria]

---

## Estágio 7: Advocacy

**Touchpoints:**
- [Referral, review, case study, community, upsell]

**Ações do Usuário:**
- [Recomenda, escreve review, participa de comunidade]

**Pensamentos & Perguntas:**
- "[Pergunta]"

**Emoção:** [Emoção] — Intensidade: [1-5]

**Pain Points:**
- [Fricção]

**Oportunidades:**
- [Melhoria]

---

## Momentos Críticos

### Aha Moment
**Quando:** [Estágio e momento específico]
**O que acontece:** [Primeira experiência com valor core]
**Indicador:** [Como saber que o usuário chegou aqui — ação ou métrica]
**% que atinge:** [Proporção dos usuários]

### Moments of Truth

| # | Estágio | Momento | Decisão | Taxa de Conversão |
|---|---------|---------|---------|-------------------|
| 1 | [Estágio] | [Descrição do momento] | [Continuar vs. Abandonar] | [%] |
| 2 | [Estágio] | [Descrição] | [Decisão] | [%] |
| 3 | [Estágio] | [Descrição] | [Decisão] | [%] |

### Churn Triggers

| # | Estágio | Trigger | Impacto | Frequência |
|---|---------|---------|---------|------------|
| 1 | [Estágio] | [O que causa abandono] | [Alto/Médio/Baixo] | [%] |
| 2 | [Estágio] | [Trigger] | [Impacto] | [%] |
| 3 | [Estágio] | [Trigger] | [Impacto] | [%] |

---

## Recomendações Priorizadas

| # | Estágio | Recomendação | Impacto | Esforço | Prioridade |
|---|---------|-------------|---------|---------|------------|
| 1 | [Estágio] | [O que fazer] | [Alto/Médio] | [Baixo/Médio/Alto] | [P1/P2/P3] |
| 2 | [Estágio] | [O que fazer] | [Impacto] | [Esforço] | [Prioridade] |
| 3 | [Estágio] | [O que fazer] | [Impacto] | [Esforço] | [Prioridade] |
| 4 | [Estágio] | [O que fazer] | [Impacto] | [Esforço] | [Prioridade] |
| 5 | [Estágio] | [O que fazer] | [Impacto] | [Esforço] | [Prioridade] |

**Quick wins (alto impacto + baixo esforço):**
- [Recomendação]
- [Recomendação]

**Investimentos estratégicos (alto impacto + alto esforço):**
- [Recomendação]
```

---

## Exemplo

**Input:**
> Produto: CRM B2B SaaS mid-market. Persona: Novo sales rep (SDR) fazendo onboarding no CRM pela primeira vez. Objetivo: mapear jornada completa para identificar onde perdemos usuários.

**Output:**

```markdown
# Customer Journey Map

## Persona
**Nome:** Mariana Costa
**Cargo:** SDR (Sales Development Representative)
**Objetivo:** Usar o CRM para gerenciar pipeline e bater meta de reuniões agendadas
**Contexto:** Acabou de entrar na empresa, gestor definiu que o time usa esse CRM. Mariana usava HubSpot na empresa anterior.

---

## Journey Map — Visão Geral

| Estágio | Emoção Dominante | Conversão | Pain Point Principal |
|---------|-----------------|-----------|---------------------|
| Awareness | Indiferença 2/5 | 100% → | Não escolheu o produto — decisão do gestor |
| Consideration | Ceticismo 2/5 | 95% → | "Será que é melhor que o que eu usava?" |
| Acquisition | Expectativa 3/5 | 90% → | Processo de signup/invite confuso |
| Onboarding | Frustração 2/5 | 55% → | Não sabe por onde começar, dados não migrados |
| Engagement | Alívio → Rotina 3/5 | 40% → | Features que usa são básicas, resto é confuso |
| Retention | Conformidade 3/5 | 85% → | Não vê valor além do obrigatório |
| Advocacy | Neutralidade 2/5 | 5% | Não recomendaria ativamente |

---

## Estágio 1: Awareness

**Touchpoints:**
- Reunião de equipe onde gestor anuncia o CRM
- E-mail do admin com link de convite
- Menção em onboarding de empresa (handbook)

**Ações do Usuário:**
- Recebe comunicação passivamente
- Pergunta a colegas "como é esse CRM?"
- Busca reviews rápidos no Google

**Pensamentos & Perguntas:**
- "Mais uma ferramenta para aprender..."
- "Será que é parecido com o HubSpot?"
- "Quanto tempo vou perder configurando isso?"

**Emoção:** Indiferença com leve apreensão — Intensidade: 2/5

**Pain Points:**
- Não teve escolha na decisão — motivação intrínseca baixa
- Comunicação do gestor não vende o valor, só comunica obrigação

**Oportunidades:**
- Criar material de "por que este CRM" para gestores compartilharem com time
- E-mail de boas-vindas que foque em "como isso te ajuda a bater meta"

---

## Estágio 2: Consideration

**Touchpoints:**
- Google: pesquisa "[CRM] reviews"
- Conversa com colega que já usa
- Página de features do site

**Ações do Usuário:**
- Lê 2-3 reviews rápidos
- Pergunta ao colega mais experiente: "vale a pena mesmo?"
- Olha screenshots no site para ter noção da interface

**Pensamentos & Perguntas:**
- "Tem integração com meu email e LinkedIn?"
- "Vou conseguir importar meus contatos?"
- "Parece complicado ou simples?"

**Emoção:** Ceticismo cauteloso — Intensidade: 2/5

**Pain Points:**
- Reviews no G2/Capterra mencionam curva de aprendizado
- Não encontra comparação clara com o CRM anterior (HubSpot)

**Oportunidades:**
- Criar página "Migrando do HubSpot" com comparação lado a lado
- Depoimentos de SDRs (não de gestores) que fizeram a transição

---

## Estágio 3: Acquisition

**Touchpoints:**
- E-mail de convite do admin
- Página de signup/accept invite
- Configuração de senha e perfil

**Ações do Usuário:**
- Clica no link de convite
- Cria senha, preenche perfil básico
- Faz primeiro login

**Pensamentos & Perguntas:**
- "Preciso fazer isso agora, meu gestor cobrou"
- "Quanto tempo vai levar essa configuração?"

**Emoção:** Expectativa com pressa — Intensidade: 3/5

**Pain Points:**
- Link de convite expira em 24h — SDRs que não fazem no dia perdem o link
- Formulário de signup pede informações que o admin já tem (redundância)

**Oportunidades:**
- Estender validade do convite para 7 dias
- Pre-fill informações que o admin já cadastrou
- Reduzir signup para 2 cliques (aceitar convite + criar senha)

---

## Estágio 4: Onboarding

**Touchpoints:**
- Primeiro login: home vazia
- Tutorial (se existir)
- Importação de dados
- Configuração de pipeline
- Primeiro deal criado

**Ações do Usuário:**
- Abre o CRM e vê tela vazia — paralisa
- Tenta encontrar onde importar contatos
- Desiste da importação e cria 1-2 contatos manualmente
- Pode ou não criar primeiro deal

**Pensamentos & Perguntas:**
- "O que eu faço primeiro?"
- "Cadê meus contatos? Como importo?"
- "Isso não parece com o HubSpot — onde está o pipeline?"
- "Vou perguntar pro colega amanhã"

**Emoção:** Frustração e confusão — Intensidade: 2/5

**Pain Points:**
- Home vazia sem orientação (paralisia de primeiro uso)
- Importação de dados complexa — CSV com mapeamento manual
- Não existe "quick start" para SDRs (genérico para todos os cargos)
- Time-to-first-value muito longo (>1 dia para sentir que funciona)

**Oportunidades:**
- Checklist de onboarding específico para SDR (5 passos)
- Template de pipeline pré-configurado para SDR
- Importação simplificada (arrastar CSV, mapeamento automático)
- "Start fresh" mode com dados de exemplo para testar antes de importar

---

## Estágio 5: Engagement

**Touchpoints:**
- Uso diário: registrar atividades, mover deals no pipeline
- Integrações: email, calendário, LinkedIn
- Relatórios: ver métricas pessoais
- Mobile: consultar info antes de call

**Ações do Usuário:**
- Registra calls e emails (se integração funcionar)
- Move deals entre estágios do pipeline
- Consulta contatos antes de reuniões
- Usa ~30% das features disponíveis

**Pensamentos & Perguntas:**
- "Funciona para o básico, mas tem muita coisa que não uso"
- "Queria que a integração com email fosse automática"
- "O app mobile é lento demais para usar antes de uma call"

**Emoção:** Rotina com frustrações pontuais — Intensidade: 3/5

**Pain Points:**
- Integração com email requer configuração manual recorrente
- App mobile lento e com features limitadas
- Relatórios prontos não mostram as métricas que o SDR quer (calls/dia, response rate)
- Muitas features para outros perfis (CSM, gestor) poluem a interface

**Oportunidades:**
- View personalizada para SDR (esconder features irrelevantes)
- Dashboard "Meu dia" com métricas de SDR
- Melhorar performance do app mobile
- Automação de registro de email (sync bidirecional)

---

## Estágio 6: Retention

**Touchpoints:**
- Check-in trimestral de CS (com gestor, não com SDR)
- Renovação de contrato (decisão do gestor)
- Novos releases e features
- Comparação com alternativas que colegas mencionam

**Ações do Usuário:**
- Continua usando por obrigação (gestor exige)
- Não explora features novas (não sabe que existem)
- Quando frustra muito, busca workarounds (planilha paralela)

**Pensamentos & Perguntas:**
- "Faz o que preciso, mas poderia ser melhor"
- "Meu colega na outra empresa usa [concorrente] e parece mais fácil"
- "Não sei se tem features novas — ninguém me avisa"

**Emoção:** Conformidade passiva — Intensidade: 3/5

**Pain Points:**
- CS fala com gestor, nunca com end-user (SDR)
- Release notes são técnicas, não mostram valor para SDR
- Não tem canal de feedback acessível para o SDR
- Workarounds em planilha indicam gaps não atendidos

**Oportunidades:**
- Comunicação de features novas dentro do produto (in-app)
- Canal de feedback direto para end-users
- CS touchpoint com end-users, não só gestores
- Identificar e resolver os workarounds em planilha

---

## Estágio 7: Advocacy

**Touchpoints:**
- Conversa informal com colegas de outras empresas
- Reviews em G2/Capterra (se pedido)
- Referral program (se existir)

**Ações do Usuário:**
- Quando perguntam, diz "é ok, faz o trabalho"
- Não escreve reviews proativamente
- Não participa de comunidade do produto

**Pensamentos & Perguntas:**
- "Não amo nem odeio — é ferramenta de trabalho"
- "Se me pedissem review, daria 3/5"
- "Não vou recomendar ativamente, mas também não falo mal"

**Emoção:** Neutralidade — Intensidade: 2/5

**Pain Points:**
- Produto não gera entusiasmo suficiente para advocacy
- Não existe programa de referral ou incentivo
- NPS de SDRs é neutro (passives, não promoters)

**Oportunidades:**
- Criar "power user" features que SDRs amem (gamificação de metas?)
- Programa de referral com benefício tangível
- Comunidade de SDRs (não de admins) para troca de melhores práticas
- Coletar e agir sobre feedback para converter passives em promoters

---

## Momentos Críticos

### Aha Moment
**Quando:** Onboarding — quando o SDR cria o primeiro deal e vê o pipeline visual com o deal nele.
**O que acontece:** "Ah, agora entendi — eu arrasto e vejo meu funil inteiro aqui." Pela primeira vez, o CRM faz sentido como ferramenta de gestão visual do pipeline.
**Indicador:** Criar ≥1 deal + visualizar pipeline view no D1.
**% que atinge:** ~30% dos novos SDRs (correlação: quem atinge tem 3x mais retenção D7)

### Moments of Truth

| # | Estágio | Momento | Decisão | Taxa de Conversão |
|---|---------|---------|---------|-------------------|
| 1 | Onboarding | Primeiro login — tela vazia | Explorar vs. Fechar e "ver depois" | 55% continuam |
| 2 | Onboarding | Tentativa de importar dados | Completar vs. Desistir | 40% completam |
| 3 | Engagement | Primeira semana de uso diário | Adotar como ferramenta principal vs. Usar minimamente | 60% adotam |

### Churn Triggers

| # | Estágio | Trigger | Impacto | Frequência |
|---|---------|---------|---------|------------|
| 1 | Onboarding | Não conseguir importar dados do CRM anterior | Alto | 35% dos novos |
| 2 | Engagement | Integração de email para de funcionar | Médio | 20% dos ativos/mês |
| 3 | Retention | Gestor troca de empresa e novo gestor prefere outro CRM | Alto | 8% ao ano |

---

## Recomendações Priorizadas

| # | Estágio | Recomendação | Impacto | Esforço | Prioridade |
|---|---------|-------------|---------|---------|------------|
| 1 | Onboarding | Checklist interativo de 5 passos para SDR (guiar até Aha Moment) | Alto | Médio | P1 |
| 2 | Onboarding | Importação simplificada (drag-and-drop CSV com mapeamento automático) | Alto | Alto | P1 |
| 3 | Engagement | Dashboard "Meu dia" com métricas de SDR (calls, emails, deals) | Médio | Médio | P2 |
| 4 | Acquisition | Pre-fill signup + estender convite para 7 dias | Médio | Baixo | P2 |
| 5 | Retention | Comunicação in-app de features novas relevantes para SDR | Médio | Baixo | P2 |

**Quick wins (alto impacto + baixo esforço):**
- Estender validade do link de convite de 24h para 7 dias
- E-mail de boas-vindas focado em "como bater sua meta com o CRM"
- Release notes in-app com linguagem de SDR (não técnica)

**Investimentos estratégicos (alto impacto + alto esforço):**
- Onboarding interativo específico por role (SDR, AE, CSM, Gestor)
- Importação inteligente com mapeamento automático de campos
- Redesign mobile com foco em performance e features de SDR
```

---

## Dicas

- **Uma persona por journey map.** A jornada de um SDR é completamente diferente da de um VP de Sales. Se mapear para "o usuário", o mapa não serve para ninguém. Faça mapas separados.
- **Emoções não são achismo.** Baseie em dados: NPS por estágio, verbatims de entrevistas, tickets de suporte categorizados. Se não tem dados, marque como hipótese e valide.
- **O mapa é meio, não fim.** Journey map que vira pôster na parede e ninguém usa é desperdício. O valor está nas recomendações priorizadas e na ação sobre elas.
- **Atualize com frequência.** A jornada muda quando o produto muda. Revise a cada quarter ou após mudanças significativas no produto.
