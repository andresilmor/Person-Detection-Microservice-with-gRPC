import strawberry.type as entity

@entity
class Pacient:
    def __init__(self, label = None, id = None, name = None):
        self.label = label
        self.id = id
        self.name = name
        pass
    
    label: str
    id: str
    name: str