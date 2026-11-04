# 🌐 Browser Agent: `browser-use/jev-ultrafast`

Um dos casos mais impressionantes demonstrados pela TypeSafe + Browser Use é o uso do Jev como navegador autônomo (**`browser-use/jev-ultrafast`**).

---

## 📊 Benchmark Oficial: Navegação Web Autônoma

Quando um agente de navegador tradicional (baseado em LLM Sistema 2) navega numa página DOM com centenas de elementos interativos, ele gasta segundos "pensando em voz alta" sobre qual botão clicar.

Com o **Jev (`jev-ultrafast`)**, cada passo de navegação é tratado como uma decisão Sistema 1 direta sobre os elementos visíveis da árvore DOM:

| Métrica | Agente LLM Tradicional (Sistema 2) | `browser-use/jev-ultrafast` (Sistema 1) | Ganho Real |
| :--- | :--- | :--- | :--- |
| **Velocidade Global** | 1,0x (Baseline) | **2,9x mais rápido** | Redução drástica de espera |
| **Média de Passos por Tarefa** | 12,8 passos | **4,4 passos** | **-65% de passos redundantes** |
| **Custo Médio por Tarefa** | US$ 0,045 – US$ 0,120 | **US$ 0,007 por tarefa** | **Até 15x mais barato** |

---

## 💡 Por que funciona tão bem no Browser?
Navegar em uma interface gráfica é, em 95% do tempo, **reconhecimento imediato de padrão (Sistema 1)**:
1. *"Qual destes 40 elementos é o botão de Login?"* → `choice`
2. *"A página já terminou de carregar os resultados?"* → `choice` (`sim` / `não`)
3. *"Qual a confiança de que chegamos na tela final do checkout?"* → `score` (`0.0` .. `1.0`)
