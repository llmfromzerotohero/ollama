# Hospedagem Local de Modelos LLM via Ollama

Este README resume a apresentação **Hospedagem Local de Modelos LLM via Ollama**, organizada como parte da trilha **LLM do Zero**. O material apresenta o Ollama como uma ferramenta prática para instalar, executar, gerenciar e integrar modelos de linguagem de grande porte em ambientes locais, com foco em aprendizagem, prototipação, experimentação controlada e validação inicial de aplicações com IA Generativa.

A ideia central da apresentação é que a inferência local com LLMs oferece privacidade, controle técnico e baixo custo de experimentação, mas exige disciplina operacional, documentação dos testes, conhecimento das limitações de hardware e atenção à reprodutibilidade.

A apresentação (pdf) está disponível neste [link](https://github.com/llmfromzerotohero/ollama/blob/main/Apresentacao_Ollama_LLM_Local.pdf)

## Objetivos de aprendizagem

Ao final da unidade, o estudante deve ser capaz de:

- Instalar e validar o Ollama em diferentes ambientes, como Linux, macOS, Windows/WSL2 e Docker.
- Baixar, executar, inspecionar, remover e documentar modelos locais.
- Utilizar tags e versões para garantir reprodutibilidade dos experimentos.
- Controlar o comportamento dos modelos por meio de parâmetros de inferência e arquivos `Modelfile`.
- Criar prompts estruturados, reutilizáveis e parametrizáveis.
- Utilizar o Ollama como serviço local por meio da API nativa e da API compatível com OpenAI.
- Desenvolver exemplos com streaming, visão computacional e embeddings.
- Avaliar limitações de CPU, RAM, VRAM, disco, quantização e contexto.
- Aplicar boas práticas para experimentação, desenvolvimento e monitoramento de LLMs locais.

## Sequência da apresentação

A apresentação mantém a sequência de tópicos da versão original e amplia cada unidade com explicações, exemplos práticos, comandos, checklists e recomendações operacionais.

| Unidade | Tema central | Principais pontos abordados |
|---|---|---|
| Unidade 1 | Instalação e configuração | Instalação no Linux, macOS, Windows/WSL2 e Docker; validação da CLI e API; sistema de arquivos; variáveis de ambiente; diagnóstico inicial. |
| Unidade 2 | Gerenciamento e execução de modelos | Comandos da CLI, ciclo de vida dos modelos, sessões ativas, tags, versões, reprodutibilidade e documentação experimental. |
| Unidade 3 | Parâmetros de inferência e prompt engineering | Controle do comportamento do modelo por requisição e por `Modelfile`; temperatura, top-p, top-k, contexto, templates e prompts reutilizáveis. |
| Unidade 4 | Ollama como serviço | Uso da API nativa, API compatível com OpenAI, chamadas HTTP, integração com Python, streaming, vision e embeddings. |
| Unidade 5 | Limitações de hardware e boas práticas | CPU, RAM, VRAM, disco, quantização, sintomas de saturação, monitoramento e critérios para decidir quando não usar inferência local. |

## Unidade 1 — Instalação e Configuração

A primeira parte da apresentação explica como preparar o ambiente local para executar modelos LLM com Ollama. O ponto de partida é entender que o Ollama simplifica a execução local de modelos abertos, oferecendo uma CLI simples, um serviço HTTP local e suporte a modelos pré-empacotados.

### Por que hospedar LLMs localmente?

Hospedar modelos localmente pode ser útil para:

- Aprender conceitos de inferência, prompts, parâmetros e integração com APIs.
- Prototipar aplicações sem custo por token.
- Executar testes em dados sensíveis sem enviar conteúdo para serviços externos.
- Controlar versões, tags, parâmetros e comportamento do modelo.
- Validar ideias antes de migrar para arquiteturas mais robustas.

Apesar dessas vantagens, a apresentação reforça que um ambiente local não substitui uma arquitetura de produção escalável. Para muitos usuários simultâneos, baixa latência garantida, autenticação, observabilidade e escalabilidade horizontal, soluções como vLLM, clusters GPU e gateways multi-modelo são mais adequadas.

### Instalação por ambiente

A apresentação aborda diferentes cenários de instalação:

- **Linux:** instalação por script oficial, uso como serviço do sistema e validação com `systemctl`.
- **macOS:** uso do aplicativo do Ollama, integração com terminal e atenção à memória unificada em máquinas Apple Silicon.
- **Windows:** uso do instalador nativo ou WSL2 para ambientes mais próximos do Linux.
- **Docker:** alternativa para isolamento, automação e reprodutibilidade.

Exemplos de validação inicial:

```bash
ollama --version
ollama list
curl http://localhost:11434/api/tags
```

### Sistema de arquivos e variáveis de ambiente

A apresentação destaca que modelos LLM ocupam bastante espaço em disco e devem ser tratados como dependências pesadas do ambiente experimental. O diretório de armazenamento pode ser configurado com a variável `OLLAMA_MODELS`.

Variáveis úteis:

```bash
export OLLAMA_HOST=0.0.0.0:11434
export OLLAMA_MODELS=/srv/ollama/models
export OLLAMA_KEEP_ALIVE=10m
```

Atenção: expor o Ollama em `0.0.0.0` torna o serviço acessível pela rede. Isso deve ser feito somente com firewall, proxy, autenticação ou outros controles de segurança.

### Diagnóstico inicial

Antes de usar modelos maiores, recomenda-se validar:

- Se a CLI está funcionando.
- Se a API local responde.
- Se o modelo foi baixado corretamente.
- Se há memória suficiente.
- Se CPU, RAM e VRAM estão dentro de limites aceitáveis.
- Se os logs do serviço indicam algum erro.

Comandos úteis:

```bash
ollama list
ollama ps
curl http://localhost:11434/api/tags
journalctl -u ollama -n 80
```

## Unidade 2 — Gerenciamento e Execução de Modelos

A segunda parte trata do ciclo de vida dos modelos no Ollama. A apresentação mostra que a CLI cobre as principais operações necessárias para baixar, executar, inspecionar, monitorar e remover modelos.

### Operações mais comuns

```bash
ollama pull qwen2.5:7b
ollama run qwen2.5:7b
ollama list
ollama show qwen2.5:7b
ollama ps
ollama stop qwen2.5:7b
ollama rm qwen2.5:7b
```

Esses comandos devem ser acompanhados de registro experimental. Em cada teste, recomenda-se documentar:

- Nome do modelo.
- Tag utilizada.
- Prompt executado.
- Parâmetros de inferência.
- Hardware usado.
- Data do teste.
- Resultado observado.
- Sintomas de desempenho ou instabilidade.

### Tags e reprodutibilidade

A apresentação destaca o uso de tags para evitar resultados ambíguos. Em vez de usar apenas `latest`, é melhor registrar explicitamente o modelo e a versão utilizada, sempre que possível.

Exemplo de documentação mínima:

```text
Modelo: llama3.2:3b
Tarefa: resumo técnico
Temperatura: 0.2
Contexto: 4096 tokens
Hardware: CPU/RAM/VRAM disponíveis
Data: AAAA-MM-DD
Observações: latência, qualidade e estabilidade
```

## Unidade 3 — Parâmetros de Inferência e Prompt Engineering

A apresentação explica que o comportamento do modelo pode ser controlado de duas formas principais:

1. **Por requisição**, usando parâmetros enviados junto com a chamada à API.
2. **Por definição do modelo**, usando um arquivo `Modelfile`.

### Parâmetros importantes

Os parâmetros de inferência ajudam a ajustar criatividade, previsibilidade, tamanho da resposta e uso de contexto. Entre os mais importantes estão:

| Parâmetro | Função |
|---|---|
| `temperature` | Controla aleatoriedade e criatividade da resposta. |
| `top_p` | Limita a amostragem aos tokens mais prováveis acumulados. |
| `top_k` | Limita a escolha aos k tokens mais prováveis. |
| `num_ctx` | Define o tamanho da janela de contexto. |
| `num_predict` | Limita a quantidade de tokens gerados. |
| `stop` | Define sequências que encerram a geração. |

Exemplo conceitual de uso por requisição:

```json
{
  "model": "llama3.2:3b",
  "prompt": "Explique o conceito de RAG em 5 tópicos.",
  "options": {
    "temperature": 0.2,
    "num_predict": 250
  }
}
```

### Uso de Modelfile

O `Modelfile` permite criar variações customizadas de modelos, com parâmetros e mensagens de sistema predefinidas. Isso ajuda a padronizar comportamentos e facilitar a repetição de experimentos.

Exemplo simplificado:

```text
FROM llama3.2:3b

PARAMETER temperature 0.2
PARAMETER num_ctx 4096

SYSTEM "Você é um assistente técnico que responde de forma objetiva, estruturada e didática."
```

### Estrutura básica de prompt

A apresentação recomenda estruturar prompts com os seguintes elementos:

- **Papel:** quem o modelo deve simular ou qual função deve desempenhar.
- **Tarefa:** o que deve ser feito.
- **Contexto:** informações necessárias para orientar a resposta.
- **Formato:** como a resposta deve ser organizada.
- **Restrições:** limites, regras, tom, tamanho ou critérios de qualidade.

Template sugerido:

```text
Papel: {papel}
Tarefa: {instrucao}
Contexto: {dominio}
Formato de resposta: {formato}
Restrições: {regras}
```

## Unidade 4 — Usando o Ollama como Serviço

A apresentação mostra que o Ollama não precisa ser usado apenas no terminal. Ele também expõe um serviço HTTP local, normalmente em:

```text
http://localhost:11434
```

Esse serviço permite integrar modelos locais a aplicações, scripts Python, protótipos web, pipelines de RAG, ferramentas de automação e experimentos com embeddings.

### API nativa

A API nativa do Ollama pode ser usada com chamadas HTTP ou bibliotecas específicas. Ela oferece endpoints para geração, chat, embeddings, listagem de modelos e outras operações.

Exemplo conceitual com `curl`:

```bash
curl http://localhost:11434/api/generate \
  -d '{
    "model": "llama3.2:3b",
    "prompt": "Explique o que é inferência local com LLMs."
  }'
```

### API compatível com OpenAI

A apresentação também destaca a compatibilidade com o padrão da OpenAI, o que facilita adaptar aplicações já existentes para executar localmente.

Exemplo conceitual em Python:

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

response = client.chat.completions.create(
    model="llama3.2:3b",
    messages=[
        {"role": "user", "content": "Explique Ollama em 5 linhas."}
    ]
)

print(response.choices[0].message.content)
```

### Funcionalidades exploradas

A apresentação organiza três funcionalidades práticas importantes:

| Funcionalidade | Objetivo | Exemplo de uso |
|---|---|---|
| Streaming | Receber tokens gradualmente durante a geração. | Chat em tempo real e interfaces interativas. |
| Vision | Enviar imagens para modelos multimodais. | Análise de figuras, prints, diagramas e documentos visuais. |
| Embedding | Gerar vetores de texto. | Busca semântica, RAG, recomendação e similaridade textual. |

## Protótipos relacionados

Além da apresentação, existem três protótipos práticos relacionados ao uso do Ollama em aplicações:

### 1. Streaming

Protótipo voltado para demonstrar geração de respostas em fluxo contínuo, permitindo que o usuário receba partes da resposta à medida que o modelo produz os tokens.

Link: <https://github.com/llmfromzerotohero/ollama/tree/main/streaming>

### 2. Vision

Protótipo voltado para demonstrar o uso de modelos multimodais com Ollama, permitindo o envio e a análise de imagens.

Link: <https://github.com/llmfromzerotohero/ollama/tree/main/vision>

### 3. Embedding

Protótipo voltado para demonstrar a geração de embeddings, que podem ser usados em busca semântica, comparação de textos, recuperação de contexto e aplicações RAG.

Link: <https://github.com/llmfromzerotohero/ollama/tree/main/embedding>

## Unidade 5 — Limitações de Hardware e Boas Práticas

A última parte da apresentação mostra que executar LLMs localmente depende fortemente dos recursos disponíveis. O desempenho e a estabilidade são influenciados por CPU, RAM, VRAM, disco, tamanho do modelo, quantização, tamanho do contexto e volume de requisições.

### Recursos computacionais envolvidos

| Recurso | Função principal | Impacto na inferência |
|---|---|---|
| CPU | Orquestração e inferência quando não há GPU. | Pode funcionar, mas com maior latência. |
| RAM | Armazena pesos, buffers e parte do contexto. | RAM insuficiente causa OOM, swap e lentidão. |
| VRAM | Armazena pesos na GPU e acelera operações matriciais. | Principal recurso para baixa latência. |
| Disco | Armazena modelos e influencia carregamento inicial. | Disco lento aumenta tempo de inicialização. |

### CPU

A inferência em CPU é útil para testes, aulas e modelos pequenos, mas tende a apresentar maior latência. É funcional para protótipos simples, mas não é indicada para uso interativo intenso ou múltiplos usuários simultâneos.

### RAM

A RAM influencia a estabilidade do ambiente. Quando não há memória suficiente, o sistema pode usar swap em disco, encerrar processos ou apresentar respostas extremamente lentas.

### VRAM

A VRAM é crítica para executar modelos médios e grandes com baixa latência. Mesmo que um modelo carregue inicialmente, respostas longas ou contexto maior podem aumentar o consumo e causar instabilidade.

Comando útil para GPUs NVIDIA:

```bash
nvidia-smi
```

### Quantização

A quantização reduz a precisão dos pesos do modelo para diminuir o consumo de memória. A apresentação apresenta a quantização como uma troca entre eficiência e qualidade.

| Formato | Característica | Uso típico |
|---|---|---|
| FP16 | Maior qualidade, maior uso de memória. | GPUs modernas e maior fidelidade. |
| INT8 | Boa relação entre qualidade e eficiência. | Inferência eficiente. |
| INT4/Q4 | Grande economia de memória. | Máquinas com hardware limitado. |

A recomendação central é testar a tarefa real. Uma quantização pode funcionar bem para resumo, mas não ser adequada para geração de código, raciocínio matemático ou tarefas sensíveis.

### Sintomas de saturação

Sinais comuns de que o ambiente local está acima da capacidade:

- Travamentos do sistema.
- Processo finalizado pelo sistema operacional.
- CPU em 100% por longos períodos.
- RAM ou VRAM próximas do limite.
- Uso intenso de swap.
- Respostas muito lentas ou incompletas.
- Aquecimento elevado e queda de desempenho.

### Boas práticas

A apresentação recomenda:

- Começar com modelos pequenos, como 3B ou 7B.
- Usar versões quantizadas em máquinas comuns.
- Testar um modelo por vez.
- Limitar tokens de saída.
- Evitar contextos muito grandes durante desenvolvimento.
- Monitorar CPU, RAM, VRAM e temperatura.
- Documentar comandos, prompts, parâmetros e resultados.
- Separar testes de integração de testes de qualidade.
- Usar inferência local para aprendizagem, prototipação e validação inicial.


## Quando não usar inferência local

A apresentação reforça que o Ollama local não é a solução ideal para todos os cenários. Deve-se considerar outras arquiteturas quando houver:

- Muitos usuários simultâneos.
- Alto volume de requisições.
- SLA rígido de latência e disponibilidade.
- Necessidade de autenticação, auditoria, quotas e logs centralizados.
- Modelos muito grandes para o hardware disponível.
- Necessidade de escalabilidade horizontal com múltiplas GPUs.

Alternativas típicas:

- **vLLM** para serving de alta performance.
- **Clusters GPU** para cargas maiores.
- **Gateways multi-modelo** para governança, roteamento e controle de acesso.
- **Filas e workers** para workloads batch.
- **Observabilidade com métricas e logs** para ambientes de produção.

## Checklist final de laboratório

Antes de considerar o ambiente pronto para aulas ou protótipos, recomenda-se verificar:

- [ ] Ollama instalado e versão registrada.
- [ ] API local respondendo em `http://localhost:11434`.
- [ ] Modelo pequeno baixado e testado.
- [ ] Diretório de modelos identificado.
- [ ] Espaço em disco verificado.
- [ ] Prompt, parâmetros e tag documentados.
- [ ] CPU, RAM, VRAM e temperatura monitoradas.
- [ ] Resultados registrados em arquivo ou planilha.
- [ ] Evidências salvas para reprodução do experimento.

Estrutura sugerida para um laboratório reprodutível:

```text
resultado_esperado/
  README.md
  ambiente.md
  prompts/
  modelfiles/
  resultados.csv
  evidencias/
    print_ollama_ps.png
    nvidia_smi.txt
```

## Conclusão

O Ollama é uma ferramenta adequada para introduzir estudantes e desenvolvedores à hospedagem local de LLMs. Ele reduz a complexidade inicial de instalação e execução, oferece integração via CLI e API, permite experimentos com modelos abertos e facilita a criação de protótipos com streaming, visão e embeddings.

A principal mensagem da apresentação é que executar LLMs localmente exige controle técnico. O sucesso do laboratório depende menos de simplesmente “rodar um modelo” e mais de compreender o ambiente, registrar versões, controlar parâmetros, monitorar recursos e reconhecer os limites entre prototipação local e arquitetura de produção.
