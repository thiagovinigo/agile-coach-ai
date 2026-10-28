# Logos oficiais em cor, PNG sem fundo

O `componentes/logos/` guarda silhuetas de uma cor, que o painel pinta com a tinta da marca. Esta
pasta guarda o outro caso: o logo **em cor**, exatamente como a marca publica, em PNG transparente e
grande (até 2400 px), para o vídeo mostrar a marca de verdade em destaque. No motor 2.0 ele entra como
**adesivo** no `rosto-vidro` (MOTOR.md 4.2): na fila dos cards de cima ou ao lado da cabeça.

Nada aqui foi redesenhado, recolorido ou tirado de site de "PNG grátis": cada arquivo tem a origem e
as regras de uso registradas no `_acervo.json`.

## O que já está aqui

**189 arquivos de 91 marcas de tecnologia**, cada uma na cor dela, em PNG sem fundo. A folha
`_amostra.png` mostra todas sobre fundo escuro, e `flow-reels componentes/baixar-marca` lista uma por uma.

- **IA:** Claude, Claude Code, Anthropic, Gemini, Google, DeepSeek, Mistral, Grok, xAI, Meta, Microsoft
  Copilot, Perplexity, Hugging Face, Ollama, Qwen, Kimi, Manus, Midjourney, Runway, Suno, ElevenLabs,
  NVIDIA, OpenRouter, Groq, MCP, LangChain, Google Antigravity.
- **Programação e nuvem:** Cursor, GitHub, GitHub Copilot, VS Code, Windsurf, Lovable, Bolt, Replit,
  Firebase, Vercel, Supabase, Next.js, React, Python, Node.js, JavaScript, TypeScript, Tailwind, Docker,
  PostgreSQL, MongoDB, Redis, Cloudflare, Netlify, Railway, Render, AWS, Google Cloud, Azure, Linux,
  Ubuntu, Postman.
- **Automação e trabalho:** n8n, Make, Zapier, HubSpot, Stripe, Notion, Slack, Trello, Asana, Google
  Sheets, Gmail, Google Drive, Excel, Teams, Outlook, Salesforce, Figma, Canva, Zoom.
- **Comunicação e redes:** WhatsApp, Telegram, Instagram, YouTube, TikTok, X, LinkedIn, Discord.
- **Navegadores e sistemas:** Chrome, Firefox, Safari, Edge, Brave, Arc, Apple, Windows, Microsoft.

Os nomes seguem um padrão: `<marca>-icone.png` (o símbolo) e `<marca>-logo.png` (símbolo com nome),
na versão para **fundo escuro** (o padrão); `-fundo-claro` no fim é a versão para
fundo claro. Quatro ícones só existem em cor escura e pedem fundo claro: `kimi-icone`, `nextjs-icone`,
`runway-icone` e `suno-icone` (para esses, use o `-logo` branco). O nome escrito do Google Antigravity
e o do Mistral são cinza-escuro: sobre fundo escuro, use o ícone.

De onde veio cada um, e as regras de uso, ficam no `_acervo.json`. Claude, Claude Code, Anthropic e
n8n vieram do kit de imprensa da própria empresa; o resto, do [SVGL](https://svgl.app), acervo aberto
de logos de tecnologia que liga cada marca à página de marca dela; Make, Zapier, HubSpot e ElevenLabs,
do desenho do Simple Icons na cor oficial.

**OpenAI (ChatGPT, Codex, a flor):** o kit oficial pede aceite dos termos de marca da OpenAI, e esse
aceite é seu. Em <https://openai.com/brand/>, marque a caixa, clique em "Baixar logotipos" e passe o
zip extraído com `--arquivo`.

## As regras das marcas

- **Anthropic e Claude** ([kit de imprensa](https://www.anthropic.com/press-kit)): marcas registradas da
  Anthropic. Uso para se referir ao produto, sem alterar cor nem proporção e sem sugerir parceria.
- **n8n** ([guia de marca](https://n8n.io/brandguidelines/)): só nas cores oficiais, sem sombra, sem
  inclinar, sem esticar e sem fundo carregado; 4x de espaço livre; nunca o nome sem o ícone; no mínimo
  100 px de largura.

Por isso o adesivo de logo entra sobre uma **placa de vidro escuro**, e não solto sobre o vídeo: é o
fundo calmo que as marcas pedem, e o motor nunca põe sombra nem inclina um logo do acervo.

## Como adicionar uma marca

```bash
flow-reels componentes/baixar-marca                       # o que já existe
flow-reels componentes/baixar-marca --kit anthropic n8n   # rebaixa os kits conhecidos
flow-reels componentes/baixar-marca --url <SVG ou PNG oficial> --nome supabase-logo \
       --marca Supabase --origem https://supabase.com/brand-assets --termos "regras da página"
```

O script renderiza SVG em PNG grande no Chromium do pacote, apara a margem transparente e grava a
ficha. A fonte é sempre a página de marca ou de imprensa da empresa.

**Kit que pede para aceitar termo de uso não é baixado sozinho.** Quem aceita é a pessoa, e o
arquivo baixado entra com `--arquivo`.
