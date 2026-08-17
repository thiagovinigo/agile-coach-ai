document.addEventListener('DOMContentLoaded', () => {
    initWorkshopView();
});

function initWorkshopView() {
    const container = document.getElementById('workshop-view');
    if (!container) return;

    let currentSlide = 0;

    // We will fetch the HTML of scrumban_guia.html to reliably extract the Time de Elite sections
    let extractedSections = {};

    const slides = [
        {
            title: "O Papel do Agilista: Gestor do Fluxo",
            content: `
                <div style="text-align: center; padding: 40px;">
                    <h1 style="font-size: 2.5rem; color: #0f172a; margin-bottom: 20px;">O Papel do Agilista no Scrumban</h1>
                    <p style="font-size: 1.3rem; color: #475569; max-width: 800px; margin: 0 auto 40px; line-height: 1.6;">
                        No Scrumban, o Agilista (ou Flow Manager) não é apenas um facilitador de reuniões. 
                        Sua responsabilidade principal é a <strong>Otimização Sistêmica</strong> e a <strong>Gestão Visível do Fluxo de Valor</strong>.
                    </p>
                    <div style="display: flex; gap: 20px; justify-content: center; text-align: left;">
                        <div style="background: #f8fafc; border-left: 4px solid #3b82f6; padding: 20px; border-radius: 8px; flex: 1; max-width: 300px;">
                            <h3 style="margin-top: 0; color: #1d4ed8;">1. Visibilidade</h3>
                            <p style="color: #334155;">Tirar o trabalho oculto e expor as políticas do time no Board, garantindo que o sistema seja transparente para todos.</p>
                        </div>
                        <div style="background: #f8fafc; border-left: 4px solid #10b981; padding: 20px; border-radius: 8px; flex: 1; max-width: 300px;">
                            <h3 style="margin-top: 0; color: #047857;">2. Fluxo Contínuo</h3>
                            <p style="color: #334155;">Focar em itens que estão parados (Wait Time), resolver dependências e gerenciar os limites de WIP.</p>
                        </div>
                        <div style="background: #f8fafc; border-left: 4px solid #f59e0b; padding: 20px; border-radius: 8px; flex: 1; max-width: 300px;">
                            <h3 style="margin-top: 0; color: #b45309;">3. Previsibilidade</h3>
                            <p style="color: #334155;">Usar métricas de Lead Time e Throughput para estabelecer Acordos de Nível de Serviço (SLA) confiáveis com o cliente.</p>
                        </div>
                    </div>
                </div>
            `
        },
        {
            title: "O Board de Elite (O Sistema Completo)",
            id: "s-elite-board",
            intro: `
                <div style="background: #eff6ff; border: 1px solid #bfdbfe; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                    <h3 style="margin: 0 0 10px 0; color: #1e3a8a;">🎯 A Ferramenta do Gestor: O Board</h3>
                    <p style="margin: 0; color: #1e40af;">
                        Como Gestor do Fluxo, seu board é o reflexo do seu processo. Abaixo está o <strong>Board de Elite</strong>, divido em Upstream (Descoberta) e Downstream (Entrega).
                        Sua missão é acompanhar os itens fluindo da esquerda para a direita, monitorando gargalos em vez de microgerenciar pessoas.
                    </p>
                </div>
            `
        },
        {
            title: "Políticas Explícitas",
            id: "s-elite-politicas",
            intro: `
                <div style="background: #fef2f2; border: 1px solid #fecaca; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                    <h3 style="margin: 0 0 10px 0; color: #991b1b;">📜 Tornando as Regras Claras</h3>
                    <p style="margin: 0; color: #7f1d1d;">
                        O maior erro de um time imaturo é tratar "Pronto" como algo subjetivo. O Gestor de Fluxo garante que cada transição no board tenha uma <strong>Política Explícita</strong>.
                        Essas regras são os "Guard Rails" do time.
                    </p>
                </div>
            `
        },
        {
            title: "Touch Time vs Wait Time",
            id: "s-elite-flow",
            intro: `
                <div style="background: #ecfdf5; border: 1px solid #a7f3d0; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                    <h3 style="margin: 0 0 10px 0; color: #065f46;">⏱️ Onde o Tempo é Perdido?</h3>
                    <p style="margin: 0; color: #064e3b;">
                        Ao ensinar agilidade, um conceito crítico é a eficiência de fluxo. Um item passa em média 85% do tempo esperando.
                        O papel do Agilista é lutar contra as "filas de espera" (Wait Time), não apenas pressionar por mais "código sendo digitado" (Touch Time).
                    </p>
                </div>
            `
        },
        {
            title: "Cadências (Reuniões com Propósito)",
            id: "s-elite-cadencias",
            intro: `
                <div style="background: #fdf4ff; border: 1px solid #fbcfe8; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                    <h3 style="margin: 0 0 10px 0; color: #86198f;">🔄 Loops de Feedback</h3>
                    <p style="margin: 0; color: #701a75;">
                        Agilistas maduros não agendam reuniões sem propósito. No Scrumban, usamos cadências estritas orientadas ao fluxo (Replenishment, Daily focada no Board, Flow Review).
                    </p>
                </div>
            `
        },
        {
            title: "Conclusão: Atuando na Trincheira",
            content: `
                <div style="text-align: center; padding: 40px;">
                    <h1 style="font-size: 2.5rem; color: #0f172a; margin-bottom: 20px;">Sua Jornada Começa Agora</h1>
                    <p style="font-size: 1.3rem; color: #475569; max-width: 700px; margin: 0 auto 30px; line-height: 1.6;">
                        Gerir o fluxo é como ser um controlador de tráfego aéreo. Se você só olhar para um único avião (item), o aeroporto inteiro (sistema) para.
                    </p>
                    <div style="background: #fff; border: 2px solid #e2e8f0; border-radius: 12px; padding: 30px; max-width: 600px; margin: 0 auto; text-align: left; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                        <h3 style="color: #334155; margin-top: 0; border-bottom: 1px solid #e2e8f0; padding-bottom: 10px;">Checklist do Agilista de Elite:</h3>
                        <ul style="color: #4a5568; line-height: 1.8; font-size: 1.1rem; padding-left: 20px;">
                            <li>O Board reflete exatamente como o time trabalha hoje?</li>
                            <li>Os Limites de WIP estão sendo respeitados?</li>
                            <li>A idade dos itens (Aging) é discutida ativamente na Daily?</li>
                            <li>As políticas de Definition of Ready (DoR) bloqueiam itens ruins no Upstream?</li>
                            <li>A entrega é pautada por previsibilidade estatística ou "achismo"?</li>
                        </ul>
                    </div>
                </div>
            `
        }
    ];

    container.innerHTML = `
        <div style="background: #f8fafc; height: 100vh; display: flex; flex-direction: column; position: relative;">
            
            <!-- Header -->
            <div style="background: #fff; padding: 15px 30px; border-bottom: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <span style="font-size: 24px; color: #0078d4; cursor: pointer;" onclick="document.querySelector('a[href=\\'#agents\\']').click()">⬅️</span>
                    <h2 style="margin: 0; color: #0f172a; font-size: 1.3rem;">Workshop: Gestor de Fluxo</h2>
                </div>
                <div style="font-weight: 600; color: #64748b; font-size: 0.9rem;" id="workshop-progress-text">Slide 1 de ${slides.length}</div>
            </div>

            <!-- Progress Bar -->
            <div style="height: 4px; background: #e2e8f0; width: 100%;">
                <div id="workshop-progress-bar" style="height: 100%; background: #0078d4; width: 0%; transition: width 0.3s ease;"></div>
            </div>

            <!-- Slides Content Area -->
            <div id="workshop-slide-container" style="flex: 1; overflow-y: auto; padding: 40px; background: #f8fafc; position: relative;">
                <div style="text-align: center; color: #94a3b8; font-size: 1.2rem; margin-top: 100px;">⏳ Inicializando Workshop...</div>
            </div>

            <!-- Footer Navigation -->
            <div style="background: #fff; padding: 20px 40px; border-top: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 -2px 10px rgba(0,0,0,0.02);">
                <button id="workshop-btn-prev" style="background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; padding: 10px 24px; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 1rem; transition: all 0.2s;">
                    Anterior
                </button>
                <div style="font-weight: 500; color: #334155;" id="workshop-slide-title">Carregando...</div>
                <button id="workshop-btn-next" style="background: #0078d4; color: white; border: none; padding: 10px 24px; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 1rem; transition: all 0.2s; box-shadow: 0 2px 4px rgba(0,120,212,0.3);">
                    Próximo 🚀
                </button>
            </div>
        </div>
    `;

    // Fetch the HTML containing the Time de Elite contents
    fetch('contexto/scrumban_guia.html')
        .then(response => response.text())
        .then(htmlStr => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(htmlStr, 'text/html');
            
            // Extract necessary sections based on slides requirement
            slides.forEach(slide => {
                if(slide.id) {
                    const el = doc.getElementById(slide.id);
                    if(el) {
                        extractedSections[slide.id] = el.innerHTML;
                    } else {
                        extractedSections[slide.id] = `<div style="padding: 20px; color: red; background: #fee2e2; border-radius: 8px;">⚠️ Conteúdo não encontrado para a seção: ${slide.id}</div>`;
                    }
                }
            });

            renderSlide();
        })
        .catch(err => {
            document.getElementById('workshop-slide-container').innerHTML = `<div style="color:red; padding:40px;">Erro ao carregar o conteúdo do banco de dados de contexto: ${err}</div>`;
        });

    function renderSlide() {
        const slide = slides[currentSlide];
        const container = document.getElementById('workshop-slide-container');
        const progressText = document.getElementById('workshop-progress-text');
        const progressBar = document.getElementById('workshop-progress-bar');
        const titleText = document.getElementById('workshop-slide-title');
        
        let html = '';
        
        // Se o slide for customizado (content) ou dinâmico extraído (id)
        if (slide.content) {
            html = slide.content;
        } else if (slide.id) {
            let sectionHtml = extractedSections[slide.id] || '';
            // Limpa o fundo original do sectionHtml se existir, para não brigar com o nosso container
            html = `
                <div style="max-width: 1400px; margin: 0 auto; background: #fff; padding: 40px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.03); border: 1px solid #e2e8f0;">
                    ${slide.intro || ''}
                    <div class="extracted-content" style="overflow-x: auto;">
                        ${sectionHtml}
                    </div>
                </div>
            `;
        }

        // Animação de fade in simples
        container.style.opacity = '0';
        setTimeout(() => {
            container.innerHTML = html;
            container.scrollTop = 0; // reset scroll
            container.style.transition = 'opacity 0.4s ease';
            container.style.opacity = '1';
        }, 150);

        // Atualizar controles e progresso
        progressText.innerText = `Slide ${currentSlide + 1} de ${slides.length}`;
        progressBar.style.width = `${((currentSlide + 1) / slides.length) * 100}%`;
        titleText.innerText = slide.title;

        // Botoes
        const btnPrev = document.getElementById('workshop-btn-prev');
        const btnNext = document.getElementById('workshop-btn-next');
        
        if(currentSlide === 0) {
            btnPrev.style.opacity = '0.5';
            btnPrev.style.pointerEvents = 'none';
        } else {
            btnPrev.style.opacity = '1';
            btnPrev.style.pointerEvents = 'auto';
        }

        if(currentSlide === slides.length - 1) {
            btnNext.innerText = 'Finalizar ✨';
            btnNext.style.background = '#10b981';
            btnNext.style.boxShadow = '0 2px 4px rgba(16,185,129,0.3)';
        } else {
            btnNext.innerText = 'Próximo 🚀';
            btnNext.style.background = '#0078d4';
            btnNext.style.boxShadow = '0 2px 4px rgba(0,120,212,0.3)';
        }
    }

    document.getElementById('workshop-btn-prev').addEventListener('click', () => {
        if(currentSlide > 0) {
            currentSlide--;
            renderSlide();
        }
    });

    document.getElementById('workshop-btn-next').addEventListener('click', () => {
        if(currentSlide < slides.length - 1) {
            currentSlide++;
            renderSlide();
        } else {
            alert('🎉 Workshop Finalizado! Você já tem as ferramentas necessárias para ser um Agilista de Elite.');
            document.querySelector('a[href=\\'#agents\\']').click(); // Volta pro início
        }
    });
}
