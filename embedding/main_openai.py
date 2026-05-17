from openai import OpenAI

MODELO_LLM = 'qwen3-embedding:4b'
PERGUNTA = 'Qual é a capital da França?'

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

response = client.embeddings.create(
    model=MODELO_LLM,
    input=PERGUNTA
)

vector = response.data[0].embedding

print(len(vector))  # vector length
print(vector[:5])  # first 5 dimensions of the vector