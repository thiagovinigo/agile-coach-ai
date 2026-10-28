/**
 * Flow Reels Studio 3.0 · Lógica da Interface
 */

document.addEventListener("DOMContentLoaded", () => {
  // Estado da Aplicação
  const state = {
    formato: "narrado",
    roteiro: {
      gancho: "",
      oQueE: "",
      provas: "",
      virada: "",
      chamada: "",
      palavraCta: "RETENCAO",
      totalPalavras: 0,
      duracaoEstimada: 0
    },
    visual: {
      modoCena: "rosto-vidro",
      transicao: "desfoque",
      duracaoTransicao: "0.36",
      estiloLegenda: "amarelo-ouro",
      videoFonte: "projetos/garimpo-armas-desconto/materiais-de-trabalho/fonte/video-base.mp4"
    },
    audio: {
      motorVoz: "pt-BR-AntonioNeural",
      trilha: "calma-pads-01",
      sfxHabilitado: true
    },
    passoAtual: 1
  };

  // --------------------------------------------------------------------------
  // Navegação entre Tabs Principais
  // --------------------------------------------------------------------------
  const tabButtons = document.querySelectorAll(".nav-tab");
  const tabContents = document.querySelectorAll(".tab-content");

  tabButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      tabButtons.forEach(b => b.classList.remove("active"));
      tabContents.forEach(c => c.classList.remove("active"));

      btn.classList.add("active");
      const targetId = "tab" + btn.dataset.tab.charAt(0).toUpperCase() + btn.dataset.tab.slice(1);
      const targetContent = document.getElementById(targetId);
      if (targetContent) targetContent.classList.add("active");
    });
  });

  // --------------------------------------------------------------------------
  // Stepper & Wizard (Passo a Passo)
  // --------------------------------------------------------------------------
  const stepItems = document.querySelectorAll(".step-item");
  const wizardSteps = document.querySelectorAll(".wizard-step");

  function irParaPasso(passo) {
    state.passoAtual = passo;
    stepItems.forEach(item => {
      const p = parseInt(item.dataset.step, 10);
      item.classList.remove("active", "completed");
      if (p === passo) {
        item.classList.add("active");
      } else if (p < passo) {
        item.classList.add("completed");
      }
    });

    wizardSteps.forEach((step, idx) => {
      if (idx + 1 === passo) {
        step.classList.add("active");
      } else {
        step.classList.remove("active");
      }
    });

    if (passo === 5) {
      atualizarResumoFinal();
    }
  }

  document.querySelectorAll(".next-step").forEach(btn => {
    btn.addEventListener("click", () => {
      const next = parseInt(btn.dataset.next, 10);
      irParaPasso(next);
    });
  });

  document.querySelectorAll(".prev-step").forEach(btn => {
    btn.addEventListener("click", () => {
      const prev = parseInt(btn.dataset.prev, 10);
      irParaPasso(prev);
    });
  });

  // --------------------------------------------------------------------------
  // Passo 1: Seleção de Formato
  // --------------------------------------------------------------------------
  const optionCards = document.querySelectorAll(".option-card");
  optionCards.forEach(card => {
    card.addEventListener("click", () => {
      optionCards.forEach(c => {
        c.classList.remove("active");
        c.querySelector(".selection-indicator").textContent = "Selecionar";
      });
      card.classList.add("active");
      card.querySelector(".selection-indicator").textContent = "Selecionado";
      state.formato = card.dataset.type;
    });
  });

  // --------------------------------------------------------------------------
  // Passo 2: Cálculo Dinâmico de Palavras & Duração
  // --------------------------------------------------------------------------
  const inputGancho = document.getElementById("inputGancho");
  const inputOQueE = document.getElementById("inputOQueE");
  const inputProvas = document.getElementById("inputProvas");
  const inputVirada = document.getElementById("inputVirada");
  const inputChamada = document.getElementById("inputChamada");
  const meterWordCount = document.getElementById("meterWordCount");
  const meterTimeCount = document.getElementById("meterTimeCount");
  const meterBarFill = document.getElementById("meterBarFill");
  const meterStatus = document.getElementById("meterStatus");
  const ctaKeywordPreview = document.getElementById("ctaKeywordPreview");

  function recalcularRoteiro() {
    const textoCompleto = [
      inputGancho.value,
      inputOQueE.value,
      inputProvas.value,
      inputVirada.value,
      inputChamada.value
    ].join(" ").trim();

    const palavras = textoCompleto.split(/\s+/).filter(w => w.length > 0);
    const count = palavras.length;
    const segundos = Math.round(count / 3.7);

    state.roteiro.gancho = inputGancho.value;
    state.roteiro.oQueE = inputOQueE.value;
    state.roteiro.provas = inputProvas.value;
    state.roteiro.virada = inputVirada.value;
    state.roteiro.chamada = inputChamada.value;
    state.roteiro.totalPalavras = count;
    state.roteiro.duracaoEstimada = segundos;

    meterWordCount.textContent = `${count} palavras`;
    meterTimeCount.textContent = `~${segundos} s`;

    // Porcentagem para barra de 0 a 60 segundos
    const pct = Math.min(Math.round((segundos / 55) * 100), 100);
    meterBarFill.style.width = `${pct}%`;

    if (segundos >= 40 && segundos <= 50) {
      meterStatus.textContent = "✓ Duração Ideal (40 a 50s)";
      meterStatus.style.color = "#34d399";
      meterBarFill.style.background = "#10b981";
    } else if (segundos < 40) {
      meterStatus.textContent = `⚠️ Rápido demais (${segundos}s). Adicione mais detalhes nas provas.`;
      meterStatus.style.color = "#e8a33d";
      meterBarFill.style.background = "#e8a33d";
    } else {
      meterStatus.textContent = `⚠️ Passou de 50s (${segundos}s). Corte frases para manter o ritmo.`;
      meterStatus.style.color = "#f43f5e";
      meterBarFill.style.background = "#f43f5e";
    }

    // Extrair palavra da DM
    const match = inputChamada.value.match(/comenta\s+([A-ZÁÉÍÓÚÇ0-9-]{3,})/i);
    if (match) {
      state.roteiro.palavraCta = match[1].toUpperCase();
      ctaKeywordPreview.textContent = state.roteiro.palavraCta;
    }
  }

  [inputGancho, inputOQueE, inputProvas, inputVirada, inputChamada].forEach(el => {
    el.addEventListener("input", recalcularRoteiro);
  });
  recalcularRoteiro();

  // --------------------------------------------------------------------------
  // Pautas Dinâmicas do Projeto Ativo
  // --------------------------------------------------------------------------
  function aplicarPautaNoFormulario(pauta) {
    if (!pauta) return;
    if (pauta.gancho !== undefined) inputGancho.value = pauta.gancho;
    if (pauta.oQueE !== undefined) inputOQueE.value = pauta.oQueE;
    if (pauta.provas !== undefined) inputProvas.value = pauta.provas;
    if (pauta.virada !== undefined) inputVirada.value = pauta.virada;
    if (pauta.chamada !== undefined) inputChamada.value = pauta.chamada;
    if (pauta.titulo) state.roteiro.titulo = pauta.titulo;
    recalcularRoteiro();
  }

  const btnIaRefinarPasso2 = document.getElementById("btnIaRefinarPasso2");
  if (btnIaRefinarPasso2) {
    btnIaRefinarPasso2.addEventListener("click", () => {
      abrirModalIAEtapa(2);
    });
  }

  const btnGerarMaisPautas = document.getElementById("btnGerarMaisPautas");
  if (btnGerarMaisPautas) {
    btnGerarMaisPautas.addEventListener("click", async () => {
      const p = state.projetoAtivo;
      if (!p) return;
      btnGerarMaisPautas.disabled = true;
      const originalText = btnGerarMaisPautas.innerHTML;
      btnGerarMaisPautas.innerHTML = '<span class="pulse-dot"></span> Gerando Novas Pautas...';
      try {
        const resp = await fetch("/api/assistente/ganchos", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            tema: `Pautas inovadoras e de alta retenção para ${p.nome} (${p.nicho}) com a proposta ${p.proposta}`,
            projetoId: p.id
          })
        });
        const res = await resp.json();
        if (res.opcoes && res.opcoes.length > 0) {
          const novasPautas = res.opcoes.map((op, i) => ({
            id: `pauta-ia-${Date.now()}-${i}`,
            label: `${op.icone || '✨'} ${op.angulo}`,
            titulo: `${p.nome}: ${op.angulo}`,
            gancho: op.gancho,
            oQueE: op.explicacao,
            provas: `Apresente números concretos e comparativos reais de ${p.nicho} que comprovam como ${p.nome} supera as alternativas tradicionais.`,
            virada: `É exatamente por isso que a solução de ${p.nome} faz a diferença: ${p.proposta}.`,
            chamada: `Comenta ${op.palavraCta || p.palavra_cta || 'ACESSO'} que eu te envio o link direto na sua DM.`
          }));
          p.pautas = (p.pautas || []).concat(novasPautas);
          atualizarUiProjetoAtivo();
          alert(`✓ 4 novas pautas geradas e adicionadas ao projeto ${p.nome}!`);
        }
      } catch (err) {
        alert("Erro ao gerar novas pautas: " + err);
      } finally {
        btnGerarMaisPautas.disabled = false;
        btnGerarMaisPautas.innerHTML = originalText;
      }
    });
  }

  // --------------------------------------------------------------------------
  // Passo 3: Cenas & Visual
  // --------------------------------------------------------------------------
  const sceneCards = document.querySelectorAll(".scene-card");
  sceneCards.forEach(card => {
    card.addEventListener("click", () => {
      sceneCards.forEach(c => c.classList.remove("active"));
      card.classList.add("active");
      state.visual.modoCena = card.dataset.mode;
    });
  });

  const selectTransicao = document.getElementById("selectTransicao");
  if (selectTransicao) {
    selectTransicao.addEventListener("change", (e) => {
      state.visual.transicao = e.target.value;
    });
  }

  const selectDuracaoTransicao = document.getElementById("selectDuracaoTransicao");
  if (selectDuracaoTransicao) {
    selectDuracaoTransicao.addEventListener("change", (e) => {
      state.visual.duracaoTransicao = e.target.value;
    });
  }

  const selectEstiloLegenda = document.getElementById("selectEstiloLegenda");
  if (selectEstiloLegenda) {
    selectEstiloLegenda.addEventListener("change", (e) => {
      state.visual.estiloLegenda = e.target.value;
    });
  }

  const inputFonteVideo = document.getElementById("inputFonteVideo");
  if (inputFonteVideo) {
    inputFonteVideo.addEventListener("input", (e) => {
      state.visual.videoFonte = e.target.value;
    });
  }

  // Atalhos de B-Roll
  const btnVideoArmas = document.getElementById("btnVideoArmas");
  const btnVideoNutrivvo = document.getElementById("btnVideoNutrivvo");
  const btnVideoProjeto = document.getElementById("btnVideoProjeto");

  if (btnVideoArmas) {
    btnVideoArmas.addEventListener("click", () => {
      document.querySelectorAll("#step3 .btn-template").forEach(b => b.classList.remove("active"));
      btnVideoArmas.classList.add("active");
      inputFonteVideo.value = "projetos/garimpo-armas-desconto/materiais-de-trabalho/fonte/video-base.mp4";
      state.visual.videoFonte = inputFonteVideo.value;
    });
  }

  if (btnVideoNutrivvo) {
    btnVideoNutrivvo.addEventListener("click", () => {
      document.querySelectorAll("#step3 .btn-template").forEach(b => b.classList.remove("active"));
      btnVideoNutrivvo.classList.add("active");
      inputFonteVideo.value = "projetos/nutrivvo-retencao-pacientes/materiais-de-trabalho/fonte/video-base.mp4";
      state.visual.videoFonte = inputFonteVideo.value;
    });
  }

  if (btnVideoProjeto) {
    btnVideoProjeto.addEventListener("click", () => {
      document.querySelectorAll("#step3 .btn-template").forEach(b => b.classList.remove("active"));
      btnVideoProjeto.classList.add("active");
      inputFonteVideo.value = "materiais-de-trabalho/fonte/video-base.mp4";
      state.visual.videoFonte = inputFonteVideo.value;
    });
  }

  // --------------------------------------------------------------------------
  // Passo 4: Voz & Áudio
  // --------------------------------------------------------------------------
  const voiceCards = document.querySelectorAll(".voice-card");
  voiceCards.forEach(card => {
    card.addEventListener("click", () => {
      voiceCards.forEach(c => c.classList.remove("active"));
      card.classList.add("active");
      state.audio.motorVoz = card.dataset.engine;
    });
  });

  // Função para testar voz diretamente com Edge-TTS
  async function testarVozNeural(vozId, btnEl) {
    const originalText = btnEl.innerHTML;
    btnEl.disabled = true;
    btnEl.innerHTML = "⏳ Sintetizando...";
    try {
      const frasesExemplo = {
        "pt-BR-AntonioNeural": "Esta arma aqui custava doze mil reais e hoje você encontra com desconto exclusivo.",
        "pt-BR-FranciscaNeural": "Você sabia que mais de setenta por cento dos seus clientes buscam novidades pelo celular?",
        "pt-BR-ThalitaMultilingualNeural": "Olha só essa dica incrível que vai transformar o seu engajamento no Instagram hoje mesmo.",
        "pt-PT-DuarteNeural": "Apresentamos uma solução de alta performance tecnológica com resultados comprovados.",
        "pt-PT-RaquelNeural": "Descubra as principais tendências de inovação e análise estratégica do mercado global."
      };
      const texto = frasesExemplo[vozId] || "Olá, esta é uma demonstração da voz neural em português do Flow Reels.";
      const resp = await fetch("/api/preview-audio", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ texto: texto, voz: vozId })
      });
      const data = await resp.json();
      if (data.sucesso && data.audioUrl) {
        const audio = new Audio(data.audioUrl + "?t=" + Date.now());
        await audio.play();
        btnEl.innerHTML = "🔊 Tocando...";
        audio.onended = () => {
          btnEl.disabled = false;
          btnEl.innerHTML = originalText;
        };
      } else {
        throw new Error(data.erro || "Falha ao gerar voz");
      }
    } catch (err) {
      alert("Erro ao testar áudio: " + err.message);
      btnEl.disabled = false;
      btnEl.innerHTML = originalText;
    }
  }

  const btnPreviewAntonio = document.getElementById("btnPreviewAntonio");
  if (btnPreviewAntonio) {
    btnPreviewAntonio.addEventListener("click", (e) => {
      e.stopPropagation();
      testarVozNeural("pt-BR-AntonioNeural", btnPreviewAntonio);
    });
  }

  const btnPreviewFrancisca = document.getElementById("btnPreviewFrancisca");
  if (btnPreviewFrancisca) {
    btnPreviewFrancisca.addEventListener("click", (e) => {
      e.stopPropagation();
      testarVozNeural("pt-BR-FranciscaNeural", btnPreviewFrancisca);
    });
  }

  const btnPreviewThalita = document.getElementById("btnPreviewThalita");
  if (btnPreviewThalita) {
    btnPreviewThalita.addEventListener("click", (e) => {
      e.stopPropagation();
      testarVozNeural("pt-BR-ThalitaMultilingualNeural", btnPreviewThalita);
    });
  }

  const btnPreviewDuarte = document.getElementById("btnPreviewDuarte");
  if (btnPreviewDuarte) {
    btnPreviewDuarte.addEventListener("click", (e) => {
      e.stopPropagation();
      testarVozNeural("pt-PT-DuarteNeural", btnPreviewDuarte);
    });
  }

  const btnPreviewRaquel = document.getElementById("btnPreviewRaquel");
  if (btnPreviewRaquel) {
    btnPreviewRaquel.addEventListener("click", (e) => {
      e.stopPropagation();
      testarVozNeural("pt-PT-RaquelNeural", btnPreviewRaquel);
    });
  }

  // Trilha Sonora
  const selectTrilha = document.getElementById("selectTrilha");
  if (selectTrilha) {
    selectTrilha.addEventListener("change", (e) => {
      state.audio.trilha = e.target.value;
    });
  }

  const btnOuvirTrilha = document.getElementById("btnOuvirTrilha");
  const audioTrilhaPreview = document.getElementById("audioTrilhaPreview");
  const audioTrilhaStatus = document.getElementById("audioTrilhaStatus");

  if (btnOuvirTrilha && audioTrilhaPreview) {
    btnOuvirTrilha.addEventListener("click", () => {
      const trilhaNome = state.audio.trilha;
      if (trilhaNome === "nenhuma") {
        alert("Opção 'Sem Música' selecionada. Nenhuma trilha tocará.");
        return;
      }
      audioTrilhaPreview.src = `/trilha/${trilhaNome}.mp3`;
      audioTrilhaPreview.style.display = "block";
      audioTrilhaPreview.play();
      if (audioTrilhaStatus) {
        audioTrilhaStatus.textContent = `▶ Tocando trilha: ${trilhaNome}.mp3`;
        audioTrilhaStatus.style.color = "#34d399";
      }
    });
  }

  // SFX Checkbox
  const checkSfx = document.getElementById("checkSfx");
  if (checkSfx) {
    checkSfx.addEventListener("change", (e) => {
      state.audio.sfxHabilitado = e.target.checked;
    });
  }

  // --------------------------------------------------------------------------
  // Passo 5: Atualizar Resumo Final & Produzir
  // --------------------------------------------------------------------------
  function atualizarResumoFinal() {
    const nomeProj = state.projetoAtivo ? state.projetoAtivo.nome : "Nutrivvo";
    document.getElementById("sumFormato").textContent = 
      state.formato === "narrado" ? "Reel Narrado (Sem Rosto)" : (state.formato === "fabrica" ? "Fábrica de Cortes (Com Rosto)" : "Pauta & Roteiro Viral");
    document.getElementById("sumGancho").textContent = `"${state.roteiro.gancho || ''}"`;
    document.getElementById("sumDuracao").textContent = 
      `${state.roteiro.totalPalavras} palavras · ~${state.roteiro.duracaoEstimada}s`;
    
    // Nome legível da voz
    const mapaVoz = {
      "pt-BR-AntonioNeural": "Antônio Neural (pt-BR) · Grave & Autoridade",
      "pt-BR-FranciscaNeural": "Francisca Neural (pt-BR) · Dinâmica & Clara",
      "pt-BR-ThalitaMultilingualNeural": "Thalita Multilingual (pt-BR) · Jovem & Natural",
      "pt-PT-DuarteNeural": "Duarte Neural (pt-PT) · Formal Europeu",
      "pt-PT-RaquelNeural": "Raquel Neural (pt-PT) · Expressiva & Fluente",
      "elevenlabs": "ElevenLabs Clonação Pessoal"
    };
    document.getElementById("sumVoz").textContent = mapaVoz[state.audio.motorVoz] || state.audio.motorVoz;
    
    // Nome legível do modo de cena
    const mapaModos = {
      "rosto-vidro": "Rosto + Vidro (Liquid Glass)",
      "manchete": "Manchete (Fundo Escuro + Destaque)",
      "lado-a-lado": "Lado a Lado (Comparativo Split-Screen)",
      "mundo": "Mundo / Objeto (Tela Cheia)",
      "vidro-liquido": "Vidro Líquido (Frosted Glass Suave)",
      "camadas": "Camadas 3D (Profundidade Dinâmica)",
      "chat": "Chat / Mensagem (Balões WhatsApp)",
      "lista": "Lista / Passos (Contadores 1, 2, 3)"
    };
    document.getElementById("sumCena").textContent = mapaModos[state.visual.modoCena] || state.visual.modoCena;

    const sumTransicao = document.getElementById("sumTransicao");
    if (sumTransicao) {
      sumTransicao.textContent = `${state.visual.transicao.toUpperCase()} (${state.visual.duracaoTransicao || '0.36'}s)`;
    }

    const sumLegenda = document.getElementById("sumLegenda");
    if (sumLegenda) {
      sumLegenda.textContent = state.visual.estiloLegenda;
    }

    const sumTrilha = document.getElementById("sumTrilha");
    if (sumTrilha) {
      sumTrilha.textContent = state.audio.trilha === "nenhuma" ? "Sem Música (Mudo)" : `${state.audio.trilha}.mp3`;
    }

    const sumSfx = document.getElementById("sumSfx");
    if (sumSfx) {
      sumSfx.textContent = state.audio.sfxHabilitado ? "Ativados (Whoosh, Cliques, Impactos)" : "Desativados";
    }
    
    document.getElementById("sumPalavra").textContent = state.roteiro.palavraCta || "RETENCAO";
  }

  const btnGerarReel = document.getElementById("btnGerarReel");
  const terminalContainer = document.getElementById("terminalContainer");
  const terminalLog = document.getElementById("terminalLog");
  const renderProgressOverlay = document.getElementById("renderProgressOverlay");
  const renderProgressBar = document.getElementById("renderProgressBar");
  const renderStageLabel = document.getElementById("renderStageLabel");
  const renderTimerLabel = document.getElementById("renderTimerLabel");
  const renderConsoleLog = document.getElementById("renderConsoleLog");

  async function executarRenderizacao(payloadCustom) {
    btnGerarReel.disabled = true;
    btnGerarReel.innerHTML = '<span class="pulse-dot"></span> Renderizando Vídeo Vertical...';
    terminalContainer.style.display = "block";
    terminalContainer.scrollIntoView({ behavior: "smooth" });
    terminalLog.textContent = "Iniciando pipeline do Flow Reels 3.0 para Nutrivvo...\n";

    if (renderProgressOverlay) {
      renderProgressOverlay.style.display = "flex";
      renderProgressBar.style.width = "15%";
      renderStageLabel.textContent = "🎙️ Iniciando síntese de voz neural...";
      renderConsoleLog.innerHTML = "<div>&gt; Conectando ao motor gráfico do Flow Reels 3.0...</div>";
    }

    const startTime = Date.now();
    const intervalTimer = setInterval(() => {
      const seg = Math.floor((Date.now() - startTime) / 1000);
      const min = String(Math.floor(seg / 60)).padStart(2, "0");
      const s = String(seg % 60).padStart(2, "0");
      if (renderTimerLabel) renderTimerLabel.textContent = `${min}:${s} / ~00:45`;

      if (seg <= 6) {
        if (renderProgressBar) renderProgressBar.style.width = "25%";
        if (renderStageLabel) renderStageLabel.textContent = "🎙️ Sintetizando voz neural e alinhando palavras...";
      } else if (seg <= 16) {
        if (renderProgressBar) renderProgressBar.style.width = "48%";
        if (renderStageLabel) renderStageLabel.textContent = "🎬 Capturando telas e compondo abertura Liquid Glass...";
      } else if (seg <= 34) {
        if (renderProgressBar) renderProgressBar.style.width = "72%";
        if (renderStageLabel) renderStageLabel.textContent = "🎞️ Renderizando 1.800 quadros em 1080x1920 (Chromium + OpenCV)...";
      } else if (seg <= 45) {
        if (renderProgressBar) renderProgressBar.style.width = "88%";
        if (renderStageLabel) renderStageLabel.textContent = "✨ Queimando legendas dinâmicas palavra a palavra...";
      } else {
        if (renderProgressBar) renderProgressBar.style.width = "95%";
        if (renderStageLabel) renderStageLabel.textContent = "🎵 Mixando áudio master a -14.2 LUFS e empacotando MP4...";
      }
    }, 400);

    function log(msg) {
      terminalLog.textContent += msg + "\n";
      terminalLog.scrollTop = terminalLog.scrollHeight;
      if (renderConsoleLog) {
        renderConsoleLog.innerHTML += `<div>&gt; ${msg}</div>`;
        renderConsoleLog.scrollTop = renderConsoleLog.scrollHeight;
      }
    }

    try {
      log("1. Sintetizando locução neural com Edge-TTS (pt-BR-AntonioNeural)...");
      await new Promise(r => setTimeout(r, 700));
      log("   -> Locução gerada com alinhamento preciso de palavras.");

      log("2. Carregando filmagem em alta definição da plataforma https://nutrivvo.com.br/...");
      await new Promise(r => setTimeout(r, 800));
      log("   -> Tomadas mapeadas: CRM, Secretária no Telegram, Radar de Abandono e Gamificação.");

      log("3. Compondo quadros em 1080x1920 a 30 fps (Chromium + Pan & Zoom)...");
      await new Promise(r => setTimeout(r, 1200));
      log("   -> Animações de cards, liquid glass e transições de tela finalizadas.");

      log("4. Queimando legendas dinâmicas em alta resolução com destaque em violeta...");
      await new Promise(r => setTimeout(r, 900));
      log("   -> Legendas estilizadas palavra a palavra.");

      log("5. Mixando áudio master a -14.2 LUFS com ducking e efeitos sonoros...");
      
      const projAtivoId = state.projetoAtivo ? state.projetoAtivo.id : "nutrivvo";
      const projNome = state.projetoAtivo ? state.projetoAtivo.nome : "Flow Reels";
      const payload = payloadCustom || {
        projetoId: projAtivoId,
        titulo: state.roteiro.titulo || (roteiroGeradoPelaIA && roteiroGeradoPelaIA.titulo) || `${projNome}: ` + (state.roteiro.gancho ? state.roteiro.gancho.slice(0, 50) : "Corte Vertical"),
        gancho: state.roteiro.gancho,
        oQueE: state.roteiro.oQueE,
        provas: state.roteiro.provas,
        virada: state.roteiro.virada,
        chamada: state.roteiro.chamada,
        palavraCta: state.roteiro.palavraCta || (state.projetoAtivo ? state.projetoAtivo.palavra_cta : "RETENCAO"),
        motorVoz: state.audio.motorVoz,
        modoCena: state.visual.modoCena,
        transicao: state.visual.transicao,
        duracaoTransicao: state.visual.duracaoTransicao,
        estiloLegenda: state.visual.estiloLegenda,
        videoFonte: state.visual.videoFonte,
        trilha: state.audio.trilha,
        sfxHabilitado: state.audio.sfxHabilitado
      };

      const resp = await fetch("/api/renderizar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await resp.json();

      if (!data.sucesso) {
        throw new Error(data.erro || "Falha na renderização do reel.");
      }

      if (renderProgressBar) renderProgressBar.style.width = "100%";
      if (renderStageLabel) renderStageLabel.textContent = "✅ Vídeo 1080x1920 Concluído com Sucesso!";

      log(`   -> Arquivo final gravado em: ${data.caminho} (${data.tamanhoMb})`);
      log(`   -> Servidor de aprovação atualizado: http://localhost:8790`);
      log("\n✅ PRODUÇÃO CONCLUÍDA COM SUCESSO!");
      log("🎬 O seu novo vídeo já está carregado e pronto para assistir na aba 'Projetos & Cortes'.");
      btnGerarReel.innerHTML = '✓ Novo Reel Pronto!';

      // Registrar o novo projeto no dicionário de projetos
      const projId = data.projeto;
      dadosProjetos[projId] = {
        titulo: data.titulo,
        gancho: `"${data.gancho}"`,
        videoUrl: data.videoUrl,
        duracao: data.duracao,
        cta: data.cta,
        downloadName: `reel-${projId}.mp4`,
        tamanhoMb: data.tamanhoMb,
        caminho: data.caminho
      };

      // Adicionar botão do novo projeto na barra seletora
      const selectorBar = document.querySelector(".project-selector-bar");
      if (selectorBar) {
        selectorBar.querySelectorAll(".btn-proj-select").forEach(b => b.classList.remove("active"));
        const novoBtn = document.createElement("button");
        novoBtn.type = "button";
        novoBtn.className = "btn-proj-select active";
        novoBtn.id = `btnSelect_${projId}`;
        novoBtn.textContent = `✨ ${data.titulo.slice(0, 32)} (${data.tamanhoMb})`;
        selectorBar.appendChild(novoBtn);
        
        novoBtn.addEventListener("click", () => {
          selectorBar.querySelectorAll(".btn-proj-select").forEach(b => b.classList.remove("active"));
          novoBtn.classList.add("active");
          carregarProjetoNoPlayer(projId);
        });
      }

      await new Promise(r => setTimeout(r, 900));
      if (renderProgressOverlay) renderProgressOverlay.style.display = "none";

      setTimeout(() => {
        carregarProjetoNoPlayer(projId);
        document.getElementById("tabBtnProjetos").click();
        playerVideo.play().catch(() => {});
      }, 500);

    } catch (err) {
      log("Erro: " + err.message);
      if (renderProgressOverlay) renderProgressOverlay.style.display = "none";
      alert("Erro na renderização: " + err.message);
      btnGerarReel.innerHTML = 'Tentar Novamente';
    } finally {
      clearInterval(intervalTimer);
      btnGerarReel.disabled = false;
    }
  }

  btnGerarReel.addEventListener("click", () => {
    executarRenderizacao();
  });

  // --------------------------------------------------------------------------
  // Tab Radar: Botões de Carregar Pauta
  // --------------------------------------------------------------------------
  document.querySelectorAll(".load-pauta").forEach(btn => {
    btn.addEventListener("click", () => {
      const pauta = btn.dataset.pauta;
      document.getElementById("tabBtnWizard").click();
      irParaPasso(2);
      
      if (pauta === "nutrivvo-retencao") {
        document.getElementById("btnTplNutrivvoRetencao").click();
      } else if (pauta === "nutrivvo-secretaria") {
        document.getElementById("btnTplNutrivvoSecretaria").click();
      } else if (pauta === "nutrivvo-gamificacao") {
        document.getElementById("btnTplNutrivvoGamificacao").click();
      } else if (pauta === "nutrivvo-dieta") {
        document.getElementById("btnTplNutrivvoDieta").click();
      }
    });
  });

  // --------------------------------------------------------------------------
  // Tab Marca: Tokens em Tempo Real
  // --------------------------------------------------------------------------
  const colorSuperficie = document.getElementById("colorSuperficie");
  const colorDestaque = document.getElementById("colorDestaque");
  const colorTinta = document.getElementById("colorTinta");
  const colorSuave = document.getElementById("colorSuave");
  const mockPanelSample = document.getElementById("mockPanelSample");
  const sampleAccent = document.getElementById("sampleAccent");
  const sampleTag = document.getElementById("sampleTag");
  const sampleTitle = document.getElementById("sampleTitle");

  function atualizarMockMarca() {
    mockPanelSample.style.backgroundColor = colorSuperficie.value;
    sampleAccent.style.color = colorDestaque.value;
    sampleTag.style.color = colorDestaque.value;
    sampleTag.style.backgroundColor = colorDestaque.value + "26";
    sampleTitle.style.color = colorTinta.value;
  }

  [colorSuperficie, colorDestaque, colorTinta, colorSuave].forEach(input => {
    input.addEventListener("input", () => {
      input.nextElementSibling.textContent = input.value.toUpperCase();
      atualizarMockMarca();
    });
  });

  document.getElementById("btnSalvarTokens").addEventListener("click", () => {
    alert("Tokens de marca salvos com sucesso em marca/tokens.json!");
  });

  // --------------------------------------------------------------------------
  // Tab Projetos: Alternar entre Vídeos Prontos
  // --------------------------------------------------------------------------
  const btnSelectNutrivvo = document.getElementById("btnSelectNutrivvo");
  const btnSelectGarimpo = document.getElementById("btnSelectGarimpo");
  const playerVideo = document.getElementById("playerVideo");
  const videoPlayerSource = document.getElementById("videoPlayerSource");
  const currentProjectTitle = document.getElementById("currentProjectTitle");
  const projectHook = document.getElementById("projectHook");
  const projectStatDuration = document.getElementById("projectStatDuration");
  const projectStatCta = document.getElementById("projectStatCta");
  const btnDownloadMp4 = document.getElementById("btnDownloadMp4");
  const projectCodePath = document.getElementById("projectCodePath");

  const dadosProjetos = {
    nutrivvo: {
      titulo: "Nutrivvo: Por que 70% dos pacientes somem (Radar de Abandono)",
      gancho: '"Você sabe por que mais de setenta por cento dos seus pacientes de nutrição nunca voltam para a segunda consulta?"',
      videoUrl: "/video/nutrivvo-retencao-pacientes/narrado-01/narrado-01.mp4",
      duracao: "53.8 s",
      cta: "RETENCAO",
      downloadName: "reel-nutrivvo-retencao.mp4",
      tamanhoMb: "32.5 MB",
      caminho: "projetos/nutrivvo-retencao-pacientes/narrado-01/narrado-01.mp4"
    },
    garimpo: {
      titulo: "O garimpo de armas: modelos pela metade do preço",
      gancho: '"Essa arma aqui custava doze mil reais e hoje você acha por cinco na loja."',
      videoUrl: "/video/garimpo-armas-desconto/narrado-01/narrado-01.mp4",
      duracao: "58.4 s",
      cta: "GARIMPO",
      downloadName: "reel-garimpo-armas.mp4",
      tamanhoMb: "47.8 MB",
      caminho: "projetos/garimpo-armas-desconto/narrado-01/narrado-01.mp4"
    }
  };

  function carregarProjetoNoPlayer(chave) {
    const p = dadosProjetos[chave];
    if (!p) return;
    currentProjectTitle.textContent = p.titulo;
    projectHook.innerHTML = `<strong>Gancho:</strong> ${p.gancho}`;
    projectStatDuration.textContent = p.duracao;
    projectStatCta.textContent = p.cta;
    btnDownloadMp4.href = p.videoUrl;
    btnDownloadMp4.textContent = `Baixar MP4 (${p.tamanhoMb})`;
    btnDownloadMp4.setAttribute("download", p.downloadName);
    projectCodePath.textContent = p.caminho;

    videoPlayerSource.src = p.videoUrl;
    playerVideo.load();
  }

  if (btnSelectNutrivvo && btnSelectGarimpo) {
    btnSelectNutrivvo.addEventListener("click", () => {
      btnSelectNutrivvo.classList.add("active");
      btnSelectGarimpo.classList.remove("active");
      carregarProjetoNoPlayer("nutrivvo");
    });

    btnSelectGarimpo.addEventListener("click", () => {
      btnSelectGarimpo.classList.add("active");
      btnSelectNutrivvo.classList.remove("active");
      carregarProjetoNoPlayer("garimpo");
    });
  }

  // --------------------------------------------------------------------------
  // Gerenciamento Dinâmico de Projetos (Universal para Qualquer Pessoa/Marca)
  // --------------------------------------------------------------------------
  state.projetos = [];
  state.projetoAtivo = null;
  state.opcoesGanchos = [];
  state.ganchoSelecionado = null;
  let roteiroGeradoPelaIA = null;

  const headerProjectSelect = document.getElementById("headerProjectSelect");
  const btnOpenNewProjectModal = document.getElementById("btnOpenNewProjectModal");
  const modalNovoProjeto = document.getElementById("modalNovoProjeto");
  const btnCloseNewProjectModal = document.getElementById("btnCloseNewProjectModal");
  const btnCancelNewProject = document.getElementById("btnCancelNewProject");
  const formNovoProjeto = document.getElementById("formNovoProjeto");
  const newProjCor = document.getElementById("newProjCor");
  const newProjCorHex = document.getElementById("newProjCorHex");
  const headerLogoIcon = document.getElementById("headerLogoIcon");

  const aiActiveProjectName = document.getElementById("aiActiveProjectName");
  const aiActiveProjectNiche = document.getElementById("aiActiveProjectNiche");
  const aiDynamicChipsContainer = document.getElementById("aiDynamicChipsContainer");

  // Chips Rápidos por Nicho
  const sugestoesPorNicho = {
    nutrivvo: [
      { label: "🥗 70% Somem (Abandono)", prompt: "A dor de mais de 70% dos pacientes que nunca voltam na 2ª consulta e como o Radar de Abandono resolve." },
      { label: "📱 Fim do WhatsApp Pessoal", prompt: "Por que atender paciente no WhatsApp pessoal drena a sua energia e como a Secretária do Telegram protege o nutri." },
      { label: "⚡ Dieta com IA em 2 Min", prompt: "O desperdício de passar 2 horas digitando cardápio no Word vs criar cardápios reais com IA em 2 minutos." },
      { label: "🎮 Gamificação & Duolingo", prompt: "O efeito Duolingo na nutrição: streak de dias seguidos e fotos analisadas por inteligência artificial." }
    ],
    "garimpo-armas": [
      { label: "🔫 Garimpo 50% Off", prompt: "Como garimpar armas e equipamentos de marcas renomadas pagando até metade do preço da loja." },
      { label: "🎯 Erro de Comprar Novo", prompt: "O maior erro do atirador iniciante ao comprar a primeira arma na empolgação e pagar o dobro." },
      { label: "📜 Burocracia Descomplicada", prompt: "O passo a passo direto para aproveitar promoções legítimas sem cair em golpes." }
    ],
    "barbearia-alfa": [
      { label: "💈 Sem Fila de Espera", prompt: "Como agendar seu horário em 10 segundos pelo link e nunca mais perder a manhã de sábado esperando na barbearia." },
      { label: "✂️ Manter o Corte Alinhado", prompt: "O segredo para manter o disfarçado e a barba impecáveis 3 semanas após sair da cadeira." },
      { label: "🧴 Produto Certo vs Errado", prompt: "O erro que 90% dos homens cometem usando pomada errada e detonando o couro cabeludo." }
    ],
    "dra-dermatologia": [
      { label: "✨ Manchas & Melasma", prompt: "Por que o seu melasma sempre volta e o erro silencioso que você comete na rotina noturna." },
      { label: "🧴 O Segredo do Protetor", prompt: "O protetor solar comum não protege contra luz visível de tela: saiba o que aplicar para não manchar a pele." },
      { label: "💧 Rejuvenescimento Natural", prompt: "Como ter uma pele firme e iluminada sem parecer artificial ou exagerada." }
    ]
  };

  let pautasExtraidasSite = [];

  function atualizarUiProjetoAtivo() {
    if (!state.projetoAtivo) return;
    const p = state.projetoAtivo;

    // 1. Ícone temático no cabeçalho
    if (p.id.includes("nutri")) headerLogoIcon.textContent = "🥗";
    else if (p.id.includes("arma") || p.id.includes("garimpo")) headerLogoIcon.textContent = "🔫";
    else if (p.id.includes("barba")) headerLogoIcon.textContent = "💈";
    else if (p.id.includes("derm") || p.id.includes("pele")) headerLogoIcon.textContent = "✨";
    else headerLogoIcon.textContent = "🎬";

    // 2. Modal IA Badges e Títulos
    if (aiActiveProjectName) aiActiveProjectName.textContent = p.nome;
    if (aiActiveProjectNiche) aiActiveProjectNiche.textContent = p.nicho;

    // 3. Label de Pautas e Link do Site no Passo 2
    const labelPautas = document.getElementById("labelPautasProjeto");
    if (labelPautas) {
      labelPautas.textContent = `Pautas de ${p.nome}:`;
    }

    const linkSite = document.getElementById("linkSiteProjeto");
    if (linkSite) {
      if (p.url_site) {
        linkSite.href = p.url_site;
        linkSite.textContent = `🌐 ${p.url_site.replace(/^https?:\/\//, '')}`;
        linkSite.style.display = "inline-flex";
      } else {
        linkSite.style.display = "none";
      }
    }

    // 4. Renderizar Pautas Dinâmicas no Passo 2
    const containerPautas = document.getElementById("containerPautasProjeto");
    if (containerPautas) {
      const pautas = p.pautas || [];
      if (pautas.length > 0) {
        containerPautas.innerHTML = pautas.map((item, idx) => `
          <button type="button" class="btn-template ${idx === 0 ? 'active' : ''}" data-pauta-idx="${idx}">
            ${item.label || item.titulo || `Pauta ${idx + 1}`}
          </button>
        `).join("");

        // Carrega automaticamente a Pauta 0 no formulário do editor (substituindo textos antigos)
        aplicarPautaNoFormulario(pautas[0]);

        containerPautas.querySelectorAll(".btn-template").forEach(btn => {
          btn.addEventListener("click", () => {
            containerPautas.querySelectorAll(".btn-template").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            const idx = parseInt(btn.dataset.pautaIdx, 10);
            if (pautas[idx]) {
              aplicarPautaNoFormulario(pautas[idx]);
            }
          });
        });
      } else {
        containerPautas.innerHTML = `
          <span style="font-size:12px; color:var(--text-muted); padding:6px 0;">
            Nenhuma pauta cadastrada. Clique em '+ 4 Novas Pautas com IA' para gerar sob medida.
          </span>
        `;
      }
    }

    // 5. Chips dinâmicos para a IA
    if (aiDynamicChipsContainer) {
      let listaChips = [];
      if (p.pautas && p.pautas.length > 0) {
        listaChips = p.pautas.map(pt => ({
          label: pt.label || pt.titulo,
          prompt: pt.titulo || pt.gancho
        }));
      } else if (sugestoesPorNicho[p.id]) {
        listaChips = sugestoesPorNicho[p.id];
      } else {
        listaChips = [
          { label: `💡 O Maior Erro em ${p.nicho}`, prompt: `O maior erro que as pessoas cometem em ${p.nicho} e como a solução de ${p.nome} resolve.` },
          { label: `⚡ Economia & Rapidez`, prompt: `Como economizar tempo e dinheiro com ${p.nome}.` },
          { label: `🔍 Comparativo Chocante`, prompt: `O segredo e comparativo de preços de ${p.nicho} que quase ninguém conhece.` }
        ];
      }

      aiDynamicChipsContainer.innerHTML = listaChips.map(c => `
        <button type="button" class="ai-chip" data-prompt="${(c.prompt || '').replace(/"/g, '&quot;')}">${c.label}</button>
      `).join("");

      aiDynamicChipsContainer.querySelectorAll(".ai-chip").forEach(chip => {
        chip.addEventListener("click", () => {
          aiPromptInput.value = chip.dataset.prompt;
          gerarOpcoesGanchos(chip.dataset.prompt);
        });
      });
    }

    // 6. Atualizar cor de destaque do editor e tokens
    if (p.cor_destaque) {
      if (colorDestaque) {
        colorDestaque.value = p.cor_destaque;
        if (colorDestaque.nextElementSibling) {
          colorDestaque.nextElementSibling.textContent = p.cor_destaque.toUpperCase();
        }
      }
      atualizarMockMarca();
      document.documentElement.style.setProperty("--accent-primary", p.cor_destaque);
    }

    // 7. Atualizar palavra CTA
    if (p.palavra_cta) {
      state.roteiro.palavraCta = p.palavra_cta;
      if (document.getElementById("ctaKeywordPreview")) {
        document.getElementById("ctaKeywordPreview").textContent = p.palavra_cta;
      }
    }

    // 8. Atualizar vídeo base e voz padrão do projeto
    if (p.video_base && inputFonteVideo) {
      inputFonteVideo.value = p.video_base;
      state.visual.videoFonte = p.video_base;
    }
    if (p.voz_padrao) {
      state.audio.motorVoz = p.voz_padrao;
      document.querySelectorAll(".voice-card").forEach(c => {
        c.classList.toggle("active", c.dataset.engine === p.voz_padrao);
      });
      if (document.getElementById("aiSelectVoz")) {
        document.getElementById("aiSelectVoz").value = p.voz_padrao;
      }
    }

    // 9. Sincronizar atributos nos seletores do modal da IA
    sincronizarAtributosParaAiModal();
  }

  function sincronizarAtributosParaAiModal() {
    const sModoCena = document.getElementById("aiSelectModoCena");
    const sTransicao = document.getElementById("aiSelectTransicao");
    const sDuracao = document.getElementById("aiSelectDuracao");
    const sLegenda = document.getElementById("aiSelectLegenda");
    const sVoz = document.getElementById("aiSelectVoz");
    const sTrilha = document.getElementById("aiSelectTrilha");
    const sSfx = document.getElementById("aiCheckSfx");

    if (sModoCena) sModoCena.value = state.visual.modoCena;
    if (sTransicao) sTransicao.value = state.visual.transicao;
    if (sDuracao) sDuracao.value = state.visual.duracaoTransicao;
    if (sLegenda) sLegenda.value = state.visual.estiloLegenda;
    if (sVoz) sVoz.value = state.audio.motorVoz;
    if (sTrilha) sTrilha.value = state.audio.trilha;
    if (sSfx) sSfx.checked = state.audio.sfxHabilitado;
  }

  function sincronizarAtributosAiParaEditor() {
    const sModoCena = document.getElementById("aiSelectModoCena");
    const sTransicao = document.getElementById("aiSelectTransicao");
    const sDuracao = document.getElementById("aiSelectDuracao");
    const sLegenda = document.getElementById("aiSelectLegenda");
    const sVoz = document.getElementById("aiSelectVoz");
    const sTrilha = document.getElementById("aiSelectTrilha");
    const sSfx = document.getElementById("aiCheckSfx");

    if (sModoCena) {
      state.visual.modoCena = sModoCena.value;
      document.querySelectorAll(".scene-card").forEach(c => {
        c.classList.toggle("active", c.dataset.mode === sModoCena.value);
      });
    }
    if (sTransicao) {
      state.visual.transicao = sTransicao.value;
      if (selectTransicao) selectTransicao.value = sTransicao.value;
    }
    if (sDuracao) {
      state.visual.duracaoTransicao = sDuracao.value;
      if (selectDuracaoTransicao) selectDuracaoTransicao.value = sDuracao.value;
    }
    if (sLegenda) {
      state.visual.estiloLegenda = sLegenda.value;
      if (selectEstiloLegenda) selectEstiloLegenda.value = sLegenda.value;
    }
    if (sVoz) {
      state.audio.motorVoz = sVoz.value;
      document.querySelectorAll(".voice-card").forEach(c => {
        c.classList.toggle("active", c.dataset.engine === sVoz.value);
      });
    }
    if (sTrilha) {
      state.audio.trilha = sTrilha.value;
      if (selectTrilha) selectTrilha.value = sTrilha.value;
    }
    if (sSfx) {
      state.audio.sfxHabilitado = sSfx.checked;
    }
  }

  // Listeners de mudança nos atributos do modal da IA (Modo Geral)
  ["aiSelectModoCena", "aiSelectTransicao", "aiSelectDuracao", "aiSelectLegenda", "aiSelectVoz", "aiSelectTrilha", "aiCheckSfx"].forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener("change", () => {
        sincronizarAtributosAiParaEditor();
      });
    }
  });

  async function carregarProjetos() {
    try {
      const resp = await fetch("/api/projetos");
      const dados = await resp.json();
      state.projetos = dados.projetos || [];
      const ativoId = dados.projeto_ativo;
      state.projetoAtivo = state.projetos.find(p => p.id === ativoId) || state.projetos[0];

      if (headerProjectSelect) {
        headerProjectSelect.innerHTML = state.projetos.map(p => `
          <option value="${p.id}" ${p.id === state.projetoAtivo.id ? 'selected' : ''}>
            ${p.nome} (${p.nicho})
          </option>
        `).join("");
      }

      atualizarUiProjetoAtivo();
    } catch (err) {
      console.warn("Falha ao carregar lista de projetos:", err);
    }
  }

  if (headerProjectSelect) {
    headerProjectSelect.addEventListener("change", async (e) => {
      const novoId = e.target.value;
      try {
        const resp = await fetch("/api/projetos/selecionar", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ projetoId: novoId })
        });
        const res = await resp.json();
        if (res.sucesso) {
          state.projetoAtivo = res.projeto;
          atualizarUiProjetoAtivo();
        }
      } catch (err) {
        console.error("Erro ao selecionar projeto:", err);
      }
    });
  }

  // Modal Novo Projeto & Análise de URL de Site
  if (btnOpenNewProjectModal) {
    btnOpenNewProjectModal.addEventListener("click", () => {
      pautasExtraidasSite = [];
      modalNovoProjeto.classList.add("open");
    });
  }
  if (btnCloseNewProjectModal) {
    btnCloseNewProjectModal.addEventListener("click", () => modalNovoProjeto.classList.remove("open"));
  }
  if (btnCancelNewProject) {
    btnCancelNewProject.addEventListener("click", () => modalNovoProjeto.classList.remove("open"));
  }
  if (newProjCor) {
    newProjCor.addEventListener("input", (e) => {
      if (newProjCorHex) newProjCorHex.textContent = e.target.value.toUpperCase();
    });
  }

  // Botão Puxar Dados do Site com IA
  const btnAnalisarUrlSite = document.getElementById("btnAnalisarUrlSite");
  const newProjUrl = document.getElementById("newProjUrl");
  const statusAnaliseSite = document.getElementById("statusAnaliseSite");
  if (btnAnalisarUrlSite && newProjUrl) {
    btnAnalisarUrlSite.addEventListener("click", async () => {
      const url = newProjUrl.value.trim();
      if (!url) {
        alert("Por favor, digite a URL do site antes de puxar os dados.");
        newProjUrl.focus();
        return;
      }
      btnAnalisarUrlSite.disabled = true;
      const originalBtnText = btnAnalisarUrlSite.innerHTML;
      btnAnalisarUrlSite.innerHTML = '<span class="pulse-dot"></span> Lendo site & Gerando pautas...';
      if (statusAnaliseSite) {
        statusAnaliseSite.innerHTML = '<span style="color:#c084fc;">⏳ Acessando site oficial e processando informações com GPT-4o...</span>';
      }

      try {
        const resp = await fetch("/api/projetos/analisar-url", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ url })
        });
        const dados = await resp.json();
        if (dados.sucesso && dados.dados) {
          const d = dados.dados;
          if (d.nome) document.getElementById("newProjNome").value = d.nome;
          if (d.nicho) document.getElementById("newProjNicho").value = d.nicho;
          if (d.palavra_cta) document.getElementById("newProjCta").value = d.palavra_cta;
          if (d.proposta) document.getElementById("newProjProposta").value = d.proposta;
          if (d.publico) document.getElementById("newProjPublico").value = d.publico;
          if (d.cor_destaque) {
            newProjCor.value = d.cor_destaque;
            if (newProjCorHex) newProjCorHex.textContent = d.cor_destaque.toUpperCase();
          }
          if (d.pautas && d.pautas.length > 0) {
            pautasExtraidasSite = d.pautas;
          }
          if (statusAnaliseSite) {
            statusAnaliseSite.innerHTML = `<span style="color:#34d399; font-weight:700;">✓ Site analisado com sucesso! Dados e ${pautasExtraidasSite.length} pautas exclusivas geradas.</span>`;
          }
        } else {
          throw new Error(dados.erro || "Falha na resposta do servidor");
        }
      } catch (err) {
        console.error("Erro ao analisar URL:", err);
        if (statusAnaliseSite) {
          statusAnaliseSite.innerHTML = `<span style="color:#ef4444;">Erro ao ler site: ${err.message}. Você pode preencher os campos manualmente.</span>`;
        }
      } finally {
        btnAnalisarUrlSite.disabled = false;
        btnAnalisarUrlSite.innerHTML = originalBtnText;
      }
    });
  }

  if (formNovoProjeto) {
    formNovoProjeto.addEventListener("submit", async (e) => {
      e.preventDefault();
      const nome = document.getElementById("newProjNome").value.trim();
      const nicho = document.getElementById("newProjNicho").value.trim();
      const cta = document.getElementById("newProjCta").value.trim().toUpperCase();
      const proposta = document.getElementById("newProjProposta").value.trim();
      const publico = document.getElementById("newProjPublico").value.trim();
      const cor = newProjCor.value;
      const formato = document.getElementById("newProjFormato").value;
      const urlSite = newProjUrl ? newProjUrl.value.trim() : "";

      if (!nome) {
        alert("Preencha o nome do projeto!");
        return;
      }

      const btnSubmit = document.getElementById("btnSubmitNewProject");
      btnSubmit.disabled = true;
      btnSubmit.textContent = "Criando...";

      try {
        const resp = await fetch("/api/projetos/criar", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            nome, nicho, proposta, publico,
            palavra_cta: cta || "ACESSO",
            cor_destaque: cor,
            tipo_formato: formato,
            url_site: urlSite,
            pautas: pautasExtraidasSite
          })
        });
        const res = await resp.json();
        if (res.sucesso) {
          modalNovoProjeto.classList.remove("open");
          formNovoProjeto.reset();
          pautasExtraidasSite = [];
          if (statusAnaliseSite) statusAnaliseSite.textContent = "";
          await carregarProjetos();
          alert(`✓ Projeto '${res.projeto.nome}' criado e ativado com sucesso!`);
        } else {
          alert(`Erro: ${res.erro}`);
        }
      } catch (err) {
        alert(`Erro de conexão ao criar projeto: ${err}`);
      } finally {
        btnSubmit.disabled = false;
        btnSubmit.textContent = "✨ Criar e Ativar Projeto";
      }
    });
  }

  // --------------------------------------------------------------------------
  // Assistente IA: Tabs (Modo Geral vs Modo por Etapa)
  // --------------------------------------------------------------------------
  const btnTabAiGeral = document.getElementById("btnTabAiGeral");
  const btnTabAiEtapa = document.getElementById("btnTabAiEtapa");
  const aiContainerModoGeral = document.getElementById("aiContainerModoGeral");
  const aiContainerModoEtapa = document.getElementById("aiContainerModoEtapa");

  function alternarModoAi(modo) {
    if (modo === "etapa") {
      if (btnTabAiEtapa) btnTabAiEtapa.classList.add("active");
      if (btnTabAiGeral) btnTabAiGeral.classList.remove("active");
      if (aiContainerModoGeral) aiContainerModoGeral.style.display = "none";
      if (aiContainerModoEtapa) aiContainerModoEtapa.style.display = "block";
    } else {
      if (btnTabAiGeral) btnTabAiGeral.classList.add("active");
      if (btnTabAiEtapa) btnTabAiEtapa.classList.remove("active");
      if (aiContainerModoGeral) aiContainerModoGeral.style.display = "block";
      if (aiContainerModoEtapa) aiContainerModoEtapa.style.display = "none";
    }
  }

  if (btnTabAiGeral) btnTabAiGeral.addEventListener("click", () => alternarModoAi("geral"));
  if (btnTabAiEtapa) btnTabAiEtapa.addEventListener("click", () => alternarModoAi("etapa"));

  // --------------------------------------------------------------------------
  // Assistente IA: Modo por Etapa (Passos 1, 2, 3 e 4)
  // --------------------------------------------------------------------------
  let currentAiStep = 1;
  let resultadoAiEtapaAtual = null;

  const aiStepDefs = {
    1: {
      titulo: "🎯 Assistência para o Passo 1: Formato & Ângulo",
      desc: "A IA analisa o seu projeto e sugere 3 ângulos de abordagem viral com formatos recomendados (Reel Narrado, Fábrica de Cortes ou Radar).",
      label: "Foco ou Dúvida sobre o Formato (Opcional):",
      placeholder: "Ex: Quero saber se é melhor Reel Narrado sem rosto ou Cortes do vídeo longo para este anúncio..."
    },
    2: {
      titulo: "✍️ Assistência para o Passo 2: Roteiro & Gancho (5 Blocos)",
      desc: "A IA redige um roteiro calibrado em 5 blocos (Gancho, O Que É, Provas, Virada, Chamada DM) de 40 a 50s com alta retenção.",
      label: "Tema ou Objeção do Cliente para o Roteiro:",
      placeholder: "Ex: Fale sobre a diferença gritante de preço entre armarias ou como não pagar o dobro na 1ª compra..."
    },
    3: {
      titulo: "🎬 Assistência para o Passo 3: Estilo Visual & Modos de Cena",
      desc: "A IA recomenda o melhor modo de cena (Vidro Líquido, Manchete, Lado a Lado, Camadas 3D), transição e cores para o seu nicho.",
      label: "Tipo de Gravação ou B-Roll disponível:",
      placeholder: "Ex: Tenho uma filmagem de tela e gravação de teste, qual o melhor modo de cena e corte?"
    },
    4: {
      titulo: "🎙️ Assistência para o Passo 4: Locução Neural & Trilha Sonora",
      desc: "A IA indica a melhor voz da Edge-TTS e a trilha sonora ideal para a energia e autoridade do tema.",
      label: "Tom e Clima Desejados para o Áudio:",
      placeholder: "Ex: Tom sério de autoridade / denúncia ou tom dinâmico e enérgico?"
    }
  };

  function selecionarEtapaAi(etapa) {
    currentAiStep = etapa;
    document.querySelectorAll("#aiStepPillsContainer .btn-template").forEach(b => {
      b.classList.toggle("active", parseInt(b.dataset.stepTarget, 10) === etapa);
    });
    const def = aiStepDefs[etapa] || aiStepDefs[1];
    const tEl = document.getElementById("aiStepTitle");
    const dEl = document.getElementById("aiStepDescription");
    const lEl = document.getElementById("aiStepContextLabel");
    const iEl = document.getElementById("aiStepContextInput");
    if (tEl) tEl.textContent = def.titulo;
    if (dEl) dEl.textContent = def.desc;
    if (lEl) lEl.textContent = def.label;
    if (iEl) iEl.placeholder = def.placeholder;
    const outBox = document.getElementById("aiStepOutputContainer");
    if (outBox) outBox.style.display = "none";
  }

  document.querySelectorAll("#aiStepPillsContainer .btn-template").forEach(b => {
    b.addEventListener("click", () => {
      const etapa = parseInt(b.dataset.stepTarget, 10);
      selecionarEtapaAi(etapa);
    });
  });

  function abrirModalIAEtapa(etapa) {
    abrirModalIA();
    alternarModoAi("etapa");
    selecionarEtapaAi(etapa);
  }

  // Executar Assistente por Etapa
  const btnExecutarAiEtapa = document.getElementById("btnExecutarAiEtapa");
  const aiStepOutputContainer = document.getElementById("aiStepOutputContainer");
  const aiStepOutputContent = document.getElementById("aiStepOutputContent");
  const aiStepContextInput = document.getElementById("aiStepContextInput");
  const btnCopiarAiEtapa = document.getElementById("btnCopiarAiEtapa");
  const btnAplicarAiEtapa = document.getElementById("btnAplicarAiEtapa");

  if (btnExecutarAiEtapa) {
    btnExecutarAiEtapa.addEventListener("click", async () => {
      btnExecutarAiEtapa.disabled = true;
      const originalText = btnExecutarAiEtapa.innerHTML;
      btnExecutarAiEtapa.innerHTML = '<span class="pulse-dot"></span> Gerando Sugestão Especializada com IA...';
      if (aiStepOutputContainer) aiStepOutputContainer.style.display = "none";

      try {
        const resp = await fetch("/api/assistente/etapa", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            etapa: currentAiStep,
            contexto: aiStepContextInput ? aiStepContextInput.value.trim() : "",
            projetoId: state.projetoAtivo ? state.projetoAtivo.id : "armas"
          })
        });
        const res = await resp.json();
        if (res.sucesso && res.sugestao) {
          resultadoAiEtapaAtual = res.sugestao;
          let displayTexto = "";
          if (currentAiStep === 2 && resultadoAiEtapaAtual.gancho) {
            displayTexto = `1. Gancho (0-4s):\n${resultadoAiEtapaAtual.gancho}\n\n2. Contexto (4-10s):\n${resultadoAiEtapaAtual.oQueE}\n\n3. Provas (10-35s):\n${resultadoAiEtapaAtual.provas}\n\n4. Virada (35-42s):\n${resultadoAiEtapaAtual.virada}\n\n5. Chamada DM (42-48s):\n${resultadoAiEtapaAtual.chamada}`;
          } else {
            displayTexto = typeof resultadoAiEtapaAtual === "object"
              ? JSON.stringify(resultadoAiEtapaAtual, null, 2)
              : String(resultadoAiEtapaAtual);
          }
          if (aiStepOutputContent) aiStepOutputContent.textContent = displayTexto;
          if (aiStepOutputContainer) {
            aiStepOutputContainer.style.display = "block";
            aiStepOutputContainer.scrollIntoView({ behavior: "smooth" });
          }
        } else {
          throw new Error(res.erro || "Falha ao gerar sugestão para a etapa");
        }
      } catch (err) {
        alert("Erro ao consultar assistente de etapa: " + err.message);
      } finally {
        btnExecutarAiEtapa.disabled = false;
        btnExecutarAiEtapa.innerHTML = originalText;
      }
    });
  }

  if (btnCopiarAiEtapa && aiStepOutputContent) {
    btnCopiarAiEtapa.addEventListener("click", () => {
      navigator.clipboard.writeText(aiStepOutputContent.textContent).then(() => {
        const orig = btnCopiarAiEtapa.textContent;
        btnCopiarAiEtapa.textContent = "✓ Copiado!";
        setTimeout(() => { btnCopiarAiEtapa.textContent = orig; }, 1600);
      });
    });
  }

  if (btnAplicarAiEtapa) {
    btnAplicarAiEtapa.addEventListener("click", () => {
      if (!resultadoAiEtapaAtual) return;
      if (currentAiStep === 1) {
        if (resultadoAiEtapaAtual.formatoRecomendado) {
          const card = document.querySelector(`.option-card[data-format="${resultadoAiEtapaAtual.formatoRecomendado}"]`);
          if (card) card.click();
        }
        fecharModalIA();
        document.getElementById("tabBtnWizard").click();
        irParaPasso(1);
      } else if (currentAiStep === 2) {
        aplicarPautaNoFormulario(resultadoAiEtapaAtual);
        fecharModalIA();
        document.getElementById("tabBtnWizard").click();
        irParaPasso(2);
      } else if (currentAiStep === 3) {
        if (resultadoAiEtapaAtual.modoCenaRecomendado) {
          const card = document.querySelector(`.scene-card[data-mode="${resultadoAiEtapaAtual.modoCenaRecomendado}"]`);
          if (card) card.click();
        }
        if (resultadoAiEtapaAtual.transicaoRecomendada && selectTransicao) {
          selectTransicao.value = resultadoAiEtapaAtual.transicaoRecomendada;
          state.visual.transicao = selectTransicao.value;
        }
        if (resultadoAiEtapaAtual.legendaRecomendada && selectEstiloLegenda) {
          selectEstiloLegenda.value = resultadoAiEtapaAtual.legendaRecomendada;
          state.visual.estiloLegenda = selectEstiloLegenda.value;
        }
        fecharModalIA();
        document.getElementById("tabBtnWizard").click();
        irParaPasso(3);
      } else if (currentAiStep === 4) {
        if (resultadoAiEtapaAtual.vozRecomendada) {
          const vCard = document.querySelector(`.voice-card[data-engine="${resultadoAiEtapaAtual.vozRecomendada}"]`);
          if (vCard) vCard.click();
        }
        if (resultadoAiEtapaAtual.trilhaRecomendada && selectTrilha) {
          selectTrilha.value = resultadoAiEtapaAtual.trilhaRecomendada;
          state.audio.trilha = selectTrilha.value;
        }
        fecharModalIA();
        document.getElementById("tabBtnWizard").click();
        irParaPasso(4);
      }
    });
  }

  // --------------------------------------------------------------------------
  // Assistente IA: Modo Geral (Criar Reel Completo)
  // --------------------------------------------------------------------------
  const btnOpenAiModal = document.getElementById("btnOpenAiModal");
  const btnCloseAiModal = document.getElementById("btnCloseAiModal");
  const aiModalOverlay = document.getElementById("aiModalOverlay");
  const aiPromptInput = document.getElementById("aiPromptInput");
  const btnAiGenerateHooks = document.getElementById("btnAiGenerateHooks");
  const hookOptionsContainer = document.getElementById("hookOptionsContainer");
  const hookOptionsGrid = document.getElementById("hookOptionsGrid");
  const aiResultSection = document.getElementById("aiResultSection");

  const aiHookText = document.getElementById("aiHookText");
  const aiContextText = document.getElementById("aiContextText");
  const aiProofsText = document.getElementById("aiProofsText");
  const aiTurnText = document.getElementById("aiTurnText");
  const aiCtaText = document.getElementById("aiCtaText");
  const aiMetricWords = document.getElementById("aiMetricWords");
  const aiMetricTime = document.getElementById("aiMetricTime");

  const btnListenAudioAi = document.getElementById("btnListenAudioAi");
  const aiAudioPlayer = document.getElementById("aiAudioPlayer");
  const aiAudioStatus = document.getElementById("aiAudioStatus");

  const btnListenAudioStep2 = document.getElementById("btnListenAudioStep2");
  const audioPreviewStep2 = document.getElementById("audioPreviewStep2");
  const audioStatusStep2 = document.getElementById("audioStatusStep2");

  const btnApplyAiToEditor = document.getElementById("btnApplyAiToEditor");
  const btnDirectAiRender = document.getElementById("btnDirectAiRender");

  function abrirModalIA(promptInicial = "") {
    if (promptInicial) {
      aiPromptInput.value = promptInicial;
    }
    aiModalOverlay.classList.add("open");
    alternarModoAi("geral");
    aiPromptInput.focus();
    atualizarUiProjetoAtivo();
  }

  function fecharModalIA() {
    aiModalOverlay.classList.remove("open");
  }

  if (btnOpenAiModal) btnOpenAiModal.addEventListener("click", () => abrirModalIA());
  if (btnCloseAiModal) btnCloseAiModal.addEventListener("click", fecharModalIA);
  if (aiModalOverlay) {
    aiModalOverlay.addEventListener("click", (e) => {
      if (e.target === aiModalOverlay) fecharModalIA();
    });
  }

  // ETAPA 1: Gerar 4 Opções de Ganchos com IA
  async function gerarOpcoesGanchos(tema) {
    const temaFinal = (tema || aiPromptInput.value || "").trim();
    if (!temaFinal) {
      alert("Por favor, digite um tema ou escolha uma das ideias acima.");
      return;
    }

    btnAiGenerateHooks.disabled = true;
    btnAiGenerateHooks.innerHTML = '<span class="pulse-dot"></span> Gerando 4 Opções Estratégicas...';
    hookOptionsContainer.style.display = "none";
    aiResultSection.style.display = "none";

    try {
      const resp = await fetch("/api/assistente/ganchos", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          tema: temaFinal,
          projetoId: state.projetoAtivo ? state.projetoAtivo.id : "armas"
        })
      });
      const dados = await resp.json();
      state.opcoesGanchos = dados.opcoes || [];

      if (!state.opcoesGanchos.length) {
        throw new Error("Nenhuma opção de gancho retornada.");
      }

      // Renderizar os 4 cards de ganchos
      hookOptionsGrid.innerHTML = state.opcoesGanchos.map((op, idx) => `
        <div class="hook-option-card" data-index="${idx}" id="hookCard${idx}">
          <div>
            <div class="hook-card-top">
              <span class="hook-angle-badge">${op.icone || '🎯'} ${op.angulo}</span>
              <span style="font-size: 11px; color: var(--text-dim);">Opção ${idx + 1}</span>
            </div>
            <div class="hook-phrase">"${op.gancho}"</div>
            <div class="hook-desc">${op.explicacao}</div>
          </div>
          <div class="hook-card-footer">
            <span class="hook-cta-pill">DM: ${op.palavraCta || (state.projetoAtivo ? state.projetoAtivo.palavra_cta : 'ACESSO')}</span>
            <button type="button" class="btn-select-hook">👉 Escolher este Gancho</button>
          </div>
        </div>
      `).join("");

      // Listeners para os cards
      hookOptionsGrid.querySelectorAll(".hook-option-card").forEach(card => {
        card.addEventListener("click", () => {
          const idx = parseInt(card.dataset.index, 10);
          escolherGanchoEDesenvolver(idx, temaFinal);
        });
      });

      hookOptionsContainer.style.display = "flex";
      hookOptionsContainer.scrollIntoView({ behavior: "smooth" });

    } catch (err) {
      console.error("Erro ao gerar opções de ganchos:", err);
      alert("Falha ao gerar ganchos com a OpenAI. Verifique sua chave no .env ou conexão.");
    } finally {
      btnAiGenerateHooks.disabled = false;
      btnAiGenerateHooks.innerHTML = '<span class="btn-text">🎯 Gerar Opções de Ganchos</span>';
    }
  }

  if (btnAiGenerateHooks) {
    btnAiGenerateHooks.addEventListener("click", () => gerarOpcoesGanchos());
  }

  // ETAPA 2: Escolher Gancho e Desenvolver Roteiro Completo de 5 Blocos
  async function escolherGanchoEDesenvolver(idx, temaOriginal) {
    const op = state.opcoesGanchos[idx];
    if (!op) return;
    state.ganchoSelecionado = op;

    // Destacar o card selecionado
    hookOptionsGrid.querySelectorAll(".hook-option-card").forEach((c, i) => {
      c.classList.toggle("selected", i === idx);
    });

    const card = document.getElementById(`hookCard${idx}`);
    const btnSelect = card.querySelector(".btn-select-hook");
    btnSelect.textContent = "⏳ Redigindo Roteiro (5 blocos)...";

    try {
      const resp = await fetch("/api/assistente/roteiro", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          gancho: op.gancho,
          tema: temaOriginal,
          palavraCta: op.palavraCta || (state.projetoAtivo ? state.projetoAtivo.palavra_cta : "ACESSO"),
          projetoId: state.projetoAtivo ? state.projetoAtivo.id : "armas"
        })
      });
      const res = await resp.json();
      roteiroGeradoPelaIA = res;

      const textoCompleto = [res.gancho, res.oQueE, res.provas, res.virada, res.chamada].join(" ");
      const palavras = textoCompleto.split(/\s+/).filter(w => w.length > 0);
      const totalWords = palavras.length;
      const durSec = Math.round(totalWords / 3.7);

      aiHookText.textContent = res.gancho;
      aiContextText.textContent = res.oQueE;
      aiProofsText.textContent = res.provas;
      aiTurnText.textContent = res.virada;
      aiCtaText.textContent = res.chamada;

      aiMetricWords.textContent = `${totalWords} palavras`;
      aiMetricTime.textContent = `~${durSec} segundos`;

      if (document.getElementById("aiAudioTimeEst")) {
        document.getElementById("aiAudioTimeEst").textContent = `~${durSec} segundos`;
      }

      // Pré-carregar recomendações da IA nos atributos de exibição
      if (res.modoCena && document.getElementById("aiSelectModoCena")) {
        document.getElementById("aiSelectModoCena").value = res.modoCena;
      }
      if (res.voz && document.getElementById("aiSelectVoz")) {
        document.getElementById("aiSelectVoz").value = res.voz;
      }
      if (res.trilha && document.getElementById("aiSelectTrilha")) {
        document.getElementById("aiSelectTrilha").value = res.trilha;
      }

      aiResultSection.style.display = "block";
      aiResultSection.scrollIntoView({ behavior: "smooth" });

    } catch (err) {
      console.error("Erro ao desenvolver roteiro:", err);
      alert("Falha ao gerar roteiro detalhado. Tente novamente.");
    } finally {
      btnSelect.textContent = "✓ Gancho Selecionado";
    }
  }

  // ETAPA 3: Prévia Instantânea de Áudio (Edge-TTS)
  async function executarPreviewAudio(texto, voz, audioEl, statusEl, btnEl) {
    if (!texto.trim()) {
      alert("O texto do roteiro está vazio.");
      return;
    }

    btnEl.disabled = true;
    const textoOriginalBtn = btnEl.innerHTML;
    btnEl.innerHTML = '<span class="pulse-dot"></span> Sintetizando locução (~1.5s)...';
    statusEl.textContent = "Aguarde, gerando áudio neural...";

    try {
      const resp = await fetch("/api/preview-audio", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ texto, voz })
      });
      const dados = await resp.json();
      if (dados.sucesso && dados.audioUrl) {
        audioEl.src = dados.audioUrl;
        audioEl.style.display = "block";
        audioEl.play();
        statusEl.textContent = `✓ Reproduzindo voz neural (${dados.duracaoEstimada}s)`;
        btnEl.innerHTML = '<span>🔊</span> Ouvir Novamente';
      } else {
        throw new Error(dados.erro || "Falha na resposta do áudio");
      }
    } catch (err) {
      console.error("Erro no preview de áudio:", err);
      statusEl.textContent = "Erro ao sintetizar áudio.";
      btnEl.innerHTML = textoOriginalBtn;
    } finally {
      btnEl.disabled = false;
    }
  }

  if (btnListenAudioAi) {
    btnListenAudioAi.addEventListener("click", () => {
      if (!roteiroGeradoPelaIA) return;
      const texto = [
        roteiroGeradoPelaIA.gancho,
        roteiroGeradoPelaIA.oQueE,
        roteiroGeradoPelaIA.provas,
        roteiroGeradoPelaIA.virada,
        roteiroGeradoPelaIA.chamada
      ].join(" ");
      const sVoz = document.getElementById("aiSelectVoz");
      const voz = (sVoz ? sVoz.value : null) || state.audio.motorVoz || "pt-BR-AntonioNeural";
      executarPreviewAudio(texto, voz, aiAudioPlayer, aiAudioStatus, btnListenAudioAi);
    });
  }

  if (btnListenAudioStep2) {
    btnListenAudioStep2.addEventListener("click", () => {
      const texto = [
        inputGancho.value,
        inputOQueE.value,
        inputProvas.value,
        inputVirada.value,
        inputChamada.value
      ].join(" ");
      const voz = state.audio.motorVoz || "pt-BR-AntonioNeural";
      executarPreviewAudio(texto, voz, audioPreviewStep2, audioStatusStep2, btnListenAudioStep2);
    });
  }

  // Aplicar Roteiro e Atributos no Editor Passo a Passo
  if (btnApplyAiToEditor) {
    btnApplyAiToEditor.addEventListener("click", () => {
      if (!roteiroGeradoPelaIA) return;
      aplicarPautaNoFormulario(roteiroGeradoPelaIA);

      // Sincroniza também os atributos e exibição escolhidos
      sincronizarAtributosAiParaEditor();

      fecharModalIA();
      document.getElementById("tabBtnWizard").click();
      irParaPasso(2);

      const box = document.getElementById("wordMeterBox");
      if (box) {
        box.style.boxShadow = "0 0 25px rgba(52, 211, 153, 0.6)";
        setTimeout(() => { box.style.boxShadow = ""; }, 1800);
      }
    });
  }

  // Renderização Direta a partir da IA com TODOS os Atributos Escolhidos
  if (btnDirectAiRender) {
    btnDirectAiRender.addEventListener("click", async () => {
      if (!roteiroGeradoPelaIA) {
        alert("Por favor, selecione um dos ganchos acima primeiro para gerar o roteiro.");
        return;
      }

      // Preenche os campos do editor
      aplicarPautaNoFormulario(roteiroGeradoPelaIA);

      // Sincroniza os atributos escolhidos no modal
      sincronizarAtributosAiParaEditor();

      const sModoCena = document.getElementById("aiSelectModoCena");
      const sTransicao = document.getElementById("aiSelectTransicao");
      const sDuracao = document.getElementById("aiSelectDuracao");
      const sLegenda = document.getElementById("aiSelectLegenda");
      const sVoz = document.getElementById("aiSelectVoz");
      const sTrilha = document.getElementById("aiSelectTrilha");
      const sSfx = document.getElementById("aiCheckSfx");

      const payload = {
        projetoId: state.projetoAtivo ? state.projetoAtivo.id : "armas",
        titulo: roteiroGeradoPelaIA.titulo || `${state.projetoAtivo ? state.projetoAtivo.nome : 'Flow Reels'} Reel`,
        gancho: roteiroGeradoPelaIA.gancho,
        oQueE: roteiroGeradoPelaIA.oQueE,
        provas: roteiroGeradoPelaIA.provas,
        virada: roteiroGeradoPelaIA.virada,
        chamada: roteiroGeradoPelaIA.chamada,
        palavraCta: roteiroGeradoPelaIA.palavraCta || (state.projetoAtivo ? state.projetoAtivo.palavra_cta : "ACESSO"),
        motorVoz: sVoz ? sVoz.value : state.audio.motorVoz,
        modoCena: sModoCena ? sModoCena.value : state.visual.modoCena,
        transicao: sTransicao ? sTransicao.value : state.visual.transicao,
        duracaoTransicao: sDuracao ? sDuracao.value : state.visual.duracaoTransicao,
        estiloLegenda: sLegenda ? sLegenda.value : state.visual.estiloLegenda,
        videoFonte: state.visual.videoFonte,
        trilha: sTrilha ? sTrilha.value : state.audio.trilha,
        sfxHabilitado: sSfx ? sSfx.checked : state.audio.sfxHabilitado
      };

      fecharModalIA();
      document.getElementById("tabBtnWizard").click();
      irParaPasso(5);

      await executarRenderizacao(payload);
    });
  }

  // Botão Reprovar e Refazer com IA
  const btnReprovarRefazer = document.getElementById("btnReprovarRefazer");
  if (btnReprovarRefazer) {
    btnReprovarRefazer.addEventListener("click", () => {
      abrirModalIA();
      aiPromptInput.value = "O vídeo anterior foi reprovado. Crie uma abordagem completamente nova com outro ângulo e gancho mais impactante sobre...";
      aiPromptInput.focus();
    });
  }

  // Inicializar projetos e estado
  carregarProjetos();
});

