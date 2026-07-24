# /pricing

## O que essa skill faz

Gera **estrategia de pricing completa** analisando 7 modelos de pricing, willingness-to-pay, estrutura de tiers, e plano de experimentacao. Baseado nos frameworks de Lenny Rachitsky e Phuryn.

Saida: **Recomendacao de pricing** com modelo escolhido, tiers desenhados, analise competitiva, e plano de testes.

---

## Quando usar

- Lancando produto novo — precisa definir pricing inicial
- Revenue estagnada — pricing pode ser o problema
- Movendo upmarket ou downmarket — pricing precisa acompanhar
- Competitors mudaram pricing — precisa reposicionar
- Revisao semestral de pricing (todo produto deveria fazer)

---

## Input esperado

**Minimo:**
- **Produto**: O que faz, para quem
- **Valor entregue**: Qual ROI o cliente recebe
- **Estagio**: Early (PMF seeking), growth, scale
- **Modelo atual**: Se ja tem pricing, qual e

**Opcional:**
- Dados de competitors (pricing publico)
- Dados de entrevistas sobre willingness-to-pay
- Revenue atual e targets
- Segmentos de cliente com tamanhos
- Custo de servir cada cliente

---

## 7 Modelos de Pricing

### 1. Flat-rate
**Como funciona**: Preco unico, tudo incluido.
**Exemplo**: Basecamp ($99/mo, unlimited users)
**Melhor para**: Produtos simples, mensagem clara, SMB
**Risco**: Deixa dinheiro na mesa em enterprise. Nao escala com valor.

### 2. Per-seat
**Como funciona**: Cobra por usuario ativo.
**Exemplo**: Slack ($8.75/user/mo), Figma ($15/editor/mo)
**Melhor para**: Collaboration tools, produtos que escalam com team size
**Risco**: Incentiva account sharing. Friction em times grandes.

### 3. Usage-based
**Como funciona**: Paga pelo que usa (API calls, storage, compute).
**Exemplo**: AWS, Twilio ($0.0075/SMS), Stripe (2.9% + $0.30)
**Melhor para**: Infra, APIs, produtos com uso variavel
**Risco**: Revenue impredictivel. Cliente pode otimizar para gastar menos.

### 4. Tiered
**Como funciona**: 2-4 planos com features crescentes.
**Exemplo**: Notion (Free/Plus/Business/Enterprise), Zoom (Free/Pro/Business)
**Melhor para**: Maioria dos SaaS. Permite capturar valor de segmentos diferentes.
**Risco**: Tier design errado = canibalização. Feature gating complexo.

### 5. Freemium
**Como funciona**: Produto core gratis, cobra por features premium.
**Exemplo**: Spotify (free com ads / Premium $10.99), Notion, Canva
**Melhor para**: PLG, mercados grandes, viral loop forte
**Risco**: 95%+ nunca converte. Free users custam dinheiro (hosting, support).

### 6. Freemium + Usage
**Como funciona**: Free tier com limite de uso, cobra por excedente.
**Exemplo**: Vercel (free deploys + $20/mo Pro), OpenAI API (free credits + pay-per-token)
**Melhor para**: Developer tools, AI products, plataformas
**Risco**: Complexidade na billing. Users nao entendem quanto vao pagar.

### 7. Value-based
**Como funciona**: Preco baseado no valor/ROI entregue ao cliente.
**Exemplo**: Salesforce (% of pipeline managed), Palantir (custom enterprise pricing)
**Melhor para**: Enterprise, alto ROI mensuravel, sales-led
**Risco**: Requer sales sophistication. Dificil de escalar sem sales team.

---

## Principios de Pricing (Lenny Research)

### 1. Price is a measure of value
Se cliente acha caro, voce nao esta comunicando valor suficiente. Nao baixe preco — aumente percepção de valor.

### 2. Never set it and forget it
Revisar pricing a cada 6-12 meses. Mercado muda, valor muda, custos mudam.

### 3. Self-serve has a ceiling (~$10K ACV)
Acima de $10K/ano, cliente quer falar com humano. Nao force self-serve em enterprise.

### 4. Sample premium in free experience
Deixe o usuario experimentar features premium (com limite). Quem prova, converte mais.

### 5. Prioritize roadmap by WTP
80% da willingness-to-pay vem de 20% das features. Descubra quais e priorize.

### 6. Annual discount = 15-20%
Incentive annual mas nao de mais que 20% off. Senão monthly parece ripoff.

### 7. Anchor pricing works
Mostrar tier enterprise primeiro faz o Pro parecer barato. Use a psicologia a seu favor.

---

## Processo

1. **Entender valor entregue** — Qual ROI o cliente recebe? Quanto economiza/ganha?
2. **Avaliar modelos** — Qual dos 7 modelos faz sentido para seu tipo de produto?
3. **Analisar competicao** — Mapear tiers e precos de 3-5 competitors
4. **Desenhar estrutura** — 2-4 tiers, feature gating, value metric, anchor pricing
5. **Estimar sensibilidade** — Van Westendorp se tiver dados de survey
6. **Planejar experimentos** — A/B test pricing page, founder-led sales conversations
7. **Output** — Recomendacao com modelo, tiers, e plano de testes

---

## Output

```markdown
# Pricing Strategy: [Produto]

## 1. Value Analysis

### Valor entregue ao cliente
- **Problema resolvido**: [O que cliente nao precisa mais fazer]
- **Tempo economizado**: [X horas/semana × $Y/hora = $Z/mes]
- **Revenue gerado**: [Quanto mais o cliente ganha usando produto]
- **Custo evitado**: [O que cliente nao precisa pagar — tools, headcount]
- **ROI estimado**: [Para cada $1 gasto, cliente recebe $X]

### Value metric (unidade de valor)
**[A metrica que melhor representa valor entregue]**
Ex: por usuario, por projeto, por transacao, por GB, por API call

**Teste**: Se cliente dobra uso da value metric, ele recebe ~2x mais valor? Se sim, metrica esta correta.

---

## 2. Modelo Recomendado

### Modelo escolhido: [Nome do modelo]

**Por que esse modelo:**
- [Razao 1 — alinha com como cliente percebe valor]
- [Razao 2 — competitors usam similar, mercado espera]
- [Razao 3 — escala com crescimento do cliente]

**Modelos descartados:**
- [Modelo X]: Descartado porque [razao]
- [Modelo Y]: Descartado porque [razao]

---

## 3. Competitive Landscape

| Competitor | Modelo | Free Tier | Entry Price | Mid Tier | Enterprise | Diferencial |
|-----------|--------|-----------|-------------|----------|------------|-------------|
| [Comp 1] | [Tipo] | [Sim/Nao] | $[X]/mo | $[Y]/mo | $[Z]/mo | [O que inclui] |
| [Comp 2] | [Tipo] | [Sim/Nao] | $[X]/mo | $[Y]/mo | $[Z]/mo | [O que inclui] |
| [Comp 3] | [Tipo] | [Sim/Nao] | $[X]/mo | $[Y]/mo | $[Z]/mo | [O que inclui] |

### Gap analysis
- **Underserved**: [Segmento que nenhum competitor atende bem no pricing]
- **Overpriced**: [Area onde competitors cobram demais]
- **Oportunidade**: [Onde posicionar seu pricing]

---

## 4. Pricing Structure

### Tier Design

#### Free (se freemium)
- **Para quem**: [Early adopters, individual users, experimentacao]
- **Inclui**: [Features basicas, limite de uso]
- **Limite**: [X users, Y projetos, Z storage]
- **Objetivo**: Acquisition funnel — converter X% para paid

#### Starter — $[X]/mo (ou $[Y]/ano — save [Z]%)
- **Para quem**: [Individual professionals, small teams]
- **Value metric**: [Ate X users/projetos/etc]
- **Features**:
  - Tudo do Free +
  - [Feature A — resolve problema principal]
  - [Feature B — diferencial vs free]
  - [Feature C — productivity boost]
- **Anchor**: Equivale a $[X]/dia — "menos que um cafe"

#### Pro — $[X]/mo (ou $[Y]/ano)
- **Para quem**: [Growing teams, mid-market]
- **Value metric**: [Ate X users/projetos/etc]
- **Features**:
  - Tudo do Starter +
  - [Feature D — collaboration/team features]
  - [Feature E — analytics/reporting]
  - [Feature F — integrations]
- **Anchor**: "ROI em [X dias] baseado em [economia de tempo]"

#### Enterprise — Custom pricing
- **Para quem**: [100+ employees, compliance needs]
- **Trigger**: Contact sales quando [X users ou Y need]
- **Features**:
  - Tudo do Pro +
  - [SSO/SAML]
  - [Custom integrations]
  - [Dedicated support]
  - [SLA garantido]
  - [Admin controls avancados]
- **Pricing logic**: [Based on usage + seats + custom needs]

### Feature Gating Matrix

| Feature | Free | Starter | Pro | Enterprise |
|---------|------|---------|-----|------------|
| [Core Feature 1] | ✅ | ✅ | ✅ | ✅ |
| [Core Feature 2] | Limited | ✅ | ✅ | ✅ |
| [Premium Feature 1] | Sample | ✅ | ✅ | ✅ |
| [Team Feature 1] | ❌ | ❌ | ✅ | ✅ |
| [Advanced Feature 1] | ❌ | ❌ | ✅ | ✅ |
| [Enterprise Feature] | ❌ | ❌ | ❌ | ✅ |

### Pricing Psychology
- **Anchor**: Enterprise mostrado primeiro faz Pro parecer acessivel
- **Decoy**: [Se aplicavel — tier que existe para fazer outro parecer melhor]
- **Annual discount**: [X]% off = $[Y] economizado/ano
- **Social proof**: "[Z] empresas ja usam o plano Pro"

---

## 5. Unit Economics

### Revenue model
- **ARPU estimado**: $[X]/mo (blended across tiers)
- **Expected tier distribution**: [X]% Free, [Y]% Starter, [Z]% Pro, [W]% Enterprise
- **MRR target (12 meses)**: $[X]

### Cost to serve
- **Infra per user**: $[X]/mo
- **Support per user**: $[Y]/mo
- **Total cost per user**: $[Z]/mo
- **Gross margin**: [X]%

### Key ratios
- **LTV**: $[X] (based on [Y months] avg retention × $[Z] ARPU)
- **CAC**: $[X] (based on [channel mix])
- **LTV:CAC**: [X]:1 (target > 3:1)
- **Payback period**: [X months]

---

## 6. Price Sensitivity Analysis

### Van Westendorp (se dados disponiveis)
Perguntas para survey:
1. A que preco seria **tao barato** que duvidaria da qualidade?
2. A que preco seria uma **pechincha** (bom negocio)?
3. A que preco comecaria a ficar **caro** (mas ainda consideraria)?
4. A que preco seria **caro demais** (nem consideraria)?

### Sem dados de survey
**Estimativa baseada em:**
- Competitor pricing: $[X] - $[Y] range
- Value delivered: $[Z] ROI → willingness ~10-20% of ROI
- Customer segment ability to pay: [Alto/Medio/Baixo]
- **Recommended range**: $[X] - $[Y]/mo

---

## 7. Experiment Plan

### Teste 1: Pricing page A/B test
- **Variante A**: [Pricing atual ou default]
- **Variante B**: [Pricing alternativo]
- **Metrica**: Conversion rate (visitor → trial → paid)
- **Duration**: [2-4 semanas]
- **Sample**: [X visitors]

### Teste 2: Founder-led sales conversations
- **Objetivo**: Testar willingness-to-pay em conversa real
- **Processo**: Apresentar valor → perguntar "quanto pagaria?" → observar reacao
- **Sample**: [10-20 conversations]
- **Timeline**: [2 semanas]

### Teste 3: Feature gating experiment
- **Objetivo**: Qual feature lock gera mais upgrades?
- **Variante**: [Mover feature X de Free para Paid]
- **Metrica**: Upgrade rate
- **Risk**: Pode irritar free users

---

## 8. Risks e Mitigacoes

| Risk | Impacto | Mitigacao |
|------|---------|----------|
| Preco muito alto → baixa conversao | Alto | A/B test antes de launch |
| Preco muito baixo → deixa dinheiro na mesa | Medio | Revisar em 6 meses com dados |
| Free tier canibaliza paid | Alto | Limitar features estrategicamente |
| Competitor undercuts | Medio | Competir em valor, nao preco |
| Churn por pricing (nao por produto) | Alto | Exit survey perguntando motivo |

---

## Recomendacao Final

### Pricing recomendado
[Resumo de 3-5 linhas com modelo, tiers, e justificativa]

### Proximos passos
1. [Implementar pricing page com tiers recomendados]
2. [Rodar teste 1 em [X semanas]]
3. [Coletar feedback de [Y] clientes]
4. [Revisar pricing em [6 meses]]

### Assumptions criticas
- [Assumption 1 que precisa ser verdade]
- [Assumption 2]
- [Assumption 3]
```

---

## Exemplo

**Input:**
```
/pricing
Produto: CRM para vendas consultivas, mid-market (100-2000 employees)
Valor: Reduz ciclo de venda de 6 meses para 4 meses (33% faster)
Estagio: Growth (200 clientes pagos, $80K MRR)
Modelo atual: Per-seat $50/user/mo, sem free tier
Problema: Revenue estagnou, enterprise quer features mas nao quer pagar por seat
```

**Output:**
```markdown
# Pricing Strategy: Acme CRM

## 1. Value Analysis

### Valor entregue
- Tempo de ciclo de venda: 6 → 4 meses (33% reducao)
- Para deal medio de $100K: 2 meses a mais = 2 deals extras/ano/rep
- Revenue adicional por rep: ~$200K/ano
- ROI: Para cada $600/ano gasto no CRM, rep gera $200K extra = 333x ROI

### Value metric
**Por usuario ativo** (vendedor que usa diariamente)
Teste: Se cliente dobra vendedores, recebe ~2x mais valor? Sim — cada rep acelera seus deals.

---

## 2. Modelo Recomendado: Tiered + Per-seat

**Manter per-seat** (alinha com value metric) mas **adicionar tiers** para capturar enterprise.

Modelos descartados:
- Usage-based: CRM nao tem metrica de uso natural (nao e API)
- Flat-rate: Deixaria muito dinheiro na mesa em enterprise (200+ seats)
- Value-based: Requer sales team sofisticado que nao temos ainda

---

## 3. Competitive Landscape

| Competitor | Free | Entry | Pro | Enterprise |
|-----------|------|-------|-----|------------|
| Salesforce | Nao | $25/user | $80/user | $165/user |
| HubSpot | Sim (2 users) | $20/user | $50/user | $120/user |
| Pipedrive | Nao | $14/user | $49/user | $99/user |
| **Acme (atual)** | **Nao** | **$50/user** | **$50/user** | **$50/user** |

**Gap**: Acme cobra flat $50 para todos. Enterprise paga igual a individual. Estamos deixando $30-115/user na mesa vs Salesforce/HubSpot.

---

## 4. Novo Pricing

### Starter — $35/user/mo ($350/user/ano — save 17%)
- Ate 10 users
- Deal tracking + pipeline basico
- Email sync
- Mobile app

### Professional — $65/user/mo ($650/user/ano)
- Ate 100 users
- Deal war rooms (collaboration)
- Deal health score (AI)
- Advanced analytics
- Integracoes (Slack, Outlook)

### Enterprise — $95/user/mo ($950/user/ano)
- 100+ users
- SSO/SAML
- Custom fields + workflows
- Dedicated CSM
- SLA 99.9%
- API access

**Migracao**: Clientes atuais ($50) vao para Professional ($65) com 6 meses de grace period no preco antigo.

### Impacto estimado
- ARPU sobe de $50 para ~$62 (blended)
- MRR target: $80K → $99K em 6 meses (+24%)
- Enterprise captures: 20 accounts × 50 seats × $95 = +$95K MRR potencial

---

## 7. Experiment Plan

### Teste 1: A/B na pricing page
- A: Pricing atual ($50 flat)
- B: 3 tiers ($35/$65/$95)
- Metrica: Lead-to-trial conversion
- Duration: 4 semanas

### Teste 2: Enterprise conversations
- 10 calls com prospects enterprise
- Apresentar ROI ($200K/rep/ano) → pricing ($95/user)
- Observar reacao e willingness

**Proximo passo**: Implementar pricing page B e rodar teste por 4 semanas.
```

---

## Dicas

- **Preco comunica posicao**: Muito barato = parece amador. Caro demais = friction. Encontre o sweet spot.
- **Revise a cada 6 meses**: Mercado muda, valor muda. Pricing estatico e revenue estagnada.
- **Annual discount max 20%**: Mais que isso e monthly parece rip-off.
- **Free tier so se viral loop forte**: Se nao tem PLG, free users so custam dinheiro.
- **Enterprise = conversa, nao pagina**: Acima de $10K ACV, pricing page nao converte. Precisa de sales.
- **Feature gating e arte**: Lock features demais = frustra. Lock de menos = ninguem converte.
