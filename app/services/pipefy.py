import json

class PipefyClient:
    def __init__(self, pipe_id: str = "301234567"):
        self.pipe_id = pipe_id

    def create_card_mutation(self, name: str, email: str, patrimonio: float) -> str:
        """
        Structures the createCard mutation based on Pipefy's official documentation.
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
        Structures the updateCardField mutation (or updateFieldsValues for multiple) 
        based on Pipefy's official documentation.
        """
        # Using updateFieldsValues as it's more efficient for multiple fields
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
        Simulates sending the GraphQL mutation to Pipefy.
        In a real scenario, this would use httpx.post(PIPEFY_API_URL, json={"query": mutation})
        """
        print(f"Simulating Pipefy Mutation:\n{mutation}")
        return {"data": {"success": True}}
