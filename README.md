# Desafio Técnico - Mundo Invest (Backend)

Este projeto é uma API de gerenciamento de clientes e integração (simulada) com o Pipefy, desenvolvida como parte de um desafio técnico para a vaga de Desenvolvedor Backend Júnior.

## Tecnologias Utilizadas

- **Linguagem:** Python 3.10+
- **Framework:** FastAPI
- **Banco de Dados:** SQLite (SQLAlchemy ORM)
- **Validação:** Pydantic V2
- **Testes:** Pytest

## Estrutura do Projeto

```text
app/
├── api/v1/         # Endpoints da API
├── core/           # Configurações globais
├── db/             # Conexão e sessão do banco de dados
├── models/         # Modelos SQLAlchemy
├── schemas/        # Esquemas Pydantic (Validação)
├── services/       # Lógica de integração (Pipefy Client)
└── main.py         # Ponto de entrada da aplicação
tests/              # Testes automatizados
```

## Como Executar Localmente

### 1. Clonar o repositório
```bash
git clone <url-do-repositorio>
cd Desafio-ApiPipeFY
```

### 2. Configurar o ambiente virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Executar a aplicação
```bash
uvicorn app.main:app --reload
```
A API estará disponível em `http://127.0.0.1:8000`. Você pode acessar a documentação interativa (Swagger) em `http://127.0.0.1:8000/docs`.

## Executando Testes

Para rodar os testes automatizados:
```bash
pytest
```

## Exemplos de Requisição (curl)

### Fluxo 1: Criação de Cliente
```bash
curl -X POST "http://127.0.0.1:8000/clientes" \
     -H "Content-Type: application/json" \
     -d '{
       "cliente_nome": "João Silva",
       "cliente_email": "joao.silva@example.com",
       "tipo_solicitacao": "Atualização cadastral",
       "valor_patrimonio": 250000
     }'
```

### Fluxo 2: Webhook de Atualização (Pipefy)
```bash
curl -X POST "http://127.0.0.1:8000/webhooks/pipefy/card-updated" \
     -H "Content-Type: application/json" \
     -d '{
       "event_id": "evt_123",
       "card_id": "card_456",
       "cliente_email": "joao.silva@example.com",
       "timestamp": "2026-05-18T12:00:00Z"
     }'
```

## Visão de Produção (AWS)

Para escalar esta aplicação na AWS, poderíamos utilizar a seguinte arquitetura:

1.  **API Gateway:** Para gerenciar as requisições HTTP e rotear para os serviços adequados, além de fornecer segurança e throttling.
2.  **AWS Lambda:** A lógica de negócio (FastAPI) pode ser executada em funções Lambda (Serverless), o que permite escalabilidade automática conforme a demanda e redução de custos.
3.  **Amazon RDS (PostgreSQL):** Substituir o SQLite por um banco de dados relacional gerenciado para garantir persistência robusta, backups e alta disponibilidade.
4.  **Amazon DynamoDB:** Pode ser usado para armazenar os `event_id` processados (idempotência), aproveitando sua baixíssima latência e escalabilidade horizontal.
5.  **Amazon SQS:** No caso do webhook, se o volume de eventos for muito alto, poderíamos enfileirar os payloads no SQS para serem processados de forma assíncrona pelas Lambdas, garantindo que nenhum evento seja perdido em picos de tráfego.

## Mapeamento GraphQL (Pipefy)

As mutations GraphQL foram estruturadas seguindo a documentação oficial:
- `createCard`: Utilizada no Flow 1 para criar o card no Pipefy com os campos de nome, e-mail e patrimônio.
- `updateFieldsValues`: Utilizada no Flow 2 para atualizar o status e a prioridade do card de forma atômica.

A implementação detalhada pode ser encontrada em `app/services/pipefy.py`.
