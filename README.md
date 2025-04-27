# API Simples com FastAPI

Este README fornece as instruções básicas para entender a estrutura e rodar este projeto FastAPI.

## Estrutura das Rotas

Todas as rotas devem seguir a seguinte estrutura:

1.  Importar `APIRouter` do FastAPI.
2.  Instanciar `APIRouter` em uma variável chamada `router`.
3.  Usar o decorador `@router` para definir os métodos HTTP (GET, POST, PUT, DELETE, etc.) e o caminho da rota.

**Exemplo:**

```python
# Em routes/arquivo_da_rota.py
from fastapi import APIRouter
from models.model import User # Exemplo de importação do modelo

router = APIRouter()

@router.post("/users")
def create_user(user: User):
    # Lógica da rota aqui
    pass
```

## Acesso aos Dados

Os dados da aplicação (neste caso, uma lista de usuários) estão armazenados no arquivo `data.py`. Para manipular esses dados nas rotas, importe a lista necessária.

**Exemplo:**

```python
# Em routes/arquivo_da_rota.py
from data import users # Importa a lista 'users' do arquivo data.py
from fastapi import APIRouter
from models.model import User

router = APIRouter()

@router.get("/users")
def get_users():
    return users # Retorna a lista de usuários
```

## Modelo de Dados

Para garantir a validação e estrutura correta dos dados recebidos e enviados (especialmente em requisições POST e PUT), importe a classe do modelo correspondente (neste caso, `User`) do arquivo `models/model.py`.

**Exemplo:**

```python
# Em routes/arquivo_da_rota.py
from models.model import User # Importa a classe User
from fastapi import APIRouter

router = APIRouter()

# Exemplo de uso no corpo da requisição
@router.post("/users")
def create_user(user: User):
    # 'user' será uma instância validada da classe User
    pass
```

## Integração das Rotas na Aplicação Principal

Para que as rotas criadas sejam acessíveis, elas precisam ser incluídas no arquivo principal da aplicação (`main.py`) usando `app.include_router()`.

**Exemplo (`main.py`):**

```python
from fastapi import FastAPI
# Importe os módulos das rotas
from routes import create, update, delete, read # Assumindo arquivos create.py, update.py, etc. dentro de /routes

app = FastAPI()

# Inclua o router de cada módulo
app.include_router(create.router)
app.include_router(update.router)
app.include_router(delete.router)
app.include_router(read.router)

# Restante da configuração da aplicação, se houver
```

## Instalação

Antes de rodar a aplicação, instale as dependências necessárias:

```bash
pip install fastapi pydantic uvicorn[standard]
```
*Nota: `uvicorn[standard]` instala o `uvicorn` junto com dependências recomendadas para melhor performance.*

## Execução

Para rodar a aplicação localmente com recarregamento automático (útil durante o desenvolvimento), use o Uvicorn. Navegue até o diretório raiz do projeto no terminal e execute:

```bash
uvicorn main:app --reload
```
*Substitua `main` pelo nome do seu arquivo Python principal (sem a extensão `.py`) e `app` pelo nome da variável onde você instanciou `FastAPI()`.*

Após executar o comando, você deverá ver uma saída semelhante a esta no terminal, indicando que o servidor está rodando:

```
INFO:     Will watch for changes in directories: ['/caminho/para/seu/projeto']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [PID] using StatReload
INFO:     Started server process [PID]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

A API estará acessível em `http://127.0.0.1:8000`.