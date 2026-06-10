# Playbooks de Resposta a Incidentes

Consulte este arquivo quando houver incidente em andamento ou quando o usuario estiver se preparando para um cenario especifico.

## Estrutura Base (NIST SP 800-61 Rev. 2)

Todo playbook segue o ciclo:

1. **Preparacao** — antes do incidente
2. **Deteccao e Analise** — identificar e triagear
3. **Contencao, Erradicacao e Recuperacao** — agir
4. **Atividade Pos-Incidente** — aprender

---

## Playbook 1 — Ransomware

### Deteccao
- Alertas EDR sobre criptografia em massa
- Arquivos com extensoes anomalas (.locked, .encrypted, etc)
- Nota de resgate (ransom note)
- Queda abrupta de servicos

### Contencao imediata (primeiros 60 minutos)
1. **NAO desligar** a maquina — preservar memoria volatil para forense
2. **Isolar** da rede (desconectar cabo ou desabilitar Wi-Fi, segregar VLAN)
3. **Desabilitar contas** comprometidas no IdP
4. **Rotacionar credenciais** de servicos afetados
5. **Ativar CSIRT** e acionar seguranca cibernetica (se contratada)
6. **Preservar evidencias** — memoria (volatility), disco (dd/FTK Imager), logs

### Decisoes criticas
- **NAO pagar resgate** como regra — nao ha garantia de recuperacao e financia crime organizado
- Avaliar obrigacoes regulatorias (LGPD art. 48 se ha dados pessoais afetados — **2 dias uteis para ANPD**)
- Notificar autoridades — Policia Federal, CERT.br (cert@cert.br)
- Comunicar stakeholders (C-level, juridico, relacoes publicas)

### Erradicacao e recuperacao
- Identificar vetor de entrada (phishing, vulnerabilidade explorada, credencial comprometida)
- Remover backdoors e persistencia
- Restaurar de backup imutavel **verificado como limpo**
- Rebuild completo se houver duvida
- Monitoramento reforcado por 30-90 dias pos-incidente

---

## Playbook 2 — Vazamento de Dados (Data Breach)

### Deteccao
- Monitoramento de dark web (HaveIBeenPwned, DarkOwl)
- Alerta de DLP
- Denuncia externa (pesquisador, cliente, imprensa)
- Anomalia em logs de acesso a banco de dados

### Primeiras 24 horas
1. **Confirmar** o vazamento — nao presumir, verificar
2. **Determinar escopo** — quantos titulares, quais dados, sensiveis ou nao?
3. **Isolar sistemas** afetados
4. **Preservar logs** e evidencias (write-once storage)
5. **Acionar juridico e DPO** — **prazo ANPD de 2 dias uteis ja correndo**
6. **Avaliar risco aos titulares** — dados sensiveis? Credenciais? Dados financeiros?

### Comunicacoes obrigatorias (LGPD art. 48)
- **ANPD**: formulario eletronico, 2 dias uteis
- **Titulares afetados**: se houver risco relevante aos direitos e liberdades, em prazo razoavel
- Conteudo da comunicacao (Resolucao CD/ANPD 15/2024 art. 5º):
  - Descricao do incidente
  - Dados afetados
  - Numero de titulares
  - Medidas adotadas
  - Riscos
  - Contato do encarregado

### Erradicacao
- Corrigir vulnerabilidade explorada
- Rotacionar todas as credenciais expostas
- Revogar tokens de sessao ativos
- Forcar reset de senha dos titulares afetados
- Monitorar uso indevido dos dados (cartoes, credenciais)

---

## Playbook 3 — DDoS

### Deteccao
- Latencia alta + indisponibilidade
- Trafego anomalo (volume, geografia, user-agent)
- Alertas de WAF/CDN/provedor cloud

### Contencao
1. **Ativar modo "under attack"** no CDN/WAF (Cloudflare, AWS Shield Advanced)
2. **Rate limiting** agressivo temporario
3. **Geoblocking** de regioes de origem se aplicavel
4. **Challenge** (CAPTCHA, JS challenge) em endpoints criticos
5. **Scale-up** de infraestrutura se for economico
6. **Acionar provedor** de anti-DDoS (AWS Shield, Cloudflare Magic Transit, Akamai)

### Analise
- L3/L4 (volumetrico): SYN flood, UDP flood, amplification
- L7 (aplicacao): HTTP flood, Slowloris, RUDY
- Identificar se e DDoS ou pico legitimo de trafego

### Pos-incidente
- Revisar capacidade de absorcao
- Implementar anti-DDoS permanente se ainda nao houver
- Exercicios de tabletop com time

---

## Playbook 4 — Credencial Comprometida

### Deteccao
- Login de geografia/horario anomalo
- Alerta UEBA de comportamento fora do padrao
- Credencial aparece em leak database
- Denuncia do proprio usuario

### Contencao imediata
1. **Revogar sessoes ativas** no IdP
2. **Desabilitar conta** temporariamente
3. **Rotacionar tokens** API/OAuth emitidos
4. **Auditar acoes recentes** da conta — o que foi acessado, modificado, baixado
5. **Verificar laterais** — a credencial foi usada em outros sistemas?

### Investigacao
- Timeline completa de atividades
- Identificar vetor: phishing, keylogger, reuso de senha, leak de terceiro
- Verificar privilegios da conta — dano potencial?

### Recuperacao
- Reset de senha com politica forte
- Forcar enrolment MFA se ainda nao tinha
- Treinamento antiphishing especifico para o usuario
- Se for conta administrativa: revisao de todas as acoes executadas no periodo suspeito

---

## Playbook 5 — Insider Threat

### Sinais de alerta
- Acesso a dados fora do escopo de funcao
- Download massivo de arquivos
- Uso de USB/cloud storage pessoal
- Atividade em horarios atipicos
- Recusa em tirar ferias (sinal classico de fraude)
- Funcionario em processo de demissao ou insatisfeito

### Protocolo diferenciado
1. **Envolvimento obrigatorio** de RH e Juridico desde o inicio
2. **NAO confrontar** o suspeito — preservar evidencias
3. **Monitoramento silencioso** autorizado formalmente por Juridico
4. **Evidencias**: logs de acesso, emails, atividade de endpoint (respeitando limites legais)
5. **Decisao coordenada** — demissao com justa causa, acao civel, criminal

### Contencao (no momento da acao)
- Revogar todos os acessos simultaneamente
- Coletar dispositivos corporativos
- Bloquear acesso fisico
- Rotacionar credenciais compartilhadas que o funcionario conhecia
- Auditoria completa de alteracoes feitas pelo individuo

---

## Playbook 6 — Supply Chain Attack

### Exemplos historicos
- SolarWinds (2020)
- Log4Shell (2021)
- 3CX (2023)
- xz-utils backdoor (2024)

### Deteccao
- CVE critica em dependencia em uso
- Alerta de threat intel sobre biblioteca/fornecedor
- Comportamento anomalo de servico que usa dependencia especifica

### Resposta
1. **Inventariar exposicao** via SBOM — onde a dependencia afetada esta em uso?
2. **Avaliar criticidade** — e exploravel no contexto? Internet-facing?
3. **Mitigar imediatamente** — WAF rule, feature flag, network isolation
4. **Patch** assim que disponivel — priorizar pelo blast radius
5. **IOCs** — buscar evidencias de exploracao anterior ao patch
6. **Comunicar** clientes se houver exposicao downstream

### Prevencao continua
- SBOM atualizado automaticamente
- Scanning de dependencias no CI/CD
- Assinatura de artefatos (Sigstore/Cosign)
- Pinning de versoes
- SLSA level 3+ para producao

---

## Comunicacao Durante Incidentes

### Interna
- **War room** dedicado (Slack channel, Teams, Meet permanente)
- **Comunicacao horaria** com C-level em incidentes criticos
- **Template de briefing**: o que aconteceu, escopo atual, acoes em andamento, proximos passos, ETA

### Externa
- **Porta-voz unico** (CISO ou porta-voz treinado)
- **Alinhamento juridico** antes de qualquer comunicacao publica
- **Transparencia sem exposicao desnecessaria** — informar fatos, nao especular

### Regulatoria
- ANPD — 2 dias uteis (incidentes com dados pessoais)
- B3/CVM — empresas listadas em caso de fato relevante
- Banco Central — instituicoes financeiras (Resolucao 4.893/2021 — 3 dias)
- CERT.br — incidentes de seguranca da internet brasileira

---

## Pos-Incidente

### Post-mortem (dentro de 1-2 semanas)
- **Blameless** — foco em processo, nao em individuos
- Timeline factual
- Root cause analysis (5 whys, Ishikawa)
- Gaps identificados
- Action items com responsaveis e prazos
- Metricas: MTTD, MTTR, numero de titulares afetados, custo estimado

### Atualizacoes
- Atualizar playbooks com licoes aprendidas
- Ajustar deteccoes (novas regras SIEM/EDR)
- Treinamentos adicionais para o time
- Tabletop exercise do cenario real em 60-90 dias
