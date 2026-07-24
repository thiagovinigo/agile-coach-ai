# Launch Checklist

Checklist cross-functional de pré-lançamento de produto/feature.
Combina rigor operacional com estratégia de go-to-market.
Fontes: product-on-purpose launch-checklist + Lenny Rachitsky launch-marketing.

## Argumentos

- `$ARGUMENTS` — Descrição da feature/produto, data de lançamento, tier e contexto

---

## Instruções

Você é um PM sênior com experiência em lançamentos de produto B2B/B2C.
Sua missão é criar um checklist completo e acionável para o lançamento.

### Etapa 1 — Definição do contexto de lançamento

Analise `$ARGUMENTS` e extraia/defina:

- **O quê:** Nome da feature/produto
- **Quando:** Data de lançamento (soft launch + hard launch)
- **Tier do lançamento:**
  - **Tier 1:** Major launch (novo produto, rebranding, mudança de pricing)
  - **Tier 2:** Significant feature (integração importante, novo módulo)
  - **Tier 3:** Minor feature (melhoria incremental, bug fix relevante)
- **Stakeholders:** Quem precisa estar envolvido
- **Audiência:** Quem será impactado pelo lançamento

### Etapa 2 — Checklist por função

Construa o checklist completo cobrindo TODAS as áreas abaixo.
Adapte profundidade ao Tier do lançamento.

### Etapa 3 — Princípios de Lenny Rachitsky

Aplique estes princípios ao plano de marketing/comunicação:

1. **Separe soft launch de hard launch**
   - Soft launch: release silencioso para grupo limitado (beta users, power users)
   - Hard launch: anúncio público com fanfarra completa
   - Gap mínimo de 1-2 semanas entre os dois

2. **Encontre o "sizzle" feature**
   - Qual é a feature visualmente impressionante e compartilhável?
   - Que momento gera o "wow" que as pessoas querem mostrar para outros?
   - Otimize comunicação em torno desse momento

3. **Lightning strikes, not peanut butter**
   - Concentre esforços em poucos canais de alto impacto
   - Não espalhe esforço igualmente em tudo (peanut butter)
   - Identifique 2-3 canais onde sua audiência realmente está

4. **PR prep 6 semanas antes**
   - Comece outreach para jornalistas/influencers 6 semanas antes
   - Exclusivos geram melhor cobertura que press releases genéricos
   - Prepare assets visuais (screenshots, vídeos, GIFs)

5. **Distribua em círculos concêntricos**
   - Círculo 1: Time interno (2-3 semanas antes)
   - Círculo 2: Investidores e advisors (1-2 semanas antes)
   - Círculo 3: Power users e beta testers (1 semana antes)
   - Círculo 4: Público geral (dia do lançamento)

### Etapa 4 — Go/No-Go e rollback

Defina critérios claros para decisão de lançamento e plano de rollback.

---

## Formato de saída

```markdown
# Launch Checklist: [Nome do Produto/Feature]

**Data de lançamento:** [data]
**Tier:** [1/2/3]
**PM responsável:** [nome/papel]
**Go/No-Go decision:** [data] por [quem]

---

## Contexto do lançamento
[2-3 parágrafos descrevendo o que está sendo lançado, para quem, e por quê]

## Timeline de lançamento

| Marco | Data | Status |
|-------|------|--------|
| Feature freeze | [data] | [ ] |
| QA completo | [data] | [ ] |
| Soft launch (beta) | [data] | [ ] |
| Go/No-Go meeting | [data] | [ ] |
| Hard launch | [data] | [ ] |
| Post-launch review | [data + 2 semanas] | [ ] |

---

## 1. Engineering

### Feature & Quality
- [ ] Feature completa conforme spec/PRD
- [ ] Code review aprovado por [N] engenheiros
- [ ] Testes unitários cobrindo [N]% dos cenários
- [ ] Testes de integração passando
- [ ] Testes end-to-end nos fluxos críticos
- [ ] QA manual nos cenários principais
- [ ] Edge cases documentados e testados
- [ ] Performance dentro dos SLAs ([latência], [throughput])

### Infraestrutura & Monitoramento
- [ ] Load testing realizado (capacidade para [N]x tráfego normal)
- [ ] Monitoring/alertas configurados (latência, erros, throughput)
- [ ] Dashboards de health check criados
- [ ] Logs estruturados para debugging
- [ ] Feature flag configurada para rollout gradual
- [ ] Rollback plan documentado e testado
- [ ] Database migrations reversíveis
- [ ] CDN/cache configurado

### Segurança
- [ ] Security review completo
- [ ] Penetration testing (se aplicável)
- [ ] Dados sensíveis criptografados
- [ ] Rate limiting configurado
- [ ] CORS/CSP configurados

---

## 2. Design & UX

- [ ] UX review final aprovado
- [ ] Design responsivo testado (mobile, tablet, desktop)
- [ ] Accessibility review (WCAG 2.1 AA mínimo)
- [ ] Empty states desenhados
- [ ] Error states desenhados
- [ ] Loading states desenhados
- [ ] Onboarding/first-time experience revisado
- [ ] Micro-copy revisado (tooltips, labels, mensagens de erro)
- [ ] Dark mode (se aplicável)
- [ ] Internationalization (se aplicável)

---

## 3. Marketing & Comunicação

### O "Sizzle"
- **Feature destaque:** [Qual é o momento "wow"?]
- **Visual:** [Screenshot/GIF/vídeo que captura o sizzle]
- **One-liner:** [Frase que resume o valor em 1 linha]

### Conteúdo
- [ ] Blog post escrito e revisado
- [ ] Landing page atualizada/criada
- [ ] Changelog/release notes publicados
- [ ] Help center/documentação atualizada
- [ ] Vídeo demo gravado ([duração])
- [ ] Screenshots/GIFs para social media

### Distribuição (Lightning Strikes)
- **Canal principal:** [canal] — [ação específica]
- **Canal secundário:** [canal] — [ação específica]
- **Canal terciário:** [canal] — [ação específica]

### Círculos concêntricos de distribuição
| Círculo | Audiência | Quando | Canal | Status |
|---------|-----------|--------|-------|--------|
| 1 | Time interno | T-3 semanas | Slack/All-hands | [ ] |
| 2 | Investidores/Advisors | T-2 semanas | Email pessoal | [ ] |
| 3 | Power users/Beta | T-1 semana | In-app + email | [ ] |
| 4 | Público geral | Dia D | Blog + social + email | [ ] |

### PR & Imprensa (Tier 1 apenas)
- [ ] Press release escrito (T-6 semanas)
- [ ] Lista de jornalistas/influencers mapeada
- [ ] Exclusivo oferecido a [publicação]
- [ ] Press kit com assets visuais preparado
- [ ] Embargo date comunicada
- [ ] Founder/CEO disponível para entrevistas

### Email
- [ ] Email de anúncio redigido e revisado
- [ ] Segmentação de lista definida
- [ ] A/B test de subject line configurado
- [ ] Scheduled para [data/hora]
- [ ] Unsubscribe e compliance verificados

### Social Media
- [ ] Posts agendados (LinkedIn, Twitter/X, [outros])
- [ ] Hashtags definidas
- [ ] Equipe interna avisada para amplificar
- [ ] Assets visuais adaptados por plataforma

---

## 4. Sales & Revenue

- [ ] Talking points documentados
- [ ] Demo atualizada com nova feature
- [ ] Battlecard atualizado (se competitivo)
- [ ] Pricing confirmado e configurado no sistema
- [ ] CRM atualizado (campos, stages, automações)
- [ ] Sales team treinado (sessão em [data])
- [ ] Quota/target ajustados (se aplicável)
- [ ] Proposal/contract templates atualizados

---

## 5. Customer Support

- [ ] FAQ escrito ([N] perguntas cobertas)
- [ ] Time de suporte treinado (sessão em [data])
- [ ] Escalation path documentado
- [ ] Known issues documentados com workarounds
- [ ] Chatbot/help widget atualizado
- [ ] SLA de resposta definido para período de lançamento
- [ ] War room schedule definido (primeiras 48h)
- [ ] Templates de resposta para cenários comuns

---

## 6. Legal & Compliance

- [ ] Privacy impact assessment (se dados pessoais)
- [ ] Terms of Service atualizados (se necessário)
- [ ] Privacy Policy atualizada (se necessário)
- [ ] Cookie consent atualizado (se necessário)
- [ ] Regulatory check completo (LGPD, GDPR, SOC2, etc.)
- [ ] Contratos de terceiros revisados
- [ ] IP/trademark check (nome da feature)

---

## 7. Operations & Analytics

### Analytics
- [ ] Eventos de tracking definidos e implementados
- [ ] Funil de conversão mapeado
- [ ] Dashboard de métricas de lançamento criado
- [ ] Baseline metrics documentadas (antes do lançamento)
- [ ] Success metrics definidas com targets

### Métricas de sucesso

| Métrica | Baseline | Target (7d) | Target (30d) | Target (90d) |
|---------|----------|-------------|--------------|--------------|
| [Adoção] | [N] | [N] | [N] | [N] |
| [Engajamento] | [N] | [N] | [N] | [N] |
| [Retenção] | [N] | [N] | [N] | [N] |
| [Revenue impact] | [N] | [N] | [N] | [N] |

### Operacional
- [ ] Alertas de anomalia configurados
- [ ] On-call schedule para lançamento definido
- [ ] Capacity planning revisado
- [ ] Third-party dependencies verificadas (status pages, SLAs)

---

## 8. Go/No-Go Criteria

### Condições obrigatórias para Go
- [ ] Todos os itens Launch-Blocking da seção Engineering completos
- [ ] QA sign-off obtido
- [ ] Design sign-off obtido
- [ ] Legal sign-off obtido
- [ ] [Adicionar critérios específicos]

### Quem decide
- **Go/No-Go owner:** [Nome/Papel]
- **Consulted:** [Lista de pessoas]
- **Meeting:** [Data, hora, local]

### Rollback triggers
Se qualquer condição abaixo ocorrer nas primeiras 24h:
- Error rate > [N]%
- Latência p95 > [N]ms
- [N]+ tickets de suporte sobre o mesmo issue
- Revenue impact negativo > [N]%
- [Adicionar triggers específicos]

### Plano de rollback
1. **Trigger identificado** → PM notifica eng lead
2. **Eng lead confirma** → Feature flag desligada em [N] minutos
3. **Rollback executado** → Comunicação para suporte e stakeholders
4. **Post-mortem** → Agendado em 24h após rollback
5. **Re-launch plan** → Definido em 48h após rollback

---

## Cadência de check-ins

- [ ] T-4 semanas: Kick-off de lançamento (all stakeholders)
- [ ] T-3 semanas: Engineering check-in
- [ ] T-2 semanas: Marketing + Sales readiness
- [ ] T-1 semana: Full team check-in + soft launch
- [ ] T-2 dias: Go/No-Go meeting
- [ ] Dia D: War room ativo
- [ ] D+1: Quick debrief
- [ ] D+7: Métricas review
- [ ] D+14: Post-launch review completo
```

---

## Notas

- Adapte a profundidade ao Tier: Tier 3 não precisa de PR e press
- Items marcados "(se aplicável)" podem ser removidos conforme contexto
- Adicione items específicos do seu produto/indústria
- O checklist é um ponto de partida — customize para sua realidade
- Compartilhe com stakeholders cedo para alinhar expectativas

## Exemplo de uso

```
/launch-checklist Feature de integração Email + Salesforce para CRM B2B.
Tier 2. Lançamento em 6 semanas. Impacta times de vendas mid-market.
Inclui sync bidirecional de contatos, log automático de emails e
templates compartilhados. Dependência da API Salesforce REST.
```
