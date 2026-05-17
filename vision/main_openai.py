import base64
import os
from openai import OpenAI

MODELO_LLM = "gemma3"
PERGUNTA = "O que é essa imagem? você pode detalhar o máximo possível a descrição do seu conteúdo?."

# 1. Configuração do cliente apontando para o Ollama
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # Obrigatório para o SDK, ignorado pelo Ollama
)

# 2. Entrada e validação do caminho da imagem
image_path = input("Please enter the path to the image: ")
if not os.path.isfile(image_path):
    raise FileNotFoundError(f"Imagem não encontrada: {image_path}")

# 3. Conversão para Base64 (padrão OpenAI para imagens locais)
with open(image_path, "rb") as f:
    encoded_image = base64.b64encode(f.read()).decode("utf-8")

# Define o MIME type correto com base na extensão
ext = os.path.splitext(image_path)[1].lower()
mime_map = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}
mime_type = mime_map.get(ext, "image/jpeg")

print("Aguarde...")

# 4. Chamada no formato OpenAI Vision
stream = client.chat.completions.create(
    model=MODELO_LLM,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": PERGUNTA},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:{mime_type};base64,{encoded_image}"}
                }
            ]
        }
    ],
    stream=True
)

# 5. Processamento do stream em tempo real
for chunk in stream:
    if chunk.choices:
        delta = chunk.choices[0].delta
        if delta.content:
            print(delta.content, end="", flush=True)

print("\n\n--- Stream finalizado ---")