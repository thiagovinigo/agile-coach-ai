# marca/fontes

As fontes que os seus cortes usam. **Esta pasta já vem com a Quicksand**, que é o padrão do pacote,
em três arquivos:

- `Quicksand-Bold.ttf`, o peso da legenda e dos títulos
- `Quicksand-Medium.ttf`, o peso dos textos menores
- `Quicksand.ttf`, a fonte variável de origem, guardada para gerar outro peso se precisar
- `OFL.txt`, a licença, que permite usar e redistribuir

Você não precisa fazer nada aqui. O onboarding só mexe nesta pasta se você trouxer a sua própria
fonte, e nesse caso ele copia a sua para cá e passa a apontar para ela no `tokens.json`.

**Se a sua fonte for variável**, o onboarding gera a versão estática antes de guardar. Isso é
obrigatório: o queimador de legenda do ffmpeg ignora o eixo de peso de uma fonte variável e
renderiza no peso padrão dela, que costuma ser o mais fino. Sem esse tratamento a sua legenda sai
fina e não fica claro o porquê.

**A fonte mono (JetBrains Mono, licença OFL em `OFL-JetBrainsMono.txt`)** entrou na 3.0 para o HUD de
capítulos, os timecodes e os rótulos pequenos. Ela vem no pacote para o render sair igual em qualquer
máquina: sem ela, cada sistema caía na sua própria monoespaçada.
