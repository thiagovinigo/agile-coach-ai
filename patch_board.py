import re

with open('legacy-scripts.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Export DQ to window.DQ
if "window.DQ = DQ;" not in code:
    code = code.replace("var currentDQCol = null;", "window.DQ = DQ;\nvar currentDQCol = null;")

# 2. Modify showPolicy
show_policy_start = code.find("window.showPolicy = function(colId) {")
show_policy_end = code.find("};", show_policy_start) + 2

old_show_policy = code[show_policy_start:show_policy_end]

new_show_policy = """window.showPolicy = function(colId) {
    var policy = policies[colId];
    if (!policy) return;
    
    var dqKeyMap = {
      'pronto-replen': 'pronto-rep',
      'dev-dep': 'dev-fin',
      'testes-fin': 'tests-fin',
      'validacao-po': 'valid-po',
      'nao-homologado': 'nao-homol',
      'liberada': 'lib-instalar',
      'em-producao': 'em-prod'
    };
    var dqKey = dqKeyMap[colId] || colId;
    
    var panel = document.getElementById('policy-panel');
    var title = document.getElementById('policy-title');
    var body = document.getElementById('policy-body');
    title.textContent = policy.title;
    title.style.color = policy.color;
    
    var html = policy.fields.map(function(f) {
      return '<div style="background:var(--bg-primary,#fff);border:1px solid var(--border,#e2e8f0);border-radius:8px;padding:12px 14px;">' +
        '<div style="font-size:12px;font-weight:700;color:' + policy.color + ';margin-bottom:4px;">' + f.label + '</div>' +
        '<div style="font-size:13px;line-height:1.5;color:var(--text-primary,#1e293b);">' + f.value + '</div>' +
        '</div>';
    }).join('');
    
    if (window.DQ && window.DQ[dqKey] && window.DQ[dqKey].questions && window.DQ[dqKey].questions.length > 0) {
      html += '<div style="margin-top:16px;background:#f8fafc;border:2px dashed #94a3b8;border-radius:8px;padding:12px 14px;">' +
              '<div style="font-size:14px;font-weight:800;color:#334155;margin-bottom:8px;">❓ Perguntas sugeridas para a Daily:</div>' +
              '<ul style="margin:0;padding-left:20px;font-size:13px;color:#475569;">' +
              window.DQ[dqKey].questions.map(function(q){ return '<li style="margin-bottom:6px;">' + q.q + '</li>'; }).join('') +
              '</ul></div>';
    }
    
    body.innerHTML = html;
    
    panel.style.display = 'block';
    panel.style.borderColor = policy.color;
    panel.scrollIntoView({behavior:'smooth', block:'nearest'});
    
    // highlight active column
    document.querySelectorAll('.bcol').forEach(function(el){ el.style.outline = 'none'; });
    var activeCol = document.querySelector('[data-col="' + colId + '"]');
    if (activeCol) activeCol.style.outline = '3px solid ' + policy.color;
  };"""

code = code.replace(old_show_policy, new_show_policy)

with open('legacy-scripts.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("legacy-scripts.js modificado com sucesso!")
