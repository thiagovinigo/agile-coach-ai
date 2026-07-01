# Lean Inception (Case Prático do Início ao Fim)

Criada por Paulo Caroli, a **Lean Inception** é um workshop focado em alinhar stakeholders sobre o *Produto Mínimo Viável (MVP)*. 

Para sair da teoria, vamos simular uma Lean Inception do início ao fim com um case real: **"Criar um App de Saúde para Agendamento de Consultas Rápido"**. 

---

<div class="card orange">
    <div class="card-title">⚠️ Preparação e Anti-Padrões</div>
    <div class="card-desc">
        <ul>
            <li><strong>Erro Comum:</strong> Começar sem ter o problema bem definido pela Diretoria.</li>
            <li><strong>O Facilitador (Você):</strong> Precisa garantir que a sala tenha as três esferas: Negócios (Sponsors/Diretores), UX (Designers) e Tecnologia (Tech Leads).</li>
            <li><strong>Duração:</strong> 5 dias focados (geralmente manhãs).</li>
        </ul>
    </div>
</div>

---

## 📅 Dia 1: O Que Estamos Fazendo Aqui?

### 1. Visão do Produto
O objetivo é alinhar todos em uma única frase.

<div class="info-box">
  <strong>🔥 Dinâmica na Prática (App de Saúde):</strong><br>
  O facilitador pede para o grupo preencher o template de "Elevator Pitch".<br><br>
  <em>"Para pacientes sem plano (Público), o HealthApp (Produto) é um aplicativo móvel (Categoria) que conecta rapidamente pacientes a médicos disponíveis em até 2 horas (Benefício principal). Diferente de ligar para clínicas (Concorrente), nosso produto faz o pagamento e agendamento instantâneo via Pix (Diferencial)."</em>
</div>

### 2. O Produto É / Não É / Faz / Não Faz
A dinâmica mais importante para cortar o delírio corporativo.

<div class="info-box">
  <strong>🗣️ Diálogo Tenso Simulado:</strong><br>
  <strong>Sponsor:</strong> "Ah, e nós podíamos vender telemedicina pelo app!"<br>
  <strong>Facilitador:</strong> "Boa ideia. Mas para esse MVP inicial, nós faremos isso? Coloquem os post-its."<br><br>
  <strong>Resultado do Board:</strong><br>
  ✅ <strong>É:</strong> Um conector rápido, Simples, Focado em Clínico Geral.<br>
  ❌ <strong>Não É:</strong> Um plano de saúde, Um substituto para emergências graves.<br>
  ✅ <strong>Faz:</strong> Agendamento instantâneo, Pagamento via Pix.<br>
  ❌ <strong>Não Faz:</strong> Telemedicina (Fica para v2!), Gestão de prontuário eletrônico.
</div>

---

## 📅 Dia 2: Para Quem Estamos Construindo?

### 1. Personas
Criar empatia com o usuário.

<div class="info-box">
  <strong>👤 Persona: "Maria Apressada"</strong><br>
  - Mãe, 35 anos, autônoma sem plano de saúde.<br>
  - <strong>Dor:</strong> Quando o filho fica doente, perde 3 horas ligando para clínicas tentando achar vaga hoje.<br>
  - <strong>Necessidade:</strong> "Quero ver quem tem vaga às 14h perto de mim e pagar na hora".
</div>

### 2. Jornada do Usuário
Mapear o fluxo da Maria desde a dor até o sucesso.

<div class="info-box">
  <strong>🗺️ A Jornada da Maria:</strong><br>
  1. O filho acorda com febre alta.<br>
  2. Maria pega o celular desesperada.<br>
  3. Ela abre o aplicativo HealthApp.<br>
  4. Ela filtra por "Pediatria hoje".<br>
  5. Ela vê uma clínica a 2km com vaga às 14h.<br>
  6. Ela agenda e paga o Pix.<br>
  7. Ela leva o filho ao médico.
</div>

---

## 📅 Dia 3: Brainstorming de Funcionalidades

### 1. Ideação
Cruzando a Jornada com as Dores. "O que podemos construir para ajudar a Maria no passo 4 e 5?"

<div class="info-box">
  <strong>🧠 Lista Bruta de Features (Ideias da sala):</strong><br>
  - Login via Google<br>
  - Filtro por geolocalização (GPS)<br>
  - Filtro por especialidade<br>
  - Avaliação de médicos por estrelas (Review)<br>
  - Integração com API do Banco Central (Pix)
</div>

### 2. Revisão Técnica e de Negócio (Gráfico de Semáforo)
O momento em que os devs dizem a verdade e os sponsors decidem o valor.

<div class="card dark">
    <div class="card-title">🚥 Tabela de Classificação</div>
    <div class="card-desc">
        <ul>
            <li><strong>Integração PIX:</strong> Valor Negócio Alto ($$$) | Esforço Dev Alto (🔴) | Confiança Alta</li>
            <li><strong>Login via Google:</strong> Valor Negócio Médio ($$) | Esforço Dev Baixo (🟢) | Confiança Alta</li>
            <li><strong>Avaliação de Médicos (Estrelas):</strong> Valor Negócio Baixo ($) | Esforço Dev Médio (🟡) | Confiança Baixa (ninguém sabe como evitar reviews falsos).</li>
        </ul>
    </div>
</div>

---

## 📅 Dia 4: O Sequenciador (A Batalha Final)

Esta é a alma da Lean Inception. As funcionalidades do Dia 3 são jogadas em um Board com "Ondas". A Regra: Cada onda suporta no máximo 3 "cartões" de Esforço, e não pode ter mais de 1 cartão vermelho por onda.

<div class="info-box">
  <strong>🌊 A Batalha:</strong><br>
  <strong>Sponsor:</strong> "Precisamos das Estrelas (Avaliações) na Onda 1 para passar confiança!"<br>
  <strong>Tech Lead:</strong> "A Integração PIX já é um cartão Vermelho. Se colocarmos as Avaliações (Amarelo) na mesma onda, estouramos o limite de esforço do time. O MVP nunca vai sair."<br>
  <strong>Facilitador:</strong> "Sem PIX a gente não ganha dinheiro. Sem estrelas a gente funciona. O que vai para a Onda 1?"<br>
  <strong>Decisão:</strong> A Onda 1 (MVP) terá: Login Google (Verde), Filtro Simples (Amarelo) e Integração PIX (Vermelho).
</div>

---

## 📅 Dia 5: O Canvas MVP

Sintetizar tudo em um poster de 1 página.

<div class="card">
    <div class="card-title">🏆 Canvas MVP: HealthApp v1</div>
    <div class="card-desc">
        <ul>
            <li><strong>Proposta MVP:</strong> Validar se mães sem plano de saúde usariam um app para achar pediatras no mesmo dia pagando antecipado.</li>
            <li><strong>Funcionalidades (Onda 1):</strong> Login Simples, Filtro por Bairro/Especialidade, Checkout PIX.</li>
            <li><strong>O que NÃO entra agora:</strong> Avaliações, Telemedicina, Chat com o médico.</li>
            <li><strong>Custo & Cronograma:</strong> 3 Desenvolvedores, 1 Mês.</li>
            <li><strong>Métrica de Sucesso (O que valida o negócio):</strong> 100 agendamentos pagos na primeira semana do piloto no bairro XYZ.</li>
        </ul>
    </div>
</div>

<div class="card orange">
    <div class="card-title">➡️ Próximo Passo Crítico</div>
    <div class="card-desc">
        O Canvas MVP está pronto. Todos saem felizes. Mas como isso vira tarefa no Jira para os desenvolvedores trabalharem amanhã?
        A resposta é o <strong>Product Backlog Building (PBB)</strong>. (Veja a próxima aba).
    </div>
</div>
