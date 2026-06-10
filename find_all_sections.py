import re
import sys

with open('contexto/scrumban_guia.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's find all divs that look like a main section wrapper.
# Usually they are <div id="..." class="section"> or <section id="...">
sections = re.findall(r'<div[^>]*id="([^"]+)"[^>]*class="[^"]*section[^"]*"', html, re.IGNORECASE)
sections += re.findall(r'<section[^>]*id="([^"]+)"', html, re.IGNORECASE)

# Deduplicate
sections = list(set(sections))

with open('app.js', 'r', encoding='utf-8') as f:
    app = f.read()

app_ids = set(re.findall(r"id:\s*'([^']+)'", app))

missing = [s for s in sections if s not in app_ids]

print(f"Total top-level section IDs found in HTML: {len(sections)}")
print(f"Mapped in app.js: {len(app_ids)}")
print(f"Missing sections: {missing}")

# If we also want to find standalone h1/h2 tags that might be missed:
h_tags = re.findall(r'<(h[1-2])[^>]*>(.*?)</\1>', html, re.IGNORECASE)
print(f"\nTotal H1/H2 tags found: {len(h_tags)}")

with open('missing_sections.txt', 'w', encoding='utf-8') as f:
    f.write(f"Missing sections: {missing}\n")
