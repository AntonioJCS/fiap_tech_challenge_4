from pathlib import Path

def project_tree_generate(
    root_path: str,
    ignore: list[str] = None,
    no_expand: list[str] = None,
    prefixo: str = ""
) -> str:
    """
    Gera um diagrama de árvore da estrutura de pastas.

    Parâmetros:
    - root_path (str): Caminho base para gerar a árvore.
    - ignore (list): Lista de nomes de arquivos ou pastas a serem ignorados.
    - no_expand (list): Lista de pastas que não devem ser expandidas (exibidas apenas como nome/).
    - prefixo (str): Usado para recursão, ignora ao usar externamente.

    Retorna:
    - str: Árvore de diretórios em formato de string.
    """
    ignore = set(ignore or [])
    no_expand = set(no_expand or [])
    path = Path(root_path)
    estrutura = ""

    def montar_arvore(p: Path, prefixo: str = "") -> str:
        linhas = []
        itens = sorted([i for i in p.iterdir() if i.name not in ignore], key=lambda x: (not x.is_dir(), x.name.lower()))
        total = len(itens)

        for idx, item in enumerate(itens):
            marcador = "└── " if idx == total - 1 else "├── "
            if item.is_dir():
                linhas.append(f"{prefixo}{marcador}{item.name}/")
                if item.name not in no_expand:
                    nova_prefixo = prefixo + ("    " if idx == total - 1 else "│   ")
                    linhas.append(montar_arvore(item, nova_prefixo))
            else:
                linhas.append(f"{prefixo}{marcador}{item.name}")
        return "\n".join(linhas)

    estrutura += f"{path.name}/\n"
    estrutura += montar_arvore(path)
    return print(estrutura)


if __name__ == "__main__":
    from config import PROJECT_ROOT_DIR
    project_tree_generate(
        root_path=PROJECT_ROOT_DIR,
        ignore=['.venv', '__pycache__', '.git'],
        no_expand=['docs', 'tests', 'logs'] 
        )