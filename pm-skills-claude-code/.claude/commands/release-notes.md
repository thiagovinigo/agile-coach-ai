# /release-notes

## O que essa skill faz

Converte tickets técnicos ou PRD em **release notes orientadas a benefício**, focadas no que usuário ganha (não o que foi feito).

Saída: **Release notes** em formato pronto para marketing, in-app, ou blog.

---

## Quando usar

- Feature saiu do dev e precisa comunicar para clientes
- Sprint terminou, need summary para update executivo
- Launch de novo produto/feature grande

---

## Input esperado

**Mínimo:**
- **Tickets/features que shiparam**: Nomes ou descrições
- **Contexto de negócio**: O que resolve para usuário?
- **Público-alvo**: Todos os users ou segmento específico?

**Opcional:**
- Design mockups (para screenshot em blog)
- Metrics esperadas
- Customer quotes

---

## Processo

1. **Extração de benefício** — Por cada feature, qual problema resolve?
2. **Linguagem de usuário** — Nada de "we optimized API", falar em valor
3. **Priorização** — Features mais impactantes primeiro
4. **Call to action** — Se aplicável
5. **Formatting** — Adequado para canal (in-app, email, blog)

---

## Output

```markdown
# Release Notes — [Data/Versão]

## Headline
[1 frase que resume o update — o que mais importa]

---

## What's new

### [Feature 1 Name]
**What's changed**: [Descrição clara do que é novo]

**Why it matters**: [Qual problema resolve ou valor cria]

**What you can do now**: [Como usuário usa — 1-2 sentença]

---

### [Feature 2 Name]
**What's changed**: [...]

**Why it matters**: [...]

**What you can do now**: [...]

---

## Bug fixes
- [Bug 1]: Fixed [o que estava errado]
- [Bug 2]: [...]

---

## Performance
- [Performance improvement]: [Métrica — ex: "Deal loading 50% faster"]

---

## CTA
[Optional] "Try it now → [link]" ou "Learn more → [docs]"

---

## FAQ

**Q: [Common question]**
A: [Answer]

---

## Coming soon
- [Feature que está em progress — set expectations]

---

## Feedback
Have a suggestion? Email us at product@[company].com
```

---

## Exemplo

**Input:**
```
/release-notes
Features que shiparam:
- Guided onboarding tutorial
- Email sync com Salesforce
- Deal health score (beta)

Público: Todos os users
Contexto: Q1 launch, maior update de produto
```

**Output:**
```markdown
# Release Notes — February 2025

## 🚀 We made it easier to get started and stay on top of your deals

---

## What's new

### Guided First Deal Experience
**What's changed**: New users now see an interactive tutorial their first login that walks them through creating their first deal in 5 minutes (vs 30 mins before).

**Why it matters**: We noticed 70% of users who don't create a deal in the first week end up leaving. This guide makes sure you get that first win fast, so you feel confident using Acme.

**What you can do now**: Log in as a new user and follow the 5-step guide. It takes 5 minutes max.

---

### Native Email Sync from Salesforce
**What's changed**: Your Salesforce emails are now automatically synced into each deal. You see the full conversation history without manually copying anything.

**Why it matters**: Most of your deal conversation happens in email. Before, you'd have to manually paste emails into Acme or switch between apps. Now, everything's in one place.

**What you can do now**:
1. Connect your Salesforce account (Settings → Integrations)
2. Acme will sync your last 90 days of emails automatically
3. See all deal conversation in the deal context

---

### Deal Health Score (Beta)
**What's changed**: We now predict whether each deal is "Stalled", "On Track", or "Winning" based on real signals (email activity, # of stakeholders, deal velocity).

**Why it matters**: Salesforce pipeline is often fiction. Reps over-optimistically mark deals as "closing next week" but nothing happens. Our deal health is based on actual signals, so you know which deals are real.

**What you can do now**: Look at each deal and see the health badge. If it says "Stalled", there's usually a reason (you haven't talked to them in 2 weeks). Click for recommendations.

---

## Bug fixes
- Fixed: Email syncing would sometimes stop unexpectedly (now auto-resumes)
- Fixed: Deal name with special characters would display incorrectly
- Fixed: Mobile keyboard would overlap with deal input field

---

## Performance
- Deal loading is **50% faster** (avg 2s → 1s)
- Email sync is **3x faster** (now batches syncs intelligently)
- API calls reduced by 40% (fewer database hits)

---

## What's coming next
We're working on:
- Custom fields (Enterprise customers, March)
- AI-powered sales coaching (analyzes lost deals, recommends improvements)
- Slack integration (get deal alerts in Slack)

---

## How to get help
- [View our help center](link)
- [Watch tutorial video](link)
- Email us: support@acme.com

---

## Feedback
What do you think of these changes? We'd love to hear:
- What's working great?
- What's confusing?
- What's missing?

Reply to this email or use in-app feedback widget.

---

## FAQ

**Q: Will my existing Salesforce history sync?**
A: We sync your last 90 days on first connection. If you want older emails, email support and we can do a full historical import.

**Q: What if I don't use Salesforce?**
A: Email sync works with any email provider via manual integration. We're working on Gmail and Outlook native sync next month.

**Q: Is Deal Health Score always right?**
A: It's ~80% accurate in our internal testing. It gets smarter the more data you add (more stakeholders, more emails = better prediction).

**Q: When do I get custom fields?**
A: March 1st for early-access customers. General availability April 1st.
```

---

## Exemplo 2 (Internal/Tighter Version)

**Input:**
```
/release-notes
Tipo: Internal release notes para team
Features: Bug fixes + performance improvements, minor features
Tom: Quick, técnico mas acessível
```

**Output:**
```markdown
# v2.5.0 Release Notes — Internal

## Summary
- ✅ 50% faster deal loading
- ✅ Email sync stability improvements
- ✅ 3 bug fixes
- 🟡 2 known issues (addressed in v2.6)

---

## Features
1. **Email batch syncing** (Beta) — Reduces API calls by 40%
2. **Deal deep links** — Share specific deal with ?deal=id

## Fixes
- Email sync no longer stops on auth error (now retries)
- Deal names with emoji render correctly
- Mobile keyboard z-index issue fixed

## Performance
| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Deal load | 2000ms | 1000ms | 50% ↓ |
| List load | 500ms | 250ms | 50% ↓ |
| API calls/session | 450 | 270 | 40% ↓ |

## Known issues
- Custom fields show placeholder text (will fix in v2.6)
- Email search is slow for > 1000 emails (optimizing)

## Migration notes
- Auth flow changed slightly for email sync (see migration guide)
- No data migration needed

## Testing checklist
- [ ] Deal creation flow
- [ ] Email sync (Salesforce + Gmail)
- [ ] Mobile responsiveness
- [ ] Performance tests on staging

---

**QA Lead**: [Name]
**Timeline**: Deploy Monday Jan 15
**Rollout**: 10% → 50% → 100% over 3 days
```

---

## Dicas

- **Benefício vs Feature**: "Fixed bug" é feature. "Your deals load 3x faster" é benefício.
- **Lingua do usuário**: Evite jargão técnico. Se disse "optimized database queries", vire em "things are faster".
- **Prioridade**: Features com maior impacto primeiro. Bug fixes em seção separate.
- **Headlines importam**: 80% de users só leem headline. Make it count.
- **CTA é subtil**: "Try it now" é weak. "See what's possible → [video]" é melhor.
