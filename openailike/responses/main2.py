from openai import OpenAI
from datetime import datetime

client = OpenAI(
    base_url='http://localhost:11434/v1/',
    api_key='ollama',  # requerido, mas ignorado pelo Ollama
)

print("Aguarde...")
start_time = datetime.now()

# Habilitando streaming via SSE com stream=True
response_stream = client.chat.completions.create(
    model='llama3:8b',
    messages=[{'role': 'user', 'content': 'O que é Linux?'}],
    stream=True,  # ← Ativa o streaming estilo Server-Sent Events
)

print("\n📡 Resposta em streaming:\n" + "-"*40)
full_response = ""
first_token_time = None

for chunk in response_stream:
    # Captura o tempo do primeiro token para métrica de latência
    if first_token_time is None:
        first_token_time = datetime.now()
        print(f"\n⚡ Primeiro token: {first_token_time - start_time}\n")
    
    # Extrai o conteúdo delta do chunk
    delta = chunk.choices[0].delta.content
    if delta:
        print(delta, end='', flush=True)  # Imprime em tempo real sem quebra de linha
        full_response += delta

end_time = datetime.now()

# Métricas finais
print("\n" + "-"*40)
print(f"✅ Resposta completa recebida.")
print(f"⏱️  Tempo para primeiro token: {first_token_time - start_time}")
print(f"🕐 Tempo total de execução: {end_time - start_time}")