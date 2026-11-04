# 🧠 Sistema 1 vs. Sistema 2 na Engenharia de IA

Baseado na obra de **Daniel Kahneman** (*Thinking, Fast and Slow* / *Rápido e Devagar*, Prêmio Nobel de Economia), nosso cérebro opera em dois sistemas complementares:

## 1. Os Dois Sistemas de Kahneman

### ⚡ Sistema 1 (Rápido, Intuitivo, Automático)
- Opera sem esforço consciente e em milissegundos.
- Exemplos humanos: detectar hostilidade numa voz, ler uma placa na estrada, completar `"pão com..."`, desviar de um obstáculo.
- **No Software (Jev)**: Classificar intenção, medir urgência (`0.0` a `1.0`), aprovar/bloquear chamada de ferramenta, rotear entre filas, extrair um dado pontual.

### 🐢 Sistema 2 (Devagar, Deliberativo, Analítico)
- Exige atenção, memória de trabalho e alto gasto energético.
- Exemplos humanos: calcular `17 × 24`, preencher declaração de imposto, arquitetar um sistema distribuído.
- **No Software (Claude Opus/Sonnet, GPT-4o, o3)**: Escrever código em múltiplos arquivos, redigir uma resposta empática e personalizada ao aluno, depurar um stack trace complexo.

---

## 2. O Anti-Padrão Moderno: "Tudo no Sistema 2"

Hoje, 90% dos fluxos em **n8n**, **LangChain** e **Agentes de Código** colocam um LLM pesado na porta de entrada:
1. O usuário manda `"Oi, esqueci minha senha"`.
2. O fluxo aciona um AI Agent completo (Sistema 2), carrega memória, lê system prompt gigante e gasta 3 segundos apenas para descobrir que é um caso trivial de autoatendimento.

### A Arquitetura Correta: **Sistema 1 na Porta, Sistema 2 sob Demanda**

```text
[Evento / Mensagem / Tool Call]
       │
       ▼
⚡ JEV (Sistema 1 · ~150ms · $0.00004)
  ├─ Decisão 1 (choice): area -> "acesso_plataforma"
  ├─ Decisão 2 (choice): complexidade -> "simples"
  ├─ Decisão 3 (score):  urgencia -> 0.28
  └─ Decisão 4 (noul):   produto -> "Mastermind Flowgrammers"
       │
       ├──► Simples / Baixa Urgência ──► Haiku / Template Rápido (Barato e Imediato)
       └──► Complexo / Alta Urgência ──► Claude Sonnet/Opus + Alerta Humano (Sistema 2)
```
