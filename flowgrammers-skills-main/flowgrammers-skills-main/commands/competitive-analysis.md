# /competitive-analysis

## O que essa skill faz

Mapeia strengths e weaknesses de competitors, identifica gaps de diferenciação e recomenda posicionamento próprio.

Saída: **Matriz competitiva** com feature comparison, análise SWOT, e recomendações de diferenciação.

---

## Quando usar

- Preparando PRD ou estratégia e precisa entender mercado
- Escolhendo entre features: qual os competitors têm?
- Posicionando produto: onde está brecha no mercado?
- Levantando barra para roadmap: o que é baseline vs inovação?

---

## Input esperado

**Mínimo:**
- **Competitors**: Lista de 3-5 players diretos ou indiretos
- **Seu produto**: O que você quer ser (ex: "a melhor CRM para PMEs")
- **Contexto**: Segmento de cliente, tipo de uso

**Opcional:**
- Pricing de competitors
- Feedback de clientes sobre alternativas
- Market share ou dados públicos
- Features que você quer entregar

---

## Processo

1. **Feature matrix** — Lista features core, compara quem tem, qualidade (1-5 stars)
2. **Análise SWOT própria** — Strengths reais vs competitors, weaknesses, oportunidades
3. **Positioning** — Onde você vence? Onde você perde?
4. **Gaps** — Que features ninguém tem bem feito?
5. **Recomendações** — Features prioritárias para diferenciação

---

## Output

```markdown
# Análise Competitiva: [Seu Produto]

## Competitors mapeados
- [Competitor A]: [Posicionamento], ${pricing}
- [Competitor B]: [Posicionamento], ${pricing}
- [Competitor C]: [Posicionamento], ${pricing}

## Feature Matrix

| Feature | [Seu Produto] | [Comp A] | [Comp B] | [Comp C] | Status |
|---------|-------------|----------|----------|----------|--------|
| **Core Features** | | | | | |
| [Feature 1] | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | Paridade |
| [Feature 2] | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐ | Behind |
| [Feature 3] | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐ | Liderança |
| **Nice-to-haves** | | | | | |
| [Feature 4] | ❌ | ✅ | ❌ | ✅ | Gap |
| [Feature 5] | ✅ | ✅ | ✅ | ✅ | Tabela |

## Análise SWOT (seu produto)

### Strengths (vs competitors)
1. **[Strength 1]** — Ninguém faz melhor
   - Exemplo: [Feature detalhada]
   - Diferenciação: [Por que importa para cliente]

2. **[Strength 2]** — Você está à frente
   - Exemplo: [...]
   - Diferenciação: [...]

3. **[Strength 3]** — Facilidades únicas
   - Exemplo: [...]
   - Diferenciação: [...]

### Weaknesses (vs competitors)
1. **[Weakness 1]** — Competitor X é melhor
   - Benchmark: Ele faz [feature]
   - Impacto: [X% de clientes mencionam como razão para deixar]

2. **[Weakness 2]** — Alguém domina esse espaço
   - Benchmark: [...]
   - Impacto: [...]

### Opportunities
1. **[Oportunidade 1]** — Gap no mercado que ninguém preenche bem
   - Evidência: Entrevista com clientes mencionou [problema]
   - Competitors: Ninguém tem solução boa para [X]

2. **[Oportunidade 2]** — Seu strength pode se expandir
   - Exemplo: Você é bom em [Y], pode estender para [Z]

### Threats
1. **[Threat 1]** — Competitor X está se movendo para sua feature
   - Sinal: [Recente hire, acquisition, roadmap rumor]
   - Tempo: [Estimado em quantos meses]

2. **[Threat 2]** — Novo entrant pode bater você
   - Por quê: [Startup bem fundada, grande tech company]
   - Janela: [X meses até ser competição real]

## Posicionamento recomendado

### Seu nicho
**[Seu Produto] é para [Segmento] que precisa [job], diferente de [Competitors] porque [diferenciação única].**

Exemplo de frase: "Acme é o único CRM específico para PMEs com integração nativa com WhatsApp e foco em performance em conexões lentas."

### Segmentos onde você vence
- [Segmento A]: Por causa de [Strength 1] e [Strength 2]
- [Segmento B]: Por causa de [Oportunidade 1]

### Segmentos onde você perde
- [Segmento C]: Competitor X é muito melhor em [Feature], que é critical aqui
- [Segmento D]: Pricing ou feature table não bate

## Features prioritárias para diferenciação

### Curto prazo (próximas 2-4 semanas)
1. **[Feature de catch-up]** — Fechar gap em [Weakness 1]
   - Por quê: Baseline obrigatória, clientes esperam
   - Tempo: [Estimado]
   - ROI: [X% de churn reduction se fechado]

2. **[Quick differentiator]** — Pequena feature que aproveita [Strength 1]
   - Por quê: Diferenciar sem muito investimento
   - Tempo: [Estimado]

### Médio prazo (próximos 2-3 meses)
1. **[Feature de diferenciação]** — Explorar [Oportunidade 1] que ninguém faz
   - Por quê: Criar novo valor único
   - Tempo: [Estimado]
   - Impacto: [Novo segmento, +X% market share]

2. **[Consolidação]** — Evoluir seu [Strength 2] de bom para imbatível
   - Por quê: Aprofundar vantagem competitiva
   - Impacto: [X% customer love, referrals]

## Conclusão

### Recomendação de estratégia
1. Fechar [Weakness 1] em [timeline curta] para ser tabela em feature
2. Acelerar [Oportunidade 1] para criar diferenciação clara
3. Monitorar [Threat 1] — estar pronto se competitor se mover

### Próximos passos
- Criar /prd para [Feature de diferenciação]
- Validar com clientes se [Oportunidade 1] é real (via entrevista)
- Monitorar roadmap de [Competitor X]
```

---

## Exemplo

**Input:**
```
/competitive-analysis

Competitors: HubSpot, Pipedrive, Salesforce
Seu produto: CRM focado em vendas consultivas (deals complexos, sales cycles longos)
Contexto: Segmento Fortune 500 e mid-market

Features que importam: Deal tracking, collaboration, API, integração com email
```

**Output:**
```markdown
# Análise Competitiva: Consultive CRM

## Competitors mapeados
- **HubSpot**: All-in-one marketing + sales, freemium, $50/user/month
- **Pipedrive**: Sales-focused, visual deal pipeline, $14/user/month
- **Salesforce**: Enterprise standard, $165/user/month, highly customizable

## Feature Matrix

| Feature | Seu CRM | HubSpot | Pipedrive | Salesforce | Status |
|---------|---------|---------|-----------|-----------|--------|
| **Core** | | | | | |
| Deal tracking | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Liderança |
| Team collaboration | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | Liderança |
| Email integration | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Behind |
| Custom fields | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | Paridade |
| API | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Paridade |
| **Nice-to-haves** | | | | | |
| AI-powered insights | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | Behind |
| Workflow automation | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Behind |

## SWOT

### Strengths
1. **Deal collaboration** — Seu produto é 50% mais rápido para time alignment em deals complexos
   - Feature: Real-time collaboration, deal war rooms, quick comments
   - Diferenciação: Vendedores Fortune 500 passam 40% tempo em alignment — seu produto reduz isso

2. **Deal transparency** — Visual intuitivo de deal progression (não é linear como pipeline)
   - Feature: Deal health score, deal history timeline, stakeholder tracking
   - Diferenciação: Deals complexos têm múltiplas conversas paralelas — você mostra tudo em um lugar

3. **Onboarding + training** — Vendedores conseguem produtivo em 2 dias
   - Feature: Guided workflows, templates pré-built, video tutorials
   - Diferenciação: Salesforce leva 4+ semanas para usuário novo ser independente

### Weaknesses
1. **Email integration** — Pipedrive e HubSpot sincronizam melhor (mais histórico automático)
   - Benchmark: HubSpot puxa todo o histórico de email automaticamente
   - Impacto: 15% dos prospects mencionam como razão para não escolher você

2. **AI insights** — HubSpot tem AI para prever churn, HubSpot está à frente aqui
   - Benchmark: HubSpot diz qual deal vai fechar com 80% accuracy
   - Impacto: Médio — apenas 5% mencionaram como blocker

3. **Ecosystem** — Salesforce tem 1000+ integrações, você tem 30
   - Benchmark: Clientes precisam integração customizada com sistemas internos
   - Impacto: ~10% das deals não viram por falta de integração específica

### Opportunities
1. **Consultive selling framework** — Ninguém ensina metodologia
   - Evidência: Entrevista com 10 sales leaders: 9/10 reclamaram que CRM não ajuda em consultive process
   - Gap: Você poderia ter templates e workflows específicos para MEDDIC, Sandler, etc

2. **Sales coaching** — Integrar feedback de deals fechados com coaching de vendedores
   - Evidência: VP Sales entrevistado: "Quando um deal não fecha, ninguém aprende"
   - Gap: Seu CRM poderia capturar razão de perda e recomendar coaching por pessoa

### Threats
1. **HubSpot moving up-market** — HubSpot lançou features enterprise nos últimos 6 meses
   - Sinal: HubSpot contratou VP Sales para Fortune 500, lançou custom objects
   - Janela: ~12 meses até ser real competição em seu segmento

2. **Salesforce GenAI** — Salesforce está investindo pesado em Einstein (AI)
   - Sinal: Lançou 5+ features de AI em últimos 6 meses
   - Janela: ~9 meses até ser significativo

## Posicionamento recomendado

**Seu CRM é o único construído do zero para deals consultivos complexos — com collaboration nativa, visualização de deal progression, e templates de metodologia de venda.**

### Segmentos onde você vence
- **Enterprise B2B (Fortune 500)**: Deal cycles 6-18 meses, múltiplos stakeholders, collab crítica
  - Seu Strength 1 + 2 matam aqui
- **Mid-market com sales consultivo**: Salesforce é overkill, Pipedrive é fraco em collab
  - Seu Strength 3 (onboarding rápido) + Strength 2

### Segmentos onde você perde
- **SMB transacional**: Pipedrive é mais barato e simples
- **Marketing-first orgs**: HubSpot vence por integração marketing
- **Highly customized orgs**: Salesforce vence por flexibilidade

## Features prioritárias para diferenciação

### Próximas 4 semanas
1. **Melhorar email sync** — Fechar gap em [Weakness 1]
   - Por quê: Baseline esperada, blocker para alguns clientes
   - Esforço: 2-3 semanas eng
   - ROI: ~5% melhoria em conversão

2. **Sales methodology templates** — Explorar [Oportunidade 1]
   - Por quê: Ninguém oferece + cria lock-in
   - Esforço: 1 semana product design, 2 semanas eng
   - ROI: "Wow factor" diferenciador

### Próximos 2-3 meses
1. **Deal coaching engine** — Explorar [Oportunidade 2], criar novo valor
   - Por quê: Preencher gap que ninguém vê ainda
   - Esforço: 4-6 semanas (requer ML/data)
   - Impacto: Novo segmento de uso, maior land value

2. **Aprofundar collaboration** — Defender [Strength 1] contra HubSpot
   - Por quê: HubSpot virá aqui em 12 meses, ficar à frente agora
   - Features: Integração Slack, deal war rooms, stakeholder notifications
   - Impacto: Make switching expensive

## Conclusão e próximos passos

1. **Curto prazo**: Melhorar email sync + lançar methodology templates (diferenciar)
2. **Médio prazo**: Investir em deal coaching AI (cria novo valor único)
3. **Monitorar**: HubSpot enterprise roadmap, Salesforce Einstein features
4. **Validar**: Entrevistar 5 clientes Fortune 500 sobre deal coaching — interesse?
```

---

## Dicas

- **Não assuma**: Se não sabe feature de competitor, pesquisa. Não invente.
- **Qualidade importa**: 4⭐ de seu produto é melhor que 5⭐ de competitor se tem real usage advantage.
- **Positioning antes de features**: Decida onde você vence ANTES de construir roadmap.
- **Monitorar threats**: Revise essa análise a cada quarter — mercado muda rápido.
