from xml.dom import NO_MODIFICATION_ALLOWED_ERR

from fastapi import FastAPI
from models.model import usuario
from main import app

usuarios = []

@app.put("/usuario/{usuario_id}")
def atualizar_usuario(usuario_id: int, usuario_atualizado: usuarioAtualizacao):
    for usuario in usuarios:
        if usuario.id == usuario_id:
            if usuario_atualizado.nome is not None:
                usuario.nome = usuario_atualizado.nome
            if usuario_atualizado.idade is not None:
                usuario.idade = usuario_atualizado.idade
            if usuario_atualizado.email is not None:
                usuario.email = usuario_atualizado.email
            if usuario_atualizado.telefone is not None:
                usuario.telefone = usuario_atualizado.telefone
            if usuario_atualizado.endereco is not None:
                usuario.endereço = usuario_atualizado.endereco
            return usuario
