from fastapi import APIRouter, HTTPException
from models.model import User
from data import users

router = APIRouter()

@router.put("/users/{id}")
def update_user(id: int, user_update: User):
    for user in users:
        if user.id == id:
            if user_update.name is not None:
                user.name = user_update.name
            if user_update.age is not None:
                user.age = user_update.age
            if user_update.email is not None:
                user.email = user_update.email
            if user_update.phone is not None:
                user.phone = user_update.phone
            if user_update.address is not None:
                user.address = user_update.address
            return {"message": f"Usuário {user.name} atualizado com sucesso!"}
    raise HTTPException(status_code=404, detail="Usuário não encontrado")
