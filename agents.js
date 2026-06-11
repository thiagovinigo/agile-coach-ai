document.addEventListener('DOMContentLoaded', () => {
    const agentsView = document.getElementById('agents-view');

    const renderAgentsUI = () => {
        agentsView.innerHTML = `
            <div class="hero-section">
                <h3>🤖 AI Agents Colaboradores</h3>
                <p>Acelere seu dia a dia utilizando inteligências artificiais especializadas em papéis ágeis. Selecione um agente abaixo para receber insights, elaborar cerimônias ou analisar métricas.</p>
            </div>

            <div class="grid-cards">
                <!-- Agent 1 -->
                <div class="card" style="position:relative;">
                    <button onclick="openAgentInfo(this)" data-title="Scrum Master Bot" data-icon="🧙‍♂️" data-desc="${encodeURIComponent('Especialista em facilitação de cerimônias, resolução de conflitos e remoção de impedimentos no nível do time.')}" style="position:absolute; top:12px; right:12px; background:transparent; border:1px solid #c8c6c4; border-radius:50%; width:24px; height:24px; color:#605e5c; cursor:pointer; font-weight:bold; display:flex; justify-content:center; align-items:center;" title="Ver detalhes">?</button>
                    <div class="card-icon">🧙‍♂️</div>
                    <div class="card-title">Scrum Master Bot</div>
                    <div class="card-desc">Especialista em facilitação de cerimônias, resolução de conflitos e remoção de impedimentos no nível do time.</div>
                    <button class="card-action" onclick="openChat('Scrum Master Bot', '🧙‍♂️')">
                        Conversar
                    </button>
                </div>

                <!-- Agent 2 -->
                <div class="card" style="position:relative;">
                    <button onclick="openAgentInfo(this)" data-title="Flow Metrics AI" data-icon="📊" data-desc="${encodeURIComponent('Análise preditiva de fluxo, cálculo de previsibilidade probabilística, throughput e identificação de gargalos.')}" style="position:absolute; top:12px; right:12px; background:transparent; border:1px solid #c8c6c4; border-radius:50%; width:24px; height:24px; color:#605e5c; cursor:pointer; font-weight:bold; display:flex; justify-content:center; align-items:center;" title="Ver detalhes">?</button>
                    <div class="card-icon">📊</div>
                    <div class="card-title">Flow Metrics AI</div>
                    <div class="card-desc">Análise preditiva de fluxo, cálculo de previsibilidade probabilística, throughput e identificação de gargalos.</div>
                    <button class="card-action" onclick="openChat('Flow Metrics AI', '📊')">
                        Conversar
                    </button>
                </div>

                <!-- Agent 3 -->
                <div class="card" style="position:relative;">
                    <button onclick="openAgentInfo(this)" data-title="PO Copilot" data-icon="🧑‍💼" data-desc="${encodeURIComponent('Apoio para fatiar épicos, escrever histórias de usuário com critérios de aceite e priorizar backlog.')}" style="position:absolute; top:12px; right:12px; background:transparent; border:1px solid #c8c6c4; border-radius:50%; width:24px; height:24px; color:#605e5c; cursor:pointer; font-weight:bold; display:flex; justify-content:center; align-items:center;" title="Ver detalhes">?</button>
                    <div class="card-icon">🧑‍💼</div>
                    <div class="card-title">Product Owner Copilot</div>
                    <div class="card-desc">Apoio para fatiar épicos, escrever histórias de usuário com critérios de aceite e priorizar backlog.</div>
                    <button class="card-action" onclick="openChat('PO Copilot', '🧑‍💼')">
                        Conversar
                    </button>
                </div>
            </div>

            <div id="chat-modal" style="display:none; margin-top: 32px;">
                <div class="chat-container">
                    <div class="chat-header">
                        <span id="chat-icon" style="font-size: 24px;">🤖</span>
                        <div>
                            <h4 id="chat-title" style="color:#fff;">Agente</h4>
                            <span style="font-size:12px; color:var(--success);">● Online</span>
                        </div>
                        <button onclick="closeChat()" style="margin-left:auto; background:transparent; border:none; color:var(--text-muted); cursor:pointer; font-size:20px;">×</button>
                    </div>
                    <div class="chat-messages" id="chat-messages">
                        <div class="msg ai">Olá! Sou seu Agente Especializado. Como posso te apoiar hoje com as práticas ágeis?</div>
                    </div>
                    <div class="chat-input-area">
                        <input type="text" id="chat-input-field" class="chat-input" placeholder="Digite sua pergunta...">
                        <button class="chat-btn" onclick="sendMessage()">Enviar</button>
                    </div>
                </div>
            </div>
        `;
    };

    renderAgentsUI();
});

let currentAgileAgentPrompt = '';

function openChat(agentName, icon) {
    // Generate a simple system prompt based on the agent name
    currentAgileAgentPrompt = `Você é o agente ágil especializado: ${agentName}. Ajude o usuário respondendo de forma concisa e direta baseada em práticas de Scrum/Kanban.`;

    document.getElementById('chat-modal').style.display = 'block';
    document.getElementById('chat-title').innerText = agentName;
    document.getElementById('chat-icon').innerText = icon;
    document.getElementById('chat-messages').innerHTML = `<div class="msg ai">Olá! Sou o <strong>${agentName}</strong>. Como posso te apoiar hoje?</div>`;
    // Scroll para o chat
    document.getElementById('chat-modal').scrollIntoView({ behavior: 'smooth' });
}

function closeChat() {
    document.getElementById('chat-modal').style.display = 'none';
}

async function sendMessage() {
    const input = document.getElementById('chat-input-field');
    const msgText = input.value.trim();
    if(!msgText) return;

    const chatBox = document.getElementById('chat-messages');
    
    // User message
    const userMsg = document.createElement('div');
    userMsg.className = 'msg user';
    userMsg.innerText = msgText;
    chatBox.appendChild(userMsg);
    
    input.value = '';
    chatBox.scrollTop = chatBox.scrollHeight;

    const loadingMsg = document.createElement('div');
    loadingMsg.className = 'msg ai';
    loadingMsg.innerHTML = '<span style="color:#0078d4;">Processando resposta... ⏳</span>';
    chatBox.appendChild(loadingMsg);
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                systemPrompt: currentAgileAgentPrompt,
                messages: [{ role: 'user', content: msgText }]
            })
        });

        const data = await response.json();
        
        chatBox.removeChild(loadingMsg);

        const aiMsg = document.createElement('div');
        aiMsg.className = 'msg ai';
        if (response.ok) {
            aiMsg.innerText = data.reply;
        } else {
            aiMsg.innerHTML = `<span style="color:var(--danger);">Erro: \${data.error}</span>`;
        }
        
        chatBox.appendChild(aiMsg);
        chatBox.scrollTop = chatBox.scrollHeight;

    } catch(err) {
        chatBox.removeChild(loadingMsg);
        const aiMsg = document.createElement('div');
        aiMsg.className = 'msg ai';
        aiMsg.innerHTML = `<span style="color:var(--danger);">Erro de Conexão: O backend Serverless não respondeu (você está rodando o 'vercel dev'?).</span>`;
        chatBox.appendChild(aiMsg);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
}
