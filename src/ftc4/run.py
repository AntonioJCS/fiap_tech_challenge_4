import uvicorn

def main_public():
    """Função de entrada para o modo publico."""
    uvicorn.run("ftc4.api.public:app", reload=True)

def main_admin():
    """Função de entrada para o modo de administração."""
    uvicorn.run("ftc4.api.admin:app", reload=True)

if __name__ == "__main__":
    main_public()