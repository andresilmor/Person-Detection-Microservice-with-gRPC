import strawberry.type as entity

@entity
class Institution:
    def __init__(self, label = None, uuid = None):
        self.label = label
        self.uuid = uuid
        pass
    
    label: str
    uuid: str