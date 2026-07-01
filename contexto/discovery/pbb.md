# Product Backlog Building (PBB)

Criado por Fábio Aguiar, o **Product Backlog Building (PBB)** é o "elo perdido" entre a Discovery (Lean Inception) e o Delivery (Scrum/Kanban). 

Muitas empresas terminam uma Lean Inception com um *Canvas MVP* lindo, e no dia seguinte os desenvolvedores abrem o Jira e se perguntam: *"Tá, mas o que eu codifico primeiro?"* O PBB resolve isso fatiando a visão em Histórias de Usuário prontas para o desenvolvimento.

---

## 🏗️ Como Funciona o PBB?

O PBB usa uma estrutura em funil: **Canvas MVP ➡️ Personas ➡️ PBIs (Product Backlog Items) ➡️ User Stories.**

Vamos continuar o **Case do App de Saúde** definido na Lean Inception.

<div class="card dark">
    <div class="card-title">1️⃣ Passo: Entendendo o Contexto e Personas</div>
    <div class="card-desc">
        A equipe traz o resultado da Lean Inception.<br>
        <strong>Persona escolhida:</strong> Maria Apressada.<br>
        <strong>Problema do MVP:</strong> Encontrar pediatra rápido e pagar pelo app.
    </div>
</div>

<div class="card dark">
    <div class="card-title">2️⃣ Passo: Mapeamento de Funcionalidades (Features)</div>
    <div class="card-desc">
        Pegamos a funcionalidade da Onda 1 da Lean Inception: <em>"Checkout PIX"</em>. Essa funcionalidade ainda é muito grande para um desenvolvedor puxar. Precisamos detalhar.
    </div>
</div>

<div class="card orange">
    <div class="card-title">3️⃣ Passo: Criação de Passos (Steps) e PBIs (Fatiamento)</div>
    <div class="card-desc">
        <p>O que a Maria precisa fazer <strong>passo a passo</strong> para realizar o Checkout PIX? Para cada passo, criamos um PBI (Item do Backlog):</p>
        <ul>
            <li><strong>Passo 1 (Acessar pagamento):</strong> PBI - Exibir tela de resumo da consulta.</li>
            <li><strong>Passo 2 (Gerar código):</strong> PBI - Gerar QR Code Copia e Cola do PIX via API do Banco.</li>
            <li><strong>Passo 3 (Confirmar):</strong> PBI - Ouvir webhook do Banco para confirmar pagamento e liberar consulta.</li>
        </ul>
    </div>
</div>

<div class="card">
    <div class="card-title">4️⃣ Passo: Escrevendo as User Stories e BDD</div>
    <div class="card-desc">
        <p>Agora transformamos os PBIs em histórias prontas para o Jira, usando a taxonomia clássica e critérios de aceite (BDD - Given/When/Then).</p>
        <p><strong>Exemplo para o PBI do Passo 2:</strong></p>
        <p><em>"<strong>COMO</strong> Maria Apressada<br>
        <strong>QUERO</strong> visualizar um QR Code PIX e um código Copia-e-Cola<br>
        <strong>PARA QUE</strong> eu possa pagar a consulta imediatamente no meu app do banco."</em></p>
        
        <p><strong>Critérios de Aceite (BDD):</strong></p>
        <p><em><strong>DADO QUE</strong> a Maria clicou em "Pagar com PIX"<br>
        <strong>QUANDO</strong> a API do banco retornar sucesso<br>
        <strong>ENTÃO</strong> a tela deve exibir o QR Code em alta resolução com validade de 5 minutos.</em></p>
    </div>
</div>

---

<div class="info-box">
  <strong>💡 O Grande Valor do PBB:</strong><br>
  No fim de 1 ou 2 dias de PBB, o seu Tech Lead e seus desenvolvedores não têm mais dúvidas. O "Canvas MVP" abstrato se transformou em uma lista sequencial de tarefas granulares (User Stories) prontas para entrarem na próxima Sprint Planning ou direto na coluna "To Do" do Kanban. 
  <br><br>
  <strong>A ponte entre o Discovery e o Delivery está construída!</strong>
</div>
