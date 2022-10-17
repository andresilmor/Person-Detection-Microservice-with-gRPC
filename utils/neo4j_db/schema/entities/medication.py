import strawberry.type as entity

@entity
class Medication:
    label: str
    name: str