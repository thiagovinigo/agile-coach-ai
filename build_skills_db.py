import os
import json
import re

base_dir = r"C:\Users\User\.antigravity\Agile Coach AI\flowgrammers-skills-main\flowgrammers-skills-main"
output_file = r"C:\Users\User\.antigravity\Agile Coach AI\skills-data.js"

skills_db = []

# Regex para encontrar conexões: ../nome-da-skill/SKILL.md
link_regex = re.compile(r'\[.*?\]\((?:\.\./)+([a-zA-Z0-9-]+)/SKILL\.md\)')

for root, dirs, files in os.walk(base_dir):
    # skip .git
    if '.git' in dirs:
        dirs.remove('.git')
    
    if 'SKILL.md' in files:
        # We are inside a skill folder
        skill_id = os.path.basename(root)
        category_folder = os.path.basename(os.path.dirname(root))
        
        # If it's directly inside flowgrammers-skills-main, the category is 'Root'
        if category_folder == 'flowgrammers-skills-main':
            category = 'Uncategorized'
        else:
            # Embelezar a categoria
            category = category_folder.replace('-', ' ').title()

        if category == 'Skills' and '.agents' in root:
            category = 'Agents (Advanced Skills)'
            
        with open(os.path.join(root, 'SKILL.md'), 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
            # extract frontmatter
            title = skill_id.replace('-', ' ').title()
            description = ""
            triggers = []
            
            if content.startswith('---'):
                parts = content.split('---')
                if len(parts) >= 3:
                    frontmatter = parts[1]
                    for line in frontmatter.split('\n'):
                        if line.startswith('name:'):
                            pass
                        elif line.startswith('description:'):
                            description = line.replace('description:', '').strip()
            
            # extrair triggers do corpo do texto (linhas que começam com `/nome`)
            triggers_matches = re.findall(r'`?(/[a-z0-9-]+)`?', content)
            triggers = list(set([t for t in triggers_matches if len(t) > 2]))

            # NOVO: extrair dependencies
            dependencies_matches = link_regex.findall(content)
            dependencies = list(set([d.replace('-', ' ').title() for d in dependencies_matches]))
            
            skills_db.append({
                'id': skill_id,
                'category': category,
                'title': title,
                'description': description,
                'triggers': triggers,
                'dependencies': dependencies,
                'path': os.path.relpath(root, base_dir).replace('\\', '/') + '/SKILL.md'
            })

# Group by category
grouped = {}
for s in skills_db:
    c = s['category']
    if c not in grouped:
        grouped[c] = []
    grouped[c].append(s)

# Sort
for cat in grouped:
    grouped[cat].sort(key=lambda x: x['title'])

# Write to file
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("const skillsData = " + json.dumps(grouped, indent=4, ensure_ascii=False) + ";")

print(f"Generated skills-data.js with {len(skills_db)} skills across {len(grouped)} categories. Includes dependencies!")
