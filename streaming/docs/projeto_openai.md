
# Detalhamento do código "Stremaing" no padrão OpenAI Like

Abaixo está a explicação detalhada do código que usa a **API compatível com OpenAI** do Ollama, destacando as diferenças arquiteturais em relação à biblioteca nativa.

### 1. Configuração do Cliente OpenAI

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)
```

- **`from openai import OpenAI`**: Usa o SDK oficial da OpenAI, amplamente suportado por frameworks (LangChain, CrewAI, LlamaIndex, etc.).
- **`base_url`**: Redireciona todas as chamadas para o endpoint local do Ollama que espelha a API OpenAI.
- **`api_key`**: Obrigatório para instanciar o cliente OpenAI, mas **ignorado pelo Ollama**. Qualquer string funciona.

### 2. Requisição com Streaming
```python
stream = client.chat.completions.create(
    model="qwen2.5:7b-instruct",
    messages=[{"role": "user", "content": "What is 17 × 23?"}],
    stream=True,
)
```
- Segue exatamente o padrão da documentação OpenAI.
- `stream=True` transforma a chamada em um **gerador de Server-Sent Events (SSE)**, entregando a resposta em tempo real.

### 3. Loop de Processamento dos `chunks`
```python
for chunk in stream:
    if not chunk.choices:
        continue
        
    delta = chunk.choices[0].delta
```
- Na API OpenAI, cada evento de streaming vem empacotado em `chunk.choices[0].delta`.
- **`delta`** contém **apenas o texto novo** gerado naquele milissegundo (não a resposta completa).
- `if not chunk.choices:`: Proteção contra o último chunk, que geralmente vem vazio (apenas com `finish_reason`).

#### Extração segura de campos
```python
    thinking_chunk = getattr(delta, "thinking", None)
    content_chunk = getattr(delta, "content", None)
```
- **`content`** é padrão OpenAI.
- **`thinking`** é uma **extensão não-padrão** injetada pelo Ollama. Como o SDK OpenAI usa modelos Pydantic que não declaram esse campo, acessá-lo diretamente (`delta.thinking`) geraria `AttributeError`.
- `getattr(delta, "thinking", None)` é a forma segura de tentar ler o campo sem quebrar a execução.

#### Controle de Estado e Impressão em Tempo Real
```python
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
```
- **`in_thinking`**: Flag que detecta a transição entre a fase de raciocínio interno e a resposta final.
- **`end="", flush=True`**: 
  - `end=""` impede a quebra de linha após cada fragmento.
  - `flush=True` força o terminal a renderizar imediatamente, criando o efeito de digitação.
- As variáveis `accumulated_*` concatenam os fragmentos para reconstruir a resposta completa ao final do stream.

### 4. Formatação para Histórico (Padrão OpenAI)
```python
assistant_message = {
    "role": "assistant",
    "content": accumulated_content,
}
```
- O padrão OpenAI **não reconhece o campo `thinking`** em mensagens de histórico.
- Para manter o contexto em conversas multi-turno, você tem duas opções:
  1. **Concatenar no `content`**: `"content": f"<think>{accumulated_thinking}</think>\n{accumulated_content}"`
  2. **Armazenar externamente**: Guardar o `thinking` em um dicionário separado e injetá-lo via `system prompt` ou `metadata` na próxima chamada.


### Comparativo: Nativa vs OpenAI-Like

| Aspecto | Biblioteca `ollama` | SDK `openai` (compatibilidade) |
|---------|---------------------|--------------------------------|
| **Acesso ao texto** | `chunk.message.content` | `chunk.choices[0].delta.content` |
| **Campo `thinking`** | Tipado e oficial | Extensão não-padrão (exige `getattr`) |
| **Estrutura de histórico** | Suporta `{"thinking": "...", "content": "..."}` | Apenas `{"role": "...", "content": "..."}` |
| **Ecossistema** | Exclusivo Ollama | Compatível com 90%+ dos frameworks de LLM |

---

### Dicas para Produção
1. **Verifique `finish_reason`**: No último chunk, `chunk.choices[0].finish_reason` pode ser `"stop"`, `"length"` (truncado) ou `"error"`. É útil para validar se a resposta foi completa.
2. **Fallback para `<think>`**: Em algumas versões do Ollama, o raciocínio pode vir **dentro** do `content` entre tags `<think>...</think>`. Se `thinking_chunk` for sempre `None`, faça um parse simples no `accumulated_content`.
3. **Economia de contexto**: O `thinking` consome tokens valiosos. Em chats longos, remova-o do histórico ou resuma-o para evitar estourar o `context_window` do modelo.