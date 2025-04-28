from typing import Union
from fastapi import APIRouter, HTTPException, FastAPI
from data import users

router = APIRouter()


@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.get("/users/{user_id}")
def read_usuario(user_id: int, name: Union[str, None] = None):
    # Busca o usuário na lista pelo ID
    for user in users:
        if user.id == user_id:
            return {"user_id": user.id, "Nome": user.name, "Idade": user.age, "Email": user.email, "Telefone": user.phone, "Endereço": user.address}
    # Se não encontrar, lança uma exceção
    raise HTTPException(status_code=404, detail="User not found")