import strawberry.type as entity
import strawberry
from utils.neo4j_db.schema.entities.institution import Institution
from typing import List, Union, Optional
from strawberry.tools import merge_types

@entity
class MemberOf:
    def __init__(self, institution = None, role = None):
        self.institution = institution
        self.role = role
        pass

    institution: Institution
    role: str

@entity
class Member:
    def __init__(self, label = None, uuid = None, name = None, password = None, token = None, memberOf = None ):
        self.label = label
        self.uuid = uuid
        self.name = name
        self.password = password
        self.token = token
        self.memberOf = memberOf
        pass
    
    label: str
    uuid: str
    name: str
    password: str
    token: str
    memberOf: List[MemberOf]