import os
import json
import httpx
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import StreamingResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Verifica se o Supabase tá configurado
if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    print("ERRO: As chaves do Supabase e OpenAI não foram configuradas no .env")

@app.get("/api/config")
def get_config():
    return JSONResponse({
        "SUPABASE_URL": SUPABASE_URL,
        "SUPABASE_ANON_KEY": SUPABASE_ANON_KEY
    })

async def verify_token(request: Request):
    auth_header = request.headers.get("Authorization")
    
    # Se SUPABASE_URL não estiver configurada no backend ou se for requisição pública de visitante
    if not SUPABASE_URL or "cole_sua_url" in SUPABASE_URL:
        return True

    if not auth_header or not auth_header.startswith("Bearer "):
        # Permitir requisições públicas de chat / demo sem bloquear com 401
        return True
    
    token = auth_header.split(" ")[1]
    
    # Bypass local se for dev ou guest
    if token in ["local_dev_token", "guest_token", "public_user", "anonymous"]:
        return True

    # Valida no Supabase via REST
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{SUPABASE_URL}/auth/v1/user",
                headers={"apikey": SUPABASE_ANON_KEY, "Authorization": f"Bearer {token}"},
                timeout=5.0
            )
            if resp.status_code == 200:
                return True
    except Exception:
        pass
    return True

def generate_expert_agent_reply(agent_title: str, system_prompt: str, user_message: str, agent_id: str = "") -> str:
    msg_lower = (user_message or "").lower()
    title_lower = (agent_title or "").lower()
    
    # 1. QA & Quality Champion
    if "qa" in title_lower or "quality" in title_lower or agent_id == "qa-quality-champion":
        if any(w in msg_lower for w in ["dod", "definition of done", "pronto"]):
            return (
                "🛡️ **Definition of Done (DoD) recomendada para Engenharia de Alta Performance:**\n\n"
                "Para garantir qualidade embutida (*Built-In Quality*) e evitar retrabalho na esteira, uma DoD robusta deve contemplar 4 dimensões essenciais:\n\n"
                "1. **Código & Boas Práticas:**\n"
                "   - Código revisado e aprovado via Pull Request por ao menos 1 engenheiro peer (sem auto-merge).\n"
                "   - Análise estática aprovada no SonarQube/Linter sem novos code smells ou vulnerabilidades críticas/bloqueantes.\n"
                "   - Nenhuma credencial ou secret exposta no versionamento.\n\n"
                "2. **Estratégia de Testes Automatizados:**\n"
                "   - **Testes Unitários:** Cobertura mínima de 80% nas regras de negócio com assertions determinísticas.\n"
                "   - **Testes de Integração:** Contratos de API validados e comunicação com DB/mensageria testada com mocks controlados (ex: Testcontainers).\n"
                "   - **Testes de Regressão:** Suite de regressão básica executada com 100% de sucesso no pipeline de CI.\n\n"
                "3. **Critérios de Aceite & Validação:**\n"
                "   - Todos os critérios de aceite (Gherkin Given/When/Then) validados em ambiente de Staging/Preview.\n"
                "   - Testes exploratórios rápidos conduzidos cobrindo edge cases e fluxos de erro.\n\n"
                "4. **Operação & Observabilidade:**\n"
                "   - Logs estruturados e métricas de telemetria (OpenTelemetry/Datadog) implementados para novos fluxos.\n"
                "   - Documentação de API OpenAPI/Swagger atualizada automaticamente.\n"
                "   - Deploy automatizado no ambiente alvo com plano de rollback documentado ou Feature Flag habilitável."
            )
        elif any(w in msg_lower for w in ["pirâmide", "piramide", "pyramid", "estratégia de teste"]):
            return (
                "🛡️ **Estratégia da Pirâmide de Testes (Test Pyramid):**\n\n"
                "A pirâmide clássica de Mike Cohn e Martin Fowler continua sendo a base para manter pipelines rápidos e confiáveis:\n\n"
                "1. **Base (70% - Testes Unitários):**\n"
                "   - **Foco:** Funções puras, classes de domínio, validadores e cálculos isolados.\n"
                "   - **Execução:** Milissegundos em memória. Devem rodar no pré-commit ou a cada compilação.\n"
                "   - **Custo de Manutenção:** Extremamente baixo.\n\n"
                "2. **Meio (20% - Testes de Integração / Contrato / Componente):**\n"
                "   - **Foco:** Validação de endpoints HTTP, consultas a repositórios, persistência no banco e filas.\n"
                "   - **Execução:** Segundos. Utilizar fixtures efêmeras (ex: SQLite em memória ou Testcontainers Docker).\n\n"
                "3. **Topo (10% - Testes E2E / Ponta a Ponta):**\n"
                "   - **Foco:** Happy paths críticos do usuário (ex: fluxo completo de checkout e login).\n"
                "   - **Atenção:** Evite o antipadrão da 'casquinha de sorvete' (*Ice Cream Cone*). E2E em excesso gera lentidão e testes instáveis (flaky)."
            )
        elif any(w in msg_lower for w in ["regressão", "regressao", "ci", "pipeline", "automação", "automacao"]):
            return (
                "🛡️ **Automação de Regressão Contínua no Pipeline de CI/CD:**\n\n"
                "Para rodar testes de regressão sem engargalar a esteira de entrega contínua:\n\n"
                "1. **Fatiamento da Suíte (Fast vs. Slow Test Suites):**\n"
                "   - **Smoke Tests / P0 (Críticos):** Rodam em todo Pull Request em menos de 5 minutos (unitários + fluxos vitais).\n"
                "   - **Full Regression (P1 e P2):** Executam em paralelo ou agendados após merge na branch principal (`main`) e na esteira noturna.\n\n"
                "2. **Paralelização & Test Sharding:**\n"
                "   - Divida os testes E2E/Playwright em múltiplos workers paralelos na GitHub Actions ou GitLab CI.\n\n"
                "3. **Zero Tolerância a Testes Flaky:**\n"
                "   - Teste instável deve ser imediatamente isolado (quarentena) para investigação, nunca ignorado com retry silencioso."
            )
        else:
            return (
                f"🛡️ **Recomendação do QA & Quality Champion:**\n\n"
                f"Analisando sua solicitação: *\"{user_message}\"*\n\n"
                "Para garantir qualidade sólida e previsibilidade técnica neste cenário, recomendo:\n\n"
                "1. **Shift-Left Testing:** Envolver QA desde a fase de refinamento da história, definindo cenários de teste antes de escrever código.\n"
                "2. **Critérios de Aceite Explícitos:** Mapear cenários de sucesso, bordas e falhas em formato BDD (*Given/When/Then*).\n"
                "3. **Definição de Pronto (DoD):** Garantir que nenhuma tarefa vá para produção sem testes automatizados correspondentes.\n"
                "4. **Observabilidade:** Monitorar taxa de erros, latência e logs após o deploy para fechar o ciclo de qualidade contínua."
            )
    
    # 2. Scrum Master Bot
    elif "scrum" in title_lower:
        return (
            f"🧙‍♂️ **Orientação do Scrum Master Bot:**\n\n"
            f"Sobre o seu ponto (*\"{user_message}\"*):\n\n"
            "1. **Foco no Objetivo da Sprint:** Lembre ao time que o compromisso principal é atingir a Sprint Goal acordada no Planning.\n"
            "2. **Transparência e Autonomia:** Trate problemas de comunicação criando acordos de trabalho explícitos (Working Agreements) e garantindo segurança psicológica.\n"
            "3. **Remoção de Bloqueios:** Identifique se o impedimento é interno do time ou dependência de terceiros, escalando com o PO e stakeholders com urgência."
        )

    # 3. Retrospective Facilitator
    elif "retro" in title_lower:
        return (
            f"👥 **Facilitação de Retrospectiva:**\n\n"
            f"Para a questão levantada (*\"{user_message}\"*), sugiro estruturar a sessão em 4 etapas objetivas:\n\n"
            "1. **Check-in / Abertura (5 min):** Quebra-gelo para verificar o nível de energia e segurança do time.\n"
            "2. **Coleta de Fatos (15 min):** Utilizar matriz visual (ex: DAKI: Drop, Add, Keep, Improve) para mapear aprendizados.\n"
            "3. **Agrupamento & Votação (10 min):** Identificar as 2 causas raízes mais votadas pelo time.\n"
            "4. **Plano de Ação SMART (15 min):** Criar no máximo 2 ações práticas com responsável definido e prazo para a próxima sprint."
        )

    # 4. Agile Coach Mentor
    elif "coach" in title_lower or "mentor" in title_lower:
        return (
            f"🧠 **Diretriz do Agile Coach Mentor:**\n\n"
            f"Análise estratégica para: *\"{user_message}\"*:\n\n"
            "1. **Evolução de Maturidade:** Não force frameworks prontos (Scrum, Kanban, SAFe); adapte os princípios à realidade do time e negócio.\n"
            "2. **Cultura de Feedback & Confiança:** A agilidade floresce onde há autonomia com responsabilidade e espaço para errar rápido e aprender.\n"
            "3. **Métricas de Valor vs. Esforço:** Troque discussões de horas gastas por foco em entrega contínua de valor de negócio e satisfação do cliente."
        )

    # 5. Flow Metrics AI / Kanban Flow Architect
    elif "flow" in title_lower or "kanban" in title_lower or "metric" in title_lower:
        return (
            f"📊 **Análise de Métricas de Fluxo (Flow Metrics):**\n\n"
            f"Em relação a: *\"{user_message}\"*:\n\n"
            "1. **Limite de WIP (Work In Progress):** *'Pare de começar e comece a terminar'*. Reduza o trabalho em progresso para diminuir o Lead Time.\n"
            "2. **Previsibilidade Empírica:** Utilize simulação de Monte Carlo com base no Throughput histórico para estimativas probabilísticas (ex: 85% de confiança).\n"
            "3. **Eficiência de Fluxo:** Meça o tempo em que o item esteve realmente sendo trabalhado versus o tempo em que ficou aguardando em filas."
        )

    # 6. Product Owner Copilot / OKR Strategy
    elif "po" in title_lower or "product" in title_lower or "okr" in title_lower:
        return (
            f"🧑‍💼 **Diretriz de Gestão de Produto:**\n\n"
            f"Respondendo a: *\"{user_message}\"*:\n\n"
            "1. **Fatiamento Vertical de Histórias:** Cada item deve entregar valor perceptível ao usuário (INVEST) de ponta a ponta.\n"
            "2. **Critérios de Aceite em Gherkin:** Estruture cenários claros: *Dado que [contexto], Quando [ação], Então [resultado esperado]*.\n"
            "3. **Priorização Orientada a Impacto:** Utilize RICE ou Cost of Delay para equilibrar esforço técnico contra impacto estratégico."
        )

    # 7. Tech Lead & Craft Advisor / Engenharia
    elif "tech" in title_lower or "lead" in title_lower or "architect" in title_lower or "engenharia" in title_lower:
        return (
            f"🛠️ **Orientação do Tech Lead & Craft Advisor:**\n\n"
            f"Análise técnica sobre: *\"{user_message}\"*:\n\n"
            "1. **Design Simples & Arquitetura Limpa:** Mantenha os limites de módulos claros (bounded contexts) e evite abstrações prematuras.\n"
            "2. **Trunk-Based Development:** Prefira branches curtas e merges diários com feature flags para evitar conflitos gigantes de integração.\n"
            "3. **Gestão Ativa do Débito Técnico:** Reserve tempo de engenharia contínuo para refatorações preventivas e atualização de dependências."
        )

    # 8. Cinematic Slides & 3D Director / Slides 3D / Sketchfab / Behance / DaFont
    elif (
        "slide" in title_lower 
        or "cinematic" in title_lower 
        or "3d" in title_lower 
        or agent_id == "cinematic-slides-director" 
        or any(k in msg_lower for k in ["sketchfab", "behance", "dafont", "slide 3d", "three.js", "apresentação 3d", "apresentacao 3d"])
    ):
        if any(w in msg_lower for w in ["sketchfab", "modelo", "glb", "gltf", "3d"]):
            return (
                "🪐 **Direção de Arte & Modelos 3D — Sketchfab.com Hub:**\n\n"
                "Para integrar modelos 3D nas suas apresentações com Three.js utilizando o **Sketchfab**:\n\n"
                "1. **Curadoria & Filtros no Sketchfab:**\n"
                "   - Acesse [sketchfab.com](https://sketchfab.com) e pesquise pelo tema (ex: *cyberpunk terminal*, *drone*, *server rack*, *spacecraft*).\n"
                "   - Marque o filtro **'Downloadable'** e selecione licenças compatíveis (ex: **CC Attribution**).\n"
                "   - Prefira arquivos nativos em formato **`.glb` / `.gltf`** (binários compactos com malha e texturas embutidas).\n\n"
                "2. **Pipeline de Carregamento WebGL (Three.js):**\n"
                "   ```javascript\n"
                "   import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';\n"
                "   const loader = new GLTFLoader();\n"
                "   loader.load('path/to/model.glb', (gltf) => {\n"
                "       const model = gltf.scene;\n"
                "       model.scale.set(1.5, 1.5, 1.5);\n"
                "       scene.add(model);\n"
                "   });\n"
                "   ```\n\n"
                "3. **Iluminação Cinematográfica (Three-Point Lighting):**\n"
                "   - **Key Light:** DirectionalLight quente (intensidade 2.5, ângulo de 45°).\n"
                "   - **Fill Light:** AmbientLight suave ou azulada (intensidade 0.6) para suavizar sombras profundas.\n"
                "   - **Rim/Back Light:** PointLight ciano ou magenta atrás do modelo para destacar as silhuetas em fundos escuros."
            )
        elif any(w in msg_lower for w in ["behance", "pitch deck", "arte", "layout", "visual", "grid"]):
            return (
                "🎨 **Direção de Arte & Layouts Editoriais — Behance.net Inspo:**\n\n"
                "Para criar apresentações no nível dos maiores estúdios globais de design:\n\n"
                "1. **Curadoria Estratégica no Behance:**\n"
                "   - Acesse [behance.net](https://www.behance.net) e filtre por campos criativos: *'Motion Graphics'*, *'Branding'*, *'Interaction Design'* e termos como *'Pitch Deck Design'* e *'Kinetic Typography'*.\n"
                "   - Crie um Moodboard de referências com: (a) Grid assimétrico, (b) Hierarquia de contraste 60-30-10, (c) Tratamento monocromático com acento neon.\n\n"
                "2. **Regras de Ouro de Apresentações Cinematográficas:**\n"
                "   - **Máximo 3 Cores Ativas:** Fundo escuro profundo (`#050811`), texto neutro (`#f8fafc`) e uma cor de ênfase dramática (`#6366f1` ou `#e11d48`).\n"
                "   - **Regra de Um Ponto Focal:** Cada slide deve ter apenas um elemento dominante (ex: a estatística principal ou o modelo 3D central).\n"
                "   - **Espaço Negativo Proposital:** Pelo menos 40% da tela livre para permitir respiro e elegância executiva."
            )
        elif any(w in msg_lower for w in ["dafont", "fonte", "tipografia", "font", "display"]):
            return (
                "🔤 **Curadoria Tipográfica & Fontes Display — DaFont.com:**\n\n"
                "Para selecionar e configurar tipografias de alto impacto sem quebrar a apresentação offline:\n\n"
                "1. **Seleção no DaFont:**\n"
                "   - Acesse [dafont.com](https://www.dafont.com) e explore categorias temáticas: *Techno > Sci-Fi*, *Gothic/Brutalist*, *Retro* ou *Bitmap*.\n"
                "   - Utilize o campo de visualização (*Preview*) com o texto exato do título do seu deck.\n"
                "   - Filtre por **'100% Free'** ou **'Free for personal use'** conforme a finalidade do seu projeto.\n\n"
                "2. **Instalação Local e Zero Dependência de Rede (@font-face):**\n"
                "   ```css\n"
                "   @font-face {\n"
                "       font-family: 'SciFiDisplay';\n"
                "       src: url('fonts/scifi-display.ttf') format('truetype');\n"
                "       font-display: swap;\n"
                "   }\n"
                "   .slide-title {\n"
                "       font-family: 'SciFiDisplay', sans-serif;\n"
                "       font-size: clamp(3rem, 7vw, 6rem);\n"
                "       letter-spacing: 0.08em;\n"
                "       text-transform: uppercase;\n"
                "   }\n"
                "   ```\n\n"
                "3. **Hierarquia Tipográfica Segura:**\n"
                "   - **Títulos Display (DaFont):** Máximo 4 a 6 palavras. Puro impacto e personalidade.\n"
                "   - **Corpo do Texto & Métricas (Sans-Serif Neutra):** Utilize *Inter*, *Plus Jakarta Sans* ou *Space Grotesk* para garantir legibilidade instantânea."
            )
        else:
            return (
                f"🪐 **Diretriz do Cinematic Slides & 3D Director:**\n\n"
                f"Para atender sua necessidade visual (*\"{user_message}\"*):\n\n"
                "1. **Tríade de Recursos Visuais:**\n"
                "   - 🪐 **Sketchfab.com:** Pesquise modelos 3D `.glb` com texturas PBR e filtros de licença CC para baixar e renderizar via Three.js.\n"
                "   - 🎨 **Behance.net:** Inspire-se nos melhores pitch decks e diretórios editoriais para definir contrastes de cores e grids cinematográficos.\n"
                "   - 🔤 **DaFont.com:** Escolha fontes display de forte identidade visual (Sci-Fi, Cyberpunk, Retrô) e carregue offline com `@font-face`.\n\n"
                "2. **Storytelling em 5 Atos:** Contexto inicial -> Tensão/Problema -> Clímax da Solução -> Prova de Tração/Métricas -> Chamada para Ação (CTA).\n\n"
                "3. **WebGL & Efeitos de Câmera:** Mantenha a renderização a 60 FPS com Three.js e use interpolações de câmera (Tween/GSAP) sincronizadas com as trocas de slide."
            )

    # Resposta padrão inteligente
    return (
        f"🤖 **Recomendação Especializada ({agent_title or 'Agente Ágil'}):**\n\n"
        f"Em resposta a: *\"{user_message}\"*:\n\n"
        "1. **Diagnóstico Ágil:** Analise as causas raízes e alinhe as expectativas entre o time técnico, negócio e liderança.\n"
        "2. **Políticas Explícitas:** Estabeleça critérios claros para entrada e saída de tarefas para diminuir ruídos de comunicação.\n"
        "3. **Melhoria Contínua:** Implemente ciclos curtos de teste e iteração para validar a eficácia da solução proposta."
    )

@app.post("/api/chat")
async def chat_endpoint(request: Request, _=Depends(verify_token)):
    body = await request.json()
    messages = body.get("messages", [])
    agent_type = body.get("agentType", "kiro")
    system_prompt = body.get("systemPrompt", "")
    agent_title = body.get("agentTitle", "")
    agent_id = body.get("agentId", "")
    is_stream = body.get("stream", False)

    # Extrai a última mensagem do usuário
    user_message = ""
    for m in reversed(messages):
        if m.get("role") == "user":
            user_message = m.get("content", "")
            break

    # Se não houver system_prompt específico do frontend, usa os defaults
    if not system_prompt:
        if agent_type == 'kiro':
            system_prompt = "Você é o Kiro, um Agente Autônomo focado em Orquestração e Delivery no Microsoft Azure DevOps. Responda como terminal Kiro: [Kiro] Mensagem."
        elif agent_type == 'claude':
            system_prompt = "Você é o Claude Code, um Agente Autônomo da Anthropic focado em Orquestração, Delivery e TDD no ecossistema Open-Source. Responda como terminal Claude."
        else:
            system_prompt = "Você é um Especialista de Inteligência Artificial prestativo."

    # Se a OpenAI API Key estiver configurada, tenta chamar a OpenAI
    has_openai = OPENAI_API_KEY and "cole_sua_chave" not in OPENAI_API_KEY
    
    if has_openai:
        try:
            payload = {
                "model": "gpt-4o-mini",
                "messages": [{"role": "system", "content": system_prompt}] + messages,
                "stream": bool(is_stream)
            }
            if is_stream:
                async def stream_generator():
                    async with httpx.AsyncClient() as client:
                        async with client.stream(
                            "POST",
                            "https://api.openai.com/v1/chat/completions",
                            headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
                            json=payload,
                            timeout=30.0
                        ) as resp:
                            if resp.status_code == 200:
                                async for chunk in resp.aiter_lines():
                                    if chunk:
                                        yield chunk + "\n"
                            else:
                                fallback = generate_expert_agent_reply(agent_title or agent_type, system_prompt, user_message, agent_id)
                                for word in fallback.split(" "):
                                    yield f"data: {json.dumps({'choices': [{'delta': {'content': word + ' '}}]})}\n\n"
                                yield "data: [DONE]\n\n"
                return StreamingResponse(stream_generator(), media_type="text/event-stream")
            else:
                async with httpx.AsyncClient() as client:
                    resp = await client.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
                        json=payload,
                        timeout=25.0
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        reply_content = data["choices"][0]["message"]["content"]
                        return JSONResponse({"reply": reply_content})
        except Exception:
            pass

    # Resposta com especialista interno
    expert_reply = generate_expert_agent_reply(agent_title or agent_type, system_prompt, user_message, agent_id)

    if is_stream:
        import asyncio
        async def mock_stream():
            for word in expert_reply.split(" "):
                yield f"data: {json.dumps({'choices': [{'delta': {'content': word + ' '}}]})}\n\n"
                await asyncio.sleep(0.02)
            yield "data: [DONE]\n\n"
        return StreamingResponse(mock_stream(), media_type="text/event-stream")

    return JSONResponse({"reply": expert_reply})

# Serve arquivos estáticos da raiz para testes locais (A Vercel ignora isso)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@app.get("/")
def read_root():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/{path:path}")
def catch_all(path: str):
    file_path = os.path.join(BASE_DIR, path)
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.index:app", host="0.0.0.0", port=3000, reload=True)
