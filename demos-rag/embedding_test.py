import voyageai
v = voyageai.Client()
result = v.embed(
 ["Como criar uma conta?"],
 model="voyage-3",
 input_type="query"
)
vec = result.embeddings[0]
print(f"Dimensões do vetor: {len(vec)}")
print(f"Primeiros 5 valores: {vec[:5]}")