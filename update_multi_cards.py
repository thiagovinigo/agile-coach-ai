import re
import json

path = 'c:/Users/User/.antigravity/Agile Coach AI/fluxo_ia.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# I will just write a python script to replace the text in the file.
# Since it's easier to manipulate strings directly using a simple text replacement for each step.

content = content.replace(
    """{ id: 101, title: "Login via OTP", tags: ["Business", "Epic: Security"] },
        { id: 102, title: "Perfil do Usuário", tags: ["UX", "Epic: Core"] }""",
    """{ id: 101, title: "Login via OTP", tags: ["Business", "Sec"] },
        { id: 103, title: "Dashboard Vendas", tags: ["Business", "BI"] },
        { id: 102, title: "Perfil do Usuário", tags: ["UX", "Bloqueado"] },
        { id: 104, title: "Exportar PDF", tags: ["New", "Fila"] }"""
)

content = content.replace(
    """[MCP: Azure DevOps] 2 itens encontrados no estado 'New'.
- Avaliando #101: Tags [Business] (Aprovado)
- Avaliando #102: Tags [UX] (Ignorado pelas regras de negócio atuais)
[Kiro Action] Movendo #101 para coluna 'Ref. Funcional (IA)'.""",
    """[MCP: Azure DevOps] 4 itens encontrados no estado 'New'.
- Avaliando #101: Tags [Business] -> PULL OK.
- Avaliando #103: Tags [Business] -> PULL OK.
- Avaliando #102: Tags [UX] -> Ignorado (Regra: Requer anexo de Design).
- Avaliando #104: -> Ignorado (Lote cheio / Added Later).
[Kiro Action] Movendo #101 e #103 para coluna 'Ref. Funcional (IA)'. Restante continua na fila."""
)

content = content.replace(
    """cards: [
        { id: 101, title: "Login via OTP", tags: ["AI-Guided", "Gerando PRD"] }
      ]""",
    """cards: [
        { id: 101, title: "Login via OTP", tags: ["AI-Guided", "Lote 1"] },
        { id: 103, title: "Dashboard Vendas", tags: ["AI-Guided", "Lote 1"] }
      ]"""
)

content = content.replace(
    """$ kiro run skill-planner-po.yaml --work-item=101
[MCP] azure-devops: GET WorkItem 101
[Planner] Lendo descrição: "Preciso de um login usando SMS."
[MCP] confluence: SEARCH "Política de Segurança MFA"
[Planner] Expandindo regras de negócio com base na política da empresa.
[Planner] Gerando PRD.md (Gherkin: Given user enters phone... Then send OTP...)
[MCP] azure-devops: ATTACH PRD.md to WorkItem 101
[MCP] azure-devops: PATCH System.State = 'Ag. Ref Técnico'
[Kiro] Sucesso. Custo da operação: $0.02""",
    """$ kiro run skill-planner-po.yaml --batch="101,103"
[MCP] azure-devops: GET WorkItems [101, 103]
[Planner] Processando #101 (Login OTP)...
[MCP] confluence: SEARCH "Política de Segurança MFA"
[Planner] Gerando PRD_101.md... OK.
[Planner] Processando #103 (Dashboard Vendas)...
[MCP] confluence: SEARCH "Métricas de BI"
[Planner] Gerando PRD_103.md... OK.
[MCP] azure-devops: Movendo #101 e #103 para 'Ag. Ref Técnico'.
[Kiro] Lote processado. Custo: $0.05"""
)

content = content.replace(
    """cards: [
        { id: 101, title: "Login via OTP", tags: ["PRD Pronto", "Aguardando Tech"] }
      ]""",
    """cards: [
        { id: 101, title: "Login via OTP", tags: ["PRD Pronto"] },
        { id: 103, title: "Dashboard Vendas", tags: ["PRD Pronto"] }
      ]"""
)

content = content.replace(
    """[WIP Check] Coluna 'Ag. Ref Técnico' tem 1 item. (WIP Limit: 5)
[Pool Check] Agentes 'Architect' estão ocupados no card #98.
[Action] Card #101 colocado em FILA DE ESPERA (Wait Time: 0h 12m).
// 15 minutos depois...
[Event] Agente Architect liberado.
[Kiro] Efetuando PULL do card #101 para 'Em Ref. Técnico (IA)'.""",
    """[WIP Check] Lote com 2 itens chegou na fila. (WIP Limit: 5)
[Pool Check] Agentes 'Architect' estão ocupados refatorando o ticket #98.
[Action] #101 e #103 colocados em FILA DE ESPERA (Wait Time).
// 15 minutos depois...
[Event] Agente Architect liberado.
[Kiro] Efetuando PULL do Lote [#101, #103] para 'Em Ref. Técnico (IA)'."""
)

content = content.replace(
    """cards: [
        { id: 101, title: "Login via OTP", tags: ["AI-Guided", "Arquitetura"] }
      ]""",
    """cards: [
        { id: 101, title: "Login via OTP", tags: ["AI-Guided", "Arch"] },
        { id: 103, title: "Dashboard Vendas", tags: ["AI-Guided", "Arch"] }
      ]"""
)

content = content.replace(
    """$ kiro run skill-architect.yaml --work-item=101
[MCP] azure-devops: DOWNLOAD PRD.md
[Architect] Avaliando impacto na base de código via GitHub MCP...
[Architect] Gerando 'ADR-004_OTP_Login.md' com diagramas Mermaid.
[MCP] azure-devops: CREATE Task "API Twilio Integration" (Parent: 101)
[MCP] azure-devops: CREATE Task "Tabela DB AuthOTP" (Parent: 101)
[MCP] azure-devops: CREATE Task "Frontend Auth Modal" (Parent: 101)
[MCP] azure-devops: PATCH System.State = 'Aguardando PO'
[Kiro] Sucesso. Design pronto para aprovação humana.""",
    """$ kiro run skill-architect.yaml --batch="101,103"
[MCP] azure-devops: DOWNLOAD PRDs
[Architect] Avaliando impacto dos 2 itens na base de código...
[Architect] #101 -> Gerando 'ADR-004_OTP_Login.md'. Criando 3 Sub-Tasks no TFS.
[Architect] #103 -> Gerando 'ADR-005_Dashboard.md'. Criando 2 Sub-Tasks no TFS.
[MCP] azure-devops: PATCH System.State = 'Aguardando PO' (#101, #103)
[Kiro] Sucesso. Design do lote pronto para aprovação humana."""
)

content = content.replace(
    """cards: [
        { id: 101, title: "Login via OTP", tags: ["Humano Requerido", "Aprovação"] }
      ]""",
    """cards: [
        { id: 101, title: "Login via OTP", tags: ["Gate PO"] },
        { id: 103, title: "Dashboard Vendas", tags: ["Gate PO"] }
      ]"""
)

content = content.replace(
    """[Slack Bot] 🔔 "Card #101 requer aprovação de arquitetura."
[Humano] Executa: /kiro grill-me 101
[Kiro] "Olá, sou o Arquiteto. Que dúvidas você tem sobre a spec?"
[Humano] "A Twilio suporta WhatsApp OTP?"
[Kiro] "Sim. Posso atualizar a spec para incluir WhatsApp. Confirma?"
[Humano] "Sim. Depois disso, aprovado."
[Humano] Executa: /kiro approve 101
[Kiro] Movendo Card para 'Em Desenvolvimento'.""",
    """[Slack Bot] 🔔 "Lote de Cards [#101, #103] requer aprovação de arquitetura."
[Humano] Executa: /kiro approve 103
[Humano] Executa: /kiro grill-me 101
[Kiro] "Dúvidas sobre o OTP Login?"
[Humano] "Adicione WhatsApp OTP na spec."
[Kiro] "Feito. Confirma a aprovação do #101?"
[Humano] Executa: /kiro approve 101
[Kiro] Movendo lote para 'Em Desenvolvimento'."""
)

content = content.replace(
    """cards: [
        { id: 101, title: "Login via OTP", tags: ["AI-Guided", "Coding", "TDD"] }
      ]""",
    """cards: [
        { id: 101, title: "Login via OTP", tags: ["AI Coder"] },
        { id: 103, title: "Dashboard Vendas", tags: ["AI Coder"] }
      ]"""
)

content = content.replace(
    """$ kiro run skill-software-engineer.yaml --work-item=101
[Coder] Executando 'git checkout -b feat/101-otp-login'
[Coder] Lendo spec ADR-004_OTP_Login.md
[Coder] Criando auth.spec.ts...
[Bash] npm run test -> FALHA (Red) - auth module not found.
[Coder] Implementando auth.ts
[Bash] npm run test -> PASSOU (Green) - 14 tests passed.
[Bash] git add . && git commit -m "feat(auth): login via OTP"
[Bash] git push origin feat/101-otp-login
[MCP] azure-devops: PATCH System.State = 'Em Teste'""",
    """$ kiro run skill-software-engineer.yaml --batch="101,103"
[Coder] Iniciando agentes paralelos (Workers) para o Lote...
[Worker A - #101] branch feat/101-otp. Escrevendo testes (Red)... Codando auth.ts... Testes OK (Green).
[Worker B - #103] branch feat/103-dash. Escrevendo testes (Red)... Codando chart.ts... Testes OK (Green).
[Bash] git push origin feat/101-otp
[Bash] git push origin feat/103-dash
[MCP] azure-devops: Movendo [#101, #103] para 'Em Teste'."""
)

content = content.replace(
    """cards: [
        { id: 101, title: "Login via OTP", tags: ["AI-Guided", "QA & Sec", "OWASP"] }
      ]""",
    """cards: [
        { id: 101, title: "Login via OTP", tags: ["QA & Sec"] },
        { id: 103, title: "Dashboard Vendas", tags: ["QA & Sec"] }
      ]"""
)

content = content.replace(
    """$ kiro run skill-qa-sec.yaml --branch=feat/101-otp-login
[QA] Rodando Playwright Tests (Browser Engine: Chromium)...
[QA] 3 UI Tests Passed (Modal OTP renderizado corretamente).
[Security] Iniciando Semgrep SAST Scan...
[Security] Resultados: 0 Vulnerabilidades Críticas. 1 Warning (Dependency).
[QA] Gerando 'QA_Signoff_Report.pdf'.
[MCP] azure-devops: ATTACH QA_Signoff_Report.pdf
[MCP] azure-devops: PATCH System.State = 'Ag. Liberação PO'""",
    """$ kiro run skill-qa-sec.yaml --branches=["feat/101-otp", "feat/103-dash"]
[QA] Rodando E2E Tests em Paralelo...
[QA-101] 3 UI Tests Passed (Modal OTP OK).
[QA-103] 5 UI Tests Passed (Gráficos Renderizados).
[Security] Semgrep SAST Scan no Lote... 0 Vulnerabilidades.
[QA] Gerando 'QA_Signoff.pdf' para cada card.
[MCP] azure-devops: PATCH System.State = 'Ag. Liberação PO' (#101, #103)"""
)

content = content.replace(
    """cards: [
        { id: 101, title: "Login via OTP", tags: ["Pronto para Deploy", "Validação Final"] }
      ]""",
    """cards: [
        { id: 101, title: "Login via OTP", tags: ["UAT"] },
        { id: 103, title: "Dashboard Vendas", tags: ["UAT"] }
      ]"""
)

content = content.replace(
    """- Aprovar Deploy: /kiro approve-deploy 101
    - Reprovar (Bug): /kiro reject 101 --bug="detalhe"`,
    log: `[Vercel Preview] Deploy efêmero concluído. URL gerada.
[Slack Bot] 🚀 "Preview disponível para UAT."
[Humano] Acessa a URL, testa receber SMS no celular... Funciona!
[Humano] Executa: /kiro approve-deploy 101
[Kiro] Recebido sinal de Deploy Humano.
[MCP] azure-devops: Iniciando Merge para 'master'.
[MCP] azure-devops: PATCH System.State = 'Liberado para Instalar'""",
    """- Aprovar Lote: /kiro approve-deploy 101 103
    - Reprovar: /kiro reject [id]`,
    log: `[Vercel Preview] Deploy de 2 Previews concluído.
[Slack Bot] 🚀 "Previews disponíveis para UAT."
[Humano] Acessa URL do #101 (OTP Funciona). Acessa URL #103 (BI Funciona).
[Humano] Executa: /kiro approve-deploy 101 103
[Kiro] Aceite Humano no Lote.
[MCP] azure-devops: Fazendo Merge de ambas as branches para 'master'.
[MCP] Movendo lote para 'Liberado para Instalar'."""
)

content = content.replace(
    """cards: [
        { id: 101, title: "Login via OTP", tags: ["CI/CD Pipeline", "Deploying"] }
      ]""",
    """cards: [
        { id: 101, title: "Login via OTP", tags: ["CI/CD"] },
        { id: 103, title: "Dashboard Vendas", tags: ["CI/CD"] }
      ]"""
)

content = content.replace(
    """[TFS Auto-Rule] Status alterado para 'Done'.""",
    """[TFS Auto-Rule] Status de #101 e #103 alterado para 'Done'."""
)

content = content.replace(
    """cards: [
        { id: 101, title: "Login via OTP", tags: ["Em Produção", "Lead Time Gerado"] }
      ]""",
    """cards: [
        { id: 101, title: "Login via OTP", tags: ["Done"] },
        { id: 103, title: "Dashboard Vendas", tags: ["Done"] }
      ]"""
)

content = content.replace(
    """Feature OTP Login em PRD! Custo Kiro: $\{{cost_spent}}."`,
    log: `✅ CICLO DE VIDA ENCERRADO
----------------------------------------
[Métricas Kanban] Lead Time (New -> Done): 24h 15m.
[Eficiência Flow] Wait Time / Touch Time Ratio: 85% Touch Time (Eficiência absurda).
[Custo de IA] 
- Planner: $0.02
- Architect: $0.04
- Coder (TDD): $0.06
- QA: $0.02
[Custo Total API] $0.14 USD.
----------------------------------------
Parabéns, seu fluxo Kiro está otimizado!""",
    """Lote de 2 Features em PRD! Custo Kiro: $\{{cost_spent}}."`,
    log: `✅ LOTE DE CICLO DE VIDA ENCERRADO
----------------------------------------
[Métricas Kanban] Lote de 2 itens processado. Lead Time médio: 24h 15m.
[Eficiência Flow] Wait Time / Touch Time Ratio: 85% (Flow Eficiente).
[Custo de IA (Para o Lote de 2 features)] 
- Planner: $0.05
- Architect: $0.08
- Coder (TDD x2): $0.12
- QA Paralelo: $0.04
[Custo Total API] $0.29 USD para substituir semanas de trabalho.
----------------------------------------
Parabéns, sua fábrica Kiro processou o lote em tempo recorde!"""
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated fluxo_ia.js to handle multiple cards as requested.")
