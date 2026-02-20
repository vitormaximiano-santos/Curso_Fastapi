from fastapi import APIRouter

# rotas para autenticação
auth_router = APIRouter(prefix="/auth", tags=["auth"])
# "APIRouter" é uma classe que define rotas
# "prefix" é o caminho para a rota,serve para organizar as rotas
# "tags" é uma lista de tags para a rota, ajuda a organizar as rotas

#  prefix x tags: a diferença é que prefix é o caminho(rota) e tags são as categorias , ou seja, você pode ter várias rotas com o mesmo prefixo, mas cada rota pode ser associada a uma tag diferente

@auth_router.get("/")
async def autenticacao(): # usa async def para registrar a função que será executada quando a rota for acessada
    """
    Essa é a rota padrão de autenticação do sistema
    """
    return {"Mensagem": "Voçe acessou a rota /auth/, e esta em autenticação"}