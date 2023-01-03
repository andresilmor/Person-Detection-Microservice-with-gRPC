import strawberry.type as type
from typing import List
from .institution import Institution

@type
class MemberOf:
    def __init__(self, institution = None, role = None):
        self.institution = institution
        self.role = role
        pass

    institution: Institution
    role: str

@type
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