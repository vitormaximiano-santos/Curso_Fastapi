from models import db # "db" é o objeto que armazena a conexão com o banco de dados
from sqlalchemy.orm import sessionmaker # sessionmaker é uma classe que gerencia a sessão do banco de dados

# dependência para o banco de dados
def pegar_sessao():
    try:
        session = sessionmaker(bind=db) # bind é o objeto que armazena a conexão com o banco de dados
        session = session()
        yield session # yield é uma palavra reservada do Python que permite que a função retorne um valor,sem finalizar a função
    finally:    
        session.close()