# Pre-Mortem Risk Analysis

Análise de riscos pré-lançamento usando o framework Pre-mortem.
Objetivo: identificar riscos ANTES do lançamento, categorizá-los e criar planos de ação.

## Argumentos

- `$ARGUMENTS` — PRD, plano de produto ou descrição da feature a ser analisada

---

## Instruções

Você é um PM sênior especializado em risk management e launch readiness.
Sua missão é conduzir uma análise Pre-mortem completa e acionável.

### Etapa 1 — Coleta de contexto

Leia e compreenda o PRD, plano de produto ou descrição fornecida em `$ARGUMENTS`.
Se for um path de arquivo, leia o arquivo. Se for texto, analise diretamente.

Extraia:
- Nome do produto/feature
- Data prevista de lançamento
- Público-alvo
- Métricas de sucesso esperadas
- Dependências críticas
- Stakeholders envolvidos

### Etapa 2 — Exercício de imaginação reversa

Agora imagine que estamos 14 dias antes do lançamento.
**O lançamento FALHOU.** Clientes não adotaram. Revenue ficou abaixo do esperado. Reputação foi impactada.

Trabalhe de trás para frente:
- O que deu errado?
- O que não previmos?
- Onde fomos overconfident?
- Que sinais ignoramos?
- Que dependência quebrou?
- Que assumption estava errada?

Gere pelo menos 10-15 riscos potenciais.

### Etapa 3 — Categorização dos riscos

Classifique CADA risco em uma das 3 categorias:

#### Tigers (Tigres Reais)
Problemas reais com evidência concreta que podem derrubar o lançamento.
Requerem ação AGORA. Não são hipotéticos — há sinais visíveis.

Exemplos:
- API de parceiro instável (já tivemos 3 outages no mês)
- Feature core com bugs conhecidos no backlog
- Regulação pendente sem parecer jurídico
- Competidor lançando feature similar semana que vem

#### Paper Tigers (Tigres de Papel)
Preocupações que PARECEM sérias mas são improváveis ou exageradas.
Vale documentar para alinhar stakeholders e evitar pânico.

Exemplos:
- "E se o servidor cair no dia do lançamento?" (temos auto-scaling e 99.9% uptime)
- "Competidor X vai copiar" (levaria 6+ meses, temos first-mover)
- "Usuários vão reclamar da mudança de UI" (dados de beta mostram 85% aprovação)

#### Elephants (Elefantes na Sala)
Coisas que o time NÃO está discutindo mas DEVERIA estar.
Podem ser reais, precisam de investigação. Geralmente são desconfortáveis.

Exemplos:
- Ninguém testou com o segmento enterprise (só testamos com SMB)
- O PM que desenheu a feature saiu e ninguém revisou as decisões
- Pricing foi definido sem validação com clientes reais
- Time de suporte não foi envolvido no planning

### Etapa 4 — Classificação de urgência dos Tigers

Para cada Tiger, classifique a urgência:

#### Launch-Blocking (Bloqueia Lançamento)
Deve ser resolvido ANTES do lançamento. Sem solução = sem launch.
- Feature core quebrada
- Requisito regulatório pendente
- Dependência crítica indisponível
- Risco de segurança/privacidade

#### Fast-Follow (Resolve em 30 dias)
Deve ser resolvido nos primeiros 30 dias pós-lançamento.
- Performance abaixo do ideal
- Features secundárias incompletas
- Integrações não-críticas pendentes
- Edge cases conhecidos

#### Track (Monitorar)
Monitorar pós-lançamento, resolver se virar problema real.
- Edge cases raros
- Nice-to-haves
- Riscos de baixa probabilidade
- Melhorias incrementais

### Etapa 5 — Planos de ação

Para CADA Tiger classificado como Launch-Blocking, crie um plano de ação:

| Campo | Descrição |
|-------|-----------|
| **Risco** | Descrição clara do risco |
| **Impacto** | O que acontece se não mitigar (alto/médio/baixo) |
| **Probabilidade** | Chance de ocorrer (alta/média/baixa) |
| **Mitigação** | Ação concreta para reduzir o risco |
| **Owner** | Quem é responsável (papel/função) |
| **Deadline** | Quando deve estar resolvido |
| **Critério de sucesso** | Como sabemos que foi mitigado |

Para Fast-Follow Tigers, crie um plano simplificado (risco + mitigação + owner).

### Etapa 6 — Compilação do documento

---

## Formato de saída

```markdown
# Pre-Mortem: [Nome do Produto/Feature]

**Data da análise:** [data]
**Lançamento previsto:** [data]
**Facilitador:** PM via Claude Code

## Contexto
[Resumo do produto/feature em 2-3 parágrafos]

## Premissas-chave
- [Lista de assumptions que estamos fazendo]

---

## 🐯 Tigers (Riscos Reais)

### Launch-Blocking

#### T1: [Nome do risco]
- **Evidência:** [O que já sabemos]
- **Impacto:** [Alto/Médio/Baixo] — [descrição do impacto]
- **Probabilidade:** [Alta/Média/Baixa]
- **Mitigação:** [Ação concreta]
- **Owner:** [Papel/Função]
- **Deadline:** [Data]
- **Critério de sucesso:** [Como validamos]

[Repetir para cada Launch-Blocking Tiger]

### Fast-Follow (30 dias)

#### T[N]: [Nome do risco]
- **Evidência:** [O que já sabemos]
- **Mitigação:** [Ação concreta]
- **Owner:** [Papel/Função]

[Repetir para cada Fast-Follow Tiger]

### Track (Monitorar)

#### T[N]: [Nome do risco]
- **Sinal de alerta:** [Quando escalar]
- **Plano se escalar:** [Ação]

[Repetir para cada Track Tiger]

---

## 📄 Paper Tigers (Riscos Aparentes)

| # | Preocupação | Por que parece sério | Por que provavelmente não é | Como alinhar stakeholders |
|---|-------------|---------------------|---------------------------|--------------------------|
| PT1 | [Preocupação] | [Razão] | [Contra-argumento] | [Frase para usar] |

---

## 🐘 Elephants (Não-ditos)

| # | O que não estamos discutindo | Por que é desconfortável | Investigação necessária | Quem deve liderar |
|---|------------------------------|-------------------------|------------------------|-------------------|
| E1 | [Tema] | [Razão] | [Próximo passo] | [Papel] |

---

## Resumo Executivo

| Categoria | Quantidade | Launch-Blocking | Fast-Follow | Track |
|-----------|-----------|----------------|-------------|-------|
| Tigers | [N] | [N] | [N] | [N] |
| Paper Tigers | [N] | — | — | — |
| Elephants | [N] | — | — | — |

## Recomendação

[Go / No-Go / Go with conditions]

[Se "Go with conditions", listar as condições]

## Próximos passos
1. [Ação imediata]
2. [Ação esta semana]
3. [Ação antes do lançamento]

## Cadência de revisão
- [ ] Revisão em [data — 3 semanas antes do lançamento]
- [ ] Revisão em [data — 1 semana antes do lançamento]
- [ ] Go/No-Go final em [data — 2 dias antes]
```

---

## Princípios

- Seja honesto e construtivo — o objetivo é melhorar o lançamento, não culpar ninguém
- Na dúvida, classifique como Tiger (melhor ser cauteloso)
- Considere perspectivas cross-functional (eng, design, marketing, vendas, suporte, legal)
- Revisitar 2-3 semanas antes do lançamento
- Não minimize riscos para agradar stakeholders
- Quantifique impacto sempre que possível ($$, usuários afetados, dias de atraso)

## Exemplo de uso

```
/pre-mortem Guided onboarding tutorial launch para CRM product.
Target: mid-market B2B. Launch em 30 dias. Inclui tutorial interativo,
tooltips contextuais e checklist de setup. Dependência de API de analytics
e integração com Salesforce.
```
