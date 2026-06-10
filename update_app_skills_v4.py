import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# Replace the specific hardcoded pink/red styles
app_js = app_js.replace("catHeader.style.color = '#fff';", "catHeader.style.color = '#323130';")
app_js = app_js.replace("catHeader.style.backgroundColor = 'rgba(232,0,106,.2)';", "catHeader.style.backgroundColor = '#f3f2f1';")
app_js = app_js.replace("catHeader.style.borderLeft = '3px solid #e8006a';", "catHeader.style.borderLeft = '4px solid #0078d4';")

app_js = app_js.replace("catHeader.onmouseover = () => catHeader.style.backgroundColor = 'rgba(232,0,106,.4)';", "catHeader.onmouseover = () => catHeader.style.backgroundColor = '#e1dfdd';")
app_js = app_js.replace("catHeader.onmouseout = () => catHeader.style.backgroundColor = 'rgba(232,0,106,.2)';", "catHeader.onmouseout = () => catHeader.style.backgroundColor = '#f3f2f1';")

# Replace card header pink tags
app_js = app_js.replace("border-bottom:2px solid #e8006a;", "border-bottom:2px solid #0078d4;")
app_js = app_js.replace("border-left:4px solid #e8006a;", "border-left:4px solid #0078d4;")
app_js = app_js.replace("color: #e8006a;", "color: #0078d4;")
app_js = app_js.replace("color:#e8006a;", "color:#0078d4;")
app_js = app_js.replace("background:rgba(232,0,106,.12);", "background:rgba(0,120,212,.12);")
app_js = app_js.replace("border:1px solid rgba(232,0,106,.3);", "border:1px solid rgba(0,120,212,.3);")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
