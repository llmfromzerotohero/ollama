# Protótipo de análise de conteúdo de imagem

Este código demonstra como utilizar a **biblioteca nativa do Ollama** para fazer inferência multimodal (visão computacional), enviando uma imagem junto com um prompt de texto para um modelo com capacidade visual.

Abaixo está a explicação detalhada, bloco a bloco

### 1. Importação e Configuração
```python
from ollama import chat

MODELO_LLM = 'gemma3'
PERGUNTA = 'O que é essa imagem? você pode detalhar o máximo possível a descrição do seu conteúdo?.'
```
- `chat`: Função principal da biblioteca `ollama` para interagir com modelos.
- `MODELO_LLM`: Define o modelo a ser usado. `gemma3` é uma versão da Google com **suporte nativo a visão** (multimodal). 
  > Modelos puramente de texto ignorarão a imagem ou falharão. Sempre use modelos vision-capable (`llava`, `moondream`, `gemma3`, `qwen2.5-vl`, etc.).

---

### 2. Entrada de Dados
```python
path = input('Please enter the path to the image: ')
```
- Solicita ao usuário o caminho local da imagem (ex: `./foto.jpg`, `/home/user/imagem.png`).
- Os comentários logo abaixo mostram que a API aceita **três formatos** para imagens:
  1. **Caminho do arquivo** (string) → mais prático para uso local.
  2. **Base64** → útil para transmissão via rede ou APIs REST.
  3. **Bytes crus** → ideal quando a imagem já está em memória (ex: leitura de câmera ou upload web).

### 3. Chamada à API (Inferência Multimodal)
```python
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
```
Este é o núcleo do código. A estrutura `messages` segue o padrão de chat, mas com uma extensão crucial:
- **`'images': [path]`**: Campo obrigatório para modelos de visão. 
  - Aceita uma **lista**, permitindo enviar múltiplas imagens em uma única mensagem.
  - A biblioteca `ollama` lê o arquivo, converte para o formato esperado pelo backend e injeta os *tokens visuais* no contexto do modelo antes da geração.
- O modelo processa imagem + texto em conjunto e gera uma resposta textual baseada no conteúdo visual.

### 4. Saída
```python
print(response.message.content)
```
- `response.message.content` contém a resposta completa do modelo.
- Como `stream=True` **não foi especificado**, a chamada é **síncrona**: o código fica bloqueado até o modelo gerar tudo e retorna a resposta de uma vez.

### Pontos Técnicos Importantes

| Aspecto | Detalhe |
|--------|---------|
| **Formato de imagem** | JPG, PNG, WEBP, BMP são suportados. O Ollama faz o resize/crop interno para o *image encoder* do modelo. |
| **Múltiplas imagens** | Basta usar `'images': ['img1.jpg', 'img2.png']`. O modelo receberá todas em contexto. |
| **Sem streaming** | Este exemplo aguarda a resposta completa. Para ver a geração em tempo real, adicione `stream=True` e itere sobre `chunk.message.content`. |
| **Versão da biblioteca** | Suporte nativo a caminhos de imagem requer `ollama` ≥ `0.3.0`. Versões antigas exigem base64 manual. |
| **Tokenização visual** | Imagens consomem muitos tokens (geralmente 500~2000 por imagem, dependendo do modelo). Isso reduz o espaço disponível para texto no contexto. |


### Boas Práticas para Produção

1. **Validação do caminho**:
   ```python
   import os
   if not os.path.isfile(path):
       raise FileNotFoundError("Imagem não encontrada.")
   ```
2. **Tratamento de erros da API**:
   ```python
   try:
       response = chat(...)
   except Exception as e:
       print(f"Erro ao processar imagem: {e}")
   ```
3. **Streaming para imagens grandes**:
   Modelos de visão podem levar mais tempo para gerar. Adicionar `stream=True` melhora a UX:
   ```python
   for chunk in chat(model=..., messages=..., stream=True):
       print(chunk.message.content, end='', flush=True)
   ```
4. **Limpeza de contexto**: Se for fazer um chat contínuo com imagens, lembre-se de que cada imagem consumirá tokens do `context_window`. Em diálogos longos, remova imagens antigas ou resuma-as.

### Exemplo Rápido com Streaming + Validação
Se quiser transformar este snippet em algo mais robusto:
```python
import os
from ollama import chat

path = input("Caminho da imagem: ")
if not os.path.isfile(path):
    exit("Arquivo não encontrado.")

print("Processando imagem...")
stream = chat(
    model='gemma3',
    messages=[{'role': 'user', 'content': 'Descreva esta imagem em detalhes.', 'images': [path]}],
    stream=True
)

for chunk in stream:
    if chunk.message.content:
        print(chunk.message.content, end='', flush=True)
print("\n✅ Resposta concluída.")
```

## Sugestões: 

Adaptar esse código para **múltiplas imagens**, **chat interativo com histórico visual** ou integração com **APIs de upload** (FastAPI/Flask).