from openai import OpenAI
from datetime import datetime

client = OpenAI(
    base_url='http://localhost:11434/v1/',
    api_key='ollama',  # required but ignored
)

print("Aguarde...")
t1 = datetime.now()

chat_completion = client.chat.completions.create(
    messages=[
        {
            'role': 'user',
            'content': "O que é Linux?",
        }
    ],
    model='llama3:8b',
)
t2 = datetime.now()
print(chat_completion.choices[0].message.content)
print(f"Tempo de execução: {t2 - t1}")