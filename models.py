from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey  # SQLAlchemy: biblioteca para trabalhar com banco de dados
from sqlalchemy.orm import declarative_base  # SQLAlchemy ORM: permite trabalhar com objetos relacionados ao banco
#from sqlalchemy_utils.types import ChoiceType  # ChoiceType: permite definir uma lista de opções para um campo

# Criação do objeto de conexão com o banco de dados SQLite
db = create_engine('sqlite:///banco.db')

# Criação do objeto base para trabalhar com classes/tabelas
Base = declarative_base()

# Classe/tabela de usuários
class Usuario(Base):
    __tablename__ = "usuarios"  # Nome da tabela no banco

    id = Column(Integer, primary_key=True, autoincrement=True)  # Chave primária, auto incremento
    nome = Column(String)  # Nome do usuário
    email = Column(String, nullable=False)  # Campo obrigatório (não pode ser nulo)
    senha = Column(String)  # Senha do usuário
    ativo = Column(Boolean)  # Indica se o usuário está ativo
    admin = Column(Boolean, default=False)  # Indica se o usuário é administrador, valor padrão False

    def __init__(self, nome, email, senha, ativo, admin=False):
        # Construtor para criar objetos de usuário
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin


# Classe/tabela de pedidos
class Pedido(Base):
    __tablename__ = "pedidos"  # Nome da tabela no banco

    # Lista de status possíveis para o pedido
    """Status_Pedido = (
        ("Pendente", "Pendente"),
        ("Cancelado", "Cancelado"),
        ("Finalizado", "Finalizado")
    )"""

    id = Column(Integer, primary_key=True, autoincrement=True)  # Chave primária
    status = Column(String)  # Campo com opções pré-definidas
    usuario = Column(Integer, ForeignKey("usuarios.id"))  # Chave estrangeira para a tabela de usuários
    preco = Column(Float)  # Valor total do pedido

    def __init__(self, usuario, status="Pendente", preco=0):
        # Construtor para criar objetos de pedido
        self.status = status
        self.usuario = usuario
        self.preco = preco


# Classe/tabela de itens do pedido
class ItemPedido(Base):
    __tablename__ = "itenspedidos"  # Nome da tabela no banco

    id = Column(Integer, primary_key=True, autoincrement=True)  # Chave primária
    quantidade = Column(Integer)  # Quantidade do item
    sabor = Column(String)  # Sabor do item
    tamanho = Column(String)  # Tamanho do item
    preco_unitario = Column(Float)  # Preço unitário
    pedido = Column(Integer, ForeignKey("pedidos.id"))  # Chave estrangeira para a tabela de pedidos
