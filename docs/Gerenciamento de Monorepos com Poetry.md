## 🎯 Objetivo

Garantir o gerenciamento correto de múltiplos subprojetos em um monorepo utilizando Poetry, evitando erros como `no module`.

## 📂 Estrutura Recomendada Oficial

```bash
monorepo/
│
├── pyproject.toml
├── .env
├── app/
│   ├── pyproject.toml
│   └── main.py
├── data_pipeline/
│   ├── pyproject.toml
│   └── data_pipeline/
│       └── __init__.py
├── ml_lifecycle/
│   ├── pyproject.toml
│   └── ml_lifecycle/
        └── __init__.py
```

## 🔧 Configuração Oficial (Passo a Passo)

- O método oficial suportado e documentado pelo Poetry utiliza [Path Dependencies](https://python-poetry.org/docs/dependency-specification/).

### 1️⃣ Criar Arquivo `pyproject.toml` na Raiz

```toml
[tool.poetry]
name = "projeto-lstm-acoes-workspace"
version = "0.1.0"
description = "Workspace principal para o projeto LSTM de Ações."
authors = ["Seu Nome <seu_email@example.com>"]

[tool.poetry.dependencies]
python = "^3.10"
app = { path = "app", develop = true }
data_pipeline = { path = "data_pipeline", develop = true }
ml_lifecycle = { path = "ml_lifecycle", develop = true }

[tool.poetry.group.dev.dependencies]
pytest = "^7.4"
black = "^24.3.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

### 2️⃣ Configuração Individual dos Subprojetos

Cada subprojeto deve ter seu próprio `pyproject.toml`. Exemplo para o subprojeto `app`:

```toml
[tool.poetry]
name = "app"
version = "0.1.0"
description = "API para previsão de ações."
authors = ["Seu Nome <seu_email@example.com>"]
packages = [{include = "app"}]

[tool.poetry.dependencies]
python = "^3.10"
fastapi = "^0.110.0"
uvicorn = {extras = ["standard"], version = "^0.29.0"}

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

Repita esse procedimento para cada subprojeto, ajustando dependências específicas.

### 3️⃣ Instalando Dependências

Na raiz do monorepo, rode:

```bash
poetry install
```

Isso cria um único ambiente virtual compartilhado com dependências de todos os subprojetos.

### 4️⃣ Gerenciando Pacotes Individuais

Para adicionar uma dependência a um subprojeto específico:

```bash
cd app
poetry add fastapi
```

### 5️⃣ Executando Projetos

Use sempre o ambiente Poetry para executar scripts:

```bash
poetry run python app/main.py
poetry run python data_pipeline/data_pipeline/pipeline.py
```

### 6️⃣ Imports Entre Subprojetos

Use imports absolutos desde que pacotes estejam corretamente configurados:

```python
from ml_lifecycle import modelo
```

### 🚩 Pontos de Atenção

- Evite alterar manualmente variáveis como `PYTHONPATH` ou `sys.path`.
    
- Centralize dependências comuns e ferramentas de desenvolvimento na raiz.
    
- Sempre documente claramente o processo no README do projeto.
    

## ❓ Situações Comuns

### 1. Modificações em módulos existentes após `poetry install`

Após executar `poetry install`, você pode modificar livremente os módulos e arquivos dentro dos pacotes, pois o Poetry utiliza **symlinks** (links simbólicos) para pacotes locais com `develop = true`. Assim, alterações feitas localmente refletem-se imediatamente, sem precisar reinstalar ou atualizar pacotes constantemente.

✅ **Conclusão:** Alterações locais podem ser feitas livremente.

---

### 2. Adicionando um novo pacote após o `poetry install`

Ao adicionar uma nova camada (novo pacote), você precisa:

- Criar um novo diretório com seu próprio `pyproject.toml`.
    
- Referenciar esse novo pacote no `pyproject.toml` da raiz, usando dependências locais com `path` e `develop=true`.
    
- Rodar novamente `poetry install` para que o Poetry inclua o novo pacote corretamente no ambiente virtual.
    

Exemplo atualizado no `pyproject.toml` raiz:

```toml
[tool.poetry.dependencies]
python = "^3.10"
app = { path = "app", develop = true }
data_pipeline = { path = "data_pipeline", develop = true }
ml_lifecycle = { path = "ml_lifecycle", develop = true }
novo_pacote = { path = "novo_pacote", develop = true }
```

✅ **Conclusão:** Ao adicionar um novo pacote, atualize o `pyproject.toml` e execute novamente `poetry install`.

---

### 3. Pacotes instalados no `.venv` ou symlinks?

Os pacotes **externos** são instalados no ambiente virtual (`.venv`). Já os pacotes locais (com `develop = true`) usam **symlinks**, permitindo que qualquer alteração feita localmente esteja disponível imediatamente.

✅ **Conclusão:** Pacotes locais usam symlinks; externos ficam no `.venv`.

---

### 4. Uso do `python -m` ao invés de `poetry run python`

Você pode utilizar diretamente o Python desde que o ambiente virtual gerado pelo Poetry esteja ativado:

- Ative o ambiente virtual:
    

```bash
source .venv/bin/activate   # Linux/Mac
.venv\\Scripts\\activate    # Windows
```

- Após ativar, use diretamente:
    

```bash
python -m app.main
```

✅ **Conclusão:** É possível usar `python -m`, desde que o ambiente Poetry esteja ativado.

---

### 5. Criando o `.venv` sem o Poetry instalado localmente

Se Poetry não estiver instalado globalmente, você pode usar uma instalação isolada do Poetry via `pipx` ou executar diretamente o script de instalação temporária recomendado oficialmente pelo Poetry:

- Instalação temporária via script:
    

```bash
curl -sSL https://install.python-poetry.org | python -
```

- Instalação via pip (menos recomendado oficialmente, mas possível):
    

```bash
pip install poetry
```

✅ **Conclusão:** É recomendado instalar temporariamente o Poetry se não estiver disponível.

---

### 6. Execução direta com Python sem Poetry instalado no sistema

Se alguém clonar seu projeto sem Poetry instalado e tentar executar diretamente `python -m` sem ativar o ambiente virtual:

- **Vai dar erro**, pois as dependências não estarão instaladas no ambiente padrão do Python da máquina do usuário.
    
- É preciso ter o Poetry para instalar dependências e configurar o ambiente virtual corretamente.
    

Alternativa recomendada no seu README:

- Incluir instruções detalhadas para instalação do Poetry e ativação do ambiente.
    

Exemplo rápido:

```bash
curl -sSL https://install.python-poetry.org | python -
poetry install
source .venv/bin/activate
python -m app.main
```

✅ **Conclusão:** Sem Poetry ou ambiente virtual ativado, ocorrerá erro ao executar.

---

💡 **Sugestão adicional:**  
Sempre inclua um guia breve de instalação e uso no seu README para garantir que outros usuários consigam executar o projeto facilmente.

---

Essas práticas garantem clareza, eficiência e uma boa experiência ao utilizar Poetry em monorepos. 🚀📚

## 📖 Documentação Oficial

- [Página principal Poetry](https://python-poetry.org/docs/)
    
- [Path Dependencies](https://python-poetry.org/docs/dependency-specification/#path-dependencies)
    
- [Estrutura do pyproject.toml](https://python-poetry.org/docs/pyproject/)