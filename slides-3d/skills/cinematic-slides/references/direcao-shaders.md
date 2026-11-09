# Shaders como linguagem de apresentação

Procure oportunidades reais ao longo do deck, não apenas na capa ou na troca final. Um shader pode criar presença, revelar informação ou tornar uma relação visível. A ambição deve alcançar mais de uma cena quando houver espaço didático, sem aplicar o mesmo preset a tudo.

## Mapear oportunidades antes de escolher bibliotecas

Para cada cena, pergunte: qual fenômeno, material, escala ou revelação reforçaria sua mensagem? Considere atmosfera, entrada, explicação e passagem separadamente. Compare pelo menos duas propostas de shader com funções distintas quando o conceito permitir; registre candidatos e recusas em `component-research.md`. Pesquise exemplos específicos no catálogo de [pesquisa-componentes.md](pesquisa-componentes.md), não apenas termos genéricos.

| Oportunidade | Gesto possível | Proteção didática |
| --- | --- | --- |
| Luz em profundidade | Feixes suaves atravessam planos e revelam o ambiente. | Recortar fora do texto; não gerar clarões repetidos. |
| Névoa e presença | Campo de densidade se dissipa, conduzindo ao sujeito. | Revelação termina; não manter o animal encoberto durante explicação. |
| Água e reflexo | Caústicas ou distorção restrita à superfície da água. | Máscara preserva rosto, anatomia e legenda; não deformar a foto inteira. |
| Percepção | Campo visual, pulso ou varredura destaca a região explicada. | Identificar como pista esquemática; não alegar visão fisiológica real. |
| Território e percurso | Contornos ou textura procedural respondem ao caminho revelado. | Valores, rota e rótulos ficam legíveis; distinguir esquema de mapa medido. |
| Material de um produto | Refração, rugosidade, metal ou iluminação revela forma. | Manter geometria e propriedades verdadeiras; separar conceito de produto real. |
| Forma e transformação | Campo de distância transforma uma forma em outra ideia. | Correspondência clara, sem substituir argumento por abstração incompreensível. |
| Revelação por textura | Limiar de luminosidade, dissolução orgânica ou máscara mostra a mídia. | A mídia só começa a aparecer na entrada; sem revelar e depois reiniciar. |
| Conexão entre cenas | Luz, grão material ou forma transporta a atenção. | Shader de passagem separado; termina em superfície vazia, não no próximo slide completo. |

Estas são hipóteses de direção, não alegações sobre componentes disponíveis nem um pacote obrigatório para toda apresentação. Para uma floresta, luz entre folhas, reflexo restrito à água e contornos do território podem compartilhar temperatura e ritmo sem fazer o mesmo trabalho.

## Dar autoria e variar intensidade

- Não encerre a curadoria depois do primeiro Ripple ou gradiente. Explore o repertório e crie uma segunda intervenção quando ela acrescentar um papel diferente à história.
- Prefira uma família visual comum: frequências, cores, luz e ritmo relacionados. A variedade vem da função, máscara, área e intensidade, não de estilos aleatórios.
- Separe momentos de descoberta de momentos de explicação. O efeito pode ser rico na entrada e assentar em uma textura estática ou movimento periférico muito discreto na leitura.
- Proteja áreas de texto por máscara, posição, opacidade ou composição. Evite variações de brilho sob as letras, movimento constante no foco de leitura e filtros sobre gráficos quantitativos.
- Não exija 3D onde uma técnica 2D produz o gesto. Materiais ou câmeras que precisam de geometria e múltiplos ângulos exigem assets adequados; não simule uma promessa impossível com uma foto plana.

## Contrato técnico por intervenção

No storyboard, registre:

`cena | função | área/máscara | fonte da técnica | fase de início | estado inicial dos uniforms | duração | estado de leitura | pausa/limpeza | fallback`

Um shader de conteúdo só fica visível na fase de entrada definida em [ciclo-de-cena.md](ciclo-de-cena.md). Antes de mostrar o Canvas, inicialize programa, texturas e uniforms em revelação zero/alpha zero ou outro estado oculto adequado. O primeiro desenho visível não pode ser o estado final. A timeline da cena controla progresso; não crie um relógio independente que comece na montagem da página.

Um shader de passagem vive numa camada separada. Encerrada a passagem, limpe essa camada, apresente a superfície vazia e só então inicie o shader de conteúdo, se houver. Não reaplique o shader de passagem como animação de entrada do mesmo material.

Controle resolução, DPR, frequência de desenho, número de contextos e descarte de recursos pelo custo observado. Pause fora da cena, em pausa explícita e quando a página ficar oculta. Prefira estado final estático quando movimento contínuo não acrescentar significado. Ausência de WebGL/WebGPU, perda de contexto, erro de compilação ou textura indisponível precisam de alternativa legível.

## Julgar no palco real

Veja a cena com fontes e imagens finais, em movimento e durante a leitura. Verifique ordem, contraste e contribuição ao entendimento antes de espalhar o efeito por outras cenas. Um programa compilado não prova valor visual. Se prejudicar a didática, ajuste a área, intensidade ou duração antes de descartá-lo; a primeira tentativa ruim não encerra a exploração criativa.

Não declare desempenho de dispositivo que não testou. Registre limitações reais e preserve as informações sob movimento reduzido. Mais shaders devem significar mais oportunidades bem dirigidas, não mais motores concorrentes ou distrações.
