import os
import re
import json

RUFLO_DIR = "ruflo"
OUTPUT_FILE = "ruflo-data.js"

def parse_frontmatter(content):
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    if not match:
        return {}, content
    fm_text = match.group(1)
    body = match.group(2)
    meta = {}
    for line in fm_text.split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, body

def get_first_paragraph(content):
    lines = content.split('\n')
    desc_lines = []
    started = False
    for line in lines:
        line = line.strip()
        if not line:
            if started:
                break
            continue
        if line.startswith('#'):
            continue
        if line.startswith('>') or line.startswith('!['):
            continue
        started = True
        desc_lines.append(line)
        if len(' '.join(desc_lines)) > 140:
            break
    desc = ' '.join(desc_lines)
    return desc[:180] + ('...' if len(desc) > 180 else '')

def extract_guides():
    guides = [
        {
            "id": "ruflo-readme",
            "title": "Visão Geral do Ruflo (Meta-Harness)",
            "description": "Arquitetura completa do Ruflo: meta-harness para Claude Code e Codex, swarms, memória vetorial e MCP.",
            "icon": "🌊",
            "path": "ruflo/README.md"
        },
        {
            "id": "ruflo-explained",
            "title": "RuFlo Explained (Guia dos 14 Capítulos)",
            "description": "Artigo completo por rUv Cohen: do zero ao swarm coordenado, memória adaptativa, plugins e governança.",
            "icon": "📖",
            "path": "ruflo/docs/ruflo-explained.md"
        },
        {
            "id": "ruflo-agents-guide",
            "title": "Guia de Orquestração (AGENTS.md)",
            "description": "Regras de ouro: Codex/Claude executa, Ruflo orquestra. Padrões de swarm, memória e recipes prontas.",
            "icon": "🤖",
            "path": "ruflo/AGENTS.md"
        },
        {
            "id": "ruflo-claude-guide",
            "title": "Diretrizes e Invariantes (CLAUDE.md)",
            "description": "Regras de governança estritas, isolamento em worktrees, contratos de autorização e política anti-drift.",
            "icon": "🛡️",
            "path": "ruflo/CLAUDE.md"
        },
        {
            "id": "ruflo-metaharness-guide",
            "title": "MetaHarness User Guide",
            "description": "Flywheel de evolução contínua: avaliação empírica, auto-otimização e envelopes de segurança.",
            "icon": "⚙️",
            "path": "ruflo/docs/metaharness-user-guide.md"
        },
        {
            "id": "ruflo-userguide",
            "title": "Manual do Usuário Completo (USERGUIDE.md)",
            "description": "Referência exaustiva de configuração, comandos CLI, Terminal UI (TUI) e integração de ecossistema.",
            "icon": "📚",
            "path": "ruflo/docs/USERGUIDE.md"
        }
    ]
    return guides

def categorize_plugin(name):
    name = name.lower()
    if name in ['ruflo-core', 'ruflo-swarm', 'ruflo-autopilot', 'ruflo-loop-workers', 'ruflo-workflows', 'ruflo-console', 'ruflo-mods']:
        return "PLUGINS: CORE & SWARM"
    elif name in ['ruflo-agentdb', 'ruflo-ruvector', 'ruflo-rag-memory', 'ruflo-rvf', 'ruflo-knowledge-graph', 'ruflo-intelligence', 'ruflo-daa', 'ruflo-graph-intelligence']:
        return "PLUGINS: MEMÓRIA & VETORIAL"
    elif name in ['ruflo-sparc', 'ruflo-adr', 'ruflo-ddd', 'ruflo-metaharness', 'ruflo-goals']:
        return "PLUGINS: ARQUITETURA & MÉTODOS"
    elif name in ['ruflo-security-audit', 'ruflo-aidefence', 'ruflo-protector', 'ruflo-testgen', 'ruflo-browser']:
        return "PLUGINS: SEGURANÇA & QA"
    elif name in ['ruflo-jujutsu', 'ruflo-docs', 'ruflo-ruvllm', 'ruflo-agent', 'ruflo-plugin-creator', 'ruflo-migrations', 'ruflo-observability', 'ruflo-cost-tracker', 'ruflo-arena']:
        return "PLUGINS: FERRAMENTAS & DEV"
    else:
        return "PLUGINS: DOMÍNIO & ECOSSISTEMA"

def extract_plugins():
    plugins_dir = os.path.join(RUFLO_DIR, "plugins")
    if not os.path.exists(plugins_dir):
        return {}
    
    categories = {
        "PLUGINS: CORE & SWARM": [],
        "PLUGINS: MEMÓRIA & VETORIAL": [],
        "PLUGINS: ARQUITETURA & MÉTODOS": [],
        "PLUGINS: SEGURANÇA & QA": [],
        "PLUGINS: FERRAMENTAS & DEV": [],
        "PLUGINS: DOMÍNIO & ECOSSISTEMA": []
    }

    icons = {
        "ruflo-core": "🎛️",
        "ruflo-swarm": "🐝",
        "ruflo-autopilot": "🚀",
        "ruflo-loop-workers": "🔄",
        "ruflo-workflows": "🔀",
        "ruflo-console": "💻",
        "ruflo-mods": "🛡️",
        "ruflo-agentdb": "💾",
        "ruflo-ruvector": "🧠",
        "ruflo-rag-memory": "📚",
        "ruflo-rvf": "📦",
        "ruflo-knowledge-graph": "🕸️",
        "ruflo-intelligence": "💡",
        "ruflo-daa": "🧩",
        "ruflo-graph-intelligence": "🔬",
        "ruflo-sparc": "⚡",
        "ruflo-adr": "📝",
        "ruflo-ddd": "🏛️",
        "ruflo-metaharness": "⚙️",
        "ruflo-goals": "🎯",
        "ruflo-security-audit": "🔒",
        "ruflo-aidefence": "🛡️",
        "ruflo-protector": "🐕",
        "ruflo-testgen": "🧪",
        "ruflo-browser": "🌐",
        "ruflo-jujutsu": "🪓",
        "ruflo-docs": "📑",
        "ruflo-ruvllm": "🤖",
        "ruflo-agent": "📦",
        "ruflo-plugin-creator": "🛠️",
        "ruflo-migrations": "🗄️",
        "ruflo-observability": "📊",
        "ruflo-cost-tracker": "💰",
        "ruflo-arena": "🏟️",
        "ruflo-federation": "🌐",
        "ruflo-ruos": "🖥️",
        "ruflo-iot-cognitum": "📡",
        "ruflo-neural-trader": "📈",
        "ruflo-market-data": "📉",
        "ruflo-ai-team": "👥",
        "ruflo-business-pods": "🏢",
        "ruflo-deepseek-harness": "🐋",
        "ruflo-bbs-federation": "📻",
        "ruflo-chatgpt-federation": "💬",
        "ruflo-agntcy": "🤝",
        "ruflo-music": "🎵",
        "ruflo-x-gateway": "🚪"
    }

    for item in sorted(os.listdir(plugins_dir)):
        p_path = os.path.join(plugins_dir, item)
        if os.path.isdir(p_path):
            readme_path = os.path.join(p_path, "README.md")
            desc = f"Plugin Ruflo oficial {item} para Claude Code e Codex."
            if os.path.exists(readme_path):
                try:
                    with open(readme_path, 'r', encoding='utf-8') as f:
                        c = f.read()
                        extracted_desc = get_first_paragraph(c)
                        if extracted_desc:
                            desc = extracted_desc
                except:
                    pass
            
            cat = categorize_plugin(item)
            item_data = {
                "id": item,
                "title": item.replace("ruflo-", "").replace("-", " ").title() + f" ({item})",
                "description": desc,
                "icon": icons.get(item, "🧩"),
                "path": f"ruflo/plugins/{item}/README.md" if os.path.exists(readme_path) else f"ruflo/plugins/{item}"
            }
            categories[cat].append(item_data)

    return categories

def categorize_agent(subpath):
    subpath = subpath.replace('\\', '/').lower()
    if '/core/' in subpath or '/development/' in subpath:
        return "AGENTES: CORE & DEV"
    elif '/consensus/' in subpath or '/hive-mind/' in subpath:
        return "AGENTES: CONSENSO & HIVE-MIND"
    elif '/swarm/' in subpath or '/dual-mode/' in subpath or '/goal/' in subpath or '/reasoning/' in subpath:
        return "AGENTES: SWARM & COORDENAÇÃO"
    elif '/sparc/' in subpath or '/architecture/' in subpath:
        return "AGENTES: SPARC & ARQUITETURA"
    elif '/github/' in subpath or '/devops/' in subpath or '/documentation/' in subpath:
        return "AGENTES: DEVOPS & GITHUB"
    elif '/optimization/' in subpath or '/sublinear/' in subpath or '/neural/' in subpath or '/sona/' in subpath:
        return "AGENTES: OTIMIZAÇÃO & PERFORMANCE"
    elif '/v3/' in subpath or '/specialized/' in subpath or '/data/' in subpath or '/testing/' in subpath:
        return "AGENTES: V3 FLEET & ESPECIALISTAS"
    else:
        return "AGENTES: ESPECIALIZADOS DIVERSOS"

def extract_agents():
    agents_dir = os.path.join(RUFLO_DIR, ".claude", "agents")
    if not os.path.exists(agents_dir):
        return {}

    categories = {
        "AGENTES: CORE & DEV": [],
        "AGENTES: CONSENSO & HIVE-MIND": [],
        "AGENTES: SWARM & COORDENAÇÃO": [],
        "AGENTES: SPARC & ARQUITETURA": [],
        "AGENTES: DEVOPS & GITHUB": [],
        "AGENTES: OTIMIZAÇÃO & PERFORMANCE": [],
        "AGENTES: V3 FLEET & ESPECIALISTAS": [],
        "AGENTES: ESPECIALIZADOS DIVERSOS": []
    }

    for root, dirs, files in os.walk(agents_dir):
        for file in files:
            if file.endswith('.md') and not file.startswith('MIGRATION'):
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, RUFLO_DIR).replace('\\', '/')
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    meta, body = parse_frontmatter(content)
                    name = meta.get('name', file.replace('.md', ''))
                    desc = meta.get('description', '')
                    if not desc:
                        desc = get_first_paragraph(body)
                    if not desc:
                        desc = f"Agente autônomo Ruflo especializado: {name}."

                    cat = categorize_agent(rel_path)
                    
                    agent_item = {
                        "id": "agent-" + name,
                        "title": name.replace('-', ' ').title(),
                        "description": desc,
                        "icon": "🤖",
                        "path": f"ruflo/{rel_path}"
                    }
                    categories[cat].append(agent_item)
                except Exception as e:
                    pass

    return {k: v for k, v in categories.items() if v}

def main():
    guides = extract_guides()
    plugins_cats = extract_plugins()
    agents_cats = extract_agents()

    all_data = {
        "VISÃO GERAL & GUIAS": guides
    }
    all_data.update(plugins_cats)
    all_data.update(agents_cats)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(f"const rufloData = {json.dumps(all_data, indent=4, ensure_ascii=False)};\n\n")
        f.write("if(typeof module !== 'undefined') module.exports = rufloData;\n")

    total_items = sum(len(items) for items in all_data.values())
    print(f"Generated {OUTPUT_FILE} with {len(all_data)} categories and {total_items} total items.")

if __name__ == '__main__':
    main()
