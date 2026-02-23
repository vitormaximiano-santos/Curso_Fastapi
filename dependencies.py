from fastapi import Depends, HTTPException
from main import SECRET_KEY, ALGORITHM, oauth2_scheme
from models import db # "db" é o objeto que armazena a conexão com o banco de dados
from sqlalchemy.orm import sessionmaker,Session # sessionmaker é uma classe que gerencia a sessão do banco de dados
from models import Usuario
from jose import jwt, JWTError


# dependência para o banco de dados
def pegar_sessao():
    try:
        session = sessionmaker(bind=db) # bind é o objeto que armazena a conexão com o banco de dados
        session = session()
        yield session # yield é uma palavra reservada do Python que permite que a função retorne um valor,sem finalizar a função
    finally:    
        session.close()
        

def verificar_token(token:str = Depends(oauth2_scheme), session:Session = Depends(pegar_sessao)):
    try:
        dic_info  = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = int(dic_info.get("sub"))
        
    except JWTError:
         raise HTTPException(status_code=400, detail="Acesso negado,verifique a validade do token")
    # verifica se o token é válido
    # extrai o id_usuario do token
    usuario= session.query(Usuario).filter(Usuario.id == id_usuario).first()
             
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso negado, usuário não encontrado")
    return usuario