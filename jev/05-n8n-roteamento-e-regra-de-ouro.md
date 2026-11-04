# ⚙️ Jev no n8n + A Regra de Ouro

No **n8n**, o Jev entra como um nó **HTTP Request** ultra-leve logo após o seu **Webhook** ou **Trigger** (WhatsApp / Evolution API / Telegram / HubSpot / Typeform).

---

## 🏗️ Arquitetura dos 2 Workflows Oficiais da Aula

### 1. `flowgrammers-jev-triagem-alunos.json` — Triagem Inteligente (Sistema 1 + Sistema 2)
1. **Webhook (`POST /triagem-aluno`)**: Recebe `nome`, `email`, `turma` e `mensagem` do aluno.
2. **Jev · Sistema 1 (`HTTP Request`)**: Em **uma única chamada** de ~150ms avalia:
   - `area` (`choice`): `acesso_plataforma`, `duvida_tecnica_n8n`, `duvida_claude_code`, `financeiro`, `comunidade`
   - `complexidade` (`choice`): `simples` vs `complexa`
   - `sentimento` (`choice`): `positivo`, `neutro`, `frustrado`, `urgente`
   - `urgencia` (`score`): `0.00` a `1.00`
   - `ferramenta` (`noul`): ferramenta citada na mensagem
3. **Switch Inteligente**:
   - **Rota Simples**: Envia para **Claude 3.5 Haiku** (resposta rápida, objetiva e barata).
   - **Rota Complexa**: Envia para **Claude Sonnet/Opus** (análise técnica profunda passo a passo).
4. **Alerta de Urgência (`If urgencia >= 0.75`)**: Dispara alerta prioritário para o time humano da comunidade quando o aluno está travado em produção.

### 2. `flowgrammers-jev-benchmark.json` — Benchmark Prático de Latência
- Dispara cenários reais contra `https://api.typesafe.ai/v1/systemone`, mede o tempo exato em milissegundos (`latency_ms`), calcula o custo em frações de centavo (`US$ 0.042 / 1M input tokens`) e consolida o relatório comparativo Sistema 1 vs Sistema 2.

---

## ⚖️ A Regra de Ouro: Quando Usar vs. Quando NÃO Usar o Jev

| ✅ USE O JEV (Sistema 1) QUANDO... | ❌ NÃO USE O JEV (Use Sistema 2) QUANDO... |
| :--- | :--- |
| A resposta é uma **escolha entre opções fixas** (`choice`) | Você precisa **redigir um texto, e-mail ou código** |
| Você precisa de um **score numérico calibrado de 0 a 1** (`score`) | A decisão exige **raciocínio matemático/lógico em múltiplas etapas** |
| Você quer **extrair um termo curto** do texto (`noul`) | Você precisa **explicar o porquê** detalhadamente para o cliente |
| Latência de **< 300ms** é crítica (voz, guardrails, hooks, roteamento) | A tarefa é criativa, aberta ou conversacional |
| Você quer avaliar **5 a 10 classificações diferentes de uma só vez** | O contexto exige leitura profunda de dezenas de páginas com síntese |
