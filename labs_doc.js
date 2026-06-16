
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
                white-space: pre;
            }
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
            .lab-tabs {
                display: flex;
                gap: 10px;
                margin-bottom: 30px;
                border-bottom: 2px solid #e2e8f0;
                padding-bottom: 10px;
                overflow-x: auto;
            }
            .lab-tab-btn {
                background: #f1f5f9;
                border: 1px solid #cbd5e1;
                padding: 10px 20px;
                border-radius: 8px;
                cursor: pointer;
                font-weight: 600;
                color: #475569;
                transition: all 0.2s;
                white-space: nowrap;
            }
            .lab-tab-btn:hover {
                background: #e2e8f0;
            }
            .lab-tab-btn.active {
                background: #3b82f6;
                color: #fff;
                border-color: #2563eb;
            }
            .lab-tab-content {
                display: none;
            }
            .lab-tab-content.active {
                display: block;
            }
        </style>

        <div class="page-header" style="background:linear-gradient(135deg, #0f172a, #000000);">
            <div class="tag" style="background:#3b82f6;">BOOTCAMP "10.000 HORAS"</div>
            <h2>🔬 Laboratórios de Elite: Discovery to Delivery & MCPs</h2>
            <p style="margin-top:10px;">Aqui o código ganha vida. Estes laboratórios formam o treinamento avançado para dominar Inteligência Artificial aplicada ao desenvolvimento de software, com foco extremo na criação e uso do <strong>Model Context Protocol (MCP)</strong>.</p>
        </div>

        <div class="lab-tabs" id="lab-tabs">
            <button class="lab-tab-btn active" onclick="switchLabTab('tab-upstream', this)">💡 Upstream & Discovery</button>
            <button class="lab-tab-btn" onclick="switchLabTab('tab-mcp', this)">🛠️ Construindo MCPs do Zero</button>
            <button class="lab-tab-btn" onclick="switchLabTab('tab-downstream', this)">🚀 Downstream & Delivery</button>
            <button class="lab-tab-btn" onclick="switchLabTab('tab-mastery', this)">🧠 Mastery em Agentes & IA</button>
            <button class="lab-tab-btn" style="background:#e0e7ff; border:1px solid #c7d2fe; color:#3730a3;" onclick="switchLabTab('tab-final', this)">🌟 O Ecossistema Final</button>
        </div>

        <!-- TAB 1: UPSTREAM -->
        <div id="tab-upstream" class="lab-tab-content active">
            <div class="lab-card">
                <div class="lab-header" style="border-bottom-color: #3b82f6;">
                    <span style="font-size:24px;">📝</span> 
                    <h3>Lab 1: Quebra Automática de Épicos (AI Planner)</h3>
                </div>
                <div class="lab-content">
                    <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                        <strong style="color: #166534; display: flex; align-items: center; gap: 8px;">🎯 O Que É</strong>
                        <p style="margin: 5px 0 0 0; color: #166534;">O uso de Agentes para ler um documento de negócio extenso (Épico) e destrinchá-lo em User Stories perfeitamente formatadas usando critérios de aceite INVEST.</p>
                    </div>
                    <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                        <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;">💡 Valor de Negócio</strong>
                        <p style="margin: 5px 0 0 0; color: #92400e;">Gera alinhamento cristalino entre a área de Negócios e TI. Reduz horas de reuniões de refinamento ao entregar o trabalho pesado já pronto para revisão humana.</p>
                    </div>
                    <h4 style="color: #3b82f6; margin-bottom: 15px;">🛠️ Como Fazer</h4>
                    <div class="lab-step">
                        <div class="lab-step-number">1</div>
                        <div style="width: 100%;">
                            <strong>O Prompt do Especialista (PO)</strong>
                            <div class="lab-code">
# Execute isso com o Kiro ou Claude Code:
"Atue como um Product Owner Sênior. Leia o arquivo 'epico_pagamentos.md'.
Quebre esse épico em exatamente 5 User Stories.
Para cada Story, forneça:
1. Título
2. Como [Ator], eu quero [Ação] para [Valor].
3. Critérios de Aceite no formato Gherkin (Dado/Quando/Então).
Salve a saída no arquivo 'backlog_pagamentos.md'."
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="lab-card">
                <div class="lab-header" style="border-bottom-color: #3b82f6;">
                    <span style="font-size:24px;">🏛️</span> 
                    <h3>Lab 2: Extração de Arquitetura a partir de Requisitos</h3>
                </div>
                <div class="lab-content">
                    <p>Muitas vezes o engenheiro lê uma história e não sabe por onde começar a arquitetura. Neste lab, ensinamos a IA a atuar como Software Architect.</p>
                    <div class="lab-step">
                        <div class="lab-step-number">1</div>
                        <div style="width: 100%;">
                            <strong>Gerando Modelos C4 e Diagramas Mermaid</strong>
                            <div class="lab-code">
"Atue como Arquiteto de Software. 
Leia a 'user_story_1.md'. 
Gere o diagrama de sequência em linguagem MermaidJS mostrando a 
interação entre o Frontend, o API Gateway, o Microsserviço de Pagamento 
e o Banco de Dados.
Retorne Apenas o código do Mermaid encapsulado em crases."
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 2: MCP -->
        <div id="tab-mcp" class="lab-tab-content">
            <div class="lab-card">
                <div class="lab-header" style="border-bottom-color: #8b5cf6;">
                    <span style="font-size:24px;">🔌</span> 
                    <h3>Lab 3: O que é Model Context Protocol (MCP)?</h3>
                </div>
                <div class="lab-content">
                    <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                        <strong style="color: #166534; display: flex; align-items: center; gap: 8px;">🎯 O Que É</strong>
                        <p style="margin: 5px 0 0 0; color: #166534;">O MCP (Model Context Protocol) é um padrão aberto (criado pela Anthropic) que funciona como um "USB para Inteligência Artificial". Ele permite que você conecte Modelos de IA aos seus bancos de dados locais, APIs corporativas e arquivos de forma padronizada e ultra-segura.</p>
                    </div>
                    <div style="background: #fffbeb; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px; margin-bottom: 25px;">
                        <strong style="color: #92400e; display: flex; align-items: center; gap: 8px;">💡 Valor de Negócio</strong>
                        <p style="margin: 5px 0 0 0; color: #92400e;">Em vez de colar código confidencial ou planilhas no ChatGPT, você roda um Servidor MCP local. A IA envia requisições para esse servidor para "ler a base de dados de clientes" ou "rodar uma query", mantendo os dados protegidos dentro da infraestrutura da empresa.</p>
                    </div>
                </div>
            </div>

            <div class="lab-card">
                <div class="lab-header" style="border-bottom-color: #8b5cf6;">
                    <span style="font-size:24px;">🐍</span> 
                    <h3>Lab 4: Construindo seu Primeiro Servidor MCP (Python)</h3>
                </div>
                <div class="lab-content">
                    <p>Vamos criar um MCP que expõe uma ferramenta matemática customizada para a IA.</p>
                    <div class="lab-step">
                        <div class="lab-step-number">1</div>
                        <div style="width: 100%;">
                            <strong>O Servidor Python</strong>
                            <p>Instale o SDK oficial: <code>pip install mcp</code></p>
                            <div class="lab-code">
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Instancia o servidor
app = Server("math-mcp")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="calculate_tax",
            description="Calcula o imposto corporativo complexo",
            inputSchema={
                "type": "object",
                "properties": { "amount": { "type": "number" } },
                "required": ["amount"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "calculate_tax":
        amount = arguments["amount"]
        tax = amount * 0.275  # Lógica interna da empresa
        return [TextContent(type="text", text=f"O imposto é {tax}")]
    raise ValueError(f"Tool não encontrada: {name}")

async def main():
    # Roda comunicando pela saída padrão (stdio)
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="lab-card">
                <div class="lab-header" style="border-bottom-color: #8b5cf6;">
                    <span style="font-size:24px;">📁</span> 
                    <h3>Lab 5: Expondo Resources via MCP</h3>
                </div>
                <div class="lab-content">
                    <p>Além de Tools (Ações), o MCP expõe Resources (Dados). Um recurso pode ser um log do banco de dados que a IA pode ler instantaneamente.</p>
                    <div class="lab-step">
                        <div class="lab-step-number">1</div>
                        <div style="width: 100%;">
                            <strong>Código do Resource</strong>
                            <div class="lab-code">
@app.list_resources()
async def list_resources():
    return [
        Resource(
            uri="file:///var/logs/app.log",
            name="Application Error Log",
            mimeType="text/plain"
        )
    ]

@app.read_resource()
async def read_resource(uri: str):
    if uri == "file:///var/logs/app.log":
        with open("app.log", "r") as f:
            return f.read()
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 3: DOWNSTREAM -->
        <div id="tab-downstream" class="lab-tab-content">
            <div class="lab-card">
                <div class="lab-header" style="border-bottom-color: #10b981;">
                    <span style="font-size:24px;">🤖</span> 
                    <h3>Lab 6: Claude Code consumindo o seu MCP</h3>
                </div>
                <div class="lab-content">
                    <div style="background: #f0fdf4; padding: 15px; border-left: 4px solid #22c55e; border-radius: 4px; margin-bottom: 15px;">
                        <strong style="color: #166534; display: flex; align-items: center; gap: 8px;">🎯 O Que É</strong>
                        <p style="margin: 5px 0 0 0; color: #166534;">Conectar a CLI do Claude Code (ambiente de desenvolvedor) ao servidor MCP que construímos no lab anterior.</p>
                    </div>
                    <div class="lab-step">
                        <div class="lab-step-number">1</div>
                        <div style="width: 100%;">
                            <strong>Configurando o Claude Code</strong>
                            <p>O Claude Code procura configurações globais para saber quais servidores iniciar.</p>
                            <div class="lab-code">
# No terminal, adicione o servidor Python que você criou
claude mcp add math-server python main.py

# A partir de agora, se você perguntar pro Claude:
"Claude, qual é o imposto sobre R$ 5000?"

# O Claude vai automaticamente chamar a tool "calculate_tax" 
# do seu MCP e te responder R$ 1375!
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="lab-card">
                <div class="lab-header" style="border-bottom-color: #10b981;">
                    <span style="font-size:24px;">🧪</span> 
                    <h3>Lab 7: TDD Guiado por IA</h3>
                </div>
                <div class="lab-content">
                    <p>O ciclo Delivery exige Test-Driven Development de ponta. Use o Claude Code conectado às suas ferramentas de build.</p>
                    <div class="lab-step">
                        <div class="lab-step-number">1</div>
                        <div style="width: 100%;">
                            <strong>O Fluxo Perfeito</strong>
                            <div class="lab-code">
1. "Claude, crie um arquivo de teste Jest para validar a função calculateTax."
2. O Claude escreve o teste (que vai falhar, pois a função não existe).
3. "Claude, execute 'npm test'. Analise o erro e agora crie a função para o teste passar."
4. O Claude coda a função e roda os testes sozinho.
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 4: MASTERY -->
        <div id="tab-mastery" class="lab-tab-content">
            <div class="lab-card">
                <div class="lab-header" style="border-bottom-color: #f59e0b;">
                    <span style="font-size:24px;">💸</span> 
                    <h3>Lab 8: Cost Guards & Segurança de Agent Loops</h3>
                </div>
                <div class="lab-content">
                    <p>Quando damos terminais autônomos para a IA, corremos o risco de "Loops Infinitos" consumirem toda a cota da OpenAI/Anthropic em minutos.</p>
                    <div class="lab-step">
                        <div class="lab-step-number">1</div>
                        <div style="width: 100%;">
                            <strong>Como proteger o bolso</strong>
                            <div class="lab-code">
# No Claude Code, sempre use o limitador de custos
claude --cost-limit 5.00

# Se o agente entrar em loop rodando um erro recursivo de npm, 
# a execução será automaticamente interrompida ao bater $5.00.
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="lab-card">
                <div class="lab-header" style="border-bottom-color: #f59e0b;">
                    <span style="font-size:24px;">🧠</span> 
                    <h3>Lab 9: RAG Híbrido com Servidor MCP</h3>
                </div>
                <div class="lab-content">
                    <p>Para times corporativos complexos, você pode criar um MCP que pesquisa vetores no ChromaDB ou Pinecone.</p>
                    <div class="lab-step">
                        <div class="lab-step-number">1</div>
                        <div style="width: 100%;">
                            <strong>A Tool de RAG</strong>
                            <div class="lab-code">
@app.call_tool()
async def search_company_knowledge(query: str):
    # Faz busca no banco vetorial da empresa
    results = vector_db.similarity_search(query)
    return [TextContent(type="text", text=results)]

# Agora a IA pode perguntar ao seu banco vetorial as regras 
# de compliance da empresa ANTES de escrever o código.
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 5: FINAL -->
        <div id="tab-final" class="lab-tab-content">
            <div class="lab-card">
                <div class="lab-header" style="border-bottom-color: #ec4899;">
                    <span style="font-size:24px;">🏆</span> 
                    <h3>Projeto Final: O Orquestrador Definitivo</h3>
                </div>
                <div class="lab-content">
                    <div style="background: #fdf2f8; padding: 15px; border-left: 4px solid #db2777; border-radius: 4px; margin-bottom: 25px;">
                        <strong style="color: #9d174d; display: flex; align-items: center; gap: 8px;">A Missão</strong>
                        <p style="margin: 5px 0 0 0; color: #9d174d;">Você foi promovido a Head de IA da empresa. Você precisa criar uma pipeline completa onde IAs interagem com ferramentas de negócio usando a integração do Model Context Protocol.</p>
                    </div>
                    <div class="lab-step">
                        <div class="lab-step-number">1</div>
                        <div style="width: 100%;">
                            <strong>Passo a Passo da Arquitetura Autônoma</strong>
                            <div class="lab-code">
1. O Product Owner cria uma vaga "Aumentar segurança de login" no Azure Boards.
2. O servidor MCP do Azure Boards expõe esse ticket como um Resource.
3. Você abre o seu Claude Code ou Kiro no terminal e digita:
   "Implemente o ticket 405 do Azure Boards".
4. O Claude usa a tool do MCP para LER o ticket.
5. O Claude escreve a arquitetura e os testes.
6. O Claude implementa o código no repositório local.
7. O Claude usa a tool "git_commit" para fazer o commit.
8. O Claude usa a tool "create_pr" para criar a PR, tudo de forma autônoma!

Isso é o verdadeiro poder da IA Orquestrada (Discovery to Delivery). 
Você agora é um Mestre em IA.
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    `;
}

window.initLabsView = initLabsView;
window.switchLabTab = function(tabId, btnElement) {
    document.querySelectorAll('.lab-tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.lab-tab-btn').forEach(btn => btn.classList.remove('active'));
    
    const targetTab = document.getElementById(tabId);
    if (targetTab) targetTab.classList.add('active');
    if (btnElement) btnElement.classList.add('active');
};
