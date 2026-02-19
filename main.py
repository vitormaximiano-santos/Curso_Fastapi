from fastapi import FastAPI

app = FastAPI()

# para ativar o app, execute o comando abaixo no terminal:
# # uvicorn main:app --reload 
# "--reload" é para recarregar o app quando o arquivo for alterado
# "uvicorn" é o servidor que irá executar o app
# "main:app" é o nome do app definido acima "app = FastAPI()"

from rotas_ordem import order_router
from rotas_autenticação import auth_router

from fastapi import FastAPI
from rotas_ordem import order_router   # importa o router

app = FastAPI()

# Inclui o router na aplicação principal
app.include_router(order_router)
app.include_router(auth_router)
