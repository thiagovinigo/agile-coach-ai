# 🧮 As Contas, Score de Priorização e Matriz Impacto × Esforço

Toda a credibilidade do discovery perante sponsors e C-Levels reside na **consistência matemática** das fórmulas.

---

## 1. Horas e Custo do Processo (Inventário)
```text
horas_por_mes = volume_por_mes × minutos_por_execucao ÷ 60
custo_mensal  = horas_por_mes × custo_hora
```
> **Por que o cálculo usa o caso padrão e não as exceções?**  
> Para manter o cálculo **conservador e inquestionável**. Se considerássemos os 20 minutos das exceções, o número pareceria inflado. A exceção serve para justificar o desenho técnico (fila de exceção) e entra na coluna de "Outros Ganhos".

---

## 2. Capacidade Liberada e Ganho da Oportunidade
```text
horas_liberadas_mes = horas_do_processo × %_automatizavel
ganho_mensal_reais  = custo_mensal_do_processo × %_automatizavel
ganho_anual_reais   = ganho_mensal_reais × 12
```
> **Vocabulário de Ouro:** Diga sempre **"Capacidade Liberada"**, e nunca *"Economia"* ou *"Corte de Pessoas"*. O ganho representa horas devolvidas aos especialistas para focar em tarefas de alto valor que hoje estão abandonadas por falta de tempo.

---

## 3. Score de Priorização (Escala de 1 a 5)
O score pondera quatro dimensões fundamentais. Repare que **Esforço** e **Risco** entram invertidos (`6 − nota`), pois menos esforço e menos risco aumentam a prioridade:

```text
Score = (Impacto × 0,40) + (Prontidão × 0,20) + ((6 − Esforço) × 0,25) + ((6 − Risco) × 0,15)
```

### Exemplo de Cálculo (Oportunidade O-01):
- **Impacto:** 5 (muito alto) → `5 × 0,40 = 2,00`
- **Prontidão dos Dados:** 5 (estruturado via XML/API) → `5 × 0,20 = 1,00`
- **Esforço:** 2 (1 a 2 semanas) → `(6 − 2) × 0,25 = 1,00`
- **Risco:** 2 (erro tolerável/revisável) → `(6 − 2) × 0,15 = 0,60`
- **Score Final:** `2,00 + 1,00 + 1,00 + 0,60 = 4,60` (Ranking #1 de 33 oportunidades!)

---

## 4. Matriz Impacto × Esforço (4 Quadrantes)

| Quadrante | Critério | Ação Recomendada |
| :--- | :--- | :--- |
| **🚀 Quick Win** | Impacto ≥ 4 e Esforço ≤ 2 | **Faça primeiro**, na Onda 1 (0 a 30 dias). Gera valor visível rápido e conquista os sponsors. |
| **🏛️ Projeto Estratégico** | Impacto ≥ 4 e Esforço ≥ 3 | Alto valor, mas exige integração mais pesada. Planeje para 31 a 90 dias com patrocínio dedicado. |
| **📈 Melhoria Incremental** | Impacto ≤ 3 e Esforço ≤ 2 | Encaixe quando houver capacidade ociosa do time de desenvolvimento. |
| **📦 Rever / Backlog** | Impacto ≤ 3 e Esforço ≥ 3 | Alto esforço para pouco retorno. Só reavaliar com mudança de contexto ou dados novos. |
