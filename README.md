# API Simples com FastAPI

Esta API é construída com FastAPI e oferece funcionalidades para gerenciar informações de usuários e interagir através de um chat com inteligência artificial.

**Funcionalidades:**

-   **Gerenciamento de Usuários:** A API permite criar, visualizar, atualizar e deletar registros de usuários. Os dados são armazenados em uma lista na memória.
-   **Chat Interativo:** A API inclui um chat que pode fornecer informações sobre os usuários cadastrados e interagir com o usuário. É importante notar que, devido à estrutura de dados baseada em lista, o chat não realiza alterações nos dados, mas pode trazer resultados personalizados e contextuais.

## 🚨 AVISO IMPORTANTE SOBRE A CHAVE DA API DO CHAT 🚨

##################################################################

A CHAVE DA API UTILIZADA PARA A FUNCIONALIDADE DE CHAT
EXPIRA EM: DOMINGO, 04 DE MAIO DE 2025.
APÓS ESSA DATA, A FUNCIONALIDADE DE CHAT PODE PARAR DE
FUNCIONAR. POR FAVOR, ATUALIZE A CHAVE PARA CONTINUAR
UTILIZANDO O CHAT.

##################################################################


## Dependências

Para rodar esta aplicação, você precisa das seguintes dependências Python:

fastapi==0.115.12
pydantic==2.11.3
pydantic_core==2.33.1
uvicorn==0.34.2
email_validator==2.2.0
httpx

Você pode instalar todas as dependências usando o `pip` e o arquivo `requirements.txt` através do comando: pip install -r requirements.txt.

## Instalação

1.  Certifique-se de que o Python está instalado no seu sistema.
2.  Navegue até o diretório onde o arquivo `requirements.txt` está localizado.
3.  Execute o seguinte comando para instalar as dependências:

    ```bash
    pip install -r requirements.txt
    ```

<br>

## Execução

Para rodar a API localmente com recarregamento automático, siga estes passos:

1.  Abra o terminal e navegue até o diretório raiz do projeto (onde o arquivo `main.py` está).
2.  Execute o seguinte comando:

    ```bash
    uvicorn main:app --reload
    ```

3.  Se a API iniciar com sucesso, você verá uma saída semelhante a esta:

    ```
    INFO:     Will watch for changes in directories: ['/caminho/para/seu/projeto']
    INFO:     Uvicorn running on [http://127.0.0.1:8000](http://127.0.0.1:8000) (Press CTRL+C to quit)
    INFO:     Started reloader process [PID] using StatReload
    INFO:     Started server process [PID]
    INFO:     Waiting for application startup.
    INFO:     Application startup complete.
    ```

Para visualizar a documentação interativa da API, acesse `http://127.0.0.1:8000/docs` no seu navegador.
