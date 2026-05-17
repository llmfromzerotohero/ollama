import ollama

MODELO_LLM = 'qwen3-embedding:4b'
PERGUNTA = 'Qual é a capital da França?'

single = ollama.embed(
  model=MODELO_LLM,
  input=PERGUNTA
)

print(len(single['embeddings'][0]))  # vector length
print(single['embeddings'][0][:5])  # first 5 dimensions of the vector