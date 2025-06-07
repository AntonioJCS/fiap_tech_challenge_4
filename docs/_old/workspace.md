# 🧭 Contexto Geral

Você está estruturando um projeto Python voltado para Data Science e Machine Learning, que envolve múltiplas “camadas” ou subprojetos:

- Uma API (`app`)
    
- Um pipeline de dados (`data_pipeline`)
    
- Um ciclo de vida de modelos (`ml_lifecycle`)
    

Seu objetivo é criar um ambiente bem organizado, desacoplado, escalável e fácil de manter, utilizando **Poetry** para gerenciamento de dependências e ambientes virtuais.

---

# 🏗️ Estrutura Monorepo com Workspaces

## 📂 Organização Geral

O padrão sugerido é o **monorepo** com múltiplos pacotes Python, cada um representando um “componente” do seu sistema.  
Exemplo de estrutura:

```
projeto_lstm_acoes/
│
├── pyproject.toml           # Workspace principal
├── .env                     # Variáveis de ambiente centralizadas
├── app/
│   ├── pyproject.toml       # API
│   └── ...
├── data_pipeline/
│   ├── pyproject.toml       # Pipeline de dados
│   └── ...
├── ml_lifecycle/
│   ├── pyproject.toml       # Ciclo de vida do ML
│   └── ...
```

Cada subprojeto tem sua própria configuração e dependências, mas o ambiente virtual é único para o workspace.

---

# 📦 Poetry Workspaces: Gerenciando Dependências em Monorepos

## 🚩 O que são Workspaces?

- Permitem que vários pacotes Python sejam desenvolvidos em um único repositório.
    
- Poetry cria **um único ambiente virtual**, compartilhado entre todos os subprojetos.
    
- Cada subprojeto tem seu próprio `pyproject.toml` com dependências específicas.
    

## 📝 Criando os Arquivos `pyproject.toml`

### 1️⃣ Arquivo na raiz do workspace

Esse arquivo **não contém código**, apenas:

- Metadados do projeto principal (nome, autor, etc.)
    
- Dependências **de desenvolvimento** (ex: `pytest`, `black`)
    
- Declaração dos workspaces (quais subpastas fazem parte do monorepo)
    

**Exemplo:**

```toml
[tool.poetry]
name = "projeto-lstm-acoes-workspace"
version = "0.1.0"
description = "Workspace principal para o projeto LSTM de Ações."
authors = ["Seu Nome <seu_email@example.com>"]

[tool.poetry.dependencies]
python = "^3.10"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4"
black = "^24.3.0"

[tool.poetry.workspaces]
members = [
    "app",
    "data_pipeline",
    "ml_lifecycle"
]

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

> **Obs:** Normalmente não há dependências de produção na raiz; só se todas as camadas realmente precisarem.

---

### 2️⃣ Arquivo em cada subprojeto

Cada subprojeto (`app/`, `data_pipeline/`, `ml_lifecycle/`) deve ter seu **próprio** `pyproject.toml`, criado com:

```bash
cd app
poetry init --no-interaction
# Depois edite o arquivo e preencha os campos corretamente.
```

Exemplo para a API:

```toml
[tool.poetry]
name = "stock-prediction-app"
version = "0.1.0"
description = "API para previsão de ações."
authors = ["Seu Nome <seu_email@example.com>"]
packages = [{include = "app"}]

[tool.poetry.dependencies]
python = "^3.10"
fastapi = "^0.110.0"
uvicorn = {extras = ["standard"], version = "^0.29.0"}
pydantic-settings = "^2.2.1"
sqlalchemy = "^2.0.23"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

> Repita o processo nos outros subprojetos, ajustando nome, descrição e dependências.

---

# 🚀 Adicionando/Removendo Pacotes

## 🧭 Como instalar pacotes em cada subprojeto?

- **Navegue até a pasta do subprojeto** desejado (ex: `cd ml_lifecycle`)
    
- Use `poetry add nome-do-pacote` para adicionar dependências só naquele pacote.
    
- O Poetry atualiza o `pyproject.toml` daquele subprojeto e o arquivo `poetry.lock` global.
    
- O pacote fica disponível para uso no ambiente virtual do monorepo, mas só é **"oficial"** para aquele subprojeto.
    

|Subpasta atual|Comando|Efeito|
|---|---|---|
|`app/`|`poetry add requests`|Só o `app/pyproject.toml` é atualizado|
|`data_pipeline/`|`poetry add pandas`|Só o `data_pipeline/pyproject.toml`|
|`ml_lifecycle/`|`poetry add scikit-learn`|Só o `ml_lifecycle/pyproject.toml`|

> Isso vale para **remover** (`poetry remove nome-do-pacote`) e **atualizar** (`poetry update nome-do-pacote`) também.

---

# 🏃‍♂️ Rodando Scripts e Importando entre Camadas

- Sempre rode scripts pelo ambiente virtual do workspace:
    
    ```bash
    poetry run python app/main.py
    poetry run python data_pipeline/run_pipeline.py
    ```
    
- Imports absolutos entre subprojetos funcionam (ex: `from ml_lifecycle.models import ...`), desde que cada subprojeto seja um pacote Python com sua própria pasta interna (`app/app/`, `data_pipeline/data_pipeline/`, etc).
    

---

# 🧩 Path Dependencies vs. Workspaces

- **Workspaces** (abordagem moderna):  
    Uso do campo `[tool.poetry.workspaces]` com `members = [...]` — cada subprojeto com seu próprio pacote.
    
- **Path dependencies** (alternativa):  
    Você poderia (em versões antigas do Poetry ou projetos simples) declarar cada subpacote como dependência de caminho no `pyproject.toml` da raiz, mas Workspaces são mais limpos, modernos e prontos para monorepo.
    

---

# ⚠️ Pontos de Atenção e Boas Práticas

- **Nunca manipule manualmente ********`PYTHONPATH`******** ou ********`sys.path`**: Deixe o Poetry gerenciar tudo.
    
- **Dependências de DEV** (testes, linters, etc.) devem ficar na raiz do workspace.
    
- **Documente suas configurações** em README para facilitar onboarding do time.
    
- **Segregue variáveis sensíveis no ********`.env`**, nunca em código.
