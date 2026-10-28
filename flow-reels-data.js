const flowReelsData = {
    "VISÃO GERAL & INSTALAÇÃO": [
        {
            id: "fr-comece-aqui",
            title: "Comece Aqui (Quickstart)",
            description: "Os 4 passos rápidos para abrir a pasta no Claude Code, rodar o instalador, configurar chaves e gerar o primeiro corte.",
            icon: "🚀",
            path: "flow-reels/COMECE-AQUI.md"
        },
        {
            id: "fr-readme",
            title: "Guia Completo (README 3.0)",
            description: "Visão geral da Fábrica de Cortes 3.0: comandos, modos de cena, linguagens visuais, tendências, reel narrado e estrutura de pastas.",
            icon: "📖",
            path: "flow-reels/plugins/flow-reels/README.md"
        },
        {
            id: "fr-changelog",
            title: "Novidades da Versão 3.0 (Changelog)",
            description: "O que mudou da 0.2.0 para a 3.0.0: Motor 2.0 em cenas, Liquid Glass, Visão 3D (Depth Anything + BiRefNet), Modo Mundo e 13 Gates.",
            icon: "✨",
            path: "flow-reels/plugins/flow-reels/CHANGELOG.md"
        },
        {
            id: "fr-setup-json",
            title: "Configuração do Projeto (setup.json)",
            description: "Contrato de configuração da pasta de trabalho: limites de cortes, paralelismo, nicho de pautas, zonas seguras e portas.",
            icon: "⚙️",
            path: "flow-reels/setup.json"
        },
        {
            id: "fr-nuvem",
            title: "Execução em Máquina Remota (Nuvem)",
            description: "Receita para rodar lotes grandes ou vídeos longos em servidor remoto até a etapa de revisão.",
            icon: "☁️",
            path: "flow-reels/plugins/flow-reels/instrucoes-de-nuvem.md"
        },
        {
            id: "fr-licencas",
            title: "Licenças & Tecnologias Open-Source",
            description: "Lista de modelos e bibliotecas gratuitas de uso comercial (GSAP, Playwright, FFmpeg, MediaPipe, Depth Anything, BiRefNet).",
            icon: "⚖️",
            path: "flow-reels/LICENCAS-DE-TERCEIROS.md"
        }
    ],
    "AS 8 SKILLS (COMANDOS CLAUDE CODE)": [
        {
            id: "skill-fabrica",
            title: "1. /flow-reels:fabrica (Orquestrador)",
            description: "A porta de entrada que conduz do vídeo longo aos cortes prontos, gerenciando estado e parando nos 3 pontos de decisão humana.",
            icon: "🏭",
            path: "flow-reels/plugins/flow-reels/skills/fabrica/SKILL.md"
        },
        {
            id: "skill-tendencias",
            title: "2. /flow-reels:tendencias (Radar & Pautas)",
            description: "Varre Reddit (sem chave), YouTube Brasil, GitHub, HN e Product Hunt para entregar pautas validadas com roteiro medido e kit de gravação.",
            icon: "📡",
            path: "flow-reels/plugins/flow-reels/skills/tendencias/SKILL.md"
        },
        {
            id: "skill-marca",
            title: "3. /flow-reels:marca (DNA & Identidade)",
            description: "Onboarding único da sua marca: extrai cores, fontes, superfície e foto de capa, gerando tokens.json e painel de amostra 1080x956.",
            icon: "🎨",
            path: "flow-reels/plugins/flow-reels/skills/marca/SKILL.md"
        },
        {
            id: "skill-transcrever",
            title: "4. /flow-reels:transcrever (Áudio & Alinhamento)",
            description: "Baixa de arquivo local, YouTube ou Drive e transcreve palavra a palavra com timestamps (Replicate na nuvem ou WhisperX local).",
            icon: "🎙️",
            path: "flow-reels/plugins/flow-reels/skills/transcrever/SKILL.md"
        },
        {
            id: "skill-planejar",
            title: "5. /flow-reels:planejar (Ganchos & Cenas)",
            description: "Inventário visual, varredura generosa, 6 eliminadores de gancho, subagente Leitor Frio, validação por energia de áudio e plano de cenas.",
            icon: "🧠",
            path: "flow-reels/plugins/flow-reels/skills/planejar/SKILL.md"
        },
        {
            id: "skill-produzir",
            title: "6. /flow-reels:produzir (Render Paralelo & Revisão)",
            description: "Produz múltiplos cortes em paralelo com subagentes dedicados (1 pasta = 1 dono), renderiza no Chromium/FFmpeg e sobe a revisão na porta 8790.",
            icon: "🎬",
            path: "flow-reels/plugins/flow-reels/skills/produzir/SKILL.md"
        },
        {
            id: "skill-publicar",
            title: "7. /flow-reels:publicar (Zernio & Funil DM)",
            description: "Publica ou agenda no Instagram e YouTube via API Zernio com dry-run (--seco) obrigatório e configura automação de comentário para DM.",
            icon: "📲",
            path: "flow-reels/plugins/flow-reels/skills/publicar/SKILL.md"
        },
        {
            id: "skill-narrado",
            title: "8. /flow-reels:narrado (Reel Sem Rosto / ElevenLabs)",
            description: "Formato de 40-50s sem rosto: locução ElevenLabs sobre filmagem real, cartão de abertura, zoom guiado com anel desenhado e CTA para DM.",
            icon: "🗣️",
            path: "flow-reels/plugins/flow-reels/skills/narrado/SKILL.md"
        }
    ],
    "PLANEJAMENTO, GANCHOS & ROTEIRO": [
        {
            id: "ref-gancho",
            title: "A Lei do Gancho & Os 6 Eliminadores",
            description: "Regras impiedosas de seleção de ganchos, leitura fria por subagente isolado e critérios de tensão, especificidade e payoff.",
            icon: "🪝",
            path: "flow-reels/plugins/flow-reels/skills/planejar/referencias/GANCHO.md"
        },
        {
            id: "ref-formatos",
            title: "Formatos de Corte: Afirmação vs Trajeto",
            description: "Diferença estrutural entre cortes de tese direta (Afirmação) e cortes passo a passo (Trajeto com 4 blocos obrigatórios).",
            icon: "📐",
            path: "flow-reels/plugins/flow-reels/skills/planejar/referencias/FORMATOS.md"
        },
        {
            id: "ref-levantamento",
            title: "Varredura & Levantamento em 2 Leituras",
            description: "Como ler a transcrição inteira mapeando dependência de contexto externo, silêncios longos e as 4 listas de formas conhecidas.",
            icon: "🔎",
            path: "flow-reels/plugins/flow-reels/skills/planejar/referencias/LEVANTAMENTO.md"
        },
        {
            id: "ref-corte-limpo",
            title: "Corte Limpo & Energia do Áudio",
            description: "Como cravar pontos de entrada e saída dentro de janelas reais de silêncio (<8% de energia por 150ms) sem amputar sílabas ou respirações.",
            icon: "✂️",
            path: "flow-reels/plugins/flow-reels/skills/planejar/referencias/CORTE-LIMPO.md"
        },
        {
            id: "ref-cenas",
            title: "Arquitetura de Cenas & Âncoras de Palavra",
            description: "Como planejar o reel inteiro cena a cena usando tempos presos à palavra ({'ancora': 'planilha#2'}) em vez de segundos fixos.",
            icon: "🎞️",
            path: "flow-reels/plugins/flow-reels/skills/planejar/referencias/CENAS.md"
        },
        {
            id: "ref-modelos-cenas",
            title: "Catálogo de Modos de Cena",
            description: "Exemplos práticos dos modos: rosto+vidro, tela+bolha, mundo, vidro líquido, tela cortada 3D, manchete, lado a lado, lista e tipografia.",
            icon: "🗂️",
            path: "flow-reels/plugins/flow-reels/skills/planejar/referencias/MODELOS-DE-CENAS.md"
        },
        {
            id: "ref-beat-sheet",
            title: "Beat-Sheet do Painel Superior",
            description: "Como estruturar o ritmo visual do painel para que algo relevante aconteça a cada frase sem cair em loops genéricos.",
            icon: "🥁",
            path: "flow-reels/plugins/flow-reels/skills/planejar/referencias/BEAT-SHEET.md"
        },
        {
            id: "ref-representacao",
            title: "Inventário Visual & Representação",
            description: "Como transformar cada ferramenta, número ou conceito falado no vídeo em elemento concreto na tela (logos, prints, mocks).",
            icon: "🖼️",
            path: "flow-reels/plugins/flow-reels/skills/planejar/referencias/REPRESENTACAO.md"
        },
        {
            id: "ref-valor",
            title: "Prova, Contexto & Corte de Gordura",
            description: "Como buscar a prova da promessa no vídeo, pagar dívidas de contexto e remover desvios que não servem à tese.",
            icon: "💎",
            path: "flow-reels/plugins/flow-reels/skills/planejar/referencias/VALOR.md"
        }
    ],
    "MOTOR 2.0, VISÃO 3D & GATES DE QUALIDADE": [
        {
            id: "motor-contrato",
            title: "Contrato Técnico do Motor 2.0",
            description: "Pipeline completo: editar_fala.py -> rosto.py -> visao.py -> compor.py (GSAP + Chromium) -> audio.py -> conferir_reel.py.",
            icon: "⚙️",
            path: "flow-reels/plugins/flow-reels/skills/produzir/motor/MOTOR.md"
        },
        {
            id: "motor-estetica",
            title: "As 12 Linguagens Visuais do Episódio",
            description: "Direções de arte completas: vidro, terminal, cinema, recorte, sci-fi, anos 80, mangá, profundidade 3D, editorial, turbo, calmo e manchete.",
            icon: "🎭",
            path: "flow-reels/plugins/flow-reels/skills/produzir/motor/docs-4/estetica.md"
        },
        {
            id: "motor-visao",
            title: "Visão Computacional & Camadas 3D",
            description: "Separação em camadas com Depth Anything V2 e BiRefNet: texto passando atrás da pessoa, recorte fino de cabelo e máscara do Modo Mundo.",
            icon: "👁️",
            path: "flow-reels/plugins/flow-reels/skills/produzir/motor/docs-4/visao-4-3.md"
        },
        {
            id: "motor-frames-3d",
            title: "Frames 3D & Câmeras Virtuais",
            description: "iPhone 3D, parede de telas, câmera 2.5D, dolly zoom, polaroid e placas de Liquid Glass que inclinam e mergulham.",
            icon: "🧊",
            path: "flow-reels/plugins/flow-reels/skills/produzir/motor/docs-4/frames-3d.md"
        },
        {
            id: "motor-maos-rosto",
            title: "Gatilhos de Mãos, Corpo & Expressão Facial",
            description: "Efeitos visuais disparados automaticamente por gestos das mãos e expressões do rosto rastreados via MediaPipe.",
            icon: "🖐️",
            path: "flow-reels/plugins/flow-reels/skills/produzir/motor/docs-4/maos-corpo.md"
        },
        {
            id: "motor-looks-pos",
            title: "Looks de Vídeo, Pós-Processamento & LUTs",
            description: "14 filtros de vídeo (CRT, VHS, holograma, pontilhado) e 13 efeitos de quadro inteiro mantendo a legenda 100% nítida.",
            icon: "🌈",
            path: "flow-reels/plugins/flow-reels/skills/produzir/motor/docs-4/looks.md"
        },
        {
            id: "motor-transicoes-som",
            title: "Transições, Palavras Animadas & Som Sintetizado",
            description: "15 famílias de efeitos sonoros que nunca caem sobre a sílaba tônica, mais transições de glitch, queima de filme, cubo e neon.",
            icon: "🔊",
            path: "flow-reels/plugins/flow-reels/skills/produzir/motor/docs-4/variedade-e-som.md"
        },
        {
            id: "ref-gates-7",
            title: "Os 7 Critérios & 13 Gates Automáticos",
            description: "Um defeito, um dono: como o script conferir_reel.py audita ritmo, zonas seguras, contraste, colisão legenda×rosto e volume (-14 LUFS).",
            icon: "🛡️",
            path: "flow-reels/plugins/flow-reels/skills/fabrica/referencias/GATES.md"
        },
        {
            id: "ref-gates-4-3",
            title: "Especificação Técnica dos Gates (4.3)",
            description: "Detalhamento das métricas de aprovação automática de linguagem, variedade, som e Modo Mundo antes de subir a página de revisão.",
            icon: "✅",
            path: "flow-reels/plugins/flow-reels/skills/produzir/motor/docs-4/gates-4-3.md"
        }
    ],
    "RADAR DE TENDÊNCIAS, NARRADO & PUBLICAÇÃO": [
        {
            id: "tend-criterios",
            title: "Critérios & Pontuação de Tendências",
            description: "Como filtrar achados de Reddit, YouTube, GitHub e HN: zero rumor, zero número inventado e fato conferido na fonte.",
            icon: "📊",
            path: "flow-reels/plugins/flow-reels/skills/tendencias/referencias/CRITERIOS.md"
        },
        {
            id: "tend-roteiro-kit",
            title: "Roteiro Medido na Fala & Kit de Gravação",
            description: "Estrutura dos 5 blocos para 40-50s de fala real e montagem da pasta com prints, rolagem e logos prontos.",
            icon: "📝",
            path: "flow-reels/plugins/flow-reels/skills/tendencias/referencias/ROTEIRO.md"
        },
        {
            id: "tend-radar-metodo",
            title: "Metodologia do Radar Bilingue (PT + EN)",
            description: "Como pesquisar temas em português e inglês, mapear consenso vs onde a comunidade racha e sintetizar sinais.",
            icon: "🧭",
            path: "flow-reels/plugins/flow-reels/skills/tendencias/referencias/RADAR-METODOLOGIA.md"
        },
        {
            id: "narrado-padrao",
            title: "Lei do Formato Reel Narrado",
            description: "Regras visuais e sonoras para reels sem rosto: filmagem real em largura cheia, empurrões de câmera, anel desenhado e mixagem.",
            icon: "🎞️",
            path: "flow-reels/plugins/flow-reels/skills/narrado/referencias/PADRAO-NARRADO.md"
        },
        {
            id: "pub-funil-dm",
            title: "Publicação Zernio & Funil 'Comenta a Palavra'",
            description: "Como configurar a automação de comentário -> DM no Instagram e validar a matriz de plataformas antes de publicar.",
            icon: "💬",
            path: "flow-reels/plugins/flow-reels/skills/publicar/referencias/funil-dm.md"
        },
        {
            id: "fab-pasta-video",
            title: "Arquitetura da Pasta do Vídeo (Isolamento)",
            description: "Por que a pasta corte-NN/ guarda exclusivamente o MP4 final enquanto materiais-de-trabalho/ isola todo o resto.",
            icon: "📂",
            path: "flow-reels/plugins/flow-reels/skills/fabrica/referencias/PASTA-DO-VIDEO.md"
        },
        {
            id: "studio-server",
            title: "Flow Reels Studio 3.0 (Servidor Web & UI)",
            description: "Código-fonte do servidor local (porta 8080) com Wizard passo a passo, gerador de projetos universais por URL e streaming HTTP 206.",
            icon: "🖥️",
            path: "flow-reels/studio/server.py"
        }
    ]
};
