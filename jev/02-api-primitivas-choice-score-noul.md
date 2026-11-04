# 🔌 API Reference & As 3 Primitivas (`choice`, `score`, `noul`)

O Jev expõe um único endpoint REST minimalista e ultra-rápido:

```http
POST https://api.typesafe.ai/v1/systemone
Authorization: Bearer ts_live_...
Content-Type: application/json
```

---

## 🧩 As 3 Primitivas Cognitivas

Você envia um `context` (texto ou JSON) e uma lista de `decisions`. Tudo é resolvido **em uma única chamada HTTP**:

### 1. `choice` — Escolha entre Opções Fechadas (Enum)
Força o modelo a escolher **exatamente uma** (ou `k`) opções dentro de `options`. Impossível alucinar uma categoria fora da lista.
```json
{
  "name": "area",
  "type": "choice",
  "prompt": "Qual área do suporte deve atender esta mensagem?",
  "options": ["acesso_plataforma", "duvida_tecnica_n8n", "duvida_claude_code", "financeiro", "comunidade"]
}
```

### 2. `score` — Pontuação Contínua Calibrada (`0.00` a `1.00`)
Retorna um número de ponto flutuante entre `0` e `1` medindo intensidade, probabilidade, risco ou urgência.
```json
{
  "name": "urgencia",
  "type": "score",
  "prompt": "Quão urgente é esta solicitação? Considere bloqueio total de trabalho como 1.0 e curiosidade geral como 0.0."
}
```

### 3. `noul` — Extração Pontual Direta (*Noun / Null*)
Extrai um trecho curto/entidade diretamente do contexto (ex.: nome do produto, e-mail, comando perigoso) ou retorna `null` se não existir.
```json
{
  "name": "ferramenta_mencionada",
  "type": "noul",
  "prompt": "Qual ferramenta específica o aluno mencionou estar dando erro?"
}
```

---

## 📦 Exemplo Completo: Request & Response (Multi-Decisão)

### Request (`curl`)
```bash
curl -X POST https://api.typesafe.ai/v1/systemone \
  -H "Authorization: Bearer $TYPESAFE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "jev-latest",
    "context": "Aluno: Cara, meu webhook do n8n parou de receber eventos do Stripe em produção agora e estamos em pleno lançamento! Preciso destravar urgente.",
    "decisions": [
      {
        "name": "area",
        "type": "choice",
        "prompt": "Qual é o tema principal da mensagem?",
        "options": ["acesso", "n8n_automacao", "claude_code", "financeiro"]
      },
      {
        "name": "complexidade",
        "type": "choice",
        "prompt": "Esta dúvida exige análise profunda de arquitetura/debug ou é simples?",
        "options": ["simples", "complexa"]
      },
      {
        "name": "urgencia",
        "type": "score",
        "prompt": "Nível de urgência operacional de 0 a 1."
      },
      {
        "name": "integracao_afetada",
        "type": "noul",
        "prompt": "Qual serviço externo ou integração foi citado?"
      }
    ]
  }'
```

### Response (`200 OK` em ~140 ms)
```json
{
  "model": "jev-latest",
  "results": {
    "area": "n8n_automacao",
    "complexidade": "complexa",
    "urgencia": 0.94,
    "integracao_afetada": "Stripe"
  },
  "usage": {
    "input_tokens": 118
  }
}
```
