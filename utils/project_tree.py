from pathlib import Path


def project_tree(dir, ignore=None):
    """
    Imprime a estrutura de diretórios e arquivos de forma hierárquica no estilo árvore.

    Args:
        dir (str or Path): Caminho do diretório raiz que será impresso.
        ignore (list, opcional): Lista de nomes de diretórios ou arquivos a serem ignorados.
    """
    if ignore is None:
        ignore = []

    dir = Path(dir).expanduser().resolve()

    def explorar(caminho, prefixo=""):
        try:
            itens = sorted([item for item in caminho.iterdir() if item.name not in ignore], key=lambda x: x.name.lower())
        except PermissionError:
            print(prefixo + "└── [Sem permissão]")
            return
        except FileNotFoundError:
            print(prefixo + "└── [Não encontrado]")
            return

        total = len(itens)
        for indice, item in enumerate(itens):
            marcador = "└── " if indice == total - 1 else "├── "
            print(prefixo + marcador + item.name)

            if item.is_dir():
                extensao_prefixo = "    " if indice == total - 1 else "│   "
                explorar(item, prefixo + extensao_prefixo)

    if not dir.is_dir():
        print(f"O caminho '{dir}' não é um diretório válido.")
        return

    print(f"{dir.name}/")
    explorar(dir)


if __name__ == "__main__":

    import os
    print("CWD:", os.getcwd())
    print("PYTHONPATH:", os.environ.get("PYTHONPATH"))

    project_tree(
        dir=Path(__file__).parent.parent.parent.resolve(),
        ignore=[".git", "__pycache__", ".venv", "tools", "infile", "outfile", "docs"]
    )