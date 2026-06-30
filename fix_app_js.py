import re

app_js_path = 'c:/Users/User/.antigravity/Agile Coach AI/app.js'
with open(app_js_path, 'r', encoding='utf-8') as f:
    content = f.read()

# The error comes from unescaped double quotes inside a double-quoted string literal.
# In Python: onclick='openInfoModalDirect(\"skills/refinamento/SKILL\")'
# Translates to JS: onclick='openInfoModalDirect("skills/refinamento/SKILL")' inside a string starting with "out: "...""
# Let's fix this by using &quot; instead of double quotes, or escaping them with double backslashes.

# Let's replace 'openInfoModalDirect(" with 'openInfoModalDirect(&quot;
fixed_content = content.replace('openInfoModalDirect("skills/refinamento/SKILL")', 'openInfoModalDirect(&quot;skills/refinamento/SKILL&quot;)')
fixed_content = fixed_content.replace('openInfoModalDirect("skills/arquitetura/SKILL")', 'openInfoModalDirect(&quot;skills/arquitetura/SKILL&quot;)')
fixed_content = fixed_content.replace('openInfoModalDirect("skills/engenheiro-software/SKILL")', 'openInfoModalDirect(&quot;skills/engenheiro-software/SKILL&quot;)')
fixed_content = fixed_content.replace('openInfoModalDirect("skills/engenharia-qa/SKILL")', 'openInfoModalDirect(&quot;skills/engenharia-qa/SKILL&quot;)')

with open(app_js_path, 'w', encoding='utf-8') as f:
    f.write(fixed_content)
    
print("Fixed SyntaxError in app.js")
