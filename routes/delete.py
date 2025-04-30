from fastapi import APIRouter, HTTPException
from models.model import User
from data import users

router = APIRouter()

@router.delete("/users/{user_id}", status_code=200, tags=["Users"])
def delete_user(user_id: int):
    user_to_delete = next((u for u in users if u.id == user_id), None)
    if not user_to_delete:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    users.remove(user_to_delete)
    
    # Verifica se o atributo name existe e está acessível
    user_name = getattr(user_to_delete, "name", None)
    if not user_name:
        raise HTTPException(status_code=500, detail="Erro ao acessar o nome do usuário deletado")
    
    return {"message": f"Usuário {user_name} deletado com sucesso!"}