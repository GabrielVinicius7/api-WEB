from fastapi import FastAPI
from routes import create, update, delete, read
from data import users 



app = FastAPI(swagger_ui_parameters={"syntaxHighlight": True})

app.include_router(create.router)
app.include_router(update.router)
app.include_router(delete.router)
app.include_router(read.router)