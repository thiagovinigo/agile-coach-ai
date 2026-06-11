import os
import json
import re
import yaml

base_dir = r"C:\Users\User\.antigravity\Agile Coach AI\contexto\ECC-main"
agents_dir = os.path.join(base_dir, "agents")
skills_dir = os.path.join(base_dir, "skills")

ecc_agents_file = r"C:\Users\User\.antigravity\Agile Coach AI\ecc-agents-data.js"
ecc_skills_file = r"C:\Users\User\.antigravity\Agile Coach AI\ecc-skills-data.js"

# 1. Parse Agents
agents_db = []
if os.path.exists(agents_dir):
    for filename in os.listdir(agents_dir):
        if filename.endswith(".md"):
            path = os.path.join(agents_dir, filename)
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            name = filename.replace('.md', '').replace('-', ' ').title()
            description = ""
            icon = "🤖"
            
            # parse frontmatter
            if content.startswith("---"):
                parts = content.split("---")
                if len(parts) >= 3:
                    frontmatter_text = parts[1]
                    try:
                        fm = yaml.safe_load(frontmatter_text)
                        if fm:
                            if 'name' in fm:
                                name = fm['name'].replace('-', ' ').title()
                            if 'description' in fm:
                                description = fm['description']
                    except Exception as e:
                        pass
            
            agents_db.append({
                'id': filename.replace('.md', ''),
                'title': name,
                'description': description,
                'icon': icon,
                'path': f'contexto/ECC-main/agents/{filename}'
            })

with open(ecc_agents_file, 'w', encoding='utf-8') as f:
    f.write("const eccAgentsData = " + json.dumps(agents_db, indent=4, ensure_ascii=False) + ";\n")

print(f"Generated {ecc_agents_file} with {len(agents_db)} agents.")

# 2. Parse Skills
skills_db = []
link_regex = re.compile(r'\[.*?\]\((?:\.\./)+([a-zA-Z0-9-]+)/SKILL\.md\)')

if os.path.exists(skills_dir):
    for root, dirs, files in os.walk(skills_dir):
        if 'SKILL.md' in files:
            skill_id = os.path.basename(root)
            category_folder = os.path.basename(os.path.dirname(root))
            
            if category_folder == 'skills':
                category = 'Uncategorized'
            else:
                category = category_folder.replace('-', ' ').title()
                
            with open(os.path.join(root, 'SKILL.md'), 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            title = skill_id.replace('-', ' ').title()
            description = ""
            triggers = []
            
            if content.startswith('---'):
                parts = content.split('---')
                if len(parts) >= 3:
                    frontmatter = parts[1]
                    for line in frontmatter.split('\n'):
                        if line.startswith('description:'):
                            description = line.replace('description:', '').strip().strip("'\"")
            
            triggers_matches = re.findall(r'`?(/[a-z0-9-]+)`?', content)
            triggers = list(set([t for t in triggers_matches if len(t) > 2]))
            
            dependencies_matches = link_regex.findall(content)
            dependencies = list(set([d.replace('-', ' ').title() for d in dependencies_matches]))
            
            skills_db.append({
                'id': skill_id,
                'category': category,
                'title': title,
                'description': description,
                'triggers': triggers,
                'dependencies': dependencies,
                'path': f'contexto/ECC-main/skills/{os.path.relpath(root, skills_dir).replace("\\", "/")}/SKILL.md'
            })

grouped_skills = {}
for s in skills_db:
    c = s['category']
    if c not in grouped_skills:
        grouped_skills[c] = []
    grouped_skills[c].append(s)

for cat in grouped_skills:
    grouped_skills[cat].sort(key=lambda x: x['title'])

with open(ecc_skills_file, 'w', encoding='utf-8') as f:
    f.write("const eccSkillsData = " + json.dumps(grouped_skills, indent=4, ensure_ascii=False) + ";\n")

print(f"Generated {ecc_skills_file} with {len(skills_db)} skills.")
