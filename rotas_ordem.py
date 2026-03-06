from fastapi import APIRouter,  Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import SchemaPedido, SchemaItemPedido, SchemaUsuario, SchemaResponsePedido
from models import Pedido, Usuario, ItemPedido
from typing import List


order_router = APIRouter(prefix="/pedidos", tags=["pedidos"],dependencies=[Depends(verificar_token)] )

@order_router.get("/") 
async def pedidos(): 
   
    return {"Mensagem": "Voçe acessou a rota /order/, e está retornando uma mensagem"}


@order_router.post("/pedido") 

async def criar_pedido(SchemaPedido: SchemaPedido,session: Session = Depends(pegar_sessao)): 
    
    novo_pedido = Pedido(usuario = SchemaPedido.usuario)
    
    session.add(novo_pedido)
    
    session.commit()
    
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
    

@order_router.get("/listar_pedidos")
async def listar_pedidos(session: Session = Depends(pegar_sessao),usuario:Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não tem permissão para acessar essa rota")
    
    else:
        pedidos = session.query(Pedido).all()
        return {
            "pedidos": pedidos
            }
        
    
@order_router.post("/pedido/adicionar_item/{id_pedido}")
async def adicionar_item(id_pedido:int,
                         item_pedido_schema:SchemaItemPedido,
                         session: Session = Depends(pegar_sessao),
                         usuario:Usuario = Depends(verificar_token)):
    
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem permissão para adicionar item a esse pedido")
    
    item_pedido = ItemPedido(quantidade=item_pedido_schema.quantidade,
                             sabor=item_pedido_schema.sabor,
                             tamanho=item_pedido_schema.tamanho,
                             preco_unitario=item_pedido_schema.preco_unitario,
                             pedido=pedido.id)
    
    
    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        "mensagem": f"Item adicionado com sucesso",
        "item": item_pedido
        }
    

@order_router.post("/pedido/remover_item/{id_pedido}")
async def adicionar_item(id_item_pedido:int,
                         session: Session = Depends(pegar_sessao),
                         usuario:Usuario = Depends(verificar_token)):
    
    item_pedido = session.query(ItemPedido).filter(ItemPedido.id == id_item_pedido).first()
    pedido = session.query(Pedido).filter(Pedido.id == item_pedido.pedido).first()
    
    if not item_pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem permissão para remover um item a esse pedido")
    
    session.delete(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        "mensagem": f"Item removidos com sucesso",
        "quantidade_itens_pedidos": len(pedido.itens),
        "pedido": pedido    
        } 
    

@order_router.post("/pedido/finalizar/{id_pedido}")
async def finalizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao),usuario:Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    
    if not Usuario.admin and Usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem permissão para finalizar esse pedido")
    
    pedido.status = "finalizado"
    session.commit()
    return {
        "Mensagem": f"Pedido número {pedido.id} finalizado com sucesso",
        "pedido": pedido
        }
    
@order_router.get("/pedido/{id_pedido}")
async def visualizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao),usuario:Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    
    if not Usuario.admin and Usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem permissão para visualizar esse pedido")
    
    return {
        "Quantidade de itens": len(pedido.itens),
        "Pedido": pedido
    }
    
@order_router.get("/listar/pedidos-usuario",response_model=List[SchemaResponsePedido])
def listar_pedidos_usuario(session: Session = Depends(pegar_sessao),usuario:Usuario = Depends(verificar_token)):
    pedidos = session.query(Pedido).filter(Pedido.usuario == usuario.id).all()
    return  pedidos
    