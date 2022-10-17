import strawberry.type as entity

@entity
class Pacient:
    label: str
    id: str
    name: str