# Análise sobre Poetry Workspaces e Documentação Oficial

Analisei o arquivo `workspace.md` que você forneceu e pesquisei sobre o suporte oficial a "Workspaces" no Poetry, incluindo versões recentes como a 2.x.

## Veracidade das Informações em `workspace.md`

O arquivo [[workspace]] descreve muito bem os **conceitos e objetivos** de gerenciar um monorepo (múltiplos pacotes em um único repositório) com Poetry:

*   Uso de um ambiente virtual único compartilhado.
*   `pyproject.toml` individuais para cada subprojeto (pacote) com suas dependências específicas.
*   `pyproject.toml` na raiz para dependências de desenvolvimento comuns e para orquestrar o monorepo.
*   Capacidade de adicionar dependências a subprojetos específicos.
*   Uso de `poetry run` para executar comandos.
*   Imports absolutos funcionando entre os subprojetos.

**No entanto, um ponto crucial precisa de esclarecimento:**

*   **A sintaxe `[tool.poetry.workspaces]` com `members = [...]` (ou `dependencies = [...]` como no meu exemplo anterior) não parece ser uma funcionalidade oficial e documentada das versões estáveis do Poetry até o momento (incluindo a linha 2.x).**
*   Minhas pesquisas na documentação oficial e discussões na comunidade (GitHub issues) não encontraram essa seção `[tool.poetry.workspaces]` como parte do core do Poetry.
*   Essa sintaxe pode pertencer a:
    *   Um **plugin de terceiros** (como `poetry-workspace-plugin` ou `poetry-monoranger-plugin` que foram mencionados nos resultados da busca).
    *   Uma **funcionalidade experimental** ou proposta que ainda não foi incorporada oficialmente.
    *   Uma convenção adotada por algumas ferramentas que se integram ao Poetry.

**Portanto, embora a *ideia* de workspaces descrita no arquivo esteja correta e seja um objetivo comum, a *implementação específica* usando `[tool.poetry.workspaces]` não é o método padrão ou oficialmente documentado pelo Poetry.**

## Abordagem Oficial e Documentada: Path Dependencies

A maneira **oficial e documentada** pelo Poetry para alcançar um resultado muito similar (gerenciar múltiplos pacotes locais em um monorepo e permitir imports entre eles) é usando **Path Dependencies** (Dependências de Caminho).

Isso corresponde à alternativa que mencionei anteriormente e que também é citada brevemente no seu arquivo `workspace.md`:

1.  Você tem um `pyproject.toml` na **raiz** do seu projeto (`projeto_lstm_acoes/`).
2.  Neste `pyproject.toml` da raiz, você declara cada um dos seus subdiretórios (`app`, `data_pipeline`, `ml_lifecycle`) como uma dependência, usando a chave `path` e `develop = true`.

    ```toml
    # projeto_lstm_acoes/pyproject.toml
    [tool.poetry.dependencies]
    python = "^3.10"
    # ... outras dependências comuns

    # Declarando os pacotes locais como dependências
    stock-prediction-app = { path = "app", develop = true }
    stock-prediction-data-pipeline = { path = "data_pipeline", develop = true }
    stock-prediction-ml-lifecycle = { path = "ml_lifecycle", develop = true }

    # ... dependências de dev
    ```
3.  Cada subdiretório (`app/`, `data_pipeline/`, `ml_lifecycle/`) ainda tem seu próprio `pyproject.toml` definindo suas dependências *específicas* e como ele é um pacote (usando `packages = [{include = "app"}]`, etc.).
4.  Ao executar `poetry install` na raiz, o Poetry instala todas as dependências e também cria os links necessários para que `app`, `data_pipeline` e `ml_lifecycle` sejam reconhecidos como pacotes instalados no ambiente virtual, permitindo imports cruzados.

Esta abordagem com `path dependencies` alcança o mesmo resultado funcional principal descrito no seu arquivo `workspace.md` (ambiente único, imports cruzados, gerenciamento via Poetry), mas usando a sintaxe oficialmente suportada e documentada.

## Onde Consultar a Documentação Oficial

Como a funcionalidade `[tool.poetry.workspaces]` não parece ser oficial, você não a encontrará na documentação principal. Os links relevantes na documentação oficial do Poetry são:

1.  **Página Principal da Documentação:** Ponto de partida geral.
    *   [https://python-poetry.org/docs/](https://python-poetry.org/docs/)
2.  **Especificação de Dependências (inclui Path Dependencies):** Explica como usar `path = 

"...` para declarar dependências locais.
    *   [https://python-poetry.org/docs/dependency-specification/#path-dependencies](https://python-poetry.org/docs/dependency-specification/#path-dependencies)
3.  **Estrutura do `pyproject.toml`:** Descreve todas as seções e campos possíveis no arquivo.
    *   [https://python-poetry.org/docs/pyproject/](https://python-poetry.org/docs/pyproject/)

Para funcionalidades específicas de "workspaces" como descritas no seu arquivo (com a chave `[tool.poetry.workspaces]`), você precisaria consultar a documentação dos **plugins específicos** que implementam essa funcionalidade, como os mencionados (`poetry-workspace-plugin`, `poetry-monoranger-plugin`), pois não fazem parte do core oficial do Poetry.

## Conclusão

O arquivo `workspace.md` descreve corretamente o *objetivo* de gerenciar monorepos com Poetry, mas a sintaxe específica `[tool.poetry.workspaces]` não é oficial. A abordagem **oficial e recomendada** pelo Poetry para alcançar esse objetivo é usar **Path Dependencies** no `pyproject.toml` da raiz do projeto, conforme detalhado acima e na documentação oficial.

