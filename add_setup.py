import re

path = 'c:/Users/User/.antigravity/Agile Coach AI/fluxo_ia.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

setup_step = """{
    id: 0,
    title: "0. Setup Kiro",
    board: {
      column: "Pre-Flight (Configuração)",
      cards: [
        { id: 999, title: "Ambiente e Acessos", tags: ["Infra", "Admin"] }
      ]
    },
    agent: {
      name: "Engenheiro de IA (Admin)",
      icon: "🛠️",
      desc: "Antes da mágica acontecer, o ambiente precisa ser configurado. O Kiro precisa de um Personal Access Token (PAT) do Azure DevOps, chaves de API dos provedores LLM (Anthropic/OpenAI) e configuração dos MCP Servers globais na sua máquina ou container."
    },
    skill: `# 1. Instalação Global
# npm install -g @kiro-ai/cli

# 2. Arquivo de Variáveis de Ambiente (.env)
AZURE_DEVOPS_ORG="https://dev.azure.com/SuaEmpresa"
AZURE_DEVOPS_PROJECT="BankingApp"
AZURE_DEVOPS_PAT="hx73...sua-chave-aqui...z8q"
ANTHROPIC_API_KEY="sk-ant-..."

# 3. Registro de Ferramentas (kiro-mcp.json)
{
  "mcpServers": {
    "tfs": {
      "command": "npx",
      "args": ["-y", "@microsoft/azure-devops-mcp"],
      "env": { "ADO_PAT": "\${AZURE_DEVOPS_PAT}" }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
    }
  }
}

# 4. Estrutura de Skills
# As skills (como skill-planner.yaml) ficam em 
# ./kiro/skills/ na raiz do seu repositório.`,
    log: `$ kiro init
[Kiro Setup] Inicializando workspace...
[Auth] Validando AZURE_DEVOPS_PAT... Sucesso.
[Auth] Validando chaves LLM (Anthropic)... Sucesso.
[MCP] Instalando servidor @microsoft/azure-devops-mcp... Concluído.
[MCP] Instalando servidor @modelcontextprotocol/server-github... Concluído.

$ kiro validate-skills ./kiro/skills/
✔ skill-planner-po.yaml validada.
✔ skill-architect.yaml validada.
✔ skill-software-engineer.yaml validada.

[Daemon] Ambiente pronto. Para escutar o TFS, rode:
$ kiro start-daemon`
  },
  """

content = content.replace('const fluxoIaData = [\n', 'const fluxoIaData = [\n  ' + setup_step)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Added setup step to fluxo_ia.js")
