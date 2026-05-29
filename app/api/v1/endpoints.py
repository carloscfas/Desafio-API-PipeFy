from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.client import Client
from app.models.event import ProcessedEvent
from app.schemas.client import ClientCreate, ClientResponse
from app.schemas.webhook import WebhookPayload
from app.services.pipefy import PipefyClient

router = APIRouter()
pipefy_client = PipefyClient()

@router.post("/clientes", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(client_in: ClientCreate, db: Session = Depends(get_db)):
    # Verifica se o cliente já existe
    existing_client = db.query(Client).filter(Client.cliente_email == client_in.cliente_email).first()
    if existing_client:
        raise HTTPException(status_code=400, detail="O cliente já existe")

    # Persistência Local
    db_client = Client(
        cliente_nome=client_in.cliente_nome,
        cliente_email=client_in.cliente_email,
        tipo_solicitacao=client_in.tipo_solicitacao,
        valor_patrimonio=client_in.valor_patrimonio,
        status="Aguardando Análise"
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)

    # Mapeamento Pipefy (GraphQL)
    mutation = pipefy_client.create_card_mutation(
        name=db_client.cliente_nome,
        email=db_client.cliente_email,
        patrimonio=db_client.valor_patrimonio
    )
    pipefy_client.simulate_request(mutation)

    return db_client

@router.post("/webhooks/pipefy/card-updated", status_code=status.HTTP_200_OK)
def handle_webhook(payload: WebhookPayload, db: Session = Depends(get_db)):
    # Idempotência
    already_processed = db.query(ProcessedEvent).filter(ProcessedEvent.event_id == payload.event_id).first()
    if already_processed:
        return {"message": "Evento já processado", "event_id": payload.event_id}

    # Regra de Negócio
    client = db.query(Client).filter(Client.cliente_email == payload.cliente_email).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    # Calcular prioridade
    priority = "prioridade_alta" if client.valor_patrimonio >= 200000 else "prioridade_normal"
    
    # Mapeamento de Update (GraphQL)
    mutation = pipefy_client.update_card_mutation(
        card_id=payload.card_id,
        status="Processado",
        prioridade=priority
    )
    pipefy_client.simulate_request(mutation)

    # Atualizar Banco Local
    client.status = "Processado"
    client.prioridade = priority
    
    # Marcar evento como processado
    new_event = ProcessedEvent(event_id=payload.event_id)
    db.add(new_event)
    
    db.commit()

    return {
        "message": "Webhook processado com sucesso",
        "client_status": client.status,
        "priority": priority
    }
