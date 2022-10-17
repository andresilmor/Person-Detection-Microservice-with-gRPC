import strawberry.type as entity
from utils.neo4j_db.schema.relationships.TAKES import TAKES

@entity
class Pacient:
    label: str
    id: str
    name: str