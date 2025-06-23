from fastapi import HTTPException, Header

def verify_token(authorization: str = Header(...)):
    if authorization != "Bearer meu_token_secreto":
        raise HTTPException(status_code=401, detail="Token inválido")
