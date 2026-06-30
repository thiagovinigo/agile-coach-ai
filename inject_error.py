import re

path = 'c:/Users/User/.antigravity/Agile Coach AI/index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

error_script = """<script>
window.onerror = function(msg, url, line, col, error) {
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
};
</script>
</head>"""

content = content.replace('</head>', error_script)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Injected error logger into index.html")
