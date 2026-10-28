# O roteiro

O roteiro é o que o criador lê na câmera. Ele é escrito para a boca, não para o olho: frase curta,
palavra que se fala, número que se diz em voz alta. E ele é escrito já sabendo que depois vai virar
corte na Fábrica, com painel e legenda, então cada frase importante tem um objeto para o painel
mostrar.

---

## 1. O tamanho

O tamanho sai da velocidade de fala medida, não de chute. Nos reels já gravados que serviram de base, a leitura
fica perto de **3,7 palavras por segundo**. Meça de novo antes de cada lote, porque o número muda:

```
flow-reels tendencias/medir_fala
```

| duração alvo | palavras, a 3,7 por segundo |
|---|---|
| 40 s | cerca de 150 |
| 45 s | cerca de 165 |
| 50 s | cerca de 185 |

O padrão é **40 a 50 segundos**. Roteiro acima de 185 palavras vira corte arrastado, e abaixo de 140
não cabe o formato inteiro.

## 2. O formato

Cinco blocos, nesta ordem. É o formato dos reels que já foram ao ar e funcionaram.

| bloco | tempo | o que faz | regra |
|---|---|---|---|
| **1. gancho** | 0 a 4 s | nomeia a coisa concreta e abre a tensão | até 15 palavras. O nome da ferramenta, ou o do problema, é dito aqui. Nunca "isso aqui", "olha só", "gente" |
| **2. o que é** | 4 a 10 s | uma frase que diz o que a ferramenta faz | quem nunca ouviu falar entende de primeira |
| **3. as provas** | 10 a 35 s | três fatos concretos, um por frase ou par de frases | cada fato tem número ou ação visível, e cada um vira um beat do painel |
| **4. a virada** | 35 a 42 s | por que isso importa para quem assiste | uma frase. Economiza, substitui, destrava |
| **5. a chamada** | últimos 4 a 6 s | "comenta PALAVRA que eu te mando o link na DM" | a palavra é única e ainda não foi usada (seção 4) |

O gancho é o bloco que decide tudo. Os que já funcionaram no perfil:

- "O ElevenLabs cobra. Essa aqui é de graça e clona sua voz com 3 segundos de áudio."
- "Aqui vão cinco plugins que você precisa ter se programa com Claude Code ou Codex."
- "Se você está cansado de conteúdo que parece escrito por IA, existe uma ferramenta gratuita que resolve isso."
- "O Google acabou de lançar um agente de marketing totalmente gratuito."

O que eles têm em comum: **a coisa concreta nomeada**, **um contraste ou uma dor** (paga contra
grátis, cansado de, precisa ter) e **nenhum aquecimento**. Ninguém começa com "fala, pessoal".

## 3. Regras de escrita

- **Uma ideia por frase.** Se a frase tem "e" ligando duas coisas, provavelmente são duas frases.
- **Número falado como se fala.** "Três segundos", "quinhentos idiomas", "sessenta horas". Na
  grafia da legenda ele vira algarismo sozinho.
- **Nome próprio escrito como se lê, com a grafia oficial ao lado.** No roteiro vai "Claude Code";
  na seção de grafia, "Claude Code (não Cloud Code)". É essa lista que depois corrige a legenda.
- **Nada que dependa de ver a tela para entender.** "Olha aqui em cima" só entra quando o painel
  tem mesmo aquela coisa para mostrar, e a frase tem que fazer sentido de olhos fechados.
- **Nada de travessão, "além disso", "vale ressaltar", "no mundo de hoje".** Público de nicho
  reconhece texto de IA de longe, e quem é referência não pode soar assim.
- **Primeira pessoa só com experiência real.** "Eu testei e..." só entra se o criador testou. Quando a
  frase pede um teste que ainda não foi feito, marque `[TESTAR ANTES DE GRAVAR]` ao lado dela.
- **Todo fato tem fonte.** Cada número e cada afirmação sobre o que a ferramenta faz aponta, na seção
  de fontes, para o link oficial onde ele foi conferido. Fato sem fonte sai do roteiro.

## 4. A palavra da chamada

- Uma palavra só, curta, em maiúscula, fácil de digitar no celular: VOZ, CODING, MARKETING.
- **Não pode repetir** uma palavra já usada. Antes de escolher, junte as que existem:

```
grep -rhoE "[Cc]omenta[m]? [A-ZÁÉÍÓÚÇ0-9-]{2,}" projetos/*/materiais-de-trabalho/publicacao/ projetos/*/ROTEIRO.md 2>/dev/null | sort -u
```

  A palavra fica reservada para sempre na automação de DM (a lei está no `funil-dm.md` do
  `/flow-reels:publicar`), então reusar é mandar o link errado para quem comentou.
- Ela tem a ver com o assunto, para a pessoa lembrar qual comentar: VOZ para clonagem de voz, e não
  LINK.

## 5. O arquivo `ROTEIRO.md`

Vive na raiz da pasta da pauta, à vista, porque é o que o criador abre para gravar.

```markdown
# <título curto da pauta>

**Duração alvo:** 45 s · **palavras:** 163 · **ângulo:** alternativa grátis a algo pago
**Chamada:** comenta VOZ

## Para ler na câmera

O ElevenLabs cobra. Essa aqui é de graça e clona sua voz com três segundos de áudio.

A ferramenta se chama OmniVoice. Você manda alguns segundos de qualquer voz e ela copia o tom, o
ritmo e a emoção.

...

Comenta VOZ que eu te mando o link na DM.

## Grafia para a legenda

- OmniVoice (não Omni Voice)
- ElevenLabs (não U11 Labs)
- Claude Code (não Cloud Code)

## Fontes de cada fato

| fato | fonte oficial |
|---|---|
| clona com 3 segundos de áudio | https://... |
| quase 500 idiomas | https://... |

## Antes de gravar

- [TESTAR ANTES DE GRAVAR] rodar a instalação uma vez, para poder dizer "eu testei"
- abrir o link oficial e conferir se continua grátis
```

O texto de "Para ler na câmera" é **só o que é falado**, sem marcação, sem colchete, sem instrução de
cena no meio. Instrução de gravação vai no `KIT.md`, não no roteiro.
