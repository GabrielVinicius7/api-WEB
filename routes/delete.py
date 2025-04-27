@app.delete("/users/{user_id}"), status_code=204, tags=["Users"])
async def delete_user(user_id: int):

''''
remove um usuário do banco de dados
'''

    if user_id not in user_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    del user_db[user_id]
    return {"message": "Usuário deletado com sucesso"}