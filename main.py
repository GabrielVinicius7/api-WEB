from fastapi import FastAPI, HTTPException, Depends, Body
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
import uuid
import json
import os
from datetime import datetime 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title = "API de cadastro de Usuários",
    descripition = "API para gerenciar usuários e conversar com IA sobre gerenciamento de usuários",
    version = "1.0.0",
    
)

#Adicionar CORS para permitir acesso de outros domínios
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)