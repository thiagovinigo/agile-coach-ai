import os
import re
import json

SKILLS_DIR = "contexto/superpowers/skills"
OUTPUT_FILE = "superpowers-data.js"

def parse_skill_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

    # Parse yaml frontmatter
    # Format typically:
    # ---
    # name: ...
    # description: ...
    # ---
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    if not match:
        print(f"No frontmatter found in {filepath}")
        return None

    frontmatter = match.group(1)
    body = match.group(2)

    skill_data = {}
    for line in frontmatter.split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            skill_data[key.strip()] = val.strip()
            
    # Sometimes quotes are added in description, remove them
    description = skill_data.get('description', '').strip('"').strip("'")
    name = skill_data.get('name', os.path.basename(os.path.dirname(filepath))).strip('"').strip("'")

    return {
        "id": name,
        "title": name.replace('-', ' ').title(),
        "description": description,
        "path": filepath.replace('\\', '/')
    }

def main():
    if not os.path.exists(SKILLS_DIR):
        print(f"Directory {SKILLS_DIR} not found!")
        return

    skills = []
    for skill_folder in os.listdir(SKILLS_DIR):
        folder_path = os.path.join(SKILLS_DIR, skill_folder)
        if os.path.isdir(folder_path):
            skill_md = os.path.join(folder_path, "SKILL.md")
            if os.path.exists(skill_md):
                data = parse_skill_file(skill_md)
                if data:
                    skills.append(data)

    output_data = {
        "Superpowers": skills
    }

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(f"const superpowersData = {json.dumps(output_data, indent=4)};\n")
        f.write("if(typeof module !== 'undefined') module.exports = superpowersData;\n")

    print(f"Successfully wrote {len(skills)} skills to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
