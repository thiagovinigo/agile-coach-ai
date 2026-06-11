document.addEventListener('DOMContentLoaded', () => {
    initEccAgentsView();
    initEccSkillsView();
});

function initEccAgentsView() {
    const container = document.getElementById('ecc-agents-view');
    if(!container || typeof eccAgentsData === 'undefined') return;

    let html = `
        <div class="hero-section">
            <h3>🤖 ECC AI Agents</h3>
            <p>Catálogo de Agentes e Especialistas configurados na arquitetura ECC. Escolha seu agente para interagir.</p>
        </div>
        <div class="grid-cards">
    `;

    eccAgentsData.forEach(agent => {
        html += `
            <div class="card" style="position:relative;">
                <button onclick="openAgentInfo(this)" data-title="${agent.title}" data-icon="${agent.icon || '🤖'}" data-desc="${encodeURIComponent(agent.description)}" style="position:absolute; top:12px; right:12px; background:transparent; border:1px solid #c8c6c4; border-radius:50%; width:24px; height:24px; color:#605e5c; cursor:pointer; font-weight:bold; display:flex; justify-content:center; align-items:center;" title="Ver detalhes">?</button>
                <div class="card-icon">${agent.icon || '🤖'}</div>
                <div class="card-title">${agent.title}</div>
                <div class="card-desc">${agent.description || 'Especialista em tarefas da arquitetura ECC.'}</div>
                <button class="card-action" onclick="openEccChat('${agent.title}', '${agent.icon || '🤖'}', '${encodeURIComponent(agent.description)}')">
                    Conversar
                </button>
            </div>
        `;
    });

    html += `
        </div>
        <div id="ecc-chat-modal" style="display:none; margin-top: 32px;">
            <div class="chat-container">
                <div class="chat-header">
                    <span id="ecc-chat-icon" style="font-size: 24px;">🤖</span>
                    <div>
                        <h4 id="ecc-chat-title" style="color:#fff;">Agente</h4>
                        <span style="font-size:12px; color:var(--success);">● Online</span>
                    </div>
                    <button onclick="closeEccChat()" style="margin-left:auto; background:transparent; border:none; color:var(--text-muted); cursor:pointer; font-size:20px;">×</button>
                </div>
                <div class="chat-messages" id="ecc-chat-messages">
                    <div class="msg ai">Olá! Sou seu Agente ECC.</div>
                </div>
                <div class="chat-input-area">
                    <input type="text" id="ecc-chat-input-field" class="chat-input" placeholder="Digite sua pergunta...">
                    <button class="chat-btn" onclick="sendEccMessage()">Enviar</button>
                </div>
            </div>
        </div>
    `;

    container.innerHTML = html;
}

let currentAgentSystemPrompt = '';

function openAgentInfo(btnElement) {
    const title = btnElement.getAttribute('data-title');
    const icon = btnElement.getAttribute('data-icon');
    const desc = decodeURIComponent(btnElement.getAttribute('data-desc'));

    document.getElementById('info-modal-title').innerText = title;
    document.getElementById('info-modal-icon').innerText = icon;
    document.getElementById('info-modal-content').innerHTML = `
        <p><strong>Descrição:</strong><br>${desc}</p>
        <p style="font-size:12px; color:#a19f9d; margin-top:16px;">*Este é um resumo extraído da base de conhecimento.</p>
    `;
    
    document.getElementById('agent-info-modal').style.display = 'flex';
}

function openEccChat(agentName, icon, encodedDesc) {
    currentAgentSystemPrompt = \`Você é o agente \${agentName}. \${decodeURIComponent(encodedDesc)}\`;
    
    document.getElementById('ecc-chat-modal').style.display = 'block';
    document.getElementById('ecc-chat-title').innerText = agentName;
    document.getElementById('ecc-chat-icon').innerText = icon;
    document.getElementById('ecc-chat-messages').innerHTML = \`<div class="msg ai">Olá! Sou o <strong>\${agentName}</strong>. Como posso te ajudar hoje na nossa arquitetura ECC?</div>\`;
    document.getElementById('ecc-chat-modal').scrollIntoView({ behavior: 'smooth' });
}

function closeEccChat() {
    document.getElementById('ecc-chat-modal').style.display = 'none';
}

async function sendEccMessage() {
    const input = document.getElementById('ecc-chat-input-field');
    const msgText = input.value.trim();
    if(!msgText) return;

    const chatBox = document.getElementById('ecc-chat-messages');
    
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
                systemPrompt: currentAgentSystemPrompt,
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

function initEccSkillsView() {
    const container = document.getElementById('ecc-skills-view');
    if(!container || typeof eccSkillsData === 'undefined') return;

    container.innerHTML = '';
    
    const introHeader = document.createElement('div');
    introHeader.style.padding = '20px 30px';
    introHeader.style.backgroundColor = '#fff';
    introHeader.style.borderBottom = '1px solid #edebe9';
    introHeader.style.marginBottom = '20px';
    introHeader.innerHTML = `
        <h2 style="margin-top:0; color:#0078d4; margin-bottom:10px;">Catálogo de Skills ECC</h2>
        <p style="font-size:1.1rem; line-height:1.5; color:#323130; margin:0;">
            Use as skills desta biblioteca nos agentes do <strong>ECC</strong>.
        </p>
    `;
    container.appendChild(introHeader);

    const layout = document.createElement('div');
    layout.className = 'kb-layout';

    const sidebar = document.createElement('div');
    sidebar.className = 'kb-sidebar';
    sidebar.style.overflowY = 'auto';

    const contentArea = document.createElement('div');
    contentArea.className = 'kb-page-content';
    contentArea.style.overflowY = 'auto';

    layout.appendChild(sidebar);
    layout.appendChild(contentArea);
    container.appendChild(layout);

    const categories = Object.keys(eccSkillsData).sort();
    let firstGlobalBtn = null;

    categories.forEach((category) => {
        const skillsList = eccSkillsData[category];
        
        const catHeader = document.createElement('div');
        catHeader.className = 'kb-category-header';
        catHeader.style.padding = '12px 15px';
        catHeader.style.fontWeight = 'bold';
        catHeader.style.color = '#323130';
        catHeader.style.backgroundColor = '#f3f2f1';
        catHeader.style.borderLeft = '4px solid #0078d4';
        catHeader.style.cursor = 'pointer';
        catHeader.style.marginTop = '10px';
        catHeader.style.marginBottom = '2px';
        catHeader.style.borderRadius = '0 6px 6px 0';
        catHeader.style.display = 'flex';
        catHeader.style.justifyContent = 'space-between';
        catHeader.style.alignItems = 'center';
        
        catHeader.innerHTML = `
            <span>${category} <span style="font-size:12px; font-weight:normal; color:#605e5c;">(${skillsList.length})</span></span>
            <span class="toggle-icon" style="transition: transform 0.2s;">▼</span>
        `;

        const skillsContainer = document.createElement('div');
        skillsContainer.className = 'kb-skills-list';
        skillsContainer.style.display = 'none';

        catHeader.addEventListener('click', () => {
            const isVisible = skillsContainer.style.display === 'block';
            skillsContainer.style.display = isVisible ? 'none' : 'block';
            catHeader.querySelector('.toggle-icon').style.transform = isVisible ? 'rotate(0deg)' : 'rotate(180deg)';
        });

        sidebar.appendChild(catHeader);
        sidebar.appendChild(skillsContainer);

        skillsList.forEach((skill, index) => {
            const btn = document.createElement('div');
            btn.className = 'kb-nav-btn';
            btn.textContent = skill.title;
            
            btn.addEventListener('click', () => {
                document.querySelectorAll('.kb-nav-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                contentArea.innerHTML = '';
                
                const titleNode = document.createElement('h3');
                titleNode.textContent = skill.title;
                contentArea.appendChild(titleNode);

                if(skill.path) {
                    const pathNode = document.createElement('div');
                    pathNode.innerHTML = `<strong>Localização:</strong> <code>${skill.path}</code>`;
                    pathNode.style.marginBottom = '10px';
                    pathNode.style.fontSize = '14px';
                    pathNode.style.color = '#605e5c';
                    contentArea.appendChild(pathNode);
                }

                if(skill.description) {
                    const descNode = document.createElement('p');
                    descNode.textContent = skill.description;
                    contentArea.appendChild(descNode);
                }

                if(skill.dependencies && skill.dependencies.length > 0) {
                    const depTitle = document.createElement('h4');
                    depTitle.textContent = 'Dependências:';
                    depTitle.style.marginTop = '20px';
                    contentArea.appendChild(depTitle);

                    const depList = document.createElement('ul');
                    skill.dependencies.forEach(d => {
                        const li = document.createElement('li');
                        li.textContent = d;
                        depList.appendChild(li);
                    });
                    contentArea.appendChild(depList);
                }

                if(skill.triggers && skill.triggers.length > 0) {
                    const triggerTitle = document.createElement('h4');
                    triggerTitle.textContent = 'Triggers Recomendados:';
                    triggerTitle.style.marginTop = '20px';
                    contentArea.appendChild(triggerTitle);

                    const triggerCont = document.createElement('div');
                    triggerCont.style.display = 'flex';
                    triggerCont.style.flexWrap = 'wrap';
                    triggerCont.style.gap = '8px';

                    skill.triggers.forEach(t => {
                        const tSpan = document.createElement('span');
                        tSpan.textContent = t;
                        tSpan.style.backgroundColor = '#e1dfdd';
                        tSpan.style.padding = '4px 8px';
                        tSpan.style.borderRadius = '4px';
                        tSpan.style.fontSize = '12px';
                        triggerCont.appendChild(tSpan);
                    });
                    contentArea.appendChild(triggerCont);
                }
            });

            skillsContainer.appendChild(btn);

            if(!firstGlobalBtn) {
                firstGlobalBtn = btn;
            }
        });
    });

    if(firstGlobalBtn) {
        firstGlobalBtn.click();
        const firstHeader = sidebar.querySelector('.kb-category-header');
        if(firstHeader) firstHeader.click();
    }
}
