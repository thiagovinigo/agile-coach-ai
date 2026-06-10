# Dominios Tecnicos — Referencia Detalhada

Consulte este arquivo quando a demanda envolver analise profunda de um dominio especifico.

## 1. Conformidade e Governanca

- **LGPD (Lei 13.709/2018)**: bases legais (art. 7º e 11), direitos do titular (art. 18), RIPD/DPIA (art. 38), encarregado/DPO (art. 41), comunicacao de incidentes a ANPD (art. 48 + Resolucao CD/ANPD 15/2024 — prazo de 2 dias uteis), tratamento de dados sensiveis (art. 11), transferencia internacional (art. 33-36)
- **GDPR** para operacoes internacionais — atencao a artigo 33 (72h para notificacao)
- **Frameworks**: ISO 27001/27002 (gestao), NIST CSF 2.0 (Govern/Identify/Protect/Detect/Respond/Recover), CIS Controls v8 (18 controles priorizados), SOC 2 Type II (auditoria de controles)
- **Marco Civil da Internet** (Lei 12.965/2014) e resolucoes ANPD complementares

## 2. Seguranca de Dados

- **Classificacao**: publico, interno, confidencial, restrito, sensivel LGPD
- **Criptografia em repouso**: AES-256, TDE em bancos, disk encryption (LUKS, BitLocker)
- **Criptografia em transito**: TLS 1.3 (deprecar 1.0/1.1), mTLS entre servicos, HSTS obrigatorio
- **Gestao de chaves**: KMS (AWS KMS, GCP KMS, Azure Key Vault), HSM para cargas criticas, rotacao automatica, envelope encryption
- **Mascaramento, tokenizacao e pseudonimizacao** — usar para ambientes de desenvolvimento e analytics
- **DLP** em endpoint (CrowdStrike, Microsoft Purview), rede (Forcepoint, Symantec) e cloud (Cloud DLP, Nightfall)
- **Backup 3-2-1-1-0**: 3 copias, 2 midias diferentes, 1 offsite, 1 imutavel/air-gapped, 0 erros em testes de restore
- **Retencao e descarte seguro**: NIST SP 800-88, DoD 5220.22-M, direito ao esquecimento (LGPD art. 18, VI)

## 3. Gestao de Identidade e Acesso (IAM)

- **Principio do menor privilegio** e need-to-know
- **MFA obrigatorio** para acessos administrativos e remotos — TOTP, WebAuthn/FIDO2, NUNCA SMS para cargas criticas
- **SSO**: SAML 2.0, OAuth 2.1, OIDC
- **RBAC vs ABAC**: RBAC para simplicidade, ABAC para granularidade contextual
- **PAM**: CyberArk, Delinea, HashiCorp Boundary — com session recording e approval workflows
- **Zero Trust Architecture** (NIST SP 800-207): never trust, always verify
- **JIT/JEA**: Just-in-Time access e Just-Enough-Access — acessos temporarios com expiracao automatica
- **Revisao trimestral** de acessos, offboarding automatizado via IdP, joiners/movers/leavers

## 4. Hardening de Servidores

- **CIS Benchmarks** por SO (Ubuntu, RHEL, Windows Server, Kubernetes, Docker)
- **Desabilitacao** de servicos, portas e protocolos desnecessarios
- **SSH seguro**: chaves ao inves de senha, porta nao-padrao (defense in depth, nao seguranca por obscuridade), fail2ban/CrowdSec, `PermitRootLogin no`, `PasswordAuthentication no`
- **Firewall de host**: iptables/nftables, ufw, Windows Firewall — default deny
- **SELinux/AppArmor** em modo enforcing
- **Patch management com SLA**: critico ≤72h, alto ≤7d, medio ≤30d, baixo ≤90d
- **Segregacao de redes**: VLAN, subnets, bastion hosts, jump servers
- **Time sync (NTP)** para forense confiavel — logs com timestamps consistentes

## 5. Seguranca de Aplicacao

- **OWASP Top 10 Web 2021**: A01 Broken Access Control, A02 Cryptographic Failures, A03 Injection, A04 Insecure Design, A05 Security Misconfiguration, A06 Vulnerable Components, A07 Auth Failures, A08 Software/Data Integrity Failures, A09 Logging Failures, A10 SSRF
- **OWASP API Top 10 2023**: focar em BOLA (Broken Object Level Auth) e Broken Authentication
- **SAST** (SonarQube, Semgrep, Checkmarx), **DAST** (OWASP ZAP, Burp Suite), **SCA** (Snyk, Dependabot, Trivy), **IAST** (Contrast Security)
- **WAF**: Cloudflare, AWS WAF, ModSecurity com OWASP CRS
- **Rate limiting**, throttling e protecao contra DDoS L3/L4 (Cloudflare, AWS Shield) e L7 (WAF)
- **Secrets management**: HashiCorp Vault, AWS Secrets Manager, Doppler, Infisical — **nunca em codigo, .env commitado ou variaveis de CI plaintext**
- **Security headers**: CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy
- Validacao de entrada, output encoding, prepared statements, ORMs parametrizados
- Protecao contra SSRF (allowlists), IDOR (autorizacao contextual), mass assignment (DTOs explicitos), deserializacao insegura

## 6. Ciberseguranca Operacional

- **Threat modeling**: STRIDE (Microsoft), PASTA (risk-centric), DREAD (legacy), Attack Trees
- **MITRE ATT&CK** para mapeamento de TTPs adversariais — usar matriz Enterprise para corporativo, Cloud para SaaS/IaaS
- **SIEM**: Wazuh (open-source), Splunk, Elastic SIEM, Microsoft Sentinel — com correlacao de eventos
- **EDR/XDR**: CrowdStrike Falcon, SentinelOne, Microsoft Defender for Endpoint
- **SOC 24×7** interno ou MSSP (Managed Security Service Provider)
- **Threat intelligence feeds**: MISP, OpenCTI, AlienVault OTX, commercial (Recorded Future, Mandiant)
- **UEBA** — deteccao de anomalias comportamentais (Exabeam, Securonix)
- **Honeypots e deception** quando aplicavel (T-Pot, Thinkst Canary)

## 7. Testes Ofensivos

Distincao critica — NAO sao a mesma coisa:

- **Vulnerability Assessment**: scan automatizado, Nessus/Qualys/OpenVAS, cadencia mensal/trimestral
- **Pentest**: exploracao manual controlada, black/gray/white box, escopo + rules of engagement formais
- **Red Team**: simulacao de adversario real, multiplos vetores, objetivos de impacto, sem aviso a blue team

Metodologias: PTES (Penetration Testing Execution Standard), OSSTMM, NIST SP 800-115, OWASP WSTG

Ferramentas principais: Nmap, Burp Suite Pro, Metasploit, Nessus, OWASP ZAP, BloodHound (AD), Impacket, CrackMapExec, Nuclei

Entregaveis: relatorio executivo (impacto de negocio) + relatorio tecnico (PoC, CVSS 3.1, remediacao)

Cadencia minima: pentest anual + a cada mudanca significativa de arquitetura. Bug bounty (HackerOne, BugCrowd) para cobertura continua.

## 8. Resposta a Incidentes (IR)

Playbooks detalhados em `playbooks-ir.md`. Ciclo NIST SP 800-61:

1. **Preparacao** — CSIRT, runbooks, ferramentas prontas
2. **Identificacao** — deteccao + triagem
3. **Contencao** — short-term (isolar) + long-term (patch/rebuild)
4. **Erradicacao** — remover root cause
5. **Recuperacao** — restaurar operacao normal com monitoramento reforcado
6. **Licoes Aprendidas** — post-mortem sem blame

**Comunicacao a ANPD em ate 2 dias uteis** em caso de incidente com dados pessoais. Comunicacao a titulares afetados conforme art. 48 LGPD.

Forense digital com cadeia de custodia preservada (hash MD5/SHA-256, write-blockers, documentacao).

## 9. DevSecOps

- **Shift-left** security no SDLC — achar bugs cedo e barato
- **Security gates no CI/CD**: falha do build em CVE critica (CVSS ≥9.0)
- **Container security**: imagens base minimas (distroless, alpine, chainguard), scanning (Trivy, Grype, Clair), runtime security (Falco, Tetragon)
- **IaC security**: Checkov, tfsec, KICS, Terrascan para Terraform/Ansible/Kubernetes/CloudFormation
- **Supply chain**: SBOM (CycloneDX, SPDX), assinatura de artefatos (Sigstore/Cosign), SLSA framework (niveis 1-4), in-toto attestations
- **Dependencias**: Renovate/Dependabot + politica de atualizacao com SLA
- **Branch protection**: require PR reviews, signed commits, status checks

## 10. Seguranca em Cloud

- **Shared Responsibility Model**: entender onde termina a responsabilidade do provedor (AWS, GCP, Azure) e comeca a do cliente
- **CSPM**: Prisma Cloud, Wiz, Lacework, Orca — deteccao de misconfig
- **CIEM**: identificar permissoes excessivas em IAM cloud (over-privileged roles)
- **Segregacao** por contas/projetos/subscriptions — nunca misturar producao e desenvolvimento
- **VPC design**: subnets privadas para cargas sensiveis, security groups restritivos, NACLs como defesa em profundidade, VPC endpoints/PrivateLink
- **Logs centralizados**: CloudTrail + Config (AWS), Audit Logs (GCP), Activity Logs (Azure) — retencao minima 1 ano, preferencialmente em conta separada imutavel
- **Cloud-specific**: GuardDuty (AWS), Security Command Center (GCP), Defender for Cloud (Azure)
