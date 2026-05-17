# Protótipo de analisador de imagem no padrão OpenAI Like

Este código demonstra como utilizar a **API compatível com OpenAI** do Ollama para realizar inferência multimodal (visão computacional) usando o SDK oficial `openai` do Python.

Abaixo está a explicação detalhada, bloco a bloco:

### 1. Importações e Configuração do Cliente

```python
import base64
import os
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # Obrigatório para o SDK, ignorado pelo Ollama
)
```
| Elemento | Função |
|----------|--------|
| `base64` | Codifica a imagem em texto para transmissão via API |
| `os` | Manipula caminhos de arquivos e verifica existência |
| `OpenAI` | Classe do SDK oficial que implementa o protocolo OpenAI |
| `base_url` | Redireciona as requisições para o servidor local do Ollama (porta 11434) |
| `api_key` | Chave fictícia exigida pelo SDK, mas ignorada pelo Ollama em modo local |

> **Vantagem**: Usar o SDK `openai` permite que seu código funcione com **qualquer provedor compatível** (OpenAI, Azure, Groq, vLLM, Ollama) trocando apenas a `base_url`.

### 2. Configuração do Modelo e Prompt

```python
MODEL = "gemma3"
PERGUNTA = "O que é essa imagem? você pode detalhar o máximo possível a descrição do seu conteúdo?."
```
- `MODEL`: Nome do modelo carregado no Ollama. Deve ser um modelo **multimodal** (`gemma3`, `llava`, `qwen2.5-vl`, etc.).
- `PERGUNTA`: Instrução em português solicitando descrição detalhada da imagem.

### 3. Entrada e Validação da Imagem
```python
image_path = input("Please enter the path to the image: ")
if not os.path.isfile(image_path):
    raise FileNotFoundError(f"Imagem não encontrada: {image_path}")
```
- Solicita ao usuário o caminho do arquivo.
- `os.path.isfile()` previne erros ao tentar ler um caminho inválido.

### 4. Conversão para Base64 + MIME Type
```python
with open(image_path, "rb") as f:
    encoded_image = base64.b64encode(f.read()).decode("utf-8")

ext = os.path.splitext(image_path)[1].lower()
mime_map = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}
mime_type = mime_map.get(ext, "image/jpeg")
```
| Etapa | Por que é necessária? |
|-------|----------------------|
| `base64.b64encode()` | Transforma bytes binários em string ASCII, seguro para JSON |
| `.decode("utf-8")` | Converte o objeto `bytes` para `str` utilizável no payload |
| `mime_map` | Define o tipo MIME correto (`image/jpeg`, `image/png`, etc.) para o decoder do modelo interpretar os dados |

> **Data URI**: O formato final `data:{mime_type};base64,{encoded_image}` é o padrão da especificação OpenAI para embutir imagens diretamente na requisição.

### 5. Estrutura da Mensagem no Padrão OpenAI Vision
```python
stream = client.chat.completions.create(
    model=MODEL,
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

```
Esta é a parte mais importante. Diferente da biblioteca nativa do Ollama, o padrão OpenAI exige:

| Campo | Descrição |
|-------|-----------|
| `content` como **lista** | Permite mesclar múltiplos tipos de mídia (texto + imagem) na mesma mensagem |
| `{"type": "text"}` | Bloco de texto puro com o prompt do usuário |
| `{"type": "image_url"}` | Bloco de imagem com URL no formato Data URI |
| `stream=True` | Habilita resposta em tempo real (chunks) em vez de aguardar a geração completa |

> **Atenção**: Modelos puramente de texto ignorarão o bloco `image_url` ou retornarão erro. Sempre verifique se o modelo suportar visão.

### 🔹 6. Processamento do Stream em Tempo Real
```python
for chunk in stream:
    if chunk.choices:
        delta = chunk.choices[0].delta
        if delta.content:
            print(delta.content, end="", flush=True)

print("\n\n--- Stream finalizado ---")
```
| Elemento | Função |
|----------|--------|
| `for chunk in stream` | Itera sobre cada pedaço da resposta gerada pelo modelo |
| `if chunk.choices` | Garante que o chunk contém uma escolha válida (evita erro em chunks finais vazios) |
| `delta.content` | Contém apenas o **novo texto** gerado neste chunk (não a resposta completa) |
| `end="", flush=True` | Imprime sem pular linha e força a atualização imediata do terminal (efeito "digitação") |

#### Fluxo do Stream:
```
Chunk 1: delta.content = "Esta "
Chunk 2: delta.content = "imagem "
Chunk 3: delta.content = "mostra "
...
Último chunk: choices[0].finish_reason = "stop", delta.content = None
```

---

### Comparativo: Biblioteca Nativa vs. Padrão OpenAI

| Característica | `ollama.chat()` (nativo) | `openai.ChatCompletion` (compat) |
|---------------|-------------------------|----------------------------------|
| **Imagem local** | `'images': ['caminho.jpg']` | Exige Base64 + Data URI |
| **Estrutura `content`** | String simples | Lista de objetos `{"type": ...}` |
| **Acesso ao chunk** | `chunk.message.content` | `chunk.choices[0].delta.content` |
| **Portabilidade** | Funciona apenas com Ollama | Funciona com OpenAI, Azure, Groq, vLLM, etc. |
| **Dependência** | `pip install ollama` | `pip install openai` |

### Boas Práticas para Produção

1. **Tratamento de erros robusto**:
   ```python
   try:
       stream = client.chat.completions.create(...)
   except openai.APIConnectionError:
       print("Erro: Ollama não está rodando em localhost:11434")
   except openai.BadRequestError as e:
       if "vision" in str(e).lower():
           print("Erro: Modelo não suporta processamento de imagens")
   ```

2. **Controle de tokens visuais**: 
   Imagens consomem muitos tokens (500~2500 por imagem). Em chats longos, remova imagens antigas do histórico para não estourar o `context_window`.

3. **Detecção automática de MIME**:
   Para maior robustez, use a lib `python-magic`:
   ```python
   import magic
   mime_type = magic.from_file(image_path, mime=True)  # Ex: "image/png"
   ```

4. **Timeout e cancelamento**:
   ```python
   stream = client.chat.completions.create(
       ...,
       timeout=120  # segundos
   )
   ```

### Sugestões:

Adaptar para:
- **Chat interativo com histórico** (mantendo imagens e texto no contexto)
- **Upload via API web** (FastAPI/Flask recebendo `multipart/form-data`)
- **Múltiplas imagens** na mesma mensagem (basta adicionar mais blocos `image_url` na lista `content`)
- **Extração estruturada** (forçar saída em JSON com `response_format={"type": "json_object"}`)