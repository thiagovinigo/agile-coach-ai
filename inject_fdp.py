# Script to inject FDP and Enablers content

import re

new_content = """
  <!-- O Trabalho FDP do PO -->
  <div style="background:linear-gradient(135deg, #fcd34d, #fbbf24); border-radius:12px; padding:24px; margin:24px 0; box-shadow:0 4px 6px rgba(0,0,0,0.05);">
    <h3 style="margin:0 0 16px; color:#92400e; font-size:24px; display:flex; align-items:center; gap:10px;">
      <span>🧠</span> O Trabalho "FDP" do PO
    </h3>
    <p style="font-size:15px; color:#78350f; margin-bottom:20px; line-height:1.6;">
      Para dominar o fluxo de valor, o PO tem três verbos de ação principais — o acrônimo <strong>F.D.P.</strong>:
    </p>
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:16px;">
      <div style="background:#fff; border-radius:8px; padding:16px; border-top:4px solid #b45309;">
        <div style="font-weight:900; font-size:18px; color:#b45309; margin-bottom:8px;">🔪 Fatiar</div>
        <p style="font-size:13px; color:#451a03; margin:0;">Quebrar itens grandes (Épicos/Features) em Histórias pequenas e entregáveis. O segredo do fluxo contínuo.</p>
      </div>
      <div style="background:#fff; border-radius:8px; padding:16px; border-top:4px solid #dc2626;">
        <div style="font-weight:900; font-size:18px; color:#dc2626; margin-bottom:8px;">🗑️ Descartar</div>
        <p style="font-size:13px; color:#451a03; margin:0;">Dizer "NÃO". Eliminar ideias que não geram valor ou que custam mais do que o benefício. Maximize o trabalho não feito.</p>
      </div>
      <div style="background:#fff; border-radius:8px; padding:16px; border-top:4px solid #047857;">
        <div style="font-weight:900; font-size:18px; color:#047857; margin-bottom:8px;">⭐ Priorizar</div>
        <p style="font-size:13px; color:#451a03; margin:0;">Ordenar o que sobrou pelo maior valor de negócio vs esforço/risco. Fazer a coisa certa na hora certa.</p>
      </div>
    </div>
  </div>

  <!-- A Analogia do Bolo -->
  <h3 style="margin:24px 0 12px;">🍰 A Analogia Geral: Fatiando o Bolo</h3>
  <div style="display:grid; grid-template-columns:1fr auto 1fr; gap:20px; align-items:center; margin-bottom:24px;">
    <div style="background:#fef2f2; border:2px solid #fca5a5; border-radius:8px; padding:16px;">
      <div style="color:#dc2626; font-weight:800; margin-bottom:8px;">❌ Fatia Horizontal (Errado)</div>
      <p style="font-size:13px; margin:0; color:#7f1d1d;">
        Imagine comer apenas a cobertura. Depois, apenas a massa. Depois, apenas o recheio. Não é a experiência de comer um bolo. Na TI, isso é entregar só Banco de Dados, depois só API, depois só Tela. O cliente não vê valor em nada disso sozinho.
      </p>
    </div>
    <div style="font-size:24px; color:#94a3b8;">VS</div>
    <div style="background:#f0fdf4; border:2px solid #86efac; border-radius:8px; padding:16px;">
      <div style="color:#16a34a; font-weight:800; margin-bottom:8px;">✅ Fatia Vertical (Certo)</div>
      <p style="font-size:13px; margin:0; color:#14532d;">
        Você corta uma fatia de cima a baixo. Em uma única mordida, o cliente experimenta a cobertura, a massa e o recheio. Na TI, é uma funcionalidade que atravessa Banco, API e Tela, mas faz UMA coisa ponta-a-ponta (ex: Login básico).
      </p>
    </div>
  </div>

  <!-- Enablers -->
  <h3 style="margin:24px 0 12px;">⚙️ Enablers: O Trabalho Oculto que o PO Precisa Gerenciar</h3>
  <div style="background:#f8fafc; border-left:4px solid #3b82f6; padding:16px; border-radius:0 8px 8px 0; margin-bottom:24px;">
    <p style="font-size:14px; margin-top:0;">Além de <em>User Stories</em> (que agregam valor direto ao usuário), o backlog também precisa comportar <strong>Enablers</strong>. Enablers são itens de trabalho necessários para dar suporte a futuras funcionalidades de negócio, infraestrutura ou qualidade. Sem eles, as User Stories não sobrevivem.</p>
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:12px;">
      <div style="background:#eff6ff; padding:12px; border-radius:6px; font-size:13px;">
        <strong style="color:#1d4ed8;">🔍 Exploração (Spikes)</strong><br>
        Pesquisas, provas de conceito e descoberta para entender como construir algo.
      </div>
      <div style="background:#eff6ff; padding:12px; border-radius:6px; font-size:13px;">
        <strong style="color:#1d4ed8;">🏗️ Arquitetural</strong><br>
        Mudanças estruturais, refatorações pesadas e preparação de arquitetura.
      </div>
      <div style="background:#eff6ff; padding:12px; border-radius:6px; font-size:13px;">
        <strong style="color:#1d4ed8;">☁️ Infraestrutura</strong><br>
        Pipelines CI/CD, configuração de servidores, automação de ambientes.
      </div>
      <div style="background:#eff6ff; padding:12px; border-radius:6px; font-size:13px;">
        <strong style="color:#1d4ed8;">🛡️ Conformidade (Compliance)</strong><br>
        LGPD, auditorias de segurança, padrões regulatórios exigidos.
      </div>
    </div>
  </div>

  <!-- Exemplos Visuais de Quebra -->
  <h3 style="margin:24px 0 12px;">🧩 Exemplos Práticos de Ramificação (O Que vs Como)</h3>
  <p style="font-size:14px; margin-bottom:16px;">Sempre parta do <strong>O QUE</strong> (Problema/Épico) até chegar no <strong>COMO</strong> (Critérios de Aceite). Veja as formas comuns de quebrar um Épico de "Cadastro":</p>
  
  <div style="display:grid; gap:16px; margin-bottom:24px;">
    
    <!-- CRUD -->
    <div style="border:1px solid #e2e8f0; border-radius:8px; padding:16px;">
      <h4 style="margin:0 0 12px; color:#0f172a; font-size:15px;">1️⃣ Fatiamento por Operação (CRUD)</h4>
      <div style="background:#f8fafc; padding:12px; border-radius:6px; font-size:13px; color:#475569;">
        <strong>Épico:</strong> Gestão de Usuários<br>
        <strong>↘ Features:</strong> Cadastro de Filmes, Cadastro de Usuários, Cadastro de Séries<br>
        <strong>&nbsp;&nbsp;↘ Histórias (Usuários):</strong><br>
        &nbsp;&nbsp;&nbsp;&nbsp;• <em>Cadastrar</em> Usuário (Create)<br>
        &nbsp;&nbsp;&nbsp;&nbsp;• <em>Visualizar</em> Usuário (Read)<br>
        &nbsp;&nbsp;&nbsp;&nbsp;• <em>Atualizar</em> Usuário (Update)<br>
        &nbsp;&nbsp;&nbsp;&nbsp;• <em>Excluir</em> Usuário (Delete)
      </div>
    </div>

    <!-- Fluxo -->
    <div style="border:1px solid #e2e8f0; border-radius:8px; padding:16px;">
      <h4 style="margin:0 0 12px; color:#0f172a; font-size:15px;">2️⃣ Fatiamento por Fluxo de Trabalho (Filtros/Pesquisa)</h4>
      <div style="background:#f8fafc; padding:12px; border-radius:6px; font-size:13px; color:#475569;">
        <strong>Épico:</strong> Relatório de Clientes<br>
        <strong>↘ Histórias (por variação do fluxo de busca):</strong><br>
        &nbsp;&nbsp;&nbsp;&nbsp;• Filtrar usuário por <em>Nome</em><br>
        &nbsp;&nbsp;&nbsp;&nbsp;• Filtrar usuário por <em>CPF</em>
      </div>
    </div>

    <!-- Papel -->
    <div style="border:1px solid #e2e8f0; border-radius:8px; padding:16px;">
      <h4 style="margin:0 0 12px; color:#0f172a; font-size:15px;">3️⃣ Fatiamento por Papel (Persona)</h4>
      <div style="background:#f8fafc; padding:12px; border-radius:6px; font-size:13px; color:#475569;">
        <strong>Épico:</strong> Módulo de Assinatura<br>
        <strong>↘ Histórias (separadas por quem executa):</strong><br>
        &nbsp;&nbsp;&nbsp;&nbsp;• Cadastrar usuário <em>Pagante</em> (Cliente)<br>
        &nbsp;&nbsp;&nbsp;&nbsp;• Cadastrar usuário <em>Visitante</em> (Free)
      </div>
    </div>

    <!-- Regra de Negócio -->
    <div style="border:1px solid #e2e8f0; border-radius:8px; padding:16px;">
      <h4 style="margin:0 0 12px; color:#0f172a; font-size:15px;">4️⃣ Fatiamento por Regra de Negócio (O mais avançado)</h4>
      <div style="background:#f8fafc; padding:12px; border-radius:6px; font-size:13px; color:#475569;">
        <strong>Épico:</strong> Pagamento<br>
        <strong>↘ Feature:</strong> Pagamento por cartão de crédito<br>
        <strong>&nbsp;&nbsp;↘ Histórias (adicionando regras incrementais):</strong><br>
        &nbsp;&nbsp;&nbsp;&nbsp;• Realizar pagamento com cartão (Qualquer bandeira)<br>
        &nbsp;&nbsp;&nbsp;&nbsp;• <em>Restrição:</em> Realizar pagamento apenas com cartão VISA<br>
        &nbsp;&nbsp;&nbsp;&nbsp;• <em>Restrição:</em> Realizar pagamento apenas com cartão MASTER<br>
        &nbsp;&nbsp;&nbsp;&nbsp;• <em>Condição:</em> Realizar pagamento com cartão MASTER (apenas à vista)
      </div>
    </div>

  </div>
"""

with open('contexto/scrumban_guia.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Locate the beginning of s-po-quebrando to insert near the top (after the header intro)
idx = text.find('id="s-po-quebrando"')

if idx != -1:
    # Find the end of the header card
    insert_pos = text.find('</div>', text.find('<div class="card orange"', idx)) + 6
    
    modified_text = text[:insert_pos] + new_content + text[insert_pos:]
    
    with open('contexto/scrumban_guia.html', 'w', encoding='utf-8') as f:
        f.write(modified_text)
    print("Content successfully injected!")
else:
    print("Could not find section s-po-quebrando")

