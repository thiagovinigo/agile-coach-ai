import re

files = ['labs_doc.js']

for filename in files:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    prefix = "container.innerHTML = `"
    suffix = "    `;\n}"
    
    if prefix in content and suffix in content:
        start_idx = content.find(prefix) + len(prefix)
        end_idx = content.rfind(suffix)
        
        inner_html = content[start_idx:end_idx]
        
        # We need to replace `word` with <code>word</code>
        # The easiest way is to use a regex
        inner_html_fixed = re.sub(r'`([^`]+)`', r'<code>\1</code>', inner_html)
        
        new_content = content[:start_idx] + inner_html_fixed + content[end_idx:]
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Fixed {filename}')
    else:
        print(f'Prefix/Suffix not found in {filename}')
