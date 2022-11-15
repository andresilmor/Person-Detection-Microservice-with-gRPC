import strawberry.type as entity

@entity
class Medication:
    def __init__(self, uuid = None, label = None, name = None):
        self.uuid = uuid
        self.label = label
        self.name = name
        pass
    
    uuid: str
    label: str
    name: str