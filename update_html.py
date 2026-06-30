import re

html_path = 'c:/Users/User/.antigravity/Agile Coach AI/contexto/scrumban_guia.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update buttons
old_buttons = """      <button id="btn-next-step" onclick="kiroSim.nextStep()" style="background:#3b82f6; color:white; border:none; padding:10px 20px; border-radius:6px; font-weight:bold; cursor:pointer; font-size:14px; box-shadow:0 2px 4px rgba(59,130,246,0.3); transition: background 0.2s;">
        ▶ Próximo Passo: Rodar IA
      </button>"""

new_buttons = """      <div style="display:flex; gap:10px;">
        <button id="btn-restart-step" onclick="kiroSim.resetStep()" style="background:#94a3b8; color:white; border:none; padding:10px 15px; border-radius:6px; font-weight:bold; cursor:pointer; font-size:13px; transition: opacity 0.2s;" title="Voltar ao início">
          🔄 Reiniciar
        </button>
        <button id="btn-prev-step" onclick="kiroSim.prevStep()" style="background:#64748b; color:white; border:none; padding:10px 15px; border-radius:6px; font-weight:bold; cursor:pointer; font-size:13px; transition: opacity 0.2s;" title="Passo anterior">
          ⏪ Voltar
        </button>
        <button id="btn-next-step" onclick="kiroSim.nextStep()" style="background:#3b82f6; color:white; border:none; padding:10px 20px; border-radius:6px; font-weight:bold; cursor:pointer; font-size:14px; box-shadow:0 2px 4px rgba(59,130,246,0.3); transition: background 0.2s;">
          ▶ Próximo Passo
        </button>
      </div>"""

html = html.replace(old_buttons, new_buttons)

# 2. Add Steering Section
# Locate where to inject: after the <div class="background:#1e293b; color:#f8fafc; padding:15px; border-radius:6px; font-family:monospace; ... </div></div></div>
target_steering = """<span style="color:#10b981;">&lt;/mcp_trigger&gt;</span></div>
    </div>
  </div>"""

steering_html = """<span style="color:#10b981;">&lt;/mcp_trigger&gt;</span></div>
    </div>
  </div>

  <!-- A Ciência do Steering -->
  <h3 style="margin:30px 0 15px; color:#1e293b; border-bottom:2px solid #8b5cf6; padding-bottom:8px;">🎯 A Ciência do Steering (Direcionamento)</h3>
  <p style="font-size:14px; color:#475569; margin-bottom:20px;">
    No mundo de IA Agêntica, <strong>Steering</strong> não é apenas "escrever um prompt pedindo por favor". Steering é a técnica de <em>restringir o espaço de ação matemática do modelo</em>, garantindo que ele opere de forma previsível e segura dentro do seu fluxo corporativo.
  </p>

  <div style="display:flex; gap:20px; margin-bottom:30px; flex-wrap:wrap;">
    <div style="flex:1; min-width:300px; background:#fef2f2; border:1px solid #fca5a5; padding:15px; border-radius:8px;">
      <strong style="color:#b91c1c; font-size:14px; display:flex; align-items:center; gap:8px;"><span style="font-size:20px;">❌</span> Steering Fraco (Chatbot)</strong>
      <p style="font-size:13px; color:#7f1d1d; margin-top:10px;">
        <em>"Você é um gerente de produto. Escreva um PRD detalhado usando a descrição que o usuário passou e salve no Board."</em>
      </p>
      <ul style="font-size:12px; color:#991b1b; padding-left:20px;">
        <li>Se faltar dado, a IA vai inventar (alucinar) regras para "agradar" o usuário.</li>
        <li>O formato de saída varia a cada execução.</li>
        <li>Não há bloqueio de governança (Gate).</li>
      </ul>
    </div>

    <div style="flex:1; min-width:300px; background:#f0fdf4; border:1px solid #86efac; padding:15px; border-radius:8px;">
      <strong style="color:#15803d; font-size:14px; display:flex; align-items:center; gap:8px;"><span style="font-size:20px;">✅</span> Steering Forte (Agente Kiro)</strong>
      <p style="font-size:13px; color:#166534; margin-top:10px;">
        <em>"Se a descrição tiver menos de 20 palavras ou faltarem as regras de negócio core, OBRIGATORIAMENTE interrompa a tarefa. Gere um JSON Patch na tag 'DEP-Negocio' via MCP e pare."</em>
      </p>
      <ul style="font-size:12px; color:#14532d; padding-left:20px;">
        <li>A IA é forçada a validar a entrada (Quality Gate).</li>
        <li>Se a condição não for atendida, ela usa a ferramenta para "rejeitar" o card.</li>
        <li>O fluxo se torna 100% previsível e corporativo.</li>
      </ul>
    </div>
  </div>"""

html = html.replace(target_steering, steering_html)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
    
print("Updated HTML with buttons and steering section.")
