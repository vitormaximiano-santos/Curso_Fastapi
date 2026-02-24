from fastapi import APIRouter,  Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import SchemaPedido
from models import Pedido, Usuario

# rotas para autenticação
order_router = APIRouter(prefix="/pedidos", tags=["pedidos"],dependencies=[Depends(verificar_token)] )# "APIRouter" é uma classe que define rotas
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

@order_router.post("/pedido") # usa @order_router.post() para registrar a rota
# '/pedido' faz com que a função seja executada quando o usuário acessa a rota /pedido/

async def criar_pedido(SchemaPedido: SchemaPedido,session: Session = Depends(pegar_sessao)): # usa async def para registrar a função que será executada quando a rota for acessada
    
    novo_pedido = Pedido(usuario = SchemaPedido.usuario)
    
    session.add(novo_pedido)
    
    session.commit()
    
    # a função criar_pedido() retorna um dicionário com a mensagem "Mensagem"
    return {"Mensagem": f"Pedido criado com sucesso, id do usuario: {novo_pedido.usuario}"}


@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao),usuario:Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    if not Usuario.admin and Usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem permissão para cancelar esse pedido")
    
    pedido.status = "cancelado"
    session.commit()
    return {
        "Mensagem": f"Pedido número {pedido.id} foi cancelado com sucesso",
        "pedido": pedido
        }
    

