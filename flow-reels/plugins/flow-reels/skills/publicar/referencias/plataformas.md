# Plataformas, mídia e agendamento

Tudo aqui é `POST /posts`. O que muda por destino é o bloco `platformSpecificData` e o que conta como
mídia aceitável. **Este arquivo é o dono da matriz por plataforma, das regras de mídia e das regras
de horário.** Não copie nenhum destes valores para outro arquivo.

## O envelope

```json
{
  "content": "o texto do post (no YouTube, a descrição)",
  "mediaItems": [{ "type": "video", "url": "https://…" }],
  "platforms": [
    { "platform": "instagram", "accountId": "…", "platformSpecificData": { } }
  ],
  "scheduledFor": "2026-09-22T18:00:00",
  "timezone": "America/Sao_Paulo",
  "publishNow": true,
  "isDraft": true
}
```

Os nomes dos campos são os da API, então eles ficam em inglês: é o formato do fio, não um parâmetro
nosso.

`content` é obrigatório mesmo quando vazio. `scheduledFor` e `publishNow` são alternativas: mande um
ou outro, nunca os dois. `isDraft` cria sem publicar nem agendar, e é o modo seguro para olhar no
painel antes.

## Matriz do Instagram e do YouTube

| O que é | `platform` | `platformSpecificData` | Mídia |
|---|---|---|---|
| Reel | `instagram` | `{ "contentType": "reel", "shareToFeed": true, "instagramThumbnail": "<url da capa>" }` | 1 vídeo |
| Carrossel | `instagram` | nenhum | 2 a 10 itens, na ordem do array |
| Imagem no feed | `instagram` | nenhum | exatamente 1 imagem |
| Story | `instagram` | `{ "contentType": "story" }` | 1 item |
| Short | `youtube` | `{ "contentType": "short", "title": "até 100 caracteres", "visibility": "public" }` | 1 vídeo vertical |
| Vídeo comum | `youtube` | `{ "title": "…", "visibility": "public", "tags": "a, b, c", "firstComment": "…" }` | 1 vídeo |

Detalhe que parece bug e não é: o enum de `contentType` do Instagram aceita **só** `story`. Um post
sem `contentType` vira Reels ou feed dependendo da mídia, então carrossel e imagem de feed usam o
mesmo payload, mudando só a quantidade de itens. Por isso um carrossel com um slide só publica como
post de feed sem avisar, e por isso vale contar os itens antes.

`instagramThumbnail` é a capa do Reel, em JPEG ou PNG numa URL pública. **Short do YouTube não aceita
capa própria**, então não prometa uma. No YouTube, o `content` vira a descrição e o `title` é
obrigatório.

## Outras redes

A mesma chamada atende `linkedin`, `twitter`, `threads`, `tiktok`, `facebook`, `bluesky`,
`pinterest`, `reddit`, `telegram`, `google-business` e `snapchat`. Duas particularidades úteis:

- **Thread no Twitter/X e no Threads**: `platformSpecificData.threadItems` é um array de
  `{ "content": "…" }`. O `content` do topo continua obrigatório e costuma repetir o primeiro item.
- **Mesmo conteúdo em várias redes**: um array `platforms` com várias entradas publica o mesmo
  `content` em todas, cada uma com o seu `accountId` e o seu bloco específico. O hábito é uma
  plataforma por chamada, porque os metadados são diferentes.

## Mídia

A Zernio busca o arquivo pela URL, então ela precisa ser um **arquivo público direto**. Página de
serviço de nuvem, ou qualquer endereço que responda HTML, é recusada.

Para subir um arquivo local:

```bash
flow-reels publicar/zernio midia projetos/<video>/corte-01/corte-01.mp4
```

Por baixo: `POST /media/presign` com `{ filename, contentType }`, `PUT` dos bytes na `uploadUrl`
devolvida, com o `Content-Type` certo e sem header de autorização, e a `publicUrl` da resposta é o
que entra em `mediaItems`.

O corte que sai deste pacote já nasce no formato certo: vertical 1080x1920, H.264 com áudio AAC.
Nada precisa ser reprocessado antes de subir.

## Horário

`scheduledFor` é ISO **local, sem sufixo de fuso**, acompanhado de `timezone` IANA. Mandar
`2026-09-22T18:00:00Z` junto com `timezone` é pedir confusão.

```json
{ "scheduledFor": "2026-09-22T18:00:00", "timezone": "America/Sao_Paulo" }
```

Publicar agora é `publishNow: true`, e **não tem volta**. Rascunho é `isDraft: true`.

A Zernio recusa **conteúdo duplicado dentro de 24 horas**. Republicar o mesmo corte com a mesma
legenda no mesmo dia não passa, e a resposta diz isso.

## Depois de publicar

```bash
flow-reels publicar/zernio situacao <postId>
```

O status e a atribuição vivem em `post.platforms[]`, com `status`, `platformPostId` e
`platformPostUrl` por plataforma. Enquanto o post não publicou, `platformPostUrl` vem vazio. Post
apagado na mão dentro da Zernio responde 404 no `GET /posts/{id}`.
