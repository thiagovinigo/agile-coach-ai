import os
import re
import json

AGENTS_DIR = "contexto/get-shit-done/agents"
OUTPUT_FILE = "gsd-data.js"

def parse_agent_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    if not match:
        print(f"No frontmatter found in {filepath}")
        return None

    frontmatter = match.group(1)

    agent_data = {}
    for line in frontmatter.split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            agent_data[key.strip()] = val.strip()

    name = agent_data.get('name', os.path.basename(filepath).replace('.md', '')).strip('"').strip("'")
    description = agent_data.get('description', '').strip('"').strip("'")

    return {
        "id": name,
        "title": name.replace('gsd-', '').replace('-', ' ').title(),
        "description": description,
        "path": filepath.replace('\\', '/')
    }

def main():
    if not os.path.exists(AGENTS_DIR):
        print(f"Directory {AGENTS_DIR} not found!")
        return

    agents = []
    for filename in os.listdir(AGENTS_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(AGENTS_DIR, filename)
            data = parse_agent_file(filepath)
            if data:
                agents.append(data)

    output_data = {
        "GSD Agents": agents
    }

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(f"const gsdData = {json.dumps(output_data, indent=4)};\n")
        f.write("if(typeof module !== 'undefined') module.exports = gsdData;\n")

    print(f"Successfully wrote {len(agents)} agents to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
