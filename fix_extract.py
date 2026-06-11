import re

with open('app.js', 'r', encoding='utf-8') as f:
    code = f.read()

if "extractSection('kb-tfs', 'kb-tfs');" not in code:
    code = code.replace("extractSection('kb-case', 'kb-case');", "extractSection('kb-case', 'kb-case');\n        extractSection('kb-tfs', 'kb-tfs');")
    
    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(code)

print("extractSection patched.")
