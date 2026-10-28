import os
print("ANTHROPIC_API_KEY:", "OK" if os.getenv("ANTHROPIC_API_KEY") else "FALTA")
print("SUPABASE_URL: ", "OK" if os.getenv("SUPABASE_URL") else "FALTA")
print("SUPABASE_KEY: ", "OK" if os.getenv("SUPABASE_KEY") else "FALTA")
print("VOYAGE_API_KEY: ", "OK" if os.getenv("VOYAGE_API_KEY") else "FALTA")
from anthropic import Anthropic
claude = Anthropic()
r = claude.messages.create(model="claude-haiku-4-5", max_tokens=10,
 messages=[{"role": "user", "content": "Diga ok"}])
print("\nClaude:", r.content[0].text)
import voyageai
v = voyageai.Client()
emb = v.embed(["teste"], model="voyage-3", input_type="document").embeddings[0]
print("Voyage: vetor com", len(emb), "dimensões")
from supabase import create_client
sb = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
data = sb.table("documents").select("id").limit(1).execute().data
print("Supabase: tabela documents acessível, ", len(data), "registro(s).")