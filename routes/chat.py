#rota para o chat com IA
@app.post("/chat/", response_model=ChatResponse, tags=["chat"])
async def chat_with_ai(chat_message: ChatMessage):
    '''
    conversa com a ia sobre gerenciamento de usuários ou sobre os usuários cadastrados.
    '''
    message = chat_message.message.lower()

    #comandos CRUD via chat
    if message.startswith("listar usuários") or message.startswith("listar usuarios"):
        if not users_db:
            return {"response": "Não há usuários cadastrados"}
        
        user_list = "\n\n".join([
            f"🙍‍♀️ {user_data['user'].name}\n📧 {user_data['user'].email}\n📲 {user_data['user'].phone or 'Sem telefone'}\n🏢{user_data['user'].departament or 'Sem departamento'}\n🔑{user_data['user'].role}"
            for user_data in users_db.values()
        ])

        return {"response": f"Usuários cadastrados no sistema:\n\n{user_list}"}
    
    elif message.startswith("buscar usuário") or message.startswith("buscar usuario"):
        search_term = message.replace("buscar usuário", "").replace("buscar usuario", "").strip()
        if not search_term:
            return {"response": "Por favor, forneça um termo de busca."}
        
        found_users = [
            user_data["user"] for user_data in user_db.values()
            if search_term.lower() in user_data["user"].name.lower() or
            search_term.lower() in user_data["user"].email.lower() or
            (user_data["user"].departament and search_term.lower()in user_data["user"].departament.lower()) or
            search_term.lower() in user_data["user"].role.lower()
        ]

        if not found_users:
            return {"response": f"Nenhum usuário encontrado com o termo de busca '{search_term}'."}
        
        user_list = "\n\n".join([
            f"👱‍♀️ {user.name}\n📧 {user.email}\n📲 {user.phone or 'Sem telefone'}\n🏢 {user.departament or 'Sem departamento'}\n🔑 {user.role}"
            for user in found_users
        ])

        return {"response": f"Usuários encontrados com o termo de busca '{search_term}':\n\n{user_list}"}
    
    elif message.startswith("adicionar usuário") or message.startswith("adicionar usuario"):
        try:
            #formato esperado " adicionar usuário: nome | email | telefone | departamento | senha"
            user_data = message.replace("adicionar usuário", "").replace("adicionar usuario", "").strip().split("|")
            if len(user_data) < 4:
                return {
                    "response": "Por favor, forneça o nome, email, telefone e departamento do usuário."
                }
            
            name = user_data[0].strip()
            email = user_data[1].strip()
            phone = user_data[2].strip() if user_data[2] else None
            role = user_data[3].strip
            departament = user_data[4].strip() if len(user_data) > 4 and user_data[4].strip() else None
            password = user_data[5].strip() if len(user_data) > 5 else "senha123" # senha padrão

            #verificar se o email já existe
            for existing_user in user_db.values():
                if existing_user["user"].email == email:
                    return {
                        "response": f"O email '{email}' já está cadastrado."
                    }
            
            user_id = str(uuid.uuid4())
            current_time = datetime.now().isoformat()

            new_user = User(
                id=user_id,
                name=name,
                email=email,
                phone=phone,
                role=role,
                departament=departament,
                created_at=current_time,
                updated_at=current_time
            )

            users_db[user_id] = {
                "user": new_user,
                "password": password 
            }

            return {"response": f"usuário '{name}' adicionado com sucesso! ID: {user_id}."}
        
        except Exception as e:
            return {"response": f"Erro ao adicionar usuário: {str(e)}"}
        
    elif message.startswith("remover usuário") or message.startswith("remover usuario"):
        user_id = message.replace("remover usuário", "").replace("remover usuario", "").strip()
        if user_id in users_db:
            name = users_db[user_id]["user"].name
            del users_db[user_id]
            return{"response": f"Usuário com ID '{user_id}' removido com sucesso!"}
        else:
            return {"response": f"Usuário com ID '{user_id}' não encontrado."}
        
    #caso não seja um comando CRUD, encaminha para a IA
    else:
        #prepara o contexto para a IA com informações sobre os usuários cadastrados
        users_info = ""
        if users_db:
            users_info =" Usuários no sistema: \n" + "\n".join([
                f"- {user_data['user'].name} ({user_data['user'].role})"
                for user_data in users_db.values()
            ])

        #prepara o prompt para a IA
        prompt = f""" Você é um assistente de gerenciamento de usuários que pode ajudar com informações sobre o sistema.

        {users_info}

        Pergunta do usuário: {chat_message.message}
        """

        #obter resposta da IA
        ai_response = await get_gemini_response(prompt)
        return {"response": ai_response}
    

@app.get("/", tags="Info")
async def root():
    '''
    página inicial da API
    '''
    return{
        "message": "Bem vindo à API do Gerenciamento de Usuários!"
        "endpoints": {
            "CRUD de Usuários": [
                {"POST /users/": "Criar um novo usuário"},
                {"GET /users/": "Listar todos os usuários"},
                {"GET /users/{user_id}": "Obter detalhes de um usuário específico"},
                {"PUT /users/{user_id}": "Atualizar informações de um usuário"},
                {"DELETE / users/{user_id}": "Remover um usuário"} 

            ]
        },
        "documentação": "/docs"
    }

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)        