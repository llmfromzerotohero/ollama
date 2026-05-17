from ollama import chat

MODELO_LLM = 'gemma3'
PERGUNTA = 'O que é essa imagem? você pode detalhar o máximo possível a descrição do seu conteúdo?.'

# Pass in the path to the image
path = input('Please enter the path to the image: ')

# You can also pass in base64 encoded image data
# img = base64.b64encode(Path(path).read_bytes()).decode()
# or the raw bytes
# img = Path(path).read_bytes()

print("Aguarde...")

response = chat(
  model=MODELO_LLM,
  messages=[
    {
      'role': 'user',
      'content': PERGUNTA,
      'images': [path],
    }
  ],
)

print(response.message.content)