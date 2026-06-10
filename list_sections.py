import re
import sys

with open('contexto/scrumban_guia.html', 'r', encoding='utf-8') as f:
    html = f.read()

ids = re.findall(r'id="([^"]+)"', html)
output = [f"Total IDs: {len(ids)}", "\n--- Sections found ---"]

pattern = re.compile(r'<div[^>]*id="([^"]+)"[^>]*>.*?<(h[1-3])[^>]*>(.*?)</\2>', re.DOTALL | re.IGNORECASE)
matches = pattern.findall(html)

for match in matches:
    title = re.sub(r'<[^>]+>', '', match[2]).strip()
    output.append(f"ID: {match[0]} | Tag: {match[1]} | Title: {title}")

# Also find all sections starting with s- to make sure we don't miss those without h1/h2/h3 immediately inside
s_ids = [i for i in ids if i.startswith('s-')]
output.append("\n--- All 's-*' IDs ---")
for s in s_ids:
    output.append(s)

with open('sections_output.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))
