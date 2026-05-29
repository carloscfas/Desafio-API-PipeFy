import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.session import Base, get_db

# Configurar banco de dados de teste
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield

def test_create_client():
    payload = {
        "cliente_nome": "João Silva",
        "cliente_email": "joao.silva@example.com",
        "tipo_solicitacao": "Atualização cadastral",
        "valor_patrimonio": 250000
    }
    response = client.post("/clientes", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["cliente_nome"] == "João Silva"
    assert data["status"] == "Aguardando Análise"

def test_webhook_high_priority():
    # Primeiro, crie um cliente
    client.post("/clientes", json={
        "cliente_nome": "João Rico",
        "cliente_email": "rico@example.com",
        "tipo_solicitacao": "Aporte",
        "valor_patrimonio": 300000
    })

    # Acionar webhook
    webhook_payload = {
        "event_id": "evt_high",
        "card_id": "card_high",
        "cliente_email": "rico@example.com",
        "timestamp": "2026-05-18T12:00:00Z"
    }
    response = client.post("/webhooks/pipefy/card-updated", json=webhook_payload)
    assert response.status_code == 200
    assert response.json()["priority"] == "prioridade_alta"
    assert response.json()["client_status"] == "Processado"

def test_webhook_normal_priority():
    # Primeiro, crie um cliente
    client.post("/clientes", json={
        "cliente_nome": "João Médio",
        "cliente_email": "medio@example.com",
        "tipo_solicitacao": "Dúvida",
        "valor_patrimonio": 150000
    })

    # Acionar webhook
    webhook_payload = {
        "event_id": "evt_normal",
        "card_id": "card_normal",
        "cliente_email": "medio@example.com",
        "timestamp": "2026-05-18T12:00:00Z"
    }
    response = client.post("/webhooks/pipefy/card-updated", json=webhook_payload)
    assert response.status_code == 200
    assert response.json()["priority"] == "prioridade_normal"

def test_webhook_idempotency():
    # Primeiro, crie um cliente
    client.post("/clientes", json={
        "cliente_nome": "João Repetido",
        "cliente_email": "repetido@example.com",
        "tipo_solicitacao": "Dúvida",
        "valor_patrimonio": 100000
    })

    webhook_payload = {
        "event_id": "evt_unique",
        "card_id": "card_123",
        "cliente_email": "repetido@example.com",
        "timestamp": "2026-05-18T12:00:00Z"
    }
    
    # Processar pela primeira vez
    response1 = client.post("/webhooks/pipefy/card-updated", json=webhook_payload)
    assert response1.status_code == 200
    assert "Webhook processado com sucesso" in response1.json()["message"]

    # Processe pela segunda vez com o mesmo event_id
    response2 = client.post("/webhooks/pipefy/card-updated", json=webhook_payload)
    assert response2.status_code == 200
    assert response2.json()["message"] == "Evento já processado"

