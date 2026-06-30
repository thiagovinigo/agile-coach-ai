import re

# 1. Read the HTML file
html_path = 'c:/Users/User/.antigravity/Agile Coach AI/contexto/scrumban_guia.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 2. Extract the script block
script_match = re.search(r'<script>\s*const kiroSim = (.*?);\s*// Auto-init.*?setTimeout.*?</script>', html, re.DOTALL)

if script_match:
    script_content = script_match.group(0)
    kiro_obj = script_match.group(1)
    
    # Remove from HTML
    new_html = html.replace(script_content, '')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Removed script from HTML.")

    # 3. Append to app.js
    app_js_path = 'c:/Users/User/.antigravity/Agile Coach AI/app.js'
    with open(app_js_path, 'a', encoding='utf-8') as f:
        f.write("\n\n// --- INJETADO PARA SIMULADOR KIRO ---\n")
        f.write("window.kiroSim = " + kiro_obj + ";\n")
        # Ensure it initializes when elements are present
        f.write("""
// Auto-init when DOM is ready and elements exist
setInterval(() => {
  if(document.getElementById('sim-board') && !window.kiroSim._initialized) {
    window.kiroSim.init();
    window.kiroSim._initialized = true;
  }
}, 1000);
""")
    print("Injected kiroSim into app.js successfully.")
else:
    print("Script block not found in HTML.")
