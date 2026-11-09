# Operações próprias para aprimorar slides

Use para pedidos de melhoria ou revisão. Reconheça intenção em linguagem comum; os nomes abaixo não são comandos obrigatórios. Leia o alvo, briefing e identidade existentes. Examine o render atual quando disponível antes de editar. Se o usuário só pedir crítica ou planejamento, entregue análise sem modificar o deck.

## Escolher a intervenção

| Pedido | Operação | Resultado esperado |
| --- | --- | --- |
| “Analisa”, “critica”, “o que está fraco?” | Criticar | Diagnóstico com evidência, impacto e prioridades. |
| “Planeja antes” | Estruturar | Tese, arco, composição e movimento descritos no storyboard. |
| “Mais fora da caixa”, “mais presença” | Ousar | Um gesto decisivo e específico, coerente com o projeto. |
| “Está exagerado”, “mais elegante/calmo” | Acalmar | Menos competição e estímulo, preservando caráter. |
| “Tem muita coisa/texto” | Simplificar | Menos obstáculos, sem perder raciocínio ou fatos essenciais. |
| “Capricha”, “refina”, “termina o acabamento” | Refinar | Consistência, alinhamento e estados finalizados. |
| “Não entendi”, “mais direto” | Clarificar | Mensagem e controles compreensíveis para aquele público. |
| “Melhora fontes”, “hierarquia” | Compor tipografia | Papéis claros e fonte bem aplicada ao conteúdo real. |
| “Melhora cores” | Dirigir cor | Paleta com função, contraste e continuidade. |
| “Arruma layout”, “espaços” | Compor espaço | Ordem de leitura, agrupamento e ritmo adequados. |
| “Mais movimento”, “transições melhores” | Coreografar | Movimento com função e continuidade, sob controle do uso. |
| “Algo extraordinário” | Experimentar | Técnica ambiciosa comprovada numa cena, com alternativa viável. |
| “Celular”, “projeção”, “outra proporção” | Adaptar | Composição e interação adequadas ao destino. |
| “Está lento/travando” | Otimizar | Gargalo medido e corrigido, preservando o gesto narrativo. |
| “Tem que funcionar sempre” | Robustecer | Estados, fallbacks e casos de navegação tratados. |
| “Padroniza”, “reaproveita” | Consolidar | Tokens e componentes para padrões realmente recorrentes. |
| “Mostra alternativas desta cena” | Variar | Alternativas distintas só do alvo, identificadas e comparáveis. |

Combine operações quando o pedido exigir, na ordem: verdade e funcionamento → narrativa e compreensão → direção → acabamento. Não execute todas as linhas em todo trabalho.

## Criticar com evidência

Avalie primeiro a experiência, depois os dados técnicos, para não reduzir direção a uma lista de erros de código. Nenhuma ferramenta ou avaliação por múltiplos agentes é obrigatória.

Observe: promessa e conclusão; progressão; especificidade visual; hierarquia; carga cognitiva; coerência entre imagens, fonte e paleta; curva emocional; controles, teclado e estados; legibilidade no destino; movimento e desempenho.

Teste os pontos de vista pertinentes: iniciante que depende da explicação, apresentador que precisa retornar rapidamente, pessoa lendo sozinha e pessoa que usa teclado ou movimento reduzido. Não alegue teste com usuários ou leitor de tela se apenas simulou o ponto de vista.

Entregue forças concretas e os problemas que mais importam, com cena/elemento, evidência observada, consequência e correção proposta. Diferencie falha funcional, dificuldade de compreensão, desalinhamento com o briefing e preferência estética. Não fabrique uma nota numérica universal; se uma pontuação for solicitada, explicite critérios e limites. Em pedido de análise, recomendações não autorizam alterações por si só.

## Intervir com intenção

**Ousar.** Identifique por que o alvo parece genérico: estrutura automática, escala tímida, imagem decorativa ou falta de ponto de vista. Faça um gesto estrutural completo e silencie seus concorrentes. Preserve o entorno no refinamento; não transforme “mais ousado” em nova identidade sem esse escopo.

**Acalmar.** Reduza estímulos concorrentes — saturação, peso, elementos, densidade, velocidade e deslocamento — onde atrapalham. Preserve um foco expressivo. Não transforme calma em texto pequeno, baixo contraste ou ausência de personalidade.

**Simplificar.** Corte redundância, decoração sem função e explicações que a fala ou notas já carregam. Divida raciocínio quando necessário, preservando tempo e continuidade. Não esconda qualificações, unidades, fonte ou contexto essenciais, nem transforme um deck curto em muitos slides vazios.

**Clarificar.** Reescreva títulos para dizer a ideia; apoio acrescenta informação em vez de repeti-la. Explique termos conforme o público. Controles nomeiam ações e estado; erros mostram recuperação. Preserve significado factual e condições dos dados. Texto acessível e notas não precisam obedecer à mesma concisão do título.

**Refinar.** Corrija inconsistências no nível certo: token ausente, implementação duplicada, estrutura inadequada ou defeito local. Confira alinhamentos ópticos, margens, cortes, entrelinha, ritmo, recortes, ícones, foco e final de animação. Refinamento não substitui o conceito nem muda fatos para encaixar o layout.

**Tipografia, cor e espaço.** Use [curadoria-tipografica.md](curadoria-tipografica.md), [repertorio-layouts.md](repertorio-layouts.md) e [direcao-e-acabamento.md](direcao-e-acabamento.md). Em melhorias locais, trabalhe primeiro com o sistema escolhido; se o pedido inclui novas fontes ou paleta, compare escolhas no conteúdo real e atualize o briefing.

**Coreografar e experimentar.** Traduza a ambição em uma cena ou passagem significativa. Compare técnicas com a pesquisa de [pesquisa-componentes.md](pesquisa-componentes.md), obrigatória para nova direção. Teste primeiro a cena mais exigente no palco real, valide sua contribuição e então integre. Preserve a escolha já dada; se a técnica falhar, adapte sem apagar a intenção ou fingir que foi implementada. Não acrescente áudio, autoplay ou interações de mouse que alterem o uso estabelecido apenas para impressionar.

**Variar.** Use a quantidade solicitada; quando omitida, duas ou três alternativas bastam. Diferencie estrutura, gesto ou enquadramento, mantendo conteúdo comparável. Mostre opções em arquivos ou cenas de comparação identificados, sem substituir a versão preservada. Não introduza um formulário adicional quando o usuário já delegou a escolha.

## Qualidade de implementação

**Adaptar ao destino.** Para projeção, teste de longe em tamanho equivalente e mantenha áreas seguras. Para leitura autônoma em celular, reordene, empilhe ou ofereça uma vista textual legível; diminuir um palco inteiro não basta. Para outro formato, recomponha e verifique crops e quebras. Mantenha ordem do DOM e foco coerentes, alvos de toque utilizáveis e controles fora de áreas essenciais.

**Robustecer.** Trate o que o deck realmente pode encontrar: carregamento de fontes/imagens, mídia falhando, texto longo, última/primeira cena, hash inválido, resize durante passagem, cliques rápidos, retorno, pausa, perda de contexto GPU e indisponibilidade de rede quando aplicável. Falha de um efeito não pode ocultar informação ou bloquear navegação. Não invente progresso de carregamento. Não corte texto essencial com ellipsis ou clamp para esconder overflow.

**Otimizar.** Meça antes de mexer: decodificação, tamanho de asset, trabalho por frame, pintura, layout ou loops. Agrupe leituras de medidas antes de escritas; evite recompor o DOM por frame. Limite DPR, áreas de filtro, número de partículas e contextos GPU conforme a evidência. Carregue assets críticos antes da passagem e libere recursos ao sair. Não declare 60 fps ou ganho percentual sem medir; testes em computador não comprovam fluidez em celular real.

**Consolidar.** Extraia cores semânticas, papéis de texto, margens, ritmo e contratos de movimento que realmente se repetem. Reutilize motor de navegação, botões e notas quando têm a mesma intenção; preserve composições específicas. Não crie um framework completo ou dezenas de variantes para uma exceção. Documente apenas decisões úteis no briefing ou código do projeto.

## Encerrar sem perder o foco

Uma primeira inspeção agrupada deve cobrir cenas, transições e tamanhos pertinentes; corrija achados juntos e confirme numa segunda. Encerre o polimento estético após essa confirmação. Problemas que bloqueiam uso ou requisitos precisam de correção e checks focados, sem reabrir a direção toda.

Registre mudanças e evidências no briefing existente; um relatório separado só quando fizer parte do pedido. Finalize com resultado, link e limitações concretas. Não adicione aprovações, menus ou chamadas a ferramentas de outra skill como etapa automática.
