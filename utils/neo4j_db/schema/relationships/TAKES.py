import strawberry.type as relationship


@relationship
class TAKES:
    hour: str
    quantity: str
    name: str
    label: str