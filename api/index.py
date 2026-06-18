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
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Nenhum token fornecido.")
    
    token = auth_header.split(" ")[1]
    
    # Valida no Supabase via REST (já que não temos SDK no Python, batemos na API)
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{SUPABASE_URL}/auth/v1/user",
            headers={"apikey": SUPABASE_ANON_KEY, "Authorization": f"Bearer {token}"}
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=401, detail="Sessão inválida ou expirada.")
    return True

@app.post("/api/chat")
async def chat_endpoint(request: Request, _=Depends(verify_token)):
    body = await request.json()
    messages = body.get("messages", [])
    agent_type = body.get("agentType", "kiro")

    system_prompt = "Você é um Especialista de Inteligência Artificial prestativo."
    if agent_type == 'kiro':
        system_prompt = "Você é o Kiro, um Agente Autônomo focado em Orquestração e Delivery no Microsoft Azure DevOps. Responda como terminal Kiro: [Kiro] Mensagem."
    elif agent_type == 'claude':
        system_prompt = "Você é o Claude Code, um Agente Autônomo da Anthropic focado em Orquestração, Delivery e TDD no ecossistema Open-Source. Responda como terminal Claude."

    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "system", "content": system_prompt}] + messages,
        "stream": True
    }

    async def stream_generator():
        try:
            async with httpx.AsyncClient() as client:
                async with client.stream(
                    "POST",
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
                    json=payload,
                    timeout=30.0
                ) as resp:
                    if resp.status_code != 200:
                        yield f"data: {json.dumps({'content': '[Erro na OpenAI: Verifique sua Chave API no .env]'})}\n\n"
                        yield "data: [DONE]\n\n"
                        return
                    
                    async for chunk in resp.aiter_lines():
                        if chunk:
                            yield chunk + "\n"
        except Exception as e:
            yield f"data: {json.dumps({'content': f'[Erro Interno: {str(e)}]'})}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(stream_generator(), media_type="text/event-stream")

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
