# Script to generate labs_doc.js with escaped backticks
import re

content = """
function initLabsView() {
    const container = document.getElementById('labs-view');
    if (!container) return;

    container.innerHTML = `
        <style>
            .lab-card {
                background: #fff;
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                margin-bottom: 30px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
                overflow: hidden;
            }
            .lab-header {
                padding: 20px 25px;
                background: #f8fafc;
                border-bottom: 2px solid #3b82f6;
                display: flex;
                align-items: center;
                gap: 12px;
            }
            .lab-header h3 {
                margin: 0;
                font-size: 18px;
                color: #0f172a;
            }
            .lab-content {
                padding: 25px;
                color: #475569;
                font-size: 14.5px;
                line-height: 1.7;
            }
            .lab-code {
                background: #0f172a;
                color: #e2e8f0;
                padding: 20px;
                border-radius: 8px;
                font-family: 'Courier New', Courier, monospace;
                font-size: 13px;
                line-height: 1.6;
                overflow-x: auto;
                margin: 20px 0;
                border-left: 4px solid #3b82f6;
            }
            .lab-comment { color: #64748b; font-style: italic; }
            .lab-keyword { color: #c678dd; }
            .lab-string { color: #98c379; }
            .lab-function { color: #61afef; }
            .lab-step {
                display: flex;
                align-items: flex-start;
                gap: 15px;
                margin-bottom: 20px;
            }
            .lab-step-number {
                background: #3b82f6;
                color: #fff;
                width: 30px;
                height: 30px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                flex-shrink: 0;
            }
        </style>

        <div class="page-header" style="background:linear-gradient(135deg, #0f172a, #000000);">
            <div class="tag" style="background:#3b82f6;">BOOTCAMP TÉCNICO</div>
            <h2>🔬 Laboratórios Práticos (Mão na Massa)</h2>
            <p style="margin-top:10px;">A teoria não sobrevive ao terminal. Bem-vindo aos Labs onde construímos o código por trás da mágica das IAs de Engenharia. Copie, cole, e rode no seu ambiente local.</p>
        </div>

        <!-- LAB 1: PRIVATE MCP SERVER -->
        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #f59e0b;">
                <span style="font-size:24px;">🧪</span> 
                <h3>Lab 1: Criando um Private MCP Server (Python)</h3>
            </div>
            <div class="lab-content">
                <p><strong>Cenário:</strong> Sua empresa possui um banco de dados legado em Postgres com regras de negócio obscuras. Você quer que o Claude Code consiga "consultar" esse banco de dados sem dar a ele a string de conexão direta.</p>
                <p><strong>Solução:</strong> Criar um Servidor MCP local (Model Context Protocol) que expõe uma ferramenta chamada <span style="background:#e2e8f0; padding:2px 4px; border-radius:4px; font-family:monospace;">query_legacy_db</span>.</p>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div>
                        <strong>Instale o SDK do MCP</strong>
                        <div class="lab-code">pip install mcp-sdk psycopg2-binary</div>
                    </div>
                </div>

                <div class="lab-step">
                    <div class="lab-step-number">2</div>
                    <div>
                        <strong>Crie o arquivo mcp_server.py</strong>
                        <p>Este script usará stdio para se comunicar nativamente com a IDE Agentic.</p>
                        <div class="lab-code">
<span class="lab-keyword">import</span> psycopg2
<span class="lab-keyword">from</span> mcp.server.fastmcp <span class="lab-keyword">import</span> FastMCP

<span class="lab-comment"># Inicializa o servidor</span>
mcp = FastMCP(<span class="lab-string">"LegacyDB"</span>)

<span class="lab-keyword">@mcp.tool()</span>
<span class="lab-keyword">def</span> <span class="lab-function">query_legacy_db</span>(query: str) -> str:
    <span class="lab-comment">\"\"\"Executa uma consulta RO (Read-Only) no banco legado.\"\"\"</span>
    <span class="lab-comment"># Validação de Segurança (Prevenindo SQL Injection malicioso do LLM)</span>
    <span class="lab-keyword">if</span> <span class="lab-string">"DROP"</span> <span class="lab-keyword">in</span> query.upper() <span class="lab-keyword">or</span> <span class="lab-string">"UPDATE"</span> <span class="lab-keyword">in</span> query.upper():
        <span class="lab-keyword">return</span> <span class="lab-string">"ERRO DE SEGURANÇA: Apenas comandos SELECT são permitidos."</span>
        
    conn = psycopg2.connect(<span class="lab-string">"dbname=legacy user=reader password=secret"</span>)
    cursor = conn.cursor()
    <span class="lab-keyword">try</span>:
        cursor.execute(query)
        records = cursor.fetchall()
        <span class="lab-keyword">return</span> str(records)
    <span class="lab-keyword">except</span> Exception <span class="lab-keyword">as</span> e:
        <span class="lab-keyword">return</span> <span class="lab-string">f"Erro SQL: {str(e)}"</span>

<span class="lab-keyword">if</span> __name__ == <span class="lab-string">"__main__"</span>:
    mcp.run()
                        </div>
                    </div>
                </div>

                <div class="lab-step">
                    <div class="lab-step-number">3</div>
                    <div>
                        <strong>Registre no Claude Code</strong>
                        <p>No seu terminal, diga ao Claude para usar esse script Python como um plugin.</p>
                        <div class="lab-code">
claude /plugin add local ./mcp_server.py
                        </div>
                        <p>Pronto! Agora se você pedir ao Claude: <i>"Claude, veja os últimos 5 clientes do banco legado"</i>, ele vai chamar automaticamente a função Python via protocolo MCP.</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- LAB 2: GIT HOOKS -->
        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #10b981;">
                <span style="font-size:24px;">🛡️</span> 
                <h3>Lab 2: Defesa Ativa com Git Hooks (Prevenção de Alucinação)</h3>
            </div>
            <div class="lab-content">
                <p><strong>Cenário:</strong> O Claude está refatorando arquivos e decidindo comitar as mudanças sozinho usando <code>git commit -m "refactor"</code>. Mas e se ele quebrou algo e não percebeu?</p>
                <p><strong>Solução:</strong> Criar um <code>pre-commit</code> hook que bloqueia fisicamente commits não testados.</p>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div>
                        <strong>Crie o arquivo executável no repositório</strong>
                        <div class="lab-code">
touch .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
                        </div>
                    </div>
                </div>

                <div class="lab-step">
                    <div class="lab-step-number">2</div>
                    <div>
                        <strong>Escreva o Shell Script (Bash)</strong>
                        <p>Este script aborta o commit se o Lint ou o Jest falharem, obrigando o Agente a ver o erro de saída e consertar o código antes de tentar comitar novamente.</p>
                        <div class="lab-code">
<span class="lab-comment">#!/bin/sh</span>
<span class="lab-comment"># .git/hooks/pre-commit</span>

<span class="lab-function">echo</span> <span class="lab-string">"🔍 [GIT HOOK] Verificando Linter e Testes antes de permitir o commit..."</span>

<span class="lab-comment"># Executar o Linter (ESLint)</span>
npm run lint
<span class="lab-keyword">if</span> [ $? -ne 0 ]; <span class="lab-keyword">then</span>
  <span class="lab-function">echo</span> <span class="lab-string">"❌ [GIT HOOK] Linter falhou! Corrija os erros acima."</span>
  <span class="lab-keyword">exit</span> 1
<span class="lab-keyword">fi</span>

<span class="lab-comment"># Executar Unit Tests (Jest) apenas nos arquivos modificados</span>
npm test -- --bail --findRelatedTests $(git diff --cached --name-only | grep "\.js$")
<span class="lab-keyword">if</span> [ $? -ne 0 ]; <span class="lab-keyword">then</span>
  <span class="lab-function">echo</span> <span class="lab-string">"❌ [GIT HOOK] Testes falharam! Você quebrou a suíte. Conserte antes de comitar."</span>
  <span class="lab-keyword">exit</span> 1
<span class="lab-keyword">fi</span>

<span class="lab-function">echo</span> <span class="lab-string">"✅ [GIT HOOK] Código seguro. Permitindo commit."</span>
<span class="lab-keyword">exit</span> 0
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- LAB 3: ARCHITECT YAML -->
        <div class="lab-card">
            <div class="lab-header" style="border-bottom-color: #8b5cf6;">
                <span style="font-size:24px;">🏛️</span> 
                <h3>Lab 3: O Blueprint Definitivo do Agente Arquiteto</h3>
            </div>
            <div class="lab-content">
                <p><strong>Cenário:</strong> Como o Kiro injeta regras de governança complexas em um Agente? Através do arquivo de configuração de Skill. Este é o "Padrão Ouro" YAML para orquestrar o papel de Arquiteto de Software.</p>

                <div class="lab-step">
                    <div class="lab-step-number">1</div>
                    <div style="width: 100%;">
                        <strong>O Arquivo architect.yaml</strong>
                        <p>Note a mistura de System Prompts pesados, restrições financeiras (Cost Guards) e invocação de MCPs na nuvem.</p>
                        <div class="lab-code">
<span class="lab-comment"># .kiro/skills/architect.yaml</span>
<span class="lab-keyword">agent:</span>
  <span class="lab-function">role:</span> "Tech Lead / Software Architect"
  <span class="lab-function">model:</span> "claude-3-5-sonnet-20241022"
  <span class="lab-function">temperature:</span> 0.1 <span class="lab-comment"># Baixa temperatura para decisões lógicas determinísticas</span>

<span class="lab-keyword">cost_guard:</span>
  <span class="lab-function">max_usd_per_run:</span> 1.50
  <span class="lab-function">action_on_breach:</span> "pause_and_notify_slack"

<span class="lab-keyword">mcp_servers:</span>
  - <span class="lab-function">name:</span> "confluence-enterprise" <span class="lab-comment"># Para ler regras LGPD</span>
  - <span class="lab-function">name:</span> "azure-devops" <span class="lab-comment"># Para atualizar tickets do Azure</span>

<span class="lab-keyword">workspace_rules:</span>
  <span class="lab-function">allow_write:</span> false <span class="lab-comment"># Arquiteto NÃO codifica, ele só planeja e lê.</span>
  <span class="lab-function">allow_bash:</span> false  <span class="lab-comment"># Arquiteto não roda comandos shell destrutivos.</span>

<span class="lab-keyword">system_prompt:</span> |
  <span class="lab-string">&lt;role&gt;</span>Você é o Arquiteto Principal desta empresa financeira.<span class="lab-string">&lt;/role&gt;</span>
  
  <span class="lab-string">&lt;guidelines&gt;</span>
    1. Nunca proponha bancos NoSQL. Nossa infra suporta APENAS PostgreSQL.
    2. Antes de criar a modelagem de dados, use a tool `read_confluence` e busque pela página "Regras de Máscara de Dados LGPD".
    3. Sua saída DEVE sempre conter um Diagrama Mermaid na sintaxe `graph TD`.
    4. Se o ticket atual não tiver Critérios de Aceite (ACs) descritos adequadamente, adicione uma tag "needs-po-review" no Azure DevOps e encerre sua execução.
  <span class="lab-string">&lt;/guidelines&gt;</span>

<span class="lab-keyword">on_success:</span>
  <span class="lab-comment"># Se ele terminar a arquitetura com sucesso, ele aciona 2 Coders em paralelo</span>
  <span class="lab-function">patch_ticket_state:</span> "Ready for Dev"
  <span class="lab-function">trigger_subagents:</span>
    - <span class="lab-function">skill:</span> "coder-backend.yaml"
    - <span class="lab-function">skill:</span> "coder-frontend.yaml"
                        </div>
                    </div>
                </div>
            </div>
        </div>

    `;
}

window.initLabsView = initLabsView;
"""

with open('labs_doc.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("labs_doc.js generated successfully")
