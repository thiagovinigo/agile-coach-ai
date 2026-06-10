import re

with open('contexto/scrumban_guia.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Only find main sections that likely correspond to content blocks (starting with s-)
html_ids = set(re.findall(r'<div[^>]*id="(s-[^"]+)"[^>]*>.*?<h[1-3]', html, re.IGNORECASE))
# Let's broaden it to all s- ids that have a section
html_ids = set(re.findall(r'id="(s-[^"]+)"', html))

with open('app.js', 'r', encoding='utf-8') as f:
    app = f.read()

app_ids = set(re.findall(r"id:\s*'([s]-[^\']+)'", app))

missing = sorted(list(html_ids - app_ids))

with open('missing_ids.txt', 'w', encoding='utf-8') as f:
    f.write(f"Total HTML s-* IDs: {len(html_ids)}\n")
    f.write(f"Mapped in app.js: {len(app_ids)}\n")
    f.write("Missing from app.js:\n" + '\n'.join(missing))
