# Flow Reels 3.0.0 · comece aqui

1. **Abra esta pasta no Claude Code** (no terminal, `claude` dentro dela; no app, abra a pasta na aba
   Code) e **aceite a confiança da pasta**. O plugin Flow Reels liga sozinho, e as skills aparecem como
   `/flow-reels:fabrica`, `/flow-reels:tendencias`, `/flow-reels:marca` e as outras.
2. **Prepare a pasta**, uma vez: peça "instala o flow reels", ou rode no terminal do Claude Code
   `flow-reels instalar`. Ele checa o ffmpeg e o Python, cria o `.venv`, baixa o Chromium e cria o seu
   `.env`. Se faltar algo, ele diz o que é e como resolver.
3. **Coloque as suas chaves** no `.env` (todas opcionais: Replicate para transcrever rápido, Zernio para
   publicar, ElevenLabs para o reel narrado, xAI para o X nas tendências).
4. **Mande o primeiro vídeo:** "quero fazer cortes desse vídeo: <caminho, link do YouTube ou do Drive>".
   Na primeira vez ele faz o onboarding da sua marca (fonte, cor, logo e a foto da capa).

Sem vídeo ainda? "o que está bombando no meu nicho?" ou "o que tá em alta sobre <tema>?".

O guia completo está em `plugins/flow-reels/README.md`, e as novidades em
`plugins/flow-reels/CHANGELOG.md`. Esta pasta é a sua pasta de trabalho: os seus vídeos ficam em
`projetos/`, a sua marca em `marca/` e as suas chaves no `.env`. O código mora em `plugins/flow-reels/`
e uma atualização nunca mexe no que é seu.
