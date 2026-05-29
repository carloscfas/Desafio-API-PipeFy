from pydantic import BaseModel, EmailStr, Field, ConfigDict

class ClientBase(BaseModel):
    cliente_nome: str
    cliente_email: EmailStr
    tipo_solicitacao: str
    valor_patrimonio: float = Field(ge=0)

class ClientCreate(ClientBase):
    pass

class ClientResponse(ClientBase):
    id: int
    status: str
    prioridade: str | None = None

    model_config = ConfigDict(from_attributes=True)
