from fastapi import APIRouter,HTTPException ,Depends # Depends é uma função que recebe uma função como parâmetro e retorna o resultado da função
from models import Usuario
from dependencies import pegar_sessao
from main import bcript_context
from schemas import SchemaUsuario, SchemaLogin
from sqlalchemy.orm import Session

def criar_token(id_usuario):
    token = f"awifs2jde23j2dka{id_usuario}"
    return token

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
    usuario = session.query(Usuario).filter(Usuario.email == SchemaUsuario.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    else:   
        # Criptografa a senha
        senha_criptada = bcript_context.hash(SchemaUsuario.senha)
        # Cria novo usuário (ajustando ordem dos parâmetros)
        novo_usuario = Usuario(SchemaUsuario.nome, SchemaUsuario.email, senha_criptada, SchemaUsuario.ativo, SchemaUsuario.admin)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"Conta criada com sucesso: {SchemaUsuario.email}"}

@auth_router.post("/Login")
async def login(Schema_Login: SchemaLogin, session:Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email == Schema_Login.email).first() # Verifica se já existe usuário com o mesmo email
    if not Usuario:
       raise HTTPException(status_code=400, detail="Usuário não encontrado")
    else:
      access_token = criar_token(Usuario.id)
      return {"access_token": access_token,
              "token_type": "bearer",
             }