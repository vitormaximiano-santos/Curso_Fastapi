from fastapi import FastAPI
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

load_dotenv()  # carrega variáveis do .env

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

app = FastAPI()

# para ativar o app, execute o comando abaixo no terminal:
#  uvicorn main:app --reload 
# "--reload" é para recarregar o app quando o arquivo for alterado
# "uvicorn" é o servidor que irá executar o app
# "main:app" é o nome do app definido acima "app = FastAPI()"

bcript_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # cria um objeto de contexto para bcrypt, que é usado para criptografar senhas: 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/Login_form")


from rotas_ordem import order_router
from rotas_autenticacao import auth_router

from fastapi import FastAPI
from rotas_ordem import order_router   # importa o router

app = FastAPI()

# Inclui o router na aplicação principal
app.include_router(order_router)
app.include_router(auth_router)
