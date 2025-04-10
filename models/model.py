from pydantic import BaseModel, EmailStr
#
class usuario(BaseModel):
    id: int
    nome: str
    idade: int
    email: EmailStr
    telefone: str
    endereço: str



