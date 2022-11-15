import strawberry.type as entity
import strawberry
from utils.neo4j_db.schema.entities.institution import Institution
from typing import List, Union, Optional

@entity
class Caregiver:
    def __init__(self, label = None, uuid = None, name = None, password = None, token = None, institution = None):
        self.label = label
        self.uuid = uuid
        self.name = name
        self.password = password
        self.token = token
        self.institution = institution

        pass
    
    label: str
    uuid: str
    name: str
    password: str
    token: str
    institution: List[Institution]