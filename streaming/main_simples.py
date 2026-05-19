import ollama

MODELO_LLM = 'llama3.2:3b'  # Substitua pelo modelo desejado
pergunta = "Crie um resumo sobre o Linux"

try:
    print(f"Usando o modelo: {MODELO_LLM}")
    print(f"Pergunta: {pergunta}")
    print("Aguarde... Gerando resposta com", MODELO_LLM)
    stream = ollama.chat(
        model=MODELO_LLM,
        messages=[{'role': 'user', 'content': pergunta}],
        stream=True
    )
    
    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)
        
except KeyboardInterrupt:
    print("\n⚠️ Geração interrompida pelo usuário.")
except Exception as e:
    print(f"\n❌ Erro ao gerar resposta: {e}")
finally:
    print()  # Garante a quebra de linha em qualquer cenário