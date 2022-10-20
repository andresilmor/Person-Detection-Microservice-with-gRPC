import strawberry.type as entity

@entity
class Medication:
    def __init__(self, name = None):
        self.name = name
        pass
    
    name: str