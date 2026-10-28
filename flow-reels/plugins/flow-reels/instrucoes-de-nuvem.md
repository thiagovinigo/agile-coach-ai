# Rodar na nuvem

O pacote foi feito para rodar na sua máquina, e é ali que ele roda melhor. Este documento é para o
outro caso: quando você quer que ele trabalhe **sem você estar na frente**, numa máquina emprestada
que sobe, faz o trabalho e some.

## São duas camadas, e confundir as duas custa tempo

Antes de tudo, separe o que agenda do que trabalha. São coisas diferentes, com limites
diferentes, e a maior parte da confusão vem de tratar as duas como uma.

| camada | o que é | o limite dela |
|---|---|---|
| **a rotina** | o que acorda no horário, decide se tem trabalho e conduz | sem teto de tempo por comando; ela pode esperar |
| **a caixa** | a máquina Linux temporária onde o render pesado acontece | teto de 180 s por comando, pouca memória, some no fim |

A caixa aqui é um **sandbox do Composio**, que é a opção mais direta hoje. Nada neste documento
depende dela: o mesmo raciocínio serve para qualquer máquina remota descartável, e só muda o
comando de entrada.

**A rotina não precisa de caixa para tudo.** Conferir se tem vídeo novo, ler um arquivo de
controle e te avisar são coisas que ela faz sozinha, de graça. A caixa só sobe quando existe
render para fazer.

---

## 1. Quando vale, e quando não vale

**Vale** quando o gargalo é a sua máquina ficar ocupada: um vídeo de uma hora, um lote de cinco
cortes, o render do painel travando o resto do seu trabalho por vinte minutos.

**Não vale** quando você vai ficar olhando de qualquer jeito. Subir o pacote, subir o vídeo e trazer
o resultado de volta custa mais tempo do que o render economiza num corte só.

**Nunca vale** para o passo da marca. O `/flow-reels:marca` é uma conversa com você, uma vez na vida, e
o resultado dela vai junto no pacote depois. Configure a marca na sua máquina e leve o
`marca/tokens.json` pronto.

---

## 2. O problema que a nuvem não resolve

O caminho do pacote tem **três paradas** em que ele encosta e espera você: aprovar os ganchos,
revisar os cortes e autorizar a publicação. Na nuvem não tem ninguém para aprovar.

Isso não é detalhe de configuração, é uma decisão que você precisa tomar antes de automatizar.
Existem três saídas honestas:

| saída | como funciona | o que você perde |
|---|---|---|
| **parar na porta** | a rodada vai até os ganchos e para, te avisando. Você aprova de onde estiver e ela continua | duas viagens em vez de uma |
| **produzir tudo e revisar depois** | ela ignora a aprovação de gancho, produz o teto do `setup.json` e te entrega tudo para revisar junto | render gasto em corte que você reprovaria |
| **só até a revisão** | ela produz e monta a página de revisão, e para ali. Publicar continua sendo na mão | nada, e por isso é a recomendada |

A terceira é a recomendada porque preserva a única parada que existe para proteger você de verdade:
publicar é irreversível, e nada deve publicar sozinho.

> **Nunca deixe a chave `ZERNIO_API_KEY` numa rodada automática sem supervisão.** Um erro de seleção
> na sua máquina custa um render. O mesmo erro com a chave de publicação dentro custa um post no ar.

---

## 3. O que tem dentro de uma caixa dessas

Medido numa caixa recém-criada. **Confira em vez de confiar**, porque a imagem muda com o tempo:

```
uname -a && nproc && free -m && df -h / /tmp /dev/shm && python3 -V && ffmpeg -version | head -1
```

O que costuma vir:

| recurso | o que tinha | o que isso significa para o pacote |
|---|---|---|
| processador | 1 núcleo | o render do painel fica mais lento que na sua máquina |
| memória | cerca de 985 MB | `pip install` pesado morre com código 137 sem swap |
| disco | 25 GB | sobra, o pacote inteiro tem meio megabyte |
| `/tmp` | 493 MB **em RAM** | é aqui que a maioria dos renders quebra, veja a seção 6 |
| `/dev/shm` | 493 MB | pouco para o Chromium em quadro grande |
| Python | 3.13 | serve |
| ffmpeg | 7 | serve |
| navegador | **não vem** | e o painel animado não renderiza sem ele |
| teto por comando | **180 segundos** | qualquer render demora mais, veja a seção 7 |

As duas linhas que mais mordem são as duas últimas: **não vem navegador** e **todo comando morre em
180 segundos**.

---

## 4. Levar o pacote para dentro

O pacote tem meio megabyte, então isso é fácil. Duas formas, nesta ordem de preferência.

**Por link temporário**, se o zip estiver em algum lugar com endereço:

```bash
cd ~ && curl -sSL -o fabrica.zip "<o link>" && unzip -q fabrica.zip && cd fabrica-de-cortes
```

**Escrevendo os arquivos**, se não houver link. Funciona porque o pacote é texto quase inteiro, mas
é lento e polui o histórico. Prefira o link.

**O que vai junto e o que não vai:**

- vai: o plugin (`plugins/flow-reels/` com o `.claude-plugin/marketplace.json` da raiz, ou o zip do
  pacote), o `setup.json`, e o `marca/` **com o `tokens.json` já preenchido** e as fontes tratadas.
  Na máquina remota, os scripts rodam com `plugins/flow-reels/bin/flow-reels <skill>/<script>` de
  dentro da pasta de trabalho;
- não vai: `projetos/` com trabalho antigo dentro, e o `.env`.

**Fixe qual versão está rodando.** Leve um zip com nome que diga a versão, e não "o zip mais
recente". Uma rodada automática que pega sempre o último muda de comportamento sozinha, e você
descobre isso por um corte que saiu diferente, sem saber o que mudou.

> **A chave nunca viaja dentro do zip.** Ela entra na caixa como variável de ambiente, no momento de
> rodar, e some quando a caixa some. Se você empacotar o `.env` junto, ele fica no zip para sempre.

Três regras de chave na nuvem, e as três existem porque o contrário já vazou credencial:

- **nunca escreva a chave em disco dentro da caixa.** Nada de criar um `.env` lá. Variável de
  ambiente vive na memória do processo e some junto com ele;
- **nunca cole a chave numa conversa nem num prompt.** Tudo que entra numa conversa fica no
  histórico dela;
- **nunca tire a chave de dentro de uma conexão para usar na mão.** Se a ferramenta já sabe
  autenticar por você, deixe ela autenticar. Chave extraída é chave que vazou.

---

## 5. Levar o vídeo para dentro

Aqui está o truque que muda tudo, e ele evita baixar gigabyte à toa.

**Não copie o vídeo.** Gere um **link assinado de curta duração** para ele, onde quer que ele esteja,
e deixe o ffmpeg ler direto do link. Qualquer armazenamento que sirva HTTP Range funciona, e quase
todos servem.

```bash
ffmpeg -y -ss 812.4 -i "$LINK_ASSINADO" -t 27.0 -c copy trecho.mp4
```

O ffmpeg pula direto para o segundo pedido e puxa **só os bytes daquele trecho**. Recortar 27
segundos de uma gravação de 1,5 GB lê alguns megabytes, não 1,5 GB.

Duas ressalvas:

- **a transcrição precisa do arquivo inteiro**, então ela é a exceção: ou você baixa de verdade, ou
  transcreve antes, na sua máquina, e leva só o `palavras.json` junto;
- **link assinado expira.** Se a rodada for longa, gere de novo no meio, em vez de descobrir o
  vencimento no erro.

---

## 6. Preparar a caixa

Quatro coisas, e as quatro existem por um erro que já aconteceu.

**O navegador, que não vem.** O painel animado é uma página fotografada quadro a quadro, então sem
navegador não existe painel:

```bash
python3 -m pip install --quiet playwright requests fonttools
python3 -m playwright install --with-deps chromium
```

O `--with-deps` não é enfeite: numa caixa enxuta faltam as bibliotecas de sistema que o Chromium
precisa, e sem elas ele instala e não abre.

**O `TMPDIR`, que é onde mais se perde tempo.** O `/tmp` está montado **em memória**. Uma sequência
de 156 quadros em 1080x1920 ocupa 174 MB, e uma sequência maior enche os 493 MB e derruba o render
com um erro que fala de outra coisa. Aponte para disco de verdade:

```bash
mkdir -p ~/tmp && export TMPDIR=~/tmp
```

Quando um render quebrar sem explicar, olhe `df -h /tmp` antes de culpar a memória.

**A troca, para o `pip` não morrer.** Com 985 MB, instalar o Playwright às vezes é morto pelo sistema
com código 137:

```bash
sudo fallocate -l 2G /swapfile && sudo chmod 600 /swapfile && sudo mkswap -q /swapfile && sudo swapon /swapfile
```

**A memória compartilhada, para o Chromium não engasgar** em quadro grande:

```bash
sudo mount -o remount,size=2G /dev/shm
```

---

## 7. Rodar sem bater no teto de 180 segundos

**Todo comando é morto em 180 segundos.** O render de um corte de 30 segundos passa disso com folga.
Então a regra é uma só, e não tem exceção:

> **Sempre em segundo plano, nunca em primeiro.**

```bash
cd ~/fabrica-de-cortes
setsid nohup flow-reels produzir/painel \
  --pagina projetos/<video>/materiais-de-trabalho/corte-01/painel.html \
  --saida projetos/<video>/materiais-de-trabalho/corte-01/painel.mp4 \
  > render.log 2>&1 < /dev/null &
echo "subiu"
```

Depois você volta de tempos em tempos e olha o andamento, que é comando rápido:

```bash
tail -5 render.log
```

Vale o mesmo para ffmpeg lendo de link assinado, que é trabalho de rede e demora o que a rede
quiser.

**Queime a legenda pelo `montar.py`, não pelo ffmpeg na mão.** A caixa não tem a sua fonte
instalada, e o queimador de legenda, quando não acha a fonte, **não reclama**: ele desenha no tipo
padrão e entrega um corte que parece pronto e está com a letra errada. O `montar.py` resolve isso
sozinho, entrando na pasta certa e apontando a pasta de fontes por caminho relativo, e copiando as
fontes para o lado da legenda quando o caminho relativo não existe. Chamando o ffmpeg direto, você
perde esse cuidado.

**Falhe alto, nunca degradado.** Faltou a chave da transcrição, a rodada para e diz **qual
variável** falta e em qual etapa. O que ela não faz é seguir com uma transcrição pior, um painel
sem o logo que faltava, ou um corte sem legenda. Saída degradada na nuvem é pior que erro, porque
ninguém está olhando: o arquivo ruim chega até você parecendo pronto.

**Confira a forma antes de renderizar, e nunca por contagem fixa.** Antes de gastar render, teste
que a marca chegou inteira na caixa: que `marca/tokens.json` existe e abre, e que a pasta de fontes
tem arquivo dentro. Escreva o teste como "tem pelo menos um", nunca como "tem exatamente três":
contagem apodrece na primeira vez que alguém acrescenta um peso de fonte.

**Um ponteiro só vale se resolver em bytes dentro da caixa.** Se um beat aponta para um arquivo,
confira que o arquivo está lá, não que a frase que cita ele está lá. Instrução para olhar uma coisa
que não chegou na caixa é uma etapa que vai falhar no meio, depois de você já ter pago o preparo.

**Não imprima coisa grande.** A saída de ferramenta é cortada perto de 30 mil caracteres, e mais
apertada ainda no console. Nunca mande imprimir um arquivo em base64: ele estoura o limite, some no
meio e você fica depurando um problema que não existe.

---

## 8. Tirar o resultado de lá

O corte pronto é um MP4 de alguns megabytes, e ele **não sai pelo histórico da conversa**. Não tente
passar binário por ali.

Suba um servidor mínimo dentro da caixa, protegido por um segredo que só você conhece, e deixe o
destino puxar:

```python
# servir.py, dentro da caixa
import http.server, os, functools
TOKEN = os.environ["TOKEN_SAIDA"]

class Porta(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.headers.get("X-Token") != TOKEN:
            self.send_error(403); return
        super().do_GET()

http.server.HTTPServer(("0.0.0.0", 8080), Porta).serve_forever()
```

```bash
TOKEN_SAIDA=$(head -c 24 /dev/urandom | base64) setsid nohup python3 servir.py > servir.log 2>&1 < /dev/null &
```

Três regras que valem nas duas direções:

- **nada de porta aberta sem credencial.** Enquanto o servidor está no ar, qualquer um que descubra o
  endereço baixa o que está lá;
- **derrube o servidor quando terminar**, não deixe para o fim da caixa;
- **confira o tamanho em bytes** do arquivo que chegou contra o que saiu. Transferência truncada
  produz um MP4 que abre, toca o começo e corta no meio, e isso passa despercebido.

---

## 9. Deixar rodando sozinho

Quando o caminho inteiro estiver funcionando na mão, aí sim vale agendar. A rotina agendada faz
sempre a mesma sequência:

1. sobe a caixa;
2. traz o pacote e a marca;
3. prepara a caixa, a seção 6 inteira;
4. procura vídeo novo onde você combinou que ele aparece;
5. **não achou vídeo novo, encerra sem fazer nada**, que é o caso mais comum e precisa ser barato;
6. achou, roda até a revisão;
7. devolve os cortes e te avisa;
8. derruba a caixa.

**O passo 5 é o que separa uma rotina útil de uma cara.** Uma rotina que sobe a caixa inteira todo
dia para descobrir que não tem vídeo novo gasta dinheiro para não fazer nada. Confira primeiro, com
comando barato, e só então prepare a caixa.

**Marque o que já foi feito.** Uma rotina que roda de hora em hora precisa saber que aquele vídeo já
virou corte, senão ela refaz o mesmo trabalho e você recebe o mesmo corte cinco vezes. Um arquivo de
controle com o nome dos vídeos já processados resolve.

---

## 10. Regras que custaram caro

- **Identifique o vídeo pela impressão digital, não pelo nome.** Duração, resolução e taxa de
  quadros. Duas exportações do mesmo material carregam o mesmo nome e linhas do tempo diferentes, e
  cortar a errada produz um arquivo plausível e silenciosamente errado.
- **Nunca case imagem de um arquivo com áudio de outro** quando o arquivo da imagem já tem áudio. O
  áudio que combina é justamente o que denuncia fonte errada. Descartar ele tira o único sinal que
  falharia alto.
- **Arquivo pesado anda por link assinado de curta duração**, nas duas direções, nunca pelo histórico
  da conversa e nunca por porta aberta sem credencial.
- **Confira o tamanho entregue contra o de origem** depois de qualquer transferência.
- **A caixa é descartável, o seu trabalho não.** Traga o resultado antes de encerrar. Caixa derrubada
  não volta, e não existe lixeira.

---

## 11. Limites conhecidos

- **Um núcleo e cerca de 1 GB.** Serve para composição de página e de tela. Cena pesada de três
  dimensões vai se arrastar.
- **Sem navegador de fábrica**, e instalar custa alguns minutos no começo de toda caixa nova.
- **Sem estado entre caixas.** Nada do que você instalou sobrevive. Toda rodada paga o preparo de
  novo, e é por isso que a seção 6 vira um script que você cola inteiro.
- **A transcrição local é pesada** para um núcleo. Na nuvem, ou você usa a transcrição por serviço,
  ou transcreve antes na sua máquina e leva o `palavras.json` pronto.
- **A página de revisão não se serve sozinha de dentro da caixa** para você olhar de fora sem abrir
  porta. Traga os MP4 e revise na sua máquina, que é onde a revisão pertence de qualquer jeito.
