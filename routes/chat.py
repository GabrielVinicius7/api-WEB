from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid
from data import users
from models.model import User
import httpx

router = APIRouter()

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

async def get_gemini_response(prompt: str) -> str:
    api_key = "AIzaSyA9cobgLVuyHIHPgsQoyUYPGelrROTxWUY"
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [{
            "parts":[{"text": prompt}]
        }]
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(api_url, json=data, headers=headers)
            response.raise_for_status()
            response_data = response.json()
            if "candidates" in response_data and response_data["candidates"]:
                if "content" in response_data["candidates"][0] and "parts" in response_data["candidates"][0]["content"]:
                     return response_data["candidates"][0]["content"]["parts"][0]["text"]
                else:
                     return "Não foi possível extrair a resposta da IA (estrutura inesperada)."

            else:
                if "error" in response_data and "message" in response_data["error"]:
                     return f"Erro da API do Gemini: {response_data['error']['message']}"
                else:
                    return "Não foi possível obter uma resposta da IA (sem candidatos ou erro especificado)."

        except httpx.HTTPStatusError as e:
            error_detail = e.response.text if e.response else "Detalhe não disponível."
            return f"Erro na API: {e} - Detalhe: {error_detail}"
        except Exception as e:
            return f"Ocorreu um erro ao chamar a API da IA: {e}"

@router.post("/chat/", response_model=ChatResponse, tags=["chat"])
async def chat_with_ai(chat_message: ChatMessage):
    message = chat_message.message.lower()

    if message.startswith("listar usuários") or message.startswith("listar usuarios"):
        if not users:
            return {"response": "Não há usuários cadastrados"}

        user_list = []
        for user in users:
            if isinstance(user, User):
                name = user.name
                email = user.email
                phone = user.phone if user.phone is not None else 'Sem telefone'
                address = user.address if user.address is not None else 'Sem endereço'
            else:
                name = user.get('name', 'N/A')
                email = user.get('email', 'N/A')
                phone = user.get('phone', 'Sem telefone')
                address = user.get('address', 'Sem endereço')

            user_list.append(f"🙍‍♀️ Nome: {name}\n📧 Email: {email}\n📲 Telefone: {phone}\n🏢 Endereço: {address}")

        return {"response": f"Usuários cadastrados no sistema:\n\n{'\\n\\n'.join(user_list)}"}

    elif message.startswith("buscar usuário") or message.startswith("buscar usuario"):
        search_term = message.replace("buscar usuário", "").replace("buscar usuario", "").strip()
        if not search_term:
            return {"response": "Por favor, forneça um termo de busca."}

        found_users = []
        for user in users:
            if isinstance(user, User):
                name = user.name
                email = user.email
                phone = user.phone if user.phone is not None else ''
                address = user.address if user.address is not None else ''
            else:
                name = user.get('name', '')
                email = user.get('email', '')
                phone = user.get('phone', '')
                address = user.get('address', '')

            if (search_term.lower() in name.lower() or
                search_term.lower() in email.lower() or
                search_term.lower() in address.lower() or
                search_term.lower() in phone.lower()):

                found_users.append(user)

        if not found_users:
            return {"response": f"Nenhum usuário encontrado com o termo de busca '{search_term}'."}

        user_list = []
        for user in found_users:
            if isinstance(user, User):
                name = user.name
                email = user.email
                phone = user.phone if user.phone is not None else 'Sem telefone'
                address = user.address if user.address is not None else 'Sem endereço'
            else:
                name = user.get('name', 'N/A')
                email = user.get('email', 'N/A')
                phone = user.get('phone', 'Sem telefone')
                address = user.get('address', 'Sem endereço')
            user_list.append(f"👱‍♀️ Nome: {name}\n📧 Email: {email}\n📲 Telefone: {phone}\n🏢 Endereço: {address}")

        return {"response": f"Usuários encontrados com o termo de busca '{search_term}':\n\n{'\\n\\n'.join(user_list)}"}

    elif message.startswith("adicionar usuário") or message.startswith("adicionar usuario"):
        try:
            user_data = message.replace("adicionar usuário", "").replace("adicionar usuario", "").strip().split("|")
            if len(user_data) < 5:
                return {
                    "response": "Por favor, forneça o nome, email, telefone, endereço e idade do usuário separados por '|'."
                }

            name = user_data[0].strip()
            email = user_data[1].strip()
            phone = user_data[2].strip() if user_data[2] else None
            address = user_data[3].strip() if user_data[3] else None
            age_str = user_data[4].strip()

            try:
                age = int(age_str)
                if age <= 0:
                    return {"response": "A idade deve ser um número positivo."}
            except ValueError:
                return {"response": "Idade inválida. Por favor, forneça um número para a idade."}

            for existing_user in users:
                if isinstance(existing_user, User):
                    existing_email = existing_user.email
                else:
                    existing_email = existing_user.get('email')

                if existing_email == email:
                    return {
                        "response": f"O email '{email}' já está cadastrado."
                    }

            user_id = len(users) + 1

            new_user = User(
                id=user_id,
                name=name,
                age=age,
                email=email,
                phone=phone,
                address=address
            )

            users.append(new_user.dict())

            return {"response": f"usuário '{name}' adicionado com sucesso! ID: {user_id}."}

        except Exception as e:
            return {"response": f"Erro ao adicionar usuário: {str(e)}"}

    elif message.startswith("remover usuário") or message.startswith("remover usuario"):
        user_id_str = message.replace("remover usuário", "").replace("remover usuario", "").strip()
        try:
            user_id = int(user_id_str)
        except ValueError:
            return {"response": "ID de usuário inválido. Use um número."}

        user_to_delete_index = -1
        for i, user in enumerate(users):
            if isinstance(user, User):
                current_user_id = user.id
            else:
                current_user_id = user.get('id')

            if current_user_id == user_id:
                user_to_delete_index = i
                break

        if user_to_delete_index != -1:
            removed_user = users.pop(user_to_delete_index)
            return {"response": f"Usuário com ID '{user_id}' removido com sucesso!"}
        else:
             return {"response": f"Usuário com ID '{user_id}' não encontrado."}

    else:
        users_info = ""
        if users:
            user_details = []
            for user in users:
                if isinstance(user, User):
                    name = user.name
                    email = user.email
                    age = user.age
                else:
                    name = user.get('name', 'N/A')
                    email = user.get('email', 'N/A')
                    age = user.get('age', 'N/A')
                user_details.append(f"- Nome: {name}, Email: {email}, Idade: {age}")
            users_info ="Usuários no sistema: \n" + "\n".join(user_details)

        prompt = f""" Você é um assistente de gerenciamento de usuários que pode ajudar com informações sobre os usuários cadastrados.
        Responda a pergunta do usuário de forma útil e informativa, baseando-se no contexto dos usuários cadastrados, se relevante.
        Se a pergunta não for sobre gerenciamento de usuários ou informações sobre usuários cadastrados, responda de forma geral como um assistente prestativo.

        {users_info}

        Pergunta do usuário: {chat_message.message}
        """

        ai_response = await get_gemini_response(prompt)
        return {"response": ai_response}
