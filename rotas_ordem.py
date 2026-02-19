from fastapi import APIRouter

# rotas para autenticação
order_router = APIRouter(prefix="/pedidos", tags=["pedidos"])# "APIRouter" é uma classe que define rotas
# "prefix" é o caminho para a rota,serve para organizar as rotas
# "tags" é uma lista de tags para a rota, ajuda a organizar as rotas

#  prefix x tags: a diferença é que prefix é o caminho(rota) e tags são as categorias , ou seja, você pode ter várias rotas com o mesmo prefixo, mas cada rota pode ser associada a uma tag diferente

# rotas para pedidos
@order_router.get("/") # usa @order_router.get() para registrar a rota
# '/' faz com que a função seja executada quando o usuário acessa a rota /order/

async def pedidos(): # usa async def para registrar a função que será executada quando a rota for acessada
    
    # a função pedidos() retorna um dicionário com a mensagem "Mensagem"
    return {"Mensagem": "Voçe acessou a rota /order/, e está retornando uma mensagem"}

# por enquanto, para acessar essa rota, digite http://127.0.0.1:8000/pedidos/