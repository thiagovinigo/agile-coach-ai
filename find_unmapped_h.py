import re

with open('contexto/scrumban_guia.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find all <h2> or <h1> and their closest parent ID
h_tags = re.findall(r'<div[^>]*id="([^"]+)"[^>]*>.*?<(h[1-2])[^>]*>(.*?)</\2>', html, re.DOTALL | re.IGNORECASE)

with open('app.js', 'r', encoding='utf-8') as f:
    app = f.read()

app_ids = set(re.findall(r"id:\s*'([^']+)'", app))

missing_h = []
for tag in h_tags:
    div_id = tag[0]
    title = re.sub(r'<[^>]+>', '', tag[2]).strip()
    if div_id not in app_ids:
        missing_h.append(f"{div_id}: {title}")

with open('missing_h_tags.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(missing_h))
