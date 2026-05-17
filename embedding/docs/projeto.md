# Protótipo de aplicação de embedding

Este código demonstra como utilizar a **biblioteca nativa do Ollama** para gerar **embeddings vetoriais** (representações numéricas de texto) usando um modelo da família Qwen especializado em embedding.

Abaixo está a explicação detalhada, bloco a bloco:

### 🔹 1. Importação e Configuração
```python
import ollama

MODELO_LLM = 'qwen3-embedding:4b'
PERGUNTA = 'Qual é a capital da França?'
```
| Elemento | Função |
|----------|--------|
| `import ollama` | Importa a biblioteca oficial do Ollama para Python |
| `MODELO_LLM` | Define o modelo de embedding a ser usado. `qwen3-embedding:4b` é um modelo da família Qwen especializado em transformar texto em vetores densos |
| `PERGUNTA` | Texto de entrada que será convertido em embedding |

> **O que é um Embedding?**  
> É uma representação matemática do texto como um **vetor de números reais** (ex: `[0.023, -1.45, 0.89, ...]`). Textos semanticamente similares produzem vetores próximos no espaço vetorial, permitindo buscas por significado, não apenas por palavras-chave.


### 🔹 2. Geração do Embedding (Chamada à API)
```python
single = ollama.embed(
  model=MODELO_LLM,
  input=PERGUNTA
)
```

| Parâmetro | Descrição |
|-----------|-----------|
| `model` | Nome do modelo de embedding carregado no Ollama |
| `input` | Pode ser: <br>• **String**: gera um único embedding <br>• **Lista de strings**: gera múltiplos embeddings em batch (mais eficiente) |

#### Formato da Resposta
A função retorna um **dicionário** com a seguinte estrutura:
```python
{
  'embeddings': [
    [0.0234, -1.4521, 0.8912, ..., 0.0045]  # Vetor de N dimensões
  ]
}
```
- `single['embeddings']`: Lista contendo um vetor para cada string enviada em `input`.
- `single['embeddings'][0]`: Primeiro (e único) vetor gerado, correspondente à `PERGUNTA`.


### 3. Inspeção do Vetor Gerado
```python
print(len(single['embeddings'][0]))  # vector length
print(single['embeddings'][0][:5])  # first 5 dimensions of the vector
```

| Linha | O que faz | Exemplo de saída |
|-------|-----------|-----------------|
| `len(...)` | Mostra a **dimensionalidade** do embedding (quantos números compõem o vetor) | `2048` |
| `[:5]` | Exibe as **5 primeiras dimensões** para inspeção visual | `[0.0234, -1.4521, 0.8912, 0.1105, -0.3321]` |

> **Dimensionalidade típica**: Modelos como `qwen3-embedding:4b` geralmente geram vetores de **1024**, **2048** ou **4096** dimensões. Quanto maior a dimensão, maior a capacidade de representar nuances semânticas (mas também maior o custo de armazenamento e busca).


### Conceitos-Chave sobre Embeddings

```
Texto: "Qual é a capital da França?"
       ↓
[Tokenização → Encoder → Projeção Vetorial]
       ↓
Vetor: [0.023, -1.45, 0.89, ..., 0.0045]  # 2048 números
       ↓
Similaridade com "Paris é a capital francesa?" → Alta (vetores próximos)
Similaridade com "Receita de bolo de chocolate" → Baixa (vetores distantes)
```

#### Aplicações Práticas:
| Caso de Uso | Como o embedding ajuda |
|-------------|----------------------|
| **Busca semântica** | Encontrar documentos relevantes mesmo sem palavras-chave exatas |
| **RAG (Retrieval-Augmented Generation)** | Recuperar contexto relevante para alimentar um LLM |
| **Clusterização** | Agrupar textos similares automaticamente (ex: tickets de suporte) |
| **Recomendação** | Sugerir conteúdo baseado em similaridade vetorial |

### Exemplo Prático: Comparando Similaridade
```python
import ollama
from numpy import dot
from numpy.linalg import norm

# Gera embeddings para duas frases
texts = [
    "Qual é a capital da França?",
    "Paris é a cidade principal da França."
]
result = ollama.embed(model='qwen3-embedding:4b', input=texts)

# Calcula similaridade de cosseno
vec1, vec2 = result['embeddings']
similarity = dot(vec1, vec2) / (norm(vec1) * norm(vec2))

print(f"Similaridade: {similarity:.4f}")  # Ex: 0.8721 (alta similaridade semântica)
```

### Pontos de Atenção e Boas Práticas

1. **Batch processing para eficiência**:
   ```python
   # Em vez de chamar ollama.embed() várias vezes:
   texts = ["Texto 1", "Texto 2", "Texto 3"]
   result = ollama.embed(model=MODELO_LLM, input=texts)  # Uma única chamada
   vectors = result['embeddings']  # Lista com 3 vetores
   ```

2. **Normalização dos vetores**:
   Alguns modelos retornam vetores já normalizados (norma = 1). Se não, normalize antes de calcular similaridade:
   ```python
   from numpy.linalg import norm
   normalized = vec / norm(vec)
   ```

3. **Armazenamento eficiente**:
   Vetores de 2048 dimensões em `float32` ocupam ~8KB cada. Para milhões de vetores, use:
   - Bancos vetoriais: **Chroma**, **Qdrant**, **Pinecone**, **Weaviate**
   - Compressão: quantização para `float16` ou `int8` (com perda controlada de precisão)

4. **Compatibilidade de modelos**:
   Nem todo modelo no Ollama suporta `ollama.embed()`. Use apenas modelos especializados em embedding:
   - `qwen3-embedding:*`
   - `nomic-embed-text`
   - `mxbai-embed-large`
   - `bge-m3`

5. **Context window do embedding**:
   Modelos de embedding têm limite de tokens por entrada (ex: 512 ou 8192 tokens). Textos muito longos devem ser chunked antes da embedding.

### Comparativo: Embedding Nativo vs. OpenAI Compatibility

| Característica | `ollama.embed()` (nativo) | `openai.Embedding.create()` (compat) |
|---------------|---------------------------|-------------------------------------|
| **Input** | `input=str` ou `list[str]` | `input=str` ou `list[str]` |
| **Resposta** | `{'embeddings': [[...]]}` | `{'data': [{'embedding': [...]}]}` |
| **Portabilidade** | Apenas Ollama | Funciona com OpenAI, Azure, etc. |
| **Dependência** | `pip install ollama` | `pip install openai` |

#### Exemplo OpenAI-compatible:
```python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

response = client.embeddings.create(
    model="qwen3-embedding:4b",
    input="Qual é a capital da França?"
)
vector = response.data[0].embedding
```

### Sugestões: 

Adaptar para:
- **Busca semântica em documentos locais** (carregar PDFs/TXT, gerar embeddings e buscar por similaridade)
- **Pipeline RAG completo** (embedding + retriever + LLM para respostas contextualizadas)
- **Integração com banco vetorial** (Chroma/Qdrant para persistência e busca escalável)
- **Comparação de múltiplos modelos de embedding** (avaliar qual performa melhor para seu caso)