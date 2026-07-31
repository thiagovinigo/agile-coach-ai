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
    openInfoModalDirect(title, icon, desc);
}

function openInfoModalDirect(title, icon, desc, type, path) {
    let extraHtml = '';
    if (type === 'skill' && path) {
        extraHtml = `
            <div style="display: flex; gap: 10px; margin-top: 20px;">
                <a href="${path}" download style="display:inline-block; background:#0078d4; color:#fff; padding:8px 16px; border-radius:4px; text-decoration:none; font-weight:bold;">⬇️ Baixar Skill</a>
                <a href="${path}" target="_blank" style="display:inline-block; background:#f3f2f1; color:#323130; padding:8px 16px; border-radius:4px; text-decoration:none; border:1px solid #ccc; font-weight:bold;">👀 Ver Arquivo</a>
            </div>
            <div style="margin-top:15px; background:#f4f4f4; padding:10px; border-radius:6px; border-left:4px solid #0078d4;">
                <strong style="display:block; margin-bottom:5px;">Como instalar (Claude Code):</strong>
                <code style="background:#fff; padding:4px 8px; border-radius:4px; border:1px solid #ddd;">/read ${path}</code>
            </div>
        `;
    } else if (type === 'agent') {
        extraHtml = `
            <div style="margin-top: 20px;">
                <button onclick="openEccChat('${title}', '${icon}', '${encodeURIComponent(desc)}'); document.getElementById('agent-info-modal').style.display='none';" style="background:#0078d4; color:#fff; padding:8px 16px; border-radius:4px; border:none; cursor:pointer; font-weight:bold;">
                    💬 Conversar com Agente
                </button>
            </div>
        `;
    }

    document.getElementById('info-modal-title').innerText = title;
    document.getElementById('info-modal-icon').innerText = icon;
    document.getElementById('info-modal-content').innerHTML = `
        <p style="font-size:1.1rem; color:#4a5568; line-height:1.6;"><strong>Descrição:</strong><br>${desc}</p>
        ${extraHtml}
        <p style="font-size:12px; color:#a19f9d; margin-top:16px;">*Detalhes carregados do catálogo real ECC.</p>
    `;
    
    document.getElementById('agent-info-modal').style.display = 'flex';
}

function openEccChat(agentName, icon, encodedDesc) {
    currentAgentSystemPrompt = `Você é o agente ${agentName}. ${decodeURIComponent(encodedDesc)}`;
    
    document.getElementById('ecc-chat-modal').style.display = 'block';
    document.getElementById('ecc-chat-title').innerText = agentName;
    document.getElementById('ecc-chat-icon').innerText = icon;
    document.getElementById('ecc-chat-messages').innerHTML = `<div class="msg ai">Olá! Sou o <strong>${agentName}</strong>. Como posso ajudar com sua engenharia ágil hoje?</div>`;
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

    function getContextualExamples(title) {
        const t = title.toLowerCase();
        if (t.includes('test') || t.includes('jest') || t.includes('cypress') || t.includes('playwright')) {
            return `
                <li style="margin-bottom:8px;"><code>"Por favor, crie testes unitários para este arquivo usando as diretrizes da skill ${title}."</code></li>
                <li><code>"Identifique os edge cases deste componente e gere testes de cobertura via ${title}."</code></li>
            `;
        } else if (t.includes('arch') || t.includes('defensive') || t.includes('securit') || t.includes('design') || t.includes('pattern')) {
            return `
                <li style="margin-bottom:8px;"><code>"Faça uma revisão de arquitetura e segurança neste arquivo aplicando a skill ${title}."</code></li>
                <li><code>"Quais padrões do ${title} estão sendo violados neste código? Sugira a refatoração."</code></li>
            `;
        } else if (t.includes('react') || t.includes('front') || t.includes('a11y') || t.includes('access') || t.includes('ui') || t.includes('css')) {
            return `
                <li style="margin-bottom:8px;"><code>"Revise este componente garantindo aderência às boas práticas e regras visuais do ${title}."</code></li>
                <li><code>"Atue como especialista em ${title} e melhore a estrutura e semântica deste código."</code></li>
            `;
        } else if (t.includes('review') || t.includes('lint') || t.includes('refactor') || t.includes('clean')) {
            return `
                <li style="margin-bottom:8px;"><code>"Atue como ${title} e faça um code review severo buscando code smells neste código."</code></li>
                <li><code>"Refatore esta função para deixá-la mais limpa, seguindo as regras de ${title}."</code></li>
            `;
        } else if (t.includes('build') || t.includes('error') || t.includes('debug') || t.includes('fix') || t.includes('resolve')) {
            return `
                <li style="margin-bottom:8px;"><code>"O código está falhando. Como especialista em ${title}, analise o log de erro e sugira o fix."</code></li>
                <li><code>"Invoque o conhecimento de ${title} para resolver este problema no projeto."</code></li>
            `;
        } else if (t.includes('data') || t.includes('sql') || t.includes('database') || t.includes('api') || t.includes('backend')) {
            return `
                <li style="margin-bottom:8px;"><code>"Otimize esta funcionalidade utilizando as diretrizes de performance do ${title}."</code></li>
                <li><code>"Como especialista em ${title}, estruture os dados para esta nova feature."</code></li>
            `;
        } else {
            return `
                <li style="margin-bottom:8px;"><code>"Analise as modificações deste arquivo garantindo que não estamos violando as políticas da skill ${title}."</code></li>
                <li><code>"Atue como especialista em ${title} e implemente a feature solicitada seguindo suas diretrizes."</code></li>
            `;
        }
    }

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
        catHeader.innerText = category;
        catHeader.style.padding = '12px 15px';
        catHeader.style.fontWeight = 'bold';
        catHeader.style.color = '#323130';
        catHeader.style.backgroundColor = '#f3f2f1';
        catHeader.style.borderLeft = '4px solid #6366f1';
        catHeader.style.cursor = 'pointer';
        catHeader.style.marginTop = '10px';
        sidebar.appendChild(catHeader);

        const skillsContainer = document.createElement('div');
        skillsContainer.className = 'kb-skills-list';
        skillsContainer.style.display = 'block';

        sidebar.appendChild(catHeader);

        sidebar.appendChild(skillsContainer);

        skillsList.forEach((skill, index) => {
            const btn = document.createElement('div');
            btn.className = 'kb-nav-btn';
            btn.innerHTML = `
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:1.1rem;">🧰</span>
                    <span style="font-weight:600; color:#323130; font-size:0.95rem;">${skill.title}</span>
                </div>
                <div style="font-size:0.8rem; color:#605e5c; margin-top:4px; line-height:1.3; white-space:normal;">
                    ${skill.description || 'Nenhuma descrição fornecida.'}
                </div>
            `;
            
            btn.addEventListener('click', () => {
                document.querySelectorAll('.kb-nav-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                const headerCard = `
<div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; margin-bottom: 30px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
    <h3 style="margin-top:0; color:#0f172a; display:flex; align-items:center; justify-content:space-between; gap:8px; font-size: 1.1rem; margin-bottom: 15px;">
        <span><span>📚</span> Resumo Rápido (${category})</span>
        ${window.favoritesManager ? window.favoritesManager.renderButton(skill.id, skill.title, 'ECC Skills', skill.path) : ''}
    </h3>
    <div style="background:#f1f5f9; border:1px solid #cbd5e1; padding:8px 12px; border-radius:4px; font-family:monospace; font-size:0.85rem; color:#475569; word-break:break-all; margin-bottom: 20px;">
        📂 <strong>Repositório:</strong> ${skill.path}
    </div>
    <div style="display: flex; gap: 10px; margin-bottom: 20px;">
        <a href="${skill.path}" download="${skill.id}.md" style="display:inline-block; background-color:#0078d4; color:#fff; padding:10px 20px; border-radius:6px; text-decoration:none; font-weight:bold; font-size:0.95rem; box-shadow:0 2px 4px rgba(0,0,0,0.1);">
            ⬇️ Baixar Arquivo da Skill
        </a>
        <a href="${skill.path}" target="_blank" style="display:inline-block; background-color:#f8fafc; color:#334155; padding:10px 20px; border-radius:6px; text-decoration:none; font-weight:bold; border: 1px solid #cbd5e1; font-size:0.95rem;">
            👀 Ver Arquivo
        </a>
    </div>
    <h3 style="margin-top:0; color:#0f172a; display:flex; align-items:center; gap:8px; font-size: 1.1rem;">
        <span>🧠</span> O que é?
    </h3>
    <p style="margin-top:5px; color:#475569; font-size: 0.95rem;">
        A skill <strong>${skill.title}</strong> é um padrão técnico, arquitetural ou diretriz de qualidade da biblioteca ECC.
    </p>
    <h3 style="margin-top:20px; color:#0f172a; display:flex; align-items:center; gap:8px; font-size: 1.1rem;">
        <span>⏱️</span> Quando usar?
    </h3>
    <p style="margin-top:5px; color:#475569; font-size: 0.95rem; font-weight: 500;">
        ${skill.description || '<i>Sem descrição fornecida.</i>'}
    </p>
    ${skill.dependencies && skill.dependencies.length > 0 ? `
    <div style="background:#f0f8ff; padding: 1rem; border-radius: 6px; border-left: 4px solid #0078d4; margin-top: 15px; margin-bottom: 15px;">
        <strong style="display:block; font-size:0.9rem; color:#0078d4; text-transform:uppercase; margin-bottom:5px;">🔗 Skills Vinculadas (Sub-Skills)</strong>
        <div>
            ${skill.dependencies.map(d => `<span class="tag" style="display:inline-block; background:rgba(0,120,212,.12); border:1px solid rgba(0,120,212,.3); padding:.2em .6em; border-radius:4px; font-size:.8rem; color:#0078d4; margin-right:5px; margin-bottom:3px; font-weight:bold;">${d}</span>`).join('')}
        </div>
    </div>
    ` : ''}
    <h3 style="margin-top:20px; color:#0f172a; display:flex; align-items:center; gap:8px; font-size: 1.1rem;">
        <span>🛠️</span> Como usar?
    </h3>
    <p style="margin-top:5px; color:#475569; font-size: 0.95rem; margin-bottom:8px;">No Claude Code, após ler com <code>/read ${skill.path}</code>, peça a tarefa usando linguagem natural:</p>
    <div style="background:#f8fafc; padding:10px 15px; border-radius:6px; border-left:3px solid #0078d4; font-size:0.9rem;">
        <ul style="margin:0; padding-left:20px; color:#334155;">
            ${getContextualExamples(skill.title)}
        </ul>
    </div>
</div>
`;

                contentArea.innerHTML = '<div style="padding:40px; text-align:center; color:#64748b;">⏳ Carregando ' + skill.title + '...</div>';
                
                fetch(skill.path)
                    .then(r => {
                        if(!r.ok) throw new Error("Não foi possível carregar o arquivo.");
                        return r.text();
                    })
                    .then(text => {
                        const preBlocks = [];
                        let processedText = text.replace(/```[a-z]*\n([\s\S]*?)```/g, (match, p1) => {
                            preBlocks.push(p1);
                            return `__PRE_BLOCK_${preBlocks.length - 1}__`;
                        });

                        let html = processedText
                            .replace(/^### (.*$)/gim, '<h3 style="margin-top:35px; margin-bottom:15px; color:#1e293b; font-size:1.4rem;">$1</h3>')
                            .replace(/^## (.*$)/gim, '<h2 style="margin-top:45px; margin-bottom:20px; color:#0f172a; border-bottom:1px solid #e2e8f0; padding-bottom:8px; font-size:1.8rem;">$1</h2>')
                            .replace(/^# (.*$)/gim, '<h1 style="color:#0f172a; font-size:2.2rem; margin-bottom:25px;">$1</h1>')
                            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                            .replace(/\[([^\[]+)\]\(([^\)]+)\)/g, '<strong style="color:#0078d4;">$1</strong>')
                            .replace(/^\> (.*$)/gim, '<blockquote style="background:#f8fafc; border-left:4px solid #cbd5e1; padding:15px 20px; color:#475569; margin:20px 0; border-radius:0 8px 8px 0; font-style:italic;">$1</blockquote>')
                            .replace(/^\|(.*)\|/gim, (match) => {
                                const cells = match.split('|').filter(c => c.trim() !== '');
                                if(cells.every(c => c.replace(/-/g, '').trim() === '')) return '';
                                return '<div style="display:flex; border-bottom:1px solid #e2e8f0; padding:10px 0;">' + cells.map(c => '<div style="flex:1; padding:0 10px;">' + c.trim() + '</div>').join('') + '</div>';
                            })
                            .replace(/^- (.*$)/gim, '<li style="margin-left:25px; margin-bottom:8px;">$1</li>')
                            .replace(/\n\n/g, '</p><p style="margin-bottom:15px;">')
                            .replace(/<p style="margin-bottom:15px;"><\/p>/g, '');

                        preBlocks.forEach((block, index) => {
                            html = html.replace(`__PRE_BLOCK_${index}__`, `<pre style="background:#0f172a; color:#e2e8f0; padding:15px; border-radius:8px; overflow-x:auto; font-family:monospace; font-size:13px; line-height:1.4;">${block}</pre>`);
                        });
                            
                        contentArea.innerHTML = `
                            <div style="max-width:900px; margin:0 auto; padding:40px; background:#fff; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.05); border:1px solid #edebe9; line-height:1.7; font-size:1.05rem; color:#334155;">
                                ${headerCard}
                                <p style="margin-bottom:15px;">${html}</p>
                            </div>
                        `;
                    })
                    .catch(e => {
                        contentArea.innerHTML = `
                            <div style="max-width:900px; margin:0 auto; padding:40px; background:#fff; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.05); border:1px solid #edebe9; line-height:1.7; font-size:1.05rem; color:#334155;">
                                ${headerCard}
                                <div style="padding:20px; color:red; background:#fff5f5; border-radius:6px; margin-top:20px;">Erro ao carregar documento Markdown (.md): ${e.message}</div>
                            </div>
                        `;
                    });
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
