# A API da Zernio, endpoint a endpoint

Base: `https://zernio.com/api/v1`, header `Authorization: Bearer $ZERNIO_API_KEY` e
`Content-Type: application/json`. O script `scripts/zernio.py` fala só com estes endpoints, e
`api <METODO> <caminho>` abre qualquer outro quando for preciso investigar.

Uma base diferente entra por `ZERNIO_API_BASE`, no `.env`. Serve para host alternativo e para teste,
e o `checar` mostra qual base está valendo.

## Contas e perfis

| Chamada | Para quê |
|---|---|
| `GET /accounts` | contas conectadas. É daqui que saem `ZERNIO_IG_ACCOUNT_ID` e `ZERNIO_YT_ACCOUNT_ID` |
| `GET /profiles` | perfis do workspace. O `profileId` é **obrigatório** no create da automação, e não aparece em lugar nenhum além daqui |

Os objetos vêm com `_id`. O script resolve o perfil uma vez, preferindo o que contém a conta do
Instagram, e `ZERNIO_PROFILE_ID` sobrepõe a escolha.

## Posts

| Chamada | Notas |
|---|---|
| `POST /posts` | a mídia tem que ser arquivo público direto, e conteúdo duplicado recente é recusado (a janela está em `plataformas.md`) |
| `GET /posts/{id}` | status e atribuição em `post.platforms[]`: `platform`, `status`, `platformPostId`, `platformPostUrl`, `publishedAt` |
| `GET /posts` | lista |
| `POST /media/presign` | `{ filename, contentType }` devolve `uploadUrl` e `publicUrl`. O `PUT` dos bytes vai sem header de autorização |

O payload e a matriz por plataforma estão em `plataformas.md`, que é o dono deles.

## Automações de comentário

| Chamada | Notas |
|---|---|
| `POST /comment-automations` | exige `profileId`, `accountId` e `name`. `dmMessage` é **string pura**. Sem `platformPostId`, a automação vale para a conta inteira |
| `GET /comment-automations` | lista, e é como se sabe quais palavras já estão tomadas |
| `GET /comment-automations/{id}` | leitura de volta, com `dmMessage` e `commentReply` como strings no topo do objeto |
| `PATCH /comment-automations/{id}` | aceita `isActive`, `dmMessage`, `name`, `keywords`, `matchMode`, `buttons`, `followGate`, `audience`, `dmDelaySeconds`, `dmMessageVariations` |

Aposentar é sempre `PATCH isActive: false`. Nunca `DELETE`, pelo motivo que está em `funil-dm.md`.

O shape do create, como o script manda:

```json
{
  "profileId": "…", "accountId": "…",
  "name": "Funil - guia",
  "trigger": "comment",
  "keywords": ["guia"],
  "matchMode": "word",
  "typoTolerance": true,
  "commentReply": "Mandei na sua DM, da uma olhada.",
  "dmMessage": "Oi! … https://…/guia.pdf …"
}
```

A resposta traz o objeto inteiro em `{ success, automation: { id, name, platform, trigger, keywords,
matchMode, typoTolerance, dmMessage, commentReply, isActive, stats, createdAt } }`.

Existem campos que o fluxo padrão não liga: `buttons` (de 1 a 3, dos tipos `postback` e `url`),
`followGate` nativo, `audience` filtrando por status de seguidor e `alsoMatchInDms`. Nenhum deles é
necessário para entregar um link na DM, e cada um ligado é mais uma coisa que pode quebrar sem
aviso.

## Comportamentos que mudam decisão

- **Dedupe por usuário.** Quem já recebeu DM daquela automação fica `skipped` num comentário novo.
  Um teste com a mesma conta de sempre parece quebrado sem estar.
- **Conteúdo duplicado recente é recusado** no `POST /posts`. A janela mora em `plataformas.md`.
- **A atribuição do post** (id e url nativos) vive em `post.platforms[]`, e não num bloco de
  analytics.

Estes três vieram da observação da API em uso, não de uma medição feita aqui. Se algum deles
contradisser o que a API responder na sua conta, o que a API responde ganha, e o lugar de corrigir é
este arquivo.

## O que este pacote não usa

A Zernio tem `/workflows`, que são conversas de vários passos com grafo de nós, e o painel dela tem
sequências e automações de DM. Nada disso entra aqui: o funil deste pacote é **um objeto só**, a
automação de comentário, que responde em público e entrega o link na primeira DM.

Construir um workflow para entregar o mesmo link em dois passos adiciona um objeto que nasce em
rascunho, um botão cujo título vira chave de roteamento, e um jeito novo de o funil ficar mudo sem
ninguém perceber. Se um fluxo de vários passos for mesmo necessário um dia, ele se monta no painel
da Zernio, com os olhos na tela.
