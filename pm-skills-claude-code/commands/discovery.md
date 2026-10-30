# /discovery

## O que essa skill faz

Estrutura um ciclo completo de discovery transformando um problema vago em hipóteses testáveis e um plano de experimentos.

Saída: **Síntese de descoberta** com framing, hipóteses validadas, e próximos passos.

---

## Quando usar

- Problema está mal definido ou você tem múltiplas hipóteses
- Precisa validar antes de investir em PRD/spec
- Vai rodar experimentos e precisa de estrutura

---

## Input esperado

**Mínimo:**
- **Problema**: Descrição do problema conforme entendido hoje
- **Contexto**: Tamanho do mercado, usuários afetados, ou constraints
- **Restrições**: Tempo, budget, dependências técnicas

**Opcional:**
- Dados existentes (churn, NPS, feedback)
- Competitors ou proxies
- Personas em mente

---

## Processo

1. **Framing** — Reescreve o problema em linguagem de JTBD (Jobs to Be Done)
2. **Hipóteses** — Gera 3-5 hipóteses sobre raiz do problema (não soluções)
3. **Validação** — Estrutura como testar cada hipótese (experimento, tamanho, tempo)
4. **Roadmap de experimentos** — Sequencia dos testes em 2-4 semanas
5. **Critério de sucesso** — Que resultado muda a decisão de produtos

---

## Output

```markdown
# Síntese de Discovery: [Problema]

## Framing (JTBD)
"Quando [contexto], eu quero [job], para que [outcome]"

## Hipóteses a validar
1. **Hipótese A** [texto]
   - Risco: [alto/médio/baixo]
   - Tamanho do impacto: [$X, Y users, Z% churn]

2. **Hipótese B** [texto]
   - Risco: [...]
   - Tamanho do impacto: [...]

3. **Hipótese C** [texto]
   - Risco: [...]
   - Tamanho do impacto: [...]

## Plano de experimentos (2-4 semanas)

### Semana 1
- **Experimento**: [método] com [amostra]
- **Hipótese testada**: Hipótese A
- **Critério de sucesso**: [métrica] > [threshold]
- **Esforço**: [1-3 dias PM]

### Semana 2
- **Experimento**: [método] com [amostra]
- **Hipótese testada**: Hipótese B
- **Critério de sucesso**: [métrica] > [threshold]
- **Esforço**: [1-3 dias PM]

## Próximos passos
1. Validar hipótese A com [experimento]
2. Se confirmado, design de solução
3. Se refutado, voltar para hipótese C

## Timeline
- Semana 1-2: Experimentos
- Semana 3: Análise e decisão
- Semana 4: Start de PRD ou pivot
```

---

## Exemplo

**Input:**
```
/discovery
Problema: Atrito em onboarding de novos usuários (35% churn em 7 dias)
Contexto: Produto B2B SaaS, 50 clientes, 2000 usuários
Restrições: Preciso decidir em 2 semanas se faz PRD ou não
```

**Output:**
```markdown
# Síntese de Discovery: Churn em Onboarding

## Framing (JTBD)
"Quando um usuário novo entra no produto, ele quer entender como fazer seu primeiro job com sucesso, para que sinta valor rapidamente e não cancele."

## Hipóteses a validar

1. **Falta de guia estruturado** (Setup desorganizado pede para navegar sozinho)
   - Risco: Médio
   - Impacto: 35% churn = 700 usuários/ano

2. **Integração com sistema legado é frição** (Primeira coisa é hard: conectar com Salesforce)
   - Risco: Alto (teste com 10 clientes = semanas)
   - Impacto: Se verdade, 15-20% da churn

3. **Onboarding email não convida para ação** (Deixam de voltar após primeiro login)
   - Risco: Baixo
   - Impacto: Se verdade, 5-10% da churn

## Plano de experimentos

### Semana 1: Entrevistas + Observação
- **Experimento**: Entrevistar 5 usuários que não voltaram + 5 que ficaram
- **Hipótese testada**: 1 e 3
- **Critério**: Roteiro claro de por que saíram
- **Esforço**: 3 horas PM, 2 horas eng (session replay)

### Semana 2: Teste A/B de email
- **Experimento**: Novo email com CTA clara vs controle
- **Hipótese testada**: 3
- **Critério**: 5% improvement na abertura + 3% improvement em volta ao produto
- **Esforço**: 4 horas eng, 2 horas PM

### Semana 2: Deep dive em integrações
- **Experimento**: Rastrear tempo até primeira integração bem-sucedida nos últimos 20 clientes
- **Hipótese testada**: 2
- **Critério**: Integração leva > 30min (se sim, é problema)
- **Esforço**: 1 hora PM

## Próximos passos
1. Week 1: Fazer entrevistas e observar sessions
2. Week 2: Rodar email A/B + medir integração
3. Week 3: Consolidar dados e decidir
4. If hipótese 1 ou 3 confirmada → /prd para solução
5. If hipótese 2 confirmada → trabalhar com tech lead em plano de simplificação

## Timeline
- Week 1-2: Experimentos rodam em paralelo
- Week 3: Sync com stakeholders com dados em mão
- Week 4: Start de especificação (se hipótese validada)
```

---

## Dicas

- **Não confunda problema com solução**: "Precisa de tutorial" é solução. "Não entende como começar" é problema.
- **Risco alto = teste rápido primeiro**: Se integração é problema, não faça entrevista. Query seu DB.
- **Criterio de sucesso deve ser observável**: "Usuários ficam happy" é fraco. "NPS > 7" ou "churn < 20%" é forte.
