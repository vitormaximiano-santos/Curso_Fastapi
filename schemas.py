from pydantic import BaseModel # BaseModel é uma classe que herda de pydantic.BaseModel, serve para criar modelos de dados, com validação e serialização, e integração com FastAPI, Pydantic é uma biblioteca para trabalhar com modelos de dados em Python

from typing import Optional

class SchemaUsuario(BaseModel): # cria um modelo de dados para usuários "BaseModel" é uma classe que herda de pydantic.BaseModel
    
    nome : str
    email : str
    senha : str
    ativo : Optional[bool]
    admin : Optional[bool]

    class Config:
        from_attributes = True # permite que o pydantic use os atributos do modelo como nomes de campos
        
class SchemaPedido(BaseModel): #
    usuario : int # tipo de dado: int
    
    class Config:
        from_attributes = True
    
class SchemaLogin(BaseModel):
    email: str
    senha: str
    
    class Config:
        from_attributes = True
        