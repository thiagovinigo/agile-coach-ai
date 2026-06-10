# LGPD e Analytics — Conformidade para Coleta de Dados

> Última atualização: Mai/2026.
> Fontes: ANPD, Alura, Confidata, E-Commerce Brasil, LEC, Google Cloud LGPD.

---

## O que é a LGPD

A **Lei Geral de Proteção de Dados** (Lei nº 13.709/2018) regula o tratamento de dados pessoais no Brasil. Entrou em vigor em setembro de 2020, com sanções desde agosto de 2021.

**Órgão regulador:** ANPD — Autoridade Nacional de Proteção de Dados

**Penalidades:**
- Advertência com prazo para medidas corretivas
- Multa de até 2% do faturamento no BR, limitada a R$50 milhões por infração
- Publicização da infração (dano reputacional)
- Bloqueio ou eliminação dos dados

---

## Dados Pessoais e Analytics

### O que é Dado Pessoal segundo a LGPD
Qualquer informação que identifique ou possa identificar uma pessoa natural:
- Nome, CPF, email, telefone
- Endereço IP (**é dado pessoal**)
- Cookie ID (**é dado pessoal**)
- ID de dispositivo
- Localização geográfica precisa
- Combinação de dados que identifique alguém (fingerprinting)

### Dados Sensíveis (proteção reforçada)
- Saúde e vida sexual
- Origem racial ou étnica
- Convicções religiosas ou políticas
- Dados genéticos ou biométricos

**Analytics raramente coleta sensíveis, mas:** cruzamento de dados pode criar perfil sensível indiretamente.

---

## Bases Legais para Coleta em Analytics

A LGPD define 10 bases legais. Para analytics de marketing, as principais são:

| Base Legal | Quando Usar | Cuidados |
|---|---|---|
| **Consentimento** | Cookies analíticos, publicidade | Deve ser livre, informado, específico e inequívoco |
| **Legítimo Interesse** | Analytics essencial (segurança, prevenção de fraudes) | Requer LIA (Legitimate Interest Assessment) |
| **Execução de Contrato** | Analytics para clientes logados com contrato | Limitado a dados necessários para o serviço |

**Atenção:** A ANPD publicou em 2022 que **cookies de analytics de marketing exigem consentimento** — não se enquadram em legítimo interesse automaticamente.

---

## Consentimento de Cookies: Como Implementar

### Requisitos do Guia ANPD (2022)
A ANPD estabeleceu padrões claros:

1. **Granularidade:** Consentimento separado por categoria (essencial, analítico, marketing)
2. **Opção de recusar:** Deve existir e ser tão fácil quanto aceitar
3. **Sem dark patterns:** Botão "Aceitar tudo" destacado e "Recusar" escondido é irregular
4. **Informação clara:** Quais dados, para quê, por quanto tempo, com quem compartilhados
5. **Revogação fácil:** Usuário deve poder mudar consentimento a qualquer momento
6. **Registro:** Guardar evidência do consentimento (quem, quando, o quê)

### Boas Práticas de Banner de Cookies

**Conforme LGPD:**
```
Banner com 3 opções claramente visíveis:
[ Aceitar Essenciais Apenas ] [ Personalizar ] [ Aceitar Todos ]

Categorias disponíveis:
✓ Essenciais (não podem ser desativados)
☐ Analytics (Google Analytics, Hotjar)
☐ Marketing (Meta Pixel, Google Ads)
☐ Personalização (chatbots, preferências)
```

**Ferramentas de CMP (Consent Management Platform):**
- Cookiebot (boa integração BR)
- OneTrust (enterprise)
- Complianz (WordPress)
- CookieYes
- Iubenda

---

## Google Analytics 4 e LGPD

### O que o GA4 coleta por padrão
- ID de cookie anônimo
- Tipo de dispositivo, browser, SO
- Localização aproximada (cidade, não GPS)
- Sessões, páginas, eventos de interação
- **Não** coleta endereço IP completo (anonimização automática desde GA4)

### Configurações de Privacidade Obrigatórias no GA4

**1. Anonymize IP (já padrão no GA4)**
GA4 não armazena IPs completos. Mas verifique nas configurações.

**2. Desativar Sinais do Google (Google Signals)**
Se não precisa de dados demográficos cruzados:
Admin → Configurações da Conta → Coleta de Dados de Google → Desativar

**3. Retenção de Dados**
Admin → Configurações de Dados → Retenção de Dados → Recomendado: 14 meses máximo

**4. Consent Mode v2 (Obrigatório para Ads)**
```javascript
// Configuração padrão — antes de qualquer tag
gtag('consent', 'default', {
  'analytics_storage': 'denied',
  'ad_storage': 'denied',
  'ad_user_data': 'denied',
  'ad_personalization': 'denied',
  'wait_for_update': 500
});

// Após consentimento do usuário
gtag('consent', 'update', {
  'analytics_storage': 'granted',
  'ad_storage': 'granted'
});
```

**5. DPA (Data Processing Agreement)**
Assine o acordo de processamento de dados com o Google:
Admin → Conta → Termos de Privacidade dos Dados

### Consent Mode v2 — Impacto nos Dados
Com Consent Mode ativo:
- Usuários que recusam cookies: dados modelados (não reais) no GA4
- Queda típica de 20-40% em dados reportados
- Google usa modelagem de conversão para estimar o que não foi coletado
- Para Google Ads: obrigatório a partir de março 2024

---

## Meta Pixel e LGPD

### Configurações Necessárias
1. **Advanced Matching:** Desativar ou usar apenas com consentimento explícito
2. **Automatic Events:** Revisar quais eventos são disparados
3. **Conversions API (CAPI):** Processamento server-side com dados apenas de usuários que consentiram

### Dados a NÃO enviar para Meta sem consentimento
- Email hash
- Telefone hash
- Nome e sobrenome
- Localização

---

## Mapeamento de Dados — Etapas Práticas

### 1. Inventário de Cookies
Liste todos os cookies do site:
- Nome do cookie
- Finalidade
- Duração
- Terceiro envolvido
- Base legal

### 2. Atualizar Política de Privacidade
Deve conter obrigatoriamente:
- Quais dados são coletados
- Finalidade do tratamento
- Com quem são compartilhados
- Direitos do titular
- Como exercer esses direitos
- Encarregado (DPO) — obrigatório para empresas de médio/grande porte

### 3. Direitos do Titular
A LGPD garante ao usuário:
- Acesso aos dados
- Correção de dados incorretos
- Eliminação dos dados
- Portabilidade
- Revogação do consentimento
- Informação sobre compartilhamento

Implemente formulário/processo para exercer esses direitos.

---

## Checklist de Conformidade para Analytics

- [ ] Banner de cookies com granularidade por categoria
- [ ] Botão de recusar tão acessível quanto aceitar
- [ ] Cookies carregam SOMENTE após consentimento
- [ ] Consent Mode v2 implementado no GTM/GA4
- [ ] GA4 com retenção de dados em 14 meses
- [ ] Google Signals desativado (se não necessário)
- [ ] DPA assinado com Google
- [ ] Meta Pixel com Consent Mode configurado
- [ ] Política de Privacidade atualizada e acessível
- [ ] Processo para atender direitos do titular
- [ ] Registro de consentimentos armazenado

---

## Referências

- [Guia ANPD — Cookies e Proteção de Dados](https://gcaa.com.br/guia-orientativo-da-anpd-cookies-e-protecao-de-dados-pessoais/)
- [LGPD e Google Analytics — Alura](https://www.alura.com.br/artigos/lgpd-google-analytics-como-se-adequar)
- [GA4 Cookieless — E-Commerce Brasil](https://www.ecommercebrasil.com.br/artigos/ga4-cookieless-lgpd-nao-e-desculpa-para-analytics-ruim)
- [Orientações ANPD Cookies — LEC](https://lec.com.br/guia-orientativo-da-anpd/)
- [LGPD Compliance — Google Cloud](https://cloud.google.com/security/compliance/lgpd)
