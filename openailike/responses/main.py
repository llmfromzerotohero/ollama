from openai import OpenAI
from datetime import datetime

client = OpenAI(
    base_url='http://localhost:11434/v1/',
    api_key='ollama',  # required but ignored
)

print("Aguarde...")
start_time = datetime.now()
responses_result = client.responses.create(
  model='llama3:8b',
  input='O que é Linux?',
)
end_time = datetime.now()
print(responses_result.output_text)
print(f"Tempo de execução: {end_time - start_time}")