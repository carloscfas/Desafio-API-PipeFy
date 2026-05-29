from fastapi import FastAPI
from app.api.v1 import endpoints
from app.db.session import engine, Base

# Criar tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mundo Invest - Gestão de clientes e integração com Pipefy")

app.include_router(endpoints.router)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API Mundo Invest"}
