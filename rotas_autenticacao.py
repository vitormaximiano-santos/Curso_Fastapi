from fastapi import APIRouter,HTTPException ,Depends # Depends é uma função que recebe uma função como parâmetro e retorna o resultado da função
from models import Usuario
from dependencies import pegar_sessao
from main import bcript_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import SchemaUsuario, SchemaLogin
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

def criar_token(id_usuario,duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_informacoes = {"id_usuario": id_usuario,"exp": data_expiracao}
    jwt_token = jwt.encode(dic_informacoes, SECRET_KEY,ALGORITHM)
    token = f"awifs2jde23j2dka{id_usuario}"
    return jwt_token

def verificar_token(token, session:Session = Depends(pegar_sessao)):
    # verifica se o token é válido
    # extrai o id_usuario do token
    usuario= Session.query(Usuario).filter(Usuario.id == 1).first()
    return usuario

def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False # Retorna False se o usuário não for encontrado
   
    elif not bcript_context.verify(senha, usuario.senha): # Verifica se a senha do usuário é a mesma
        return False # Retorna False se a senha não for a mesma
        
    return usuario

# rotas para autenticação
auth_router = APIRouter(prefix="/auth", tags=["auth"])
# "APIRouter" é uma classe que define rotas
# "prefix" é o caminho para a rota,serve para organizar as rotas
# "tags" é uma lista de tags para a rota, ajuda a organizar as rotas

#  prefix x tags: a diferença é que prefix é o caminho(rota) e tags são as categorias , ou seja, você pode ter várias rotas com o mesmo prefixo, mas cada rota pode ser associada a uma tag diferente

@auth_router.get("/")
async def home(): # usa async def para registrar a função que será executada quando a rota for acessada
    """
    Essa é a rota padrão de autenticação do sistema
    """
    return {"Mensagem": "Voçe acessou a rota /auth/, e esta em autenticação"}

@auth_router.post("/Criar_Conta")
async def criar_conta(Schema_Usuario: SchemaUsuario, session:Session = Depends(pegar_sessao)):
    # Verifica se já existe usuário com o mesmo email
    usuario = session.query(Usuario).filter(Usuario.email == Schema_Usuario.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    else:   
        # Criptografa a senha
        senha_criptada = bcript_context.hash(Schema_Usuario.senha)
        # Cria novo usuário (ajustando ordem dos parâmetros)
        novo_usuario = Usuario(Schema_Usuario.nome, Schema_Usuario.email, senha_criptada, Schema_Usuario.ativo, Schema_Usuario.admin)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"Conta criada com sucesso: {Schema_Usuario.email}"}

@auth_router.post("/Login")
async def login(Schema_Login: SchemaLogin, session:Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(Schema_Login.email, Schema_Login.senha, session)  
    if not usuario:
       raise HTTPException(status_code=400, detail="Usuário não encontrado, ou senha incorreta")
    else:
      access_token = criar_token(usuario.id)
      refresh_token = criar_token(usuario.id,duracao_token=timedelta(days=7))
      return {"access_token": access_token,
              "refresh_token": refresh_token,
              "token_type": "bearer"
             }
      
@auth_router.post("/Refresh_Token")
async def use_refresh_token(token):
    usuario = verificar_token(token)
    access_token = criar_token(usuario.id)
    return {"access_token": access_token,
              "token_type": "bearer"
             }