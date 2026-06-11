import re

with open('contexto/scrumban_guia.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'gerarPromptIA\((.*?)\)', r'gerarPromptIA(\1, this)', text)
text = re.sub(r'gerarPromptIA\((.*?), this, this\)', r'gerarPromptIA(\1, this)', text) # Fix double replacement if any

text = re.sub(r'copiarPromptIA\(\)', r'copiarPromptIA(this)', text)
text = re.sub(r'copiarPromptIA\(this, this\)', r'copiarPromptIA(this)', text) # Fix double replacement if any

# Also update IDs to classes for querying
text = text.replace('id="ia-story-input"', 'id="ia-story-input" class="ia-story-input"')
text = text.replace('id="ia-output-label"', 'id="ia-output-label" class="ia-output-label"')
text = text.replace('id="ia-output-text"', 'id="ia-output-text" class="ia-output-text"')
text = text.replace('id="ia-output-area"', 'id="ia-output-area" class="ia-output-area"')
text = text.replace('id="ia-copy-ok"', 'id="ia-copy-ok" class="ia-copy-ok"')

with open('contexto/scrumban_guia.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Fixed HTML')
