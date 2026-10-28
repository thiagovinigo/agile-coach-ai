---
name: transcrever
description: 'Traz o vídeo para dentro do projeto e transcreve palavra a palavra, com tempo. Aceita arquivo local, link do YouTube e link ou MCP do Google Drive. Escolhe entre a nuvem (Replicate, rápida, cobra por minuto) e a máquina do usuário (WhisperX local, gratuita e lenta), respeitando a rota já escolhida no setup.json. Entrega palavras.json, transcricao.md e audio16k.wav, que é o material que o `/flow-reels:planejar` e a legenda consomem. Use para ''transcrever esse vídeo'', ''pega o áudio dessa aula'', ''quero cortes desse link'', ''baixa esse vídeo do YouTube''. Não escolhe gancho nem corta nada.'
---

# Transcrever (/flow-reels:transcrever)

> **Onde mora cada coisa.** Esta skill está em `${CLAUDE_SKILL_DIR}` e o plugin Flow Reels em
> `${CLAUDE_PLUGIN_ROOT}`. Caminhos como `referencias/...` e `scripts/...` são desta skill;
> `skills/...` e `componentes/...` são do plugin (o que a pessoa baixou fica em `componentes/` da pasta
> de trabalho e vale por cima); `projetos/`, `marca/`, `pautas/`, `setup.json` e `.env` são da pasta de
> trabalho, o diretório onde o Claude Code está aberto. Todo script roda com `flow-reels <skill>/<script>`,
> que está no PATH enquanto o plugin está ligado e já usa o Python e o ffmpeg certos
> (`flow-reels lista` mostra todos; `flow-reels instalar` prepara uma pasta nova).

A base de tudo. Nenhuma outra etapa funciona sem o que sai daqui: o planejador escolhe o gancho
lendo a transcrição e corta por palavra, e a legenda queima os mesmos tempos na tela. Transcrição
torta vira corte com fala amputada, então esta skill prefere parar e avisar a entregar coisa errada.

A rota da nuvem cobra poucos centavos por vídeo. **Não peça confirmação e não estime custo**:
quem configurou a chave já escolheu essa rota, e parar o fluxo para perguntar atrapalha mais do
que protege. Diga que está transcrevendo e transcreva.

## O que esta skill entrega

Três arquivos, sempre os mesmos, sempre nos mesmos lugares dentro da pasta do vídeo:

| arquivo | onde cai | o que é | quem consome |
|---|---|---|---|
| `transcricao.md` | `projetos/<nome>/` | legível, uma frase por linha com marca de tempo | você, e o planejador na hora de varrer |
| `palavras.json` | `projetos/<nome>/materiais-de-trabalho/transcricao/` | cada palavra com início, fim e texto | `/flow-reels:planejar`, gerador de legenda |
| `audio16k.wav` | `projetos/<nome>/materiais-de-trabalho/transcricao/` | áudio mono em 16 kHz | validação de ponto de corte pela energia |

Só o `transcricao.md` fica à vista, porque é o único dos três que uma pessoa abre para ler. Os
outros dois são dado de máquina, e por isso moram no material de trabalho. A árvore inteira está em
`${CLAUDE_PLUGIN_ROOT}/skills/fabrica/referencias/PASTA-DO-VIDEO.md`.

Se algum dos três faltar, a etapa não terminou. O `audio16k.wav` é o mais esquecido e o mais
importante na hora do corte: é nele que se confere se o corte cai no silêncio ou no meio da palavra.

## Onde escrever

Tudo dentro de `projetos/<nome-do-video>/`, que é o diretório do projeto. Se ele ainda não existe,
crie usando um nome curto e descritivo do vídeo, em minúsculas e com hífen no lugar do espaço.

**Você não precisa montar esses caminhos na mão.** Os scripts recebem `--projeto
projetos/<nome-do-video>` e cada um sabe onde escrever: o `baixar.py` põe o arquivo em
`materiais-de-trabalho/fonte/`, e o `normalizar.py` põe o `transcricao.md` na raiz e os outros dois
em `materiais-de-trabalho/transcricao/`.

## Passo 1: descobrir o que chegou

| chegou | o que fazer |
|---|---|
| caminho de arquivo local | confira que existe e siga para o passo 2. Copie o arquivo para `projetos/<nome>/materiais-de-trabalho/fonte/` se ele ainda não estiver lá |
| link do YouTube | `flow-reels transcrever/baixar --url <link> --projeto projetos/<nome>` |
| link do Google Drive | mesmo comando. Funciona com arquivo que está com link aberto |
| Google Drive por MCP | se houver uma ferramenta de Drive conectada, baixe por ela e salve em `projetos/<nome>/materiais-de-trabalho/fonte/` |
| link de pasta do Drive | peça o link do arquivo. Pasta não serve, e o script avisa isso |

O `baixar.py` imprime o caminho final na última linha. Use exatamente esse caminho no passo 3.

Se o yt-dlp não estiver instalado, o script explica como instalar em vez de quebrar. Não invente
outro caminho: mostre a mensagem ao usuário e deixe ele escolher entre instalar ou baixar na mão.

Quando o vídeo é longo e você só quer a fala, `--apenas-audio` baixa um arquivo muito menor. Vale a
pena sempre que o vídeo original já estiver na máquina do usuário por outro caminho, ou quando for
só para transcrever.

## Passo 2: escolher a rota

Leia a chave `transcricao` do `setup.json` na raiz do pacote. Ela vale `replicate` ou `local`. Se o
usuário não disse nada em contrário, respeite o que está lá.

| | nuvem (`replicate`) | máquina do usuário (`local`) |
|---|---|---|
| velocidade | de 1 a 4 minutos | de 40 minutos por hora de vídeo, em CPU, com o modelo `small` |
| custo | centavos de dólar por vídeo | zero |
| instalação | nenhuma, só a chave no `.env` | baixa cerca de 1,5 GB na primeira vez |
| precisa de | `REPLICATE_API_TOKEN` | `uv` instalado |
| privacidade | o áudio sobe para a Replicate | nada sai da máquina |

Troque de rota sem pedir licença em dois casos: quando falta a chave da Replicate, aí ofereça a rota
local; e quando o usuário disser que o material é sigiloso, aí a rota local é a única.

## Passo 3: transcrever

**Nuvem, a recomendada:**

```bash
flow-reels transcrever/replicate \
  --entrada projetos/<nome>/materiais-de-trabalho/fonte/<arquivo> \
  --projeto projetos/<nome> \
  --idioma pt
```

O script extrai o áudio, mede a duração e dispara. Ele leva de um a quatro minutos e imprime o
andamento, então não é travamento: avise o usuário e espere.

Se o usuário tiver jargão, nome próprio ou sigla que o modelo costuma ouvir errado, passe
`--vocabulario "CRM, LTV, Marília Bastos, Grupo Cedro"`. Isso conserta o que o modelo **ouve**, e é muito mais
barato que corrigir depois: uma sigla ouvida errada aparece trinta vezes no texto.

**Local, a gratuita:**

```bash
uv run ${CLAUDE_PLUGIN_ROOT}/skills/transcrever/scripts/local.py \
  --entrada projetos/<nome>/materiais-de-trabalho/fonte/<arquivo> \
  --projeto projetos/<nome> \
  --modelo small --idioma pt
```

Em máquina sem placa de vídeo, comece por `--modelo small`. O `large-v3` é melhor, mas gasta umas
seis vezes mais tempo, e para escolher gancho o `small` já resolve. Se a máquina tem placa NVIDIA,
use `--dispositivo cuda --modelo large-v3`.

Na primeira execução o `uv` baixa o ambiente inteiro. Avise o usuário antes, porque o terminal fica
alguns minutos parecendo travado.

## Passo 4: conferir antes de passar adiante

Antes de dizer que terminou, olhe o resultado. São três conferências rápidas:

1. **Os três arquivos existem** e o `palavras.json` tem mais de uma dúzia de palavras.
2. **O `meta.alinhado` é `true`.** Se for `false`, os tempos são por trecho e não por palavra: dá
   para ler e escolher o gancho, mas todo ponto de corte vai precisar de conferência na onda do
   áudio. Diga isso ao usuário em vez de deixar a surpresa para o corte.
3. **Leia as primeiras dez linhas do `transcricao.md`.** Se o texto estiver em outro idioma, com
   palavra repetida em loop, ou vazio, foi o áudio que chegou errado, não o modelo. Refaça.

Depois, diga ao usuário quanto tempo tem o vídeo, quantas palavras saíram e onde os arquivos estão,
com caminho completo.

## O contrato do `palavras.json`

Este formato é acordo com o `/flow-reels:planejar` e com o gerador de legenda. **Não mude sem avisar as
duas pontas.** As chaves são em português e são exatamente estas três por palavra:

```json
{
  "palavras": [
    {"inicio": 0.59, "fim": 0.71, "texto": "Bom"},
    {"inicio": 0.75, "fim": 1.04, "texto": "gente"}
  ],
  "meta": {
    "fonte": "minha-aula.mp4",
    "video": "materiais-de-trabalho/fonte/minha-aula.mp4",
    "audio": "materiais-de-trabalho/transcricao/audio16k.wav",
    "duracao": 763.42,
    "idioma": "pt",
    "motor": "whisperx large-v3 via replicate (align_output)",
    "alinhado": true,
    "palavras": 1834,
    "frases": 214,
    "gerado_em": "2026-09-18T22:40:11"
  }
}
```

- `inicio` e `fim` são segundos contados do começo do áudio.
- A lista vem em ordem, sem palavra vazia, e `fim` nunca é menor que `inicio`.
- A pontuação fica colada na palavra, porque é ela que ensina a legenda onde quebrar a linha.
- `alinhado: false` significa tempo aproximado. Quem for cortar precisa saber disso.

Quem grava é sempre o `normalizar.py`, nunca a rota direto. As duas rotas passam por ele justamente
para que o formato não dependa de quem transcreveu. A explicação completa do formato está no
cabeçalho de `scripts/normalizar.py`.

## Os scripts

| script | o que faz |
|---|---|
| `scripts/baixar.py` | traz o arquivo do YouTube, do Drive ou de uma URL direta para `<projeto>/materiais-de-trabalho/fonte/` |
| `scripts/replicate.py` | transcreve na nuvem. Sobe o áudio, espera e normaliza, sem estimar custo nem pedir confirmação |
| `scripts/local.py` | transcreve na máquina, via `uv run`. Mesma saída |
| `scripts/normalizar.py` | o contrato. Grava os três arquivos e valida o formato antes de escrever |

Todos aceitam `--help` e, chamados sem argumento, explicam o que fazem em vez de quebrar.

## Quando dá errado

| o que você vê | o que é | o que fazer |
|---|---|---|
| `não achei a chave REPLICATE_API_TOKEN` | falta o `.env` ou a linha da chave | copie o `.env.exemplo` para `.env` e preencha, ou vá de rota local |
| a Replicate recusou a chave (401) | chave errada ou revogada | gere outra em replicate.com |
| a Replicate pediu pagamento (402) | conta sem cartão | cadastre, ou use a rota local |
| `o arquivo tem X MB e o limite é 100 MB` | você mandou o vídeo em vez do áudio | o script já gera o `audio16k.wav`, mande ele |
| o Drive devolveu uma página | arquivo sem link aberto | abra o compartilhamento ou baixe na mão |
| `o yt-dlp não está instalado` | falta a ferramenta de download | siga um dos comandos que a mensagem lista |
| `ffmpeg não encontrado no PATH` | o pacote não está instalado | rode o `instalar` na raiz do pacote |
| a transcrição saiu em outro idioma | o detector errou | force com `--idioma pt` |
| nome próprio sempre errado | o modelo não conhece a palavra | refaça com `--vocabulario` |
| palavra repetida em loop no meio | trecho de silêncio longo ou música | normal, o planejador ignora. Se for o vídeo inteiro, o áudio chegou corrompido |
| travou depois de `criando a transcrição` | a fila da Replicate está lenta | o script consulta sozinho por até uma hora, espere |

Se a rota da nuvem terminou mas a normalização falhou, **não pague de novo**. A resposta crua ficou
em `materiais-de-trabalho/transcricao/bruto-replicate.json`, dentro da pasta do vídeo. Reprocesse
com:

```bash
flow-reels transcrever/replicate \
  --entrada <mesmo arquivo> --projeto projetos/<nome> --reusar
```

## O que esta skill não faz

- Não escolhe gancho, não decide o que vira corte e não corta. Isso é o `/flow-reels:planejar`.
- Não gera legenda. Ela só entrega os tempos que a legenda vai usar.
- Não traduz. A transcrição sai no idioma falado.
- Não baixa conteúdo de terceiros por conta própria: baixa o que o usuário pedir, e a
  responsabilidade pelo direito de uso é dele.
