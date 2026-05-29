from fastapi import FastAPI
from app.api.v1 import endpoints
from app.db.session import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mundo Invest - Client Management & Pipefy Integration")

app.include_router(endpoints.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Mundo Invest API"}
