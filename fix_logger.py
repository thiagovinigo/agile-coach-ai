import re

path = 'c:/Users/User/.antigravity/Agile Coach AI/index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the old error script
new_error_script = """<script>
var errorCount = 0;
window.onerror = function(msg, url, line, col, error) {
    if (errorCount > 0) return;
    errorCount++;
    console.error("GLOBAL ERROR:", msg, line, col);
    
    // Create an alert so the user can copy it even if DOM is not ready
    alert("ERRO ENCONTRADO! Copie isso e envie:\\n" + msg + "\\nLinha: " + line);
    
    if (document.body) {
        var errorDiv = document.createElement('div');
        errorDiv.style.position = 'fixed';
        errorDiv.style.top = '0';
        errorDiv.style.left = '0';
        errorDiv.style.width = '100%';
        errorDiv.style.background = 'red';
        errorDiv.style.color = 'white';
        errorDiv.style.zIndex = '999999';
        errorDiv.style.padding = '20px';
        errorDiv.style.fontFamily = 'monospace';
        errorDiv.innerHTML = '<strong>Error:</strong> ' + msg + '<br>Line: ' + line + '<br>Col: ' + col + '<br>Stack: ' + (error ? error.stack : '');
        document.body.appendChild(errorDiv);
    }
};
</script>
</head>"""

# Find the old script and replace
content = re.sub(r'<script>\s*window\.onerror = function[\s\S]*?</script>\s*</head>', new_error_script, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated error logger")
