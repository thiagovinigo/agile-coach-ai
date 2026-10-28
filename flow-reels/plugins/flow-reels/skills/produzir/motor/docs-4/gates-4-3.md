# Gates 4.3: som, linguagem e variedade

Esta frente fecha três buracos que a 4.0 deixou para os gates: o efeito sonoro que cai em cima da palavra
que ele devia valorizar, a conferência da linguagem que só rodava na mão, e os sinais de "isso é template"
da pesquisa (`docs/pesquisa-4-0/04-edicao-retencao-e-som.md`, seções 4.2, 6.6, 7 e 8).

| arquivo | o que mudou |
|---|---|
| `scripts/audio.py` | efeito x sílaba tônica (adianta até 80 ms ou baixa 6 dB) e escreve o `sons.json` |
| `scripts/conferir_reel.py` | gates 10 (som), 11 (linguagem) e 12 (variedade); status N/A |
| `scripts/linguagem.py` | só expõe `avaliar(raiz, tabela, pasta)`, o miolo do `conferir`, sem imprimir |

O código de saída do `conferir_reel.py` não mudou: 0 passou (aviso, pulado e N/A não bloqueiam), 1
reprovou, 2 erro de uso. O gate 12 nunca reprova.

---

## 1. Efeito sonoro x sílaba tônica (`audio.py`)

A pesquisa (4.2): "efeito em cima da palavra mascara justamente o que se quer destacar"; o efeito cai 1 a 3
quadros antes ou no respiro. Antes da 4.3 o `audio.py` não sabia das palavras.

### 1.1 A palavra destacada

É a palavra falada (`palavras-corte.json`) que o plano destaca:

- está na `"enfase"` da legenda (a do reel ou a de uma cena), comparada sem acento, sem caixa e sem
  pontuação (`"GLM,"` = `glm`); ou
- aparece grande na tela enquanto é falada: o `"texto"` de uma sobreposição `palavra`, `objeto3d`, `titulo`,
  `manchete` ou `selo`, ou de qualquer item com `"tam"` ≥ 80; a palavra que conta usa `valor` + `sufixo`
  (`"80 MODELOS"`). Vale se ela é falada entre 1 s antes do `t` do item e 0,5 s depois do `ate`. É a
  palavra do evento, quando o evento é de uma palavra.

Artigo, preposição e conector (`de`, `o`, `para`, `que`, `isso`...) nunca são destaque.

### 1.2 A tônica, por regra

`tonica_na_palavra(texto)` devolve onde a sílaba tônica começa e termina, em fração do tempo da palavra:

1. sigla de 2 a 4 maiúsculas (`API`, `MCP`, `IA`): soletrada, tônica na última letra;
2. nome de fora conhecido (`TONICA_CONHECIDA`: Codex, Gemini, OpenRouter, Claude, Salesforce... 33 nomes),
   porque a regra do português lê "Codex" como co-DEX;
3. acento agudo ou circunflexo marca a tônica (proparoxítona sempre tem); senão o til (`não`, `irmão`);
4. sem acento: terminada em `a e o (s) am em ens` é paroxítona; o resto (`i u is us r l z x n im um om ns`)
   é oxítona; uma sílaba só é ela mesma.

As sílabas saem dos núcleos vocálicos: vogal + `i`/`u` átono é ditongo (pai, muito, partiu), `ão ãe õe` é um
núcleo, o resto é hiato (di-a, sa-ú-de); o `u` de que/qui/gue/gui é da consoante. O tempo da palavra é
dividido entre as sílabas com a tônica pesando 1,4; o centro da vogal fica a 55% da sílaba. A **zona tônica**
é o centro ± 60 ms (o número da pesquisa, seção 8), dentro da sílaba.

### 1.3 O que o `audio.py` faz

Depois de escolher o arquivo e o tom de cada efeito, ele mede a **região forte** do som: onde a energia
alisada (Hann de 20 ms) fica a até 6 dB do auge, em volta do ponto forte (num tique, 10 a 20 ms; num whoosh,
o miolo da passagem, 100 a 200 ms; na estática, 250 ms). Se ela cruza a zona tônica de uma palavra
destacada, em ordem:

1. **adianta** o som até a região forte terminar 5 ms antes do **ataque da palavra**, se isso for até 80 ms;
2. senão, adianta até ela terminar 5 ms antes da **zona tônica**, também até 80 ms;
3. senão (ou se adiantar cairia noutra tônica, antes do 0, ou a menos de 0,25 s do efeito anterior),
   o efeito toca **6 dB mais baixo**, no lugar.

Só para trás, nunca para depois: 80 ms são 2,4 quadros, dentro do "1 a 3 quadros antes" da pesquisa (o som
"puxa" o olho). O som adiantado mais que ~45 ms já é perceptível como adiantado quando é seco e isolado; por
isso o limite fica em 80 e não mais. Determinístico: só depende dos tempos, e duas rodadas dão o mesmo
`audio-final.wav` e o mesmo `sons.json`, bit a bit.

| parâmetro (`audio.py`) | padrão | o que é |
|---|---|---|
| `TONICA_RAIO` | 0,060 s | meia largura da zona tônica |
| `FORTE_DB` | 6 dB | a região forte do som |
| `DESLOCA_MAX` | 0,080 s | o máximo que o som anda para antes |
| `FOLGA_ATAQUE` | 0,005 s | margem entre o fim da região forte e o alvo |
| `BAIXA_TONICA_DB` | -6 dB | quando andar não resolve |
| `PESO_TONICA` / `NUCLEO_NA_SILABA` | 1,4 / 0,55 | o modelo do tempo dentro da palavra |
| `TIPOS_GRANDES` / `TAMANHO_GRANDE` | palavra, objeto3d, titulo, manchete, selo / 80 px | o que é "grande na tela" |

A saída do `audio.py` ganhou a coluna `tônica` na tabela dos efeitos (`"oficial": -78 ms, antes da tônica`,
`"segundos": -6 dB no lugar`) e uma linha de resumo:
`sílaba tônica: 22 palavra(s) destacada(s); 5 efeito(s) cairiam na tônica de uma delas: 2 adiantado(s) até 80 ms, 3 baixado(s) 6 dB`.

### 1.4 O `sons.json` (novo, na pasta do corte)

O `audio.py` escreve a agenda do que tocou, para o gate ler (antes ela só ia para a tela). Um efeito:

```json
{"t": 2.22, "t_som": 2.1422, "desloca_ms": -77.8, "baixa_db": 0.0, "arquivo": "glitch", "familia": "glitch",
 "som": "glitch", "peso": 3, "tipo": "transicao", "alvo": "glitch", "semitons": -0.957, "nivel_db": -20.32,
 "folga_db": 21.85, "fala": true, "comeca": 2.125, "termina": 2.3786, "forte": [2.125, 2.1621],
 "tonica": {"palavra": "oficial", "centro": 2.2149, "zona": [2.1671, 2.254], "motivo": "grande na tela",
            "acao": "antes da tônica"}}
```

No topo: `versao`, `corrigiu_tonica`, `eventos_sha256` e `fala_sha256` (para o gate saber se a agenda é
do plano de agora), `duracao`, `voz_lufs`, `efeitos_db`, `parametros`, `fora` (os eventos que não tocaram e
por quê) e `destaques` (as palavras destacadas com a zona tônica). `--sem-efeitos` grava a agenda vazia com
`"sem_efeitos": true`.

Para o gate, o `audio.py` também ganhou `agenda_do_corte(pasta, raiz, efeitos_db, corrigir_tonica)`: refaz a
agenda sem misturar nem gravar nada (o passo 2 do `processar` virou `montar_efeitos`, que os dois usam).

### 1.5 Medido

Quatro cortes copiados para uma caixa de areia (já movida para a lixeira) e o `audio.py` rodado de novo:

| corte de origem | efeitos | na tônica | adiantados | baixados | diferença no áudio | volume da entrega | sincronia p95 |
|---|---|---|---|---|---|---|---|
| codex-no-claude-code 02 | 30 | 5 | 2 (-78 e -30 ms) | 3 | só nos 5 efeitos | -14,1 LUFS, -2,0 → -2,1 dBTP | 47 ms (igual) |
| 5-plugins-claude-code 02 | 59 | 4 | 0 | 4 | só nos 4 efeitos | -14,0 LUFS, -3,7 dBTP (igual) | 53 ms (igual) |
| apis-de-ia-gratis 01 | 40 | 4 | 2 | 2 | só nos 4 efeitos (*) | -14,1 LUFS, -3,5 dBTP | 51 ms (igual) |
| teste-onda-1 42 | 14 | 0 | 0 | 0 | **idêntico bit a bit** | -14,0 LUFS, -1,6 dBTP (igual) | 47 ms (igual) |

(*) contra o mesmo `audio.py` com a correção desligada; contra o áudio de 7/10 o arquivo difere em todo
efeito, porque a biblioteca de sons foi refeita depois dele (23h40 de 7/10). As emendas também ficaram
iguais (o `audio.py` não mexe no `fala.mp4`, então a sincronia e as emendas não podiam mudar; conferi assim
mesmo). O `audio.py` inteiro continua em ~6 s para 38 s de fala.

---

## 2. Gate 10 · som (efeitos sonoros)

Lê o `sons.json`. Sem ele (entrega de antes da 4.3), refaz a agenda pelo `eventos.json` com
`corrigir_tonica=False`, que é o que o `audio.py` antigo tocou nos tempos; nesse caso o arquivo de cada
efeito é o que o `audio.py` de hoje escolheria, então **a repetição de arquivo não é conferida** (sai
"arquivo repetido não conferido (sem sons.json)").

| confere | reprova (defeito claro) | olhe |
|---|---|---|
| densidade (`duração / efeitos`) | um a cada menos de 0,75 s | um a cada menos de 1,5 s (a régua da pesquisa) |
| efeitos soando juntos (do começo ao fim de cada arquivo) | 4 ou mais | 3 |
| o mesmo arquivo em dois efeitos seguidos (qualquer família) | sempre | — |
| efeito na tônica de palavra destacada | a voz a menos de 6 dB acima dele ali (encobre) | a voz 6 dB ou mais acima, sem correção (áudio antigo) |
| pico verdadeiro de cada efeito na entrega (4x, 192 kHz, ±50 ms) | acima de -1 dBTP | — |
| `sons.json` mais velho que o `eventos.json` ou o `fala.mp4` (sha256) | — | sempre |

Efeito que o `audio.py` 4.3 adiantou ou baixou conta como resolvido (aparece no resumo: `(2 adiantado(s), 3
baixado(s))`); baixado que ainda fica a menos de 6 dB da voz reprova. Sem entrega, o pico é medido no
`audio-final.wav`. Custo: 0,4 s com o `sons.json`, ~2 s refazendo a agenda.

Por que esses limites, e não os da pesquisa: 8 dos 13 reels medidos (todos aprovados) têm um efeito a cada
1,08 a 1,41 s, abaixo da régua de 1,5 s. Reprovar ali seria gate errado; fica o olhe, e reprova o dobro do
teto (0,75 s). Os 23 efeitos que caem numa tônica nesses reels têm a voz 15 a 32 dB acima deles: não
encobrem nada, então são olhe; reprova só o que de fato mascara (menos de 6 dB, o mesmo `FOLGA_MINIMA` com
que o `audio.py` já avisava).

## 3. Gate 11 · linguagem

Com `"linguagem"` no `cenas.json`, chama `linguagem.avaliar()` (importado, a lógica não foi copiada): os
`problemas` reprovam, os `avisos` viram aviso, as `linhas` (transições, herói, sons pedidos) vão no
detalhe. Sem `"linguagem"`, o status é **N/A** ("NÃO SE APLICA" no `--json`), que não bloqueia, não conta
como pulado e não entra na contagem do "os N gates passaram". Linguagem desconhecida reprova.

## 4. Gate 12 · variedade (só aviso)

| sinal (pesquisa 04, seção 7) | régua |
|---|---|
| a mesma transição seguida (o corte seco não interrompe) | mais de 3 vezes |
| o mesmo efeito de palavra seguido | mais de 2 vezes |
| todas as cenas com a mesma duração | ±10% da mediana, com 4 cenas ou mais |
| efeito em metrônomo: momentos de peso 2 e 3 (juntando os a 0,5 s) | desvio-padrão dos intervalos < 35% da média, com 6 momentos ou mais |
| o mesmo arquivo de efeito no reel (com `sons.json`) | mais de 4 vezes |
| linguagem / herói / trilha iguais aos dos últimos reels | 2 / 4 / 8 reels (`linguagens.json`) |
| traços iguais aos do reel anterior (Jaccard) | 50% ou mais |

Os traços: linguagem, convidada, herói, trilha, estilo, legenda, modos, famílias de transição, tipos de
sobreposição, efeitos de palavra e de look, famílias de som. O histórico é o
`projetos/.historico-linguagens.json` (o `linguagem.py registrar`); ele ainda não existe, então o gate o
refaz das entregas que declaram linguagem, pela data do mp4, sem os projetos `teste*` (que não são reel
publicado). O traço de quem está no arquivo de histórico vem do `cenas.json` dele, quando a pasta existe.

## 5. Resultado nos 13 reels pedidos

| reel | veredito | 10 som | 11 linguagem | 12 variedade |
|---|---|---|---|---|
| teste-onda-1 40 | com avisos | olhe: 1 na tônica (voz +28 dB) | N/A | ok |
| teste-onda-1 41 | com avisos | olhe: 2 na tônica | N/A | olhe: metrônomo (variação 30%) |
| teste-onda-1 42, 43, 45 | **PASSOU** (os 11 gates) | ok | N/A | ok |
| teste-onda-1 44 | com avisos (+ gate 8) | olhe: 1 a cada 1,13 s; 2 na tônica | N/A | ok |
| apis-de-ia-gratis 01 | com avisos | olhe: 1 a cada 1,11 s; 4 na tônica | N/A | olhe: `conta` 3x seguidas |
| apis-de-ia-gratis 02 | com avisos | olhe: 1 a cada 1,11 s; 2 na tônica | passou | ok (nenhum anterior) |
| 5-plugins-claude-code 01 | com avisos | olhe: 1 a cada 1,41 s | N/A | ok |
| 5-plugins-claude-code 02 | com avisos | olhe: 1 a cada 1,08 s; 4 na tônica | passou | olhe: `carimbo` 3x e 4x seguidas |
| codex-no-claude-code 01 | com avisos | olhe: 1 a cada 1,12 s; 2 na tônica | N/A | ok |
| codex-no-claude-code 02 | com avisos | olhe: 1 a cada 1,27 s; 5 na tônica | passou | ok (Jaccard 25% com o anterior) |
| google-ai-boost-bites 01 | com avisos | olhe: 1 a cada 1,23 s; 1 na tônica | N/A | ok |

**Nenhum reprovou** (saída 0 nos 13). O código dos gates 1 a 9 não mudou (no apis 02, antes e depois da
frente, os 9 deram os mesmos números). Os defeitos de verdade foram
provados num corte de teste (cópia do codex 02): arquivo repetido em seguida, efeito na tônica a 3 dB da
voz, um efeito a cada 0,6 s com 4 juntos, áudio 4 dB mais quente (pico de +0,8 dBTP) e transição `cubo`
fora do terminal reprovaram; 5 persianas seguidas e linguagem/herói repetidos deram aviso; plano sem
linguagem deu N/A; `eventos.json` mexido depois do `audio.py` deu aviso.

## 6. Limites

- A tônica é estimada por regra e pelo tempo da palavra dividido por sílaba, não medida no áudio. Erra em
  hiato sem acento (a-IN-da sai "AIN-da") e em nome de fora que não está na tabela (a regra do português
  vale para ele). O erro típico é de meia sílaba, e a zona de ±60 ms absorve parte disso.
- Efeito longo (estática, whoosh, energia) quase nunca cabe nos 80 ms: vira -6 dB. Se quiser que ele
  saia da palavra, o plano move o evento.
- Entrega sem `sons.json`: a agenda é reconstruída (tempos certos; arquivo e volume do `audio.py` de hoje).
- O pico por efeito é medido na entrega (AAC), não na pista de efeitos isolada: um pico da voz perto do
  efeito conta para ele. Com -1 dBTP garantido pelo loudnorm, isso só pega o que já é defeito.
- O histórico refeito depende da data dos mp4 e só vê reels que declaram linguagem.

## 7. Pedidos ao integrador

**MOTOR.md**
- Seção 1 (quem escreve o quê): o `audio.py` escreve também `sons.json` na pasta do corte (a agenda dos
  efeitos; contrato em docs-4/gates-4-3.md 1.4) e lê o `palavras-corte.json` e o `cenas.json` (ênfase e
  textos grandes) para a sílaba tônica.
- Seção dos gates (onde estão os 9): passam a ser 12. 10 som, 11 linguagem, 12 variedade (só aviso), com
  as réguas das seções 2 a 4 daqui, e o status N/A.
- Seção 6 (som): a regra da tônica (adianta até 80 ms ou -6 dB) e o fim do limite "o audio.py não sabe da
  sílaba tônica" do variedade-e-som.md seção 5 (pode tirar essa linha de lá).

**Skills**
- `/flow-reels:produzir` (SKILL.md): "as 9 gates têm de passar" vira "os gates 1 a 11 sem
  reprovar; o 12 é aviso". Depois de mudar o `eventos.json`, rodar o `audio.py` de novo (o gate 10 avisa
  quando o `sons.json` ficou velho). O `linguagem.py conferir` antes do render continua; o gate 11 repete a
  mesma conferência no fim.
- `/flow-reels:planejar` (CENAS.md): som só em evento de peso 2 ou 3, e evento de som longo (estática,
  whoosh, energia) fora da palavra destacada, no respiro; o `audio.py` só corrige até 80 ms.
- Depois que o criador aprovar um reel: `linguagem.py registrar`, para o gate 12 comparar com o histórico
  de verdade e não com o refeito das entregas.
- Os reels de antes da 4.3 (todos os 13 acima) não têm `sons.json`: rodar o `audio.py` neles aplica a
  correção da tônica (só muda os efeitos listados no gate 10) e liga a conferência de arquivo repetido.
