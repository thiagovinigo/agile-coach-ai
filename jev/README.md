# ⚡ Jev — A IA que Decide (TypeSafe System One)

> **Mastermind Flowgrammers · Aula Completa (Ric Neves)**  
> **Sistema 1 para Software — De Daniel Kahneman ao Claude Code e ao n8n**

---

## 🎯 O Problema: Usar Canhão para Matar Mosca

Na arquitetura tradicional de agentes e automações, usamos **LLMs generativos (Sistema 2)** — como Claude 4.5 Sonnet/Opus ou GPT-4o — para **absolutamente tudo**:
- Decidir se uma mensagem é urgente ou comum (`sim` / `não`)
- Escolher para qual fila encaminhar um ticket (`suporte`, `financeiro`, `comercial`)
- Avaliar se um comando `Bash` do Claude Code é seguro (`allow`, `ask`, `deny`)
- Pontuar o risco de churn ou a qualidade de um lead (`0.00` a `1.00`)

Cada uma dessas micro-decisões custa **1.500 a 4.000 ms** de latência e consome tokens de geração, quando o que você realmente precisava era apenas **uma decisão estruturada instantânea**.

---

## 🧠 A Solução: Jev (`jev-latest` · TypeSafe AI)

Inspirado em *Rápido e Devagar* (Daniel Kahneman), o **Jev** é o primeiro modelo comercial desenhado exclusivamente como **Sistema 1 para Software**:
- **Não gera texto livre (zero chat, zero prosa)**: Ele apenas **decide** (`choice`), **pontua** (`score`) ou **extrai** (`noul`).
- **Latência Ultrabaixa**: **70 ms a 500 ms** por requisição (mesmo avaliando múltiplas decisões em paralelo no mesmo payload).
- **Custo Irkrisório**: **US$ 0,042 por 1 milhão de tokens de entrada** (~23 mil palavras por 1 centavo de dólar) e **US$ 0,00 por saída (output grátis!)**.
- **Determinismo Estruturado**: Retorna sempre JSON tipado com as chaves exatas que você definiu no array `decisions`.

| Dimensão | Sistema 1 (Jev · `jev-latest`) | Sistema 2 (Claude / GPT / Gemini) |
| :--- | :--- | :--- |
| **Papel Cognitivo** | Triagem rápida, classificação, score, guardrails | Raciocínio profundo, código, redação, síntese |
| **Latência Típica** | **70 ms – 500 ms** | 1.500 ms – 15.000 ms |
| **Formato de Saída** | `choice` (enum), `score` (0..1), `noul` (span) | Texto livre, Markdown, Tool Calls complexas |
| **Custo de Output** | **Grátis (US$ 0,00)** | US$ 2,50 a US$ 75,00 / 1M tokens |
| **Custo de Input** | **US$ 0,042 / 1M tokens** | US$ 0,80 a US$ 15,00 / 1M tokens |
