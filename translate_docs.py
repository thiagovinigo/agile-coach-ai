import os
import re
import time
import requests

requests.packages.urllib3.disable_warnings()
old_request = requests.Session.request
def new_request(self, method, url, **kwargs):
    kwargs['verify'] = False
    return old_request(self, method, url, **kwargs)
requests.Session.request = new_request

from deep_translator import GoogleTranslator

def translate_text(text):
    if not text.strip():
        return text
    try:
        # Google Translate limits length, so we chunk it by double newlines if it's too long,
        # but deep-translator handles up to 5000 chars. 
        if len(text) < 4900:
            return GoogleTranslator(source='en', target='pt').translate(text)
        else:
            chunks = text.split('\n\n')
            translated = []
            for chunk in chunks:
                if len(chunk) > 4900:
                    subchunks = chunk.split('. ')
                    tr_sub = [GoogleTranslator(source='en', target='pt').translate(sc) for sc in subchunks if sc]
                    translated.append('. '.join(tr_sub))
                elif chunk.strip():
                    translated.append(GoogleTranslator(source='en', target='pt').translate(chunk))
                else:
                    translated.append(chunk)
            return '\n\n'.join(translated)
    except Exception as e:
        print(f"Translate error: {e}")
        return text

def process_markdown(content):
    # Separate frontmatter
    frontmatter = ""
    body = content
    match = re.match(r'^(---\s*\n.*?\n---\s*\n)(.*)', content, re.DOTALL)
    if match:
        frontmatter = match.group(1)
        body = match.group(2)
        
    # We want to protect code blocks from translation
    code_blocks = []
    def save_code_block(m):
        code_blocks.append(m.group(0))
        return f"\n\n[[[CODE_BLOCK_{len(code_blocks)-1}]]]\n\n"
        
    body = re.sub(r'```[\s\S]*?```', save_code_block, body)
    
    # Translate body
    print("Translating body...")
    translated_body = translate_text(body)
    
    # Restore code blocks
    for i, block in enumerate(code_blocks):
        translated_body = translated_body.replace(f"[[[CODE_BLOCK_{i}]]]", block)
        
    return frontmatter + translated_body

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                path = os.path.join(root, file)
                print(f"Translating {path}...")
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if it looks already translated (e.g. contains "Quando usar" or similar)
                if 'Quando usar' in content or 'Você DEVE usar' in content:
                    print(f"Skipping {path}, seems already translated.")
                    continue
                    
                new_content = process_markdown(content)
                
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                time.sleep(0.5) # respect API limits

if __name__ == "__main__":
    process_directory("contexto/superpowers/skills")
    process_directory("contexto/get-shit-done/agents")
    print("Translation complete!")
