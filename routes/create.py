from fastapi import APIRouter, HTTPException
from models.model import User
from data import users

router = APIRouter()


@router.post("/users")
def create_user(user:User):
    if any(u.id == user.id for u in users):
        raise HTTPException(status_code=400, detail="ID já existe")
    users.append(user)
  
    return {"message":f"Usuário {user.name} criado com sucesso!"}