class LiveSimulator {
    constructor(containerId, agentType) {
        this.container = document.getElementById(containerId);
        this.agentType = agentType;
        this.messages = [];
        this.isTyping = false;
        
        this.render();
    }

    render() {
        const title = this.agentType === 'kiro' ? 'Kiro (Agente Azure DevOps)' : 'Claude Code (Agente Anthropic)';
        const color = this.agentType === 'kiro' ? '#8b5cf6' : '#f97316';
        
        this.container.innerHTML = `
            <div style="background:#0f172a; border-radius:10px; border:1px solid #334155; display:flex; flex-direction:column; height:600px; box-shadow:0 10px 25px rgba(0,0,0,0.5);">
                <div style="background:#1e293b; padding:15px; border-bottom:1px solid #334155; border-radius:10px 10px 0 0; display:flex; justify-content:space-between; align-items:center;">
                    <div style="display:flex; gap:8px;">
                        <div style="width:12px; height:12px; border-radius:50%; background:#ef4444;"></div>
                        <div style="width:12px; height:12px; border-radius:50%; background:#eab308;"></div>
                        <div style="width:12px; height:12px; border-radius:50%; background:#22c55e;"></div>
                    </div>
                    <strong style="color:${color}; font-family:monospace; font-size:14px;">${title}</strong>
                    <div></div>
                </div>
                
                <div class="terminal-body" style="flex:1; padding:20px; overflow-y:auto; font-family:'Courier New', monospace; font-size:14px; line-height:1.6; color:#e2e8f0;">
                    <div style="color:#64748b; margin-bottom:20px;">
                        Conectado ao Servidor Global de IA. Autenticação validada.<br>
                        Digite um comando ou descreva o problema natural.
                    </div>
                    <div class="chat-history"></div>
                </div>

                <div style="padding:15px; border-top:1px solid #334155; background:#0f172a; border-radius:0 0 10px 10px; display:flex; gap:10px; align-items:center;">
                    <span style="color:${color}; font-weight:bold; font-family:monospace;">&gt;</span>
                    <input type="text" class="terminal-input" style="flex:1; background:transparent; border:none; color:#10b981; font-family:monospace; font-size:15px; outline:none;" placeholder="Digite aqui...">
                </div>
            </div>
        `;

        const input = this.container.querySelector('.terminal-input');
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && input.value.trim() && !this.isTyping) {
                this.sendMessage(input.value.trim());
                input.value = '';
            }
        });
    }

    async sendMessage(text) {
        this.isTyping = true;
        const history = this.container.querySelector('.chat-history');
        const input = this.container.querySelector('.terminal-input');
        
        // Renderiza mensagem do usuário
        const userDiv = document.createElement('div');
        userDiv.style.marginBottom = '15px';
        userDiv.innerHTML = `<span style="color:#38bdf8;">$ ${text}</span>`;
        history.appendChild(userDiv);
        this.scrollToBottom();

        this.messages.push({ role: 'user', content: text });

        // Div de resposta da IA
        const aiDiv = document.createElement('div');
        aiDiv.style.marginBottom = '20px';
        aiDiv.style.color = '#e2e8f0';
        history.appendChild(aiDiv);
        
        input.disabled = true;

        try {
            let token = localStorage.getItem('auth_token');
            if (!token && (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')) {
                token = "local_dev_token";
            }
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': \`Bearer \${token}\`
                },
                body: JSON.stringify({
                    agentType: this.agentType,
                    messages: this.messages
                })
            });

            if(!response.ok) {
                aiDiv.innerHTML = `<span style="color:#ef4444;">[Error] Acesso negado ou falha na API. Verifique o servidor.</span>`;
                this.isTyping = false;
                input.disabled = false;
                return;
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let aiText = '';
            let buffer = '';

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                
                buffer += decoder.decode(value, {stream: true});
                const lines = buffer.split('\n');
                
                // O último elemento pode ser uma linha incompleta, então guardamos no buffer
                buffer = lines.pop() || '';
                
                for (const line of lines) {
                    if (line.startsWith('data: ') && !line.includes('[DONE]')) {
                        try {
                            const data = JSON.parse(line.replace('data: ', ''));
                            if (data.choices && data.choices[0] && data.choices[0].delta && data.choices[0].delta.content) {
                                aiText += data.choices[0].delta.content;
                            } else if (data.content) {
                                // Fallback para mensagens customizadas do backend
                                aiText += data.content;
                            }
                            // Conversão básica de \n para <br>
                            aiDiv.innerHTML = aiText.replace(/\\n/g, '<br>').replace(/\n/g, '<br>');
                            this.scrollToBottom();
                        } catch(e) {
                            console.error("JSON Parse Error on chunk:", line, e);
                        }
                    }
                }
            }

            this.messages.push({ role: 'assistant', content: aiText });

        } catch (error) {
            aiDiv.innerHTML = `<span style="color:#ef4444;">[Network Error] O Servidor Local não está rodando.</span>`;
        }

        this.isTyping = false;
        input.disabled = false;
        input.focus();
    }

    scrollToBottom() {
        const body = this.container.querySelector('.terminal-body');
        body.scrollTop = body.scrollHeight;
    }
}

// Injeta na UI
function initLiveSimView() {
    const container = document.getElementById('live-sim-view');
    if (!container) return;

    let token = localStorage.getItem('auth_token');
    
    // Bypass local para demonstração
    if (!token && (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')) {
        token = "local_dev_token";
    }

    if (!token) {
        container.innerHTML = `
            <div class="page-header" style="background:linear-gradient(135deg, #1e293b, #0f172a); text-align:center; padding: 50px 20px;">
                <div class="tag" style="background:#38bdf8; color:#0f172a;">ACESSO RESTRITO</div>
                <h2>💬 Simuladores Vivos de IA</h2>
                <p style="margin-top:10px; font-size:16px; color:#94a3b8; max-width:600px; margin-left:auto; margin-right:auto;">
                    Esta é uma área VIP conectada diretamente à API da OpenAI (Kiro e Claude). Para não esgotarmos nossa cota na nuvem, você precisa de um cadastro para testar os simuladores em tempo real.
                </p>
                <a href="login.html" style="display:inline-block; background:#38bdf8; color:#0f172a; font-weight:bold; padding:12px 24px; border-radius:6px; text-decoration:none; margin-top:20px; font-size:16px;">
                    Fazer Login para Acessar
                </a>
            </div>
        `;
        return;
    }

    container.innerHTML = `
        <div class="page-header" style="background:linear-gradient(135deg, #1e293b, #0f172a);">
            <div class="tag" style="background:#38bdf8; color:#0f172a;">EXPERIMENTAL (OPENAI)</div>
            <h2>💬 Simuladores Vivos de IA</h2>
            <p style="margin-top:10px;">Esta página se conecta diretamente à API da OpenAI pelo seu Servidor Local. Aqui você tem dois Agentes Autônomos de Terminal com a <strong>mesma proposta de valor</strong> (orquestração, delivery e resolução de problemas), divididos apenas pelo ecossistema: o Kiro (Especialista em Azure/TFS) e o Claude Code (Especialista Open-Source/Anthropic).</p>
        </div>

        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px;">
            <div>
                <h3 style="color:#8b5cf6; margin-bottom:15px; display:flex; align-items:center; gap:8px;">
                    <span>🛰️</span> Agente Kiro
                </h3>
                <div id="sim-kiro-container"></div>
            </div>
            <div>
                <h3 style="color:#f97316; margin-bottom:15px; display:flex; align-items:center; gap:8px;">
                    <span>🖥️</span> Agente Claude
                </h3>
                <div id="sim-claude-container"></div>
            </div>
        </div>
    \`;

    new LiveSimulator('sim-kiro-container', 'kiro');
    new LiveSimulator('sim-claude-container', 'claude');
}

window.initLiveSimView = initLiveSimView;
