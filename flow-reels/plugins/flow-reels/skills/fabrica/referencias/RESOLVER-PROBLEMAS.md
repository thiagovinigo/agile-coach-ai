# Resolver problemas

O que costuma dar errado, em linguagem de gente. Cada item tem o que você vê, o que está
acontecendo de verdade e o que fazer agora.

Uma orientação antes da lista: **erro de ferramenta não é culpa sua e quase nunca exige refazer o
trabalho.** A pasta do vídeo guarda tudo que já ficou pronto, então quase sempre se conserta a peça
que quebrou e se continua de onde parou.

---

## 1. "ffmpeg não encontrado" ou "ffmpeg is not recognized"

**O que é.** O ffmpeg é o programa que corta, empilha e exporta vídeo. O pacote inteiro depende
dele, e ele não vem junto: precisa estar instalado no computador e visível no PATH, que é a lista de
lugares onde o sistema procura programas.

**O que fazer.** Instale e abra um terminal novo, porque o PATH só é lido quando o terminal abre.

| sistema | comando |
|---|---|
| Windows | `winget install Gyan.FFmpeg` |
| macOS | `brew install ffmpeg` |
| Linux | `sudo apt install ffmpeg` |

Para conferir, digite `ffmpeg -version`. Se aparecer um monte de texto, está certo. Depois rode o
instalador do pacote de novo (`./instalar.sh` ou `powershell -ExecutionPolicy Bypass -File
instalar.ps1`), que ele confere tudo de uma vez.

No Windows, o erro mais comum depois de instalar é continuar no mesmo terminal antigo. Feche e abra.

---

## 2. "o Chromium não está instalado" no meio do render do painel

**O que é.** O painel de cima é uma página desenhada e fotografada quadro a quadro. Quem tira essas
fotos é um navegador sem janela, o Chromium, controlado pelo Playwright. É o ponto que mais falha em
instalação nova, porque é um download grande.

**O que fazer.**

```
python -m pip install playwright
python -m playwright install chromium
```

Se o download falhar no meio, quase sempre é a rede: tente de novo, de preferência em outra conexão.
Rede corporativa com proxy costuma bloquear esse download.

Enquanto o Chromium não estiver instalado, **só o painel para de funcionar**. Transcrição,
planejamento, recorte da face, legenda e montagem continuam rodando. Dá para adiantar tudo e deixar o
render do painel por último.

---

## 3. "não achei a chave REPLICATE_API_TOKEN", ou a chave foi recusada

**O que é.** A transcrição na nuvem é um serviço pago que pede uma chave sua. Sem ela, o script não
tem como se identificar.

**O que fazer, conforme a mensagem.**

| mensagem | o que aconteceu | conserto |
|---|---|---|
| não achei a chave | falta o arquivo `.env`, ou falta a linha | copie o `.env.exemplo` para `.env` e cole a chave |
| a chave foi recusada (401) | chave errada, com espaço sobrando, ou revogada | gere outra em replicate.com e cole de novo, sem espaço nas pontas |
| pediu pagamento (402) | a conta não tem cartão cadastrado | cadastre o cartão, ou use a rota local |

**Você não é obrigado a usar a nuvem.** A rota local transcreve na sua máquina, de graça, e o único
custo é tempo: cerca de 40 minutos para cada hora de vídeo, num computador sem placa de vídeo. Para
escolher gancho, o resultado do modelo `small` já resolve.

```
uv run skills/transcrever/scripts/local.py --entrada <arquivo> --projeto projetos/<nome> --modelo small --idioma pt
```

Se a transcrição na nuvem terminou mas a gravação dos arquivos falhou depois, **não pague de novo**.
A resposta crua ficou salva em `materiais-de-trabalho/transcricao/bruto-replicate.json`, dentro da
pasta do vídeo, e o mesmo comando com `--reusar` reaproveita ela.

---

## 4. O vídeo não tem áudio, ou o áudio veio mudo

**O que é.** Sem áudio não existe transcrição, e sem transcrição não existe corte. Acontece com
gravação de tela feita sem entrada de som, com arquivo exportado só com a trilha de vídeo e com
vídeo cuja trilha de som está em um segundo arquivo.

**Como confirmar em um comando:**

```
ffprobe -v error -select_streams a -show_entries stream=codec_name,channels -of default=nw=1 <arquivo>
```

Se não imprimir nada, o arquivo realmente não tem trilha de áudio.

**O que fazer.** Não tem conserto do lado do pacote: o som precisa existir. Os caminhos possíveis são
exportar o vídeo de novo com o áudio junto, ou juntar o áudio separado ao vídeo antes de começar:

```
ffmpeg -i video.mp4 -i audio.wav -c:v copy -c:a aac -shortest video-com-audio.mp4
```

Caso diferente, e mais chato: o arquivo **tem** trilha de áudio, mas ela está muda ou quase. Aí a
transcrição sai vazia, ou sai com a mesma palavra repetida em loop. Ouça 10 segundos do arquivo antes
de gastar de novo com transcrição.

---

## 5. A legenda saiu fina demais e some no vídeo

**O que é.** Este é o defeito mais traiçoeiro do pacote, porque não parece erro: sai uma legenda, ela
só está magra. E magra ela desaparece assim que a plataforma comprime o vídeo.

**A causa.** Fonte variável. Uma fonte variável é um arquivo só que contém a família inteira, do fino
ao gordo, e o peso é escolhido na hora de desenhar. O queimador de legenda do ffmpeg **ignora esse
controle de peso** e desenha no peso padrão do arquivo, que na maioria das famílias modernas é o mais
fino de todos. A Quicksand que vem no pacote, por exemplo, tem Light como padrão.

**O conserto.** Usar sempre uma instância estática, que é um arquivo com um peso só gravado dentro.
As do pacote já estão prontas em `marca/fontes/`:

```
--arquivo-fonte marca/fontes/Quicksand-Bold.ttf
```

Se a fonte é sua, trazida no onboarding, gere a estática antes de usar:

```
flow-reels marca/tratar_fonte caminho/da/fonte.ttf --pesos 700,500 --saida marca/fontes
```

O script diz se a fonte é variável, gera as estáticas e imprime o **nome de família real** de cada
arquivo gerado. Use esse nome, letra por letra, no `--fonte`. Chutar o nome a partir do nome do
arquivo dá legenda em fonte de sistema, sem nenhum aviso.

**Como confirmar que consertou:** extraia a faixa da costura de um quadro com legenda e olhe a
espessura do traço.

```
ffmpeg -y -ss 5.0 -i corte-01.mp4 -frames:v 1 -vf "crop=1080:420:0:750" costura.png
```

---

## 6. Erro "No option name near 'C:/...'" no ffmpeg

**O que é.** Erro de Windows, e só de Windows. Ao queimar a legenda, o caminho da pasta de fontes vai
dentro de um filtro do ffmpeg, e ali dentro os dois pontos têm significado próprio: eles separam as
opções do filtro. O `C:` do caminho é lido como o fim de uma opção, e o comando quebra.

**O conserto.** Dentro do filtro, **caminho sempre relativo**, com o processo rodando na pasta certa.
Em vez de:

```
subtitles=C:/Users/voce/fabrica-de-cortes/projetos/aula/materiais-de-trabalho/corte-01/legenda.ass
```

faça o programa entrar na pasta do corte e escreva:

```
subtitles=legenda.ass:fontsdir=../../../../marca/fontes
```

O `montar.py` já faz isso sozinho, então este erro só aparece quando alguém monta na mão. Se ele
aparecer com o `montar.py`, é sinal de que o script foi chamado de um lugar inesperado: rode da raiz
do pacote.

---

## 7. O render do painel está muito lento

**O que é.** Não é travamento, é o jeito que funciona. Cada quadro do painel é uma foto de uma página
desenhada do zero, e um corte de 30 segundos tem 360 quadros autorados. O ritmo medido está em
`skills/produzir/referencias/RECEITA-TECNICA.md` seção 7, que é a dona do número, e lá está
também quanto isso dá para um corte inteiro. O script imprime o andamento justamente para você ver
que não parou.

**Quando é lento de verdade, e o que fazer:**

| sintoma | causa provável | o que fazer |
|---|---|---|
| menos de 1 quadro por segundo | o painel usa sombra pesada, desfoque ou muitos elementos | simplifique o desenho, que ganha em nitidez também |
| lento só na primeira vez | o Chromium está sendo aberto e a fonte carregada | normal, a partir do segundo corte melhora |
| a máquina inteira engasga | pouca memória livre | feche o navegador e os programas pesados, e renderize um corte por vez |
| parou de imprimir andamento | o painel entrou em laço infinito dentro de `render(t)` | interrompa, e procure no `painel.html` alguma conta que dependa do tempo sem fim |

Antes de renderizar o corte inteiro, renderize quatro instantes soltos e olhe. Descobrir um defeito
no quadro 4 custa segundos; descobrir no vídeo pronto custa o render inteiro.

```
flow-reels produzir/painel --painel painel.html --saida quadro.png --so-quadro 7.4
```

---

## 8. O rosto saiu mal enquadrado

**O que é.** A metade de baixo do corte é um recorte vertical da sua gravação. O pacote escolhe uma
caixa fixa de recorte, olhando alguns instantes do vídeo. Quando a caixa está errada, aparece queixo
cortado, topo da cabeça cortado, pessoa encostada na borda ou pessoa fora do quadro.

**O conserto, em três passos.**

1. Gere a folha de amostras, que é uma imagem com vários instantes do vídeo e uma grade por cima:

```
flow-reels produzir/enquadrar amostrar \
  --video materiais-de-trabalho/fonte/aula.mp4 \
  --saida materiais-de-trabalho/corte-01/contato.png --n 12
```

2. Escolha a caixa olhando a grade, no formato `x:y:largura:altura`, sempre na proporção 1080 por
   964. Duas referências que resolvem quase tudo: os olhos perto do terço de cima, e um dedo de ar
   acima da cabeça.

3. Confira antes de recortar o vídeo todo:

```
flow-reels produzir/enquadrar validar \
  --video materiais-de-trabalho/fonte/aula.mp4 --caixa 760:120:1080:964 \
  --saida materiais-de-trabalho/corte-01/contato-recorte.png
```

**Olhe a imagem.** Ela mostra exatamente o que vai virar a metade de baixo do corte. Reprovou,
ajuste os números e valide de novo, que isso custa segundos.

**Quando a caixa fixa não resolve.** Caixa fixa funciona porque webcam em canto e busto em tripé não
se mexem. Se você anda pelo quadro, nenhuma caixa fixa acompanha, e o certo é dizer isso em vez de
entregar um recorte que perde a cabeça no meio. As duas saídas possíveis: gravar o próximo vídeo com
a câmera parada, ou instalar a detecção de rosto do OpenCV, que não vem no pacote justamente por ser
pesada e por não ser necessária na maioria dos casos.

---

## 9. Quando nada disso resolve

Três perguntas que costumam achar o problema mais rápido que tentar de novo:

1. **O comando rodou da raiz do pacote?** Quase todo caminho do pacote é relativo à raiz, que é a
   pasta onde está o `setup.json`.
2. **O arquivo que o comando pediu existe mesmo?** Abra a pasta do vídeo e confira. Muito erro de
   caminho é arquivo que ficou com outro nome.
3. **A etapa anterior terminou de verdade?** A transcrição precisa dos três arquivos, o corte precisa
   do `brief.md`, a montagem precisa do `painel.mp4` e do `face.mp4`. Etapa pela metade quebra a
   seguinte com uma mensagem que parece de outro assunto.

Erro que se repete três vezes pelo mesmo motivo é hora de parar e mudar de caminho, não de tentar de
novo mais devagar.
