import json

class PipefyClient:
    def __init__(self, pipe_id: str = "301234567"):
        self.pipe_id = pipe_id

    def create_card_mutation(self, name: str, email: str, patrimonio: float) -> str:
        """
        Estrutura a mutação createCard com base na documentação oficial do Pipefy.
        """
        mutation = """
        mutation {
          createCard(input: {
            pipe_id: "%s",
            title: "Solicitação de %s",
            fields_attributes: [
              { field_id: "cliente_nome", field_value: "%s" },
              { field_id: "cliente_email", field_value: "%s" },
              { field_id: "valor_patrimonio", field_value: "%s" }
            ]
          }) {
            card {
              id
              title
            }
          }
        }
        """ % (self.pipe_id, name, name, email, str(patrimonio))
        return mutation.strip()

    def update_card_mutation(self, card_id: str, status: str, prioridade: str) -> str:
        """
        Estrutura a mutação updateCardField (ou updateFieldsValues para múltiplos)
        baseado na documentação oficial do Pipefy.
        """
        # Usando updateFieldsValues porque é mais eficiente para vários campos
        mutation = """
        mutation {
          updateFieldsValues(input: {
            nodeId: "%s",
            values: [
              { fieldId: "status", value: "%s" },
              { fieldId: "prioridade", value: "%s" }
            ]
          }) {
            success
          }
        }
        """ % (card_id, status, prioridade)
        return mutation.strip()

    def simulate_request(self, mutation: str):
        """
        Simula o envio da mutação GraphQL para o Pipefy.
        Em um cenário real, isso usaria httpx.post(PIPEFY_API_URL, json={"query":mutation})
        """
        print(f"Simulando mutação no Pipefy:\n{mutation}")
        return {"data": {"success": True}}
