# Avaliação de Segurança (Security Review)

## 1. Dados e Privacidade
- [ ] Quais dados sensíveis (PII, credenciais, financeiros) esta feature manipula?
- [ ] Como os dados estão sendo criptografados em repouso (In-rest)?
- [ ] Como os dados estão sendo criptografados em trânsito (In-transit)?
- [ ] O acesso aos dados segue o Princípio do Menor Privilégio?

## 2. Autenticação e Autorização
- [ ] O endpoint/recurso está devidamente protegido contra acessos anônimos não intencionais?
- [ ] A autorização de nível de objeto (BOLA/IDOR) foi implementada e testada?
- [ ] Tokens de sessão (ex: JWT) têm expiração curta e estão sendo armazenados de forma segura (HttpOnly cookies, não em LocalStorage)?

## 3. Prevenção de Injeções (OWASP Top 10)
- [ ] As entradas de dados do usuário estão sendo validadas e sanitizadas no Backend?
- [ ] Consultas ao banco de dados estão usando Prepared Statements / Queries Parametrizadas (contra SQLi)?
- [ ] A saída de dados na interface está sendo escapada para prevenir XSS (Cross-Site Scripting)?
- [ ] Comandos de sistema operacional ou chamadas a processos estão imunes a Command Injection?

## 4. Configuração de Segurança e Dependências
- [ ] Headers de segurança (CORS, CSP, HSTS, X-Frame-Options) estão configurados corretamente?
- [ ] Existe controle de taxa (Rate Limiting) para prevenir ataques de força bruta ou DoS?
- [ ] As bibliotecas de terceiros inseridas não possuem vulnerabilidades conhecidas (CVEs)?
- [ ] Foram deixados hardcoded secrets (chaves de API, senhas) no código fonte?

## 5. Auditoria e Logs
- [ ] Operações críticas estão gerando logs de auditoria claros?
- [ ] Os logs garantem que NENHUM dado sensível (senhas, cartões) está sendo escrito neles?

## 6. Aprovação de Segurança
- **Avaliador:** [Nome/Papel]
- **Status:** [Aprovado / Requer Ajustes / Reprovado]
- **Observações:** [Detalhes adicionais]
