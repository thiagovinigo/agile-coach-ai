# 🔍 Exemplo Prático: Ficha P-01 (Conferência de XML)

Veja como uma ficha real preenchida se comporta na prática e como os dados alimentam a linha do inventário:

---

## Ficha P-01: Conferência de XML da NF-e de entrada x pedido
- **Área:** Fiscal
- **Nome do Processo:** Conferência de XML da NF-e de entrada x pedido
- **Gatilho:** XML chega por e-mail ou pelo portal da SEFAZ
- **Etapas:** Analista abre o pedido no ERP e compara item, quantidade, preço e impostos
- **Entrega Final:** Nota liberada para recebimento ou bloqueada com divergência
- **Dono:** Analista fiscal sênior
- **Frequência:** Diária
- **Volume por mês:** `9.000`
- **Minutos por execução (padrão):** `4`
- **Pessoas envolvidas:** `6`
- **% de Exceções:** `18%` (divergência de preço, imposto ou item não cadastrado)
- **Minutos na Exceção:** `20` minutos
- **Sistemas Usados:** ERP, portal da SEFAZ, e-mail
- **Entrada:** XML da NF-e e pedido no ERP (Dado estruturado: `Sim`)
- **Regras Documentadas:** `Parcial`
- **Gargalo/Espera:** Aprovação do comprador na divergência leva de 2 a 3 dias
- **Impacto do Erro:** Divergência paga sem contestação; caminhão parado na doca
- **Dor Principal (frase literal):** *"Metade do dia é conferir nota que está certa."*
- **Sazonalidade:** Páscoa, Natal e fechamento do mês
- **Custo-Hora Específico:** `R$ 55,00`
- **Candidato a:** `Automação n8n`

---

## 🧮 Contas Resultantes no Inventário:
- **Horas por Mês:** `9.000 × 4 ÷ 60 = 600 horas/mês`
- **Custo Mensal:** `600 horas × R$ 55,00 = R$ 33.000,00/mês`
- **Teste de Sanidade:** `600 horas ÷ 6 pessoas = 100 horas/pessoa/mês` (~57% da jornada de 176h). Número perfeitamente plausível e defensável diante da diretoria!
