from sqlalchemy import Column, Integer, String, Float
from app.db.session import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    cliente_nome = Column(String, index=True)
    cliente_email = Column(String, unique=True, index=True)
    tipo_solicitacao = Column(String)
    valor_patrimonio = Column(Float)
    status = Column(String, default="Aguardando Análise")
    prioridade = Column(String, nullable=True)
