# /ab-test-analysis

## O que essa skill faz

Analisa resultados de A/B tests com rigor estatístico: calcula significância, interpreta resultados, checa guardrail metrics e fornece recomendação clara de ação (ship / investigar / estender / parar).

Saída: **Analysis Summary** com tabela de resultados, interpretação estatística e recomendação.

---

## Quando usar

- Experimento A/B terminou e precisa analisar resultados
- Quer validar se diferença observada é real ou ruído
- Precisa comunicar resultados para stakeholders não-técnicos
- Quer verificar se guardrail metrics foram impactadas
- Teste está rodando e quer fazer interim check (com cuidado)

---

## Input esperado

**Mínimo:**
- **Hipótese**: O que esperava acontecer e por quê
- **Variantes**: Descrição do control e treatment
- **Primary metric**: Qual métrica principal de sucesso
- **Dados**: Tamanho da amostra e conversão por variante
- **Duração**: Quanto tempo o teste rodou

**Opcional:**
- Guardrail metrics e seus valores
- Segmentação (device, geo, user type)
- Baseline histórico da métrica
- MDE (Minimum Detectable Effect) planejado
- Split ratio (se diferente de 50/50)

---

## Processo de análise

### Passo 1 — Entender o experimento

Antes de olhar números, esclarecer:

```
EXPERIMENT OVERVIEW
═══════════════════════════════════════════════════

Hipótese: [O que esperava e por quê]
Control (A): [descrição]
Treatment (B): [descrição]
Primary metric: [nome e definição]
Guardrail metrics: [lista]
Duração: [X dias]
Split: [% control / % treatment]
Trigger: [quem foi incluído no teste]
```

### Passo 2 — Validar setup

Checklist de sanidade antes de confiar nos resultados:

- [ ] **Sample size adequado?** N suficiente para detectar o MDE desejado
- [ ] **Duração cobre ciclos de negócio?** Mínimo 1-2 semanas, incluindo dia útil + fim de semana
- [ ] **Randomização correta?** Distribuição uniforme entre variantes
- [ ] **Sample Ratio Mismatch (SRM)?** Verificar se split real ≈ split planejado
- [ ] **Novelty effect descartado?** Usuários existentes podem reagir à mudança, não à melhoria
- [ ] **Peeking controlado?** Resultados não foram analisados múltiplas vezes sem correção

#### Detectando Sample Ratio Mismatch

```
SRM CHECK
═══════════════════════════════════════════════════

Esperado:  Control = 50% | Treatment = 50%
Observado: Control = [N] ([%]) | Treatment = [N] ([%])

Chi-squared test: p = [valor]
Se p < 0.01 → SRM detectado → RESULTADOS NÃO CONFIÁVEIS
```

**Se SRM detectado**: Parar análise. Investigar bug de implementação.

### Passo 3 — Calcular significância estatística

#### Métricas de conversão (proporções)

```
CÁLCULO ESTATÍSTICO
═══════════════════════════════════════════════════

Control (A):
  N = [tamanho]
  Conversões = [número]
  Taxa = [conversões/N] = [X%]

Treatment (B):
  N = [tamanho]
  Conversões = [número]
  Taxa = [conversões/N] = [Y%]

Lift absoluto: [Y% - X%] = [diff] pontos percentuais
Lift relativo: (Y - X) / X × 100 = [Z%]

Erro padrão (pooled):
  SE = sqrt(p*(1-p)*(1/nA + 1/nB))
  onde p = (conversões_A + conversões_B) / (nA + nB)

z-score: (pB - pA) / SE = [valor]

p-value (two-tailed): [valor]

Intervalo de confiança 95% do lift:
  [(pB - pA) - 1.96*SE, (pB - pA) + 1.96*SE]
  = [[lower]%, [upper]%]
```

#### Métricas contínuas (receita, tempo)
Usar Welch's t-test em vez de z-test. Mesma estrutura: calcular lift, SE, p-value e IC 95%.

### Passo 4 — Avaliar significância

Dois tipos de significância que AMBOS importam:

#### Significância estatística
- p-value < 0.05? (threshold padrão)
- IC 95% não cruza zero?
- Power >= 80%?

#### Significância prática
- O lift é relevante para o negócio?
- Em termos absolutos, quantos [conversões/receita/usuários] a mais?
- O custo de implementação permanente justifica o ganho?

```
EVALUATION
═══════════════════════════════════════════════════

Estatisticamente significante?  [SIM / NÃO]
  p-value: [valor] ([< 0.05 / >= 0.05])
  IC 95%: [[lower]%, [upper]%]

Praticamente significante?      [SIM / NÃO]
  Lift relativo: [Z%]
  Impacto absoluto estimado: [+X conversões/mês] ou [+R$ Y/mês]
  Custo de manter: [estimativa]
```

### Passo 5 — Checar guardrail metrics

Para cada métrica guardrail, verificar se houve degradação:

```
GUARDRAIL CHECK
═══════════════════════════════════════════════════

| Métrica          | Control | Treatment | Diff    | Status |
|------------------|---------|-----------|---------|--------|
| [métrica 1]      | [val]   | [val]     | [diff]  | ✅ OK  |
| [métrica 2]      | [val]   | [val]     | [diff]  | ⚠️     |
| [métrica 3]      | [val]   | [val]     | [diff]  | ❌     |
```

Guardrail metrics comuns:
- **Crash rate / Error rate**: Não pode subir
- **Page load time**: Não pode degradar
- **Revenue per user**: Não pode cair
- **Customer support tickets**: Não pode subir significativamente
- **Outra feature usage**: Canibalização?

### Passo 6 — Interpretar e recomendar

```
DECISION MATRIX
═══════════════════════════════════════════════════

Resultado                              Ação
─────────────────────────────────────────────────
Sig positivo + guardrails OK         → SHIP IT ✅
Sig positivo + guardrail concern     → INVESTIGAR ⚠️
Não sig + tendência positiva         → ESTENDER TESTE 🔄
Não sig + flat                       → PARAR ⏹️
Sig negativo                         → NÃO SHIP ❌
```

**Detalhamento por cenário:**

**SHIP IT**: Lift real, sem danos colaterais. Implementar para 100%.

**INVESTIGAR**: Possível tradeoff. Segmentar por grupo para entender onde guardrail degrada. Considerar rollout parcial.

**ESTENDER TESTE**: Possivelmente underpowered. Calcular quanto mais tempo/amostra é necessário. Se já rodou 2x o planejado, aceitar resultado inconcluso.

**PARAR**: Sem efeito detectável. O tratamento não move a métrica. Aprender e seguir em frente.

**NÃO SHIP**: Tratamento piora a experiência. Documentar aprendizado para futuros testes.

---

## Template de output

```
╔══════════════════════════════════════════════════════════╗
║              A/B TEST ANALYSIS REPORT                    ║
╠══════════════════════════════════════════════════════════╣

📋 EXPERIMENT SUMMARY
Hipótese: [descrição]
Control: [descrição]
Treatment: [descrição]
Duração: [X dias]
Split: [%/%]

✅ SETUP VALIDATION
Sample size: [adequado / insuficiente]
SRM check: [OK / ALERTA]
Duration: [adequada / curta]
Novelty: [descartado / possível]

📊 RESULTADOS

| Métrica        | Control    | Treatment  | Lift     | p-value | Sig?  |
|----------------|------------|------------|----------|---------|-------|
| [primary]      | [val]      | [val]      | [+X%]   | [val]   | [S/N] |
| [guardrail 1]  | [val]      | [val]      | [diff]   | [val]   | -     |
| [guardrail 2]  | [val]      | [val]      | [diff]   | [val]   | -     |

IC 95% do lift primário: [[lower]%, [upper]%]

🛡️ GUARDRAIL STATUS
[✅ / ⚠️ / ❌] [métrica]: [status]

🎯 RECOMENDAÇÃO
[SHIP / INVESTIGAR / ESTENDER / PARAR / NÃO SHIP]

Razão: [explicação em 2-3 frases]

📈 IMPACTO ESTIMADO (se ship)
[+X conversões/mês] | [+R$ Y/mês] | [+Z% na métrica]

📝 PRÓXIMOS PASSOS
1. [ação 1]
2. [ação 2]
3. [ação 3]

💡 APRENDIZADOS
- [insight 1]
- [insight 2]

╚══════════════════════════════════════════════════════════╝
```

---

## Exemplo de uso

**Input:**
> /ab-test-analysis Novo tutorial de onboarding. Control: onboarding atual (3 telas). Treatment: onboarding gamificado (5 telas com progress bar). 1000 usuários em cada grupo, 14 dias. Primary metric: retenção D7. Control: 340/1000 retidos (34%). Treatment: 385/1000 retidos (38.5%). Guardrail: completion rate do onboarding não pode cair abaixo de 70%.

**Output esperado:**
- Lift relativo: +13.2%
- p-value: ~0.035 (significante)
- IC 95%: [+0.3%, +8.7%]
- Guardrail: completion rate control 82%, treatment 75% (OK, acima de 70%)
- Recomendação: SHIP IT — lift significante em retenção D7 sem violação de guardrails

---

## Erros comuns em A/B testing

| Erro | Problema | Solução |
|------|----------|---------|
| **Peeking** | Parar teste quando "parece significante" — inflaciona falsos positivos | Definir duração/sample ANTES. Usar sequential testing para interim checks |
| **Multiple Comparisons** | Testar 10 métricas, declarar vitória na significante | UMA primary metric. Bonferroni correction para secundárias |
| **Underpowered** | Amostra pequena demais para detectar efeito real | Calcular sample size antes com base no MDE |
| **Ignorar Segmentos** | Efeito médio esconde que treatment ajuda A e prejudica B | Segmentar por device, geo, new vs returning |
| **Novelty Effect** | Usuários reagem à mudança, não à melhoria | Segmentar novos vs existentes. Esperar washout (7-14 dias) |

---

## Calculadora rápida de sample size

```
Fórmula simplificada (por grupo):
  n = 16 × p × (1-p) / (MDE_absoluto)²

Exemplo: Baseline = 10%, MDE = 10% relativo (1pp absoluto)
  n = 16 × 0.10 × 0.90 / (0.01)² = 14,400 por grupo
  Duração = 28,800 / [tráfego diário]. Mínimo 7 dias.
```

---

## Referências

- Ron Kohavi — "Trustworthy Online Controlled Experiments"
- Evan Miller — "How Not to Run an A/B Test"
- Georgi Georgiev — "Statistical Methods in Online A/B Testing"

$ARGUMENTS
