import strawberry

@strawberry.type
class Mutation:
    @strawberry.field
    async def add_author(self, name: str) -> str:
       
        return name

