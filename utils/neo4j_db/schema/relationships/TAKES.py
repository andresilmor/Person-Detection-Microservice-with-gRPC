import strawberry.type as relationship
from utils.neo4j_db.schema.entities.medication import Medication

@relationship
class Pacient_TAKES_Medication:
    hour: str
    quantity: str
    medication: Medication