# Detalhamento do código "Streaming"

Este código demonstra como fazer uma requisição de chat com **streaming** usando a biblioteca oficial do Ollama, com um tratamento especial para um recurso do modelo `qwen2.5:7b-instruct`: a separação entre o **raciocínio interno** (`thinking`) e a **resposta final** (`content`).

## Explicação:

### 1. Importação e configuração da chamada

```python
from ollama import chat

stream = chat(
  model='qwen2.5:7b-instruct',
  messages=[{'role': 'user', 'content': 'What is 17 × 23?'}],
  stream=True,
)
```
- `chat()`: Função principal da biblioteca `ollama` para interagir com modelos.
- `model`: Especifica qual modelo será carregado/executado.
- `messages`: Lista que representa o histórico da conversa. Aqui, há apenas uma mensagem do usuário.
- `stream=True`: **Ponto crucial**. Em vez de esperar a resposta completa, a API retorna um **gerador/iterador** que entrega a resposta em pequenos pedaços (`chunks`) conforme o modelo os gera.

### 2. Variáveis de estado
```python
print("Aguarde...")

in_thinking = False
content = ''
thinking = ''
```
- `in_thinking`: `bool` que controla em qual fase da resposta o código está.
- `content` e `thinking`: Strings que vão **acumular** todo o texto gerado, respectivamente da resposta final e do raciocínio interno. Isso é necessário porque, no streaming, o texto chega fragmentado.

### 3. Loop de processamento dos chunks
```python
for chunk in stream:
```
O loop itera sobre cada pedaço enviado pelo modelo em tempo real.

#### Bloco de "Thinking" (Raciocínio)
```python
  if chunk.message.thinking:
    if not in_thinking:
      in_thinking = True
      print('Thinking:\n', end='', flush=True)
    print(chunk.message.thinking, end='', flush=True)
    thinking += chunk.message.thinking
```
- Alguns modelos (como o Qwen 2.5) podem gerar explicitamente um bloco de raciocínio antes da resposta final.
- `if not in_thinking`: Garante que o cabeçalho `"Thinking:"` seja impresso **apenas uma vez**, na transição.
- `end='', flush=True`: 
  - `end=''` evita que o `print` pule linha após cada chunk.
  - `flush=True` força o terminal a exibir o texto imediatamente, criando o efeito de digitação em tempo real.
- `thinking += ...`: Concatena os fragments para reconstruir o raciocínio completo.

#### Bloco de "Content" (Resposta Final)
```python
  elif chunk.message.content:
    if in_thinking:
      in_thinking = False
      print('\n\nAnswer:\n', end='', flush=True)
    print(chunk.message.content, end='', flush=True)
    content += chunk.message.content
```
- Quando o modelo para de gerar `thinking` e começa a gerar `content`, a flag `in_thinking` é desativada.
- Imprime o cabeçalho `"Answer:"` e passa a exibir a resposta final.
- Da mesma forma, acumula o texto em `content`.

### 4. Preparação para o próximo turno (Comentário)
```python
  # append the accumulated fields to the messages for the next request
  new_messages = [{ 'role': 'assistant', 'thinking': thinking, 'content': content }]
```
- Essa linha **não é executada como parte do loop atual**; é um exemplo de como formatar a resposta do assistente para ser adicionada ao histórico (`messages`) em uma próxima chamada.
- Manter `thinking` e `content` separados no histórico permite que o modelo preserve o contexto do raciocínio em conversas multi-turno (se o modelo suportar essa estrutura).

### Pontos de Atenção & Boas Práticas
1. **Versão da biblioteca**: O uso de `chunk.message.thinking` indica uma versão recente da biblioteca `ollama` (≥ 0.3.x) que retorna objetos estruturados em vez de dicionários puros.
2. `new_messages` não é utilizado no script: Para um chat contínuo, você precisaria fazer `messages.append(new_messages[0])` após o loop e chamar `chat()` novamente.
3. **Tratamento de erros**: Em produção, é recomendado envolver a chamada em `try/except` e verificar `chunk.get('done')` (ou equivalente) para detectar fim de stream ou interrupções.
4. **Consumo de memória**: Acumular todo o `thinking` e `content` em strings é fino para respostas curtas. Em diálogos longos, considere truncar ou resumir o histórico para não estourar o contexto do modelo.