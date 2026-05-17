from openai import OpenAI

URL_OLLAMA_OPENAI_COMPATIBILITY = "http://localhost:11434/v1"
MODELO_LLM = 'qwen2.5:7b-instruct'
PERGUNTA = 'What is 17 × 23?'

# 1. Configurar o cliente OpenAI apontando para o Ollama
client = OpenAI(
    base_url=URL_OLLAMA_OPENAI_COMPATIBILITY,
    api_key="ollama"  # O Ollama ignora a chave, mas o cliente OpenAI exige uma
)

# 2. Iniciar a chamada com streaming
stream = client.chat.completions.create(
    model=MODELO_LLM,
    messages=[{"role": "user", "content": PERGUNTA}],
    stream=True,
)

print("Aguarde...")

in_thinking = False
accumulated_thinking = ""
accumulated_content = ""

# 3. Processar os chunks do stream
for chunk in stream:
    # O último chunk pode vir sem choices (apenas com finish_reason)
    if not chunk.choices:
        continue
        
    delta = chunk.choices[0].delta
    
    # 'thinking' é uma extensão não-padrão do Ollama. Usamos getattr para segurança.
    thinking_chunk = getattr(delta, "thinking", None)
    content_chunk = getattr(delta, "content", None)

    if thinking_chunk:
        if not in_thinking:
            in_thinking = True
            print("Thinking:\n", end="", flush=True)
        print(thinking_chunk, end="", flush=True)
        accumulated_thinking += thinking_chunk
        
    elif content_chunk:
        if in_thinking:
            in_thinking = False
            print("\n\nAnswer:\n", end="", flush=True)
        print(content_chunk, end="", flush=True)
        accumulated_content += content_chunk

print("\n\n--- Stream finalizado ---")

# 4. Formatar a resposta no padrão OpenAI para reinserção no histórico
assistant_message = {
    "role": "assistant",
    "content": accumulated_content,
    # O padrão OpenAI não possui campo 'thinking'. 
    # Se precisar preservá-lo, armazene em metadados ou concatene no content.
}

print(assistant_message["content"])

# Exemplo de como ficaria o histórico para a próxima pergunta:
# conversation_history = [
#     {"role": "user", "content": "What is 17 × 23?"},
#     assistant_message
# ]