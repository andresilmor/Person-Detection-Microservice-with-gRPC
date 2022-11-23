import strawberry.type as entity

@entity
class Institution:
    def __init__(self, label = None, uuid = None, name = None):
        self.label = label
        self.uuid = uuid
        self.name = name
        pass
    
    label: str
    uuid: str
    name: str