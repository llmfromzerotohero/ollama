import ollama  # Importação completa do módulo

MODELO_LLM = 'qwen2.5:7b-instruct'

def gerar_resposta_suporte(pergunta: str, base_conhecimento: str) -> str:
    prompt_template = """### CONTEXTO DO SISTEMA
Você é um assistente técnico da ETIPI especializado em suporte de infraestrutura. 
Suas respostas devem ser:
- Claras, objetivas e em português do Brasil
- Baseadas apenas nas informações fornecidas abaixo
- Educadas e com tom institucional

### BASE DE CONHECIMENTO
{kb}

### SOLICITAÇÃO DO USUÁRIO
{question}

### INSTRUÇÕES DE RESPOSTA
1. Se a resposta estiver na base de conhecimento, responda diretamente
2. Se não houver informação suficiente, diga: "Não encontrei essa informação na base oficial. Consulte a equipe de suporte."
3. Nunca invente dados ou procedimentos
4. Formate a resposta em markdown, com tópicos quando aplicável

### RESPOSTA:
""".format(kb=base_conhecimento, question=pergunta)

    # Chamada ao modelo local via Ollama (API moderna `chat`)
    response = ollama.chat(
        model=MODELO_LLM,
        messages=[{"role": "user", "content": prompt_template}]
    )
    return response["message"]["content"]

# Uso prático:
if __name__ == "__main__":
    base = "• Wi-Fi: Rede 'ETIPI-Alunos', senha no setor de TI\n• Impressão: Saldo mínimo de 10 páginas"
    pergunta1 = "Qual a senha do Wi-Fi disponível?"
    pergunta2 = "Como faço para imprimir documentos?"
    
    print("Aguarde... Gerando resposta com", MODELO_LLM)
    resposta = gerar_resposta_suporte(pergunta1, base)
    print(f"\nRESPOSTA {pergunta1}:")
    print(resposta)
    
    print("Aguarde... Gerando resposta com", MODELO_LLM)
    resposta = gerar_resposta_suporte(pergunta2, base)
    print(f"\nRESPOSTA {pergunta2}:")
    print(resposta)