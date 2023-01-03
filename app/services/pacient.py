import strawberry
from strawberry.types import Info
from utils.neo4jDriver.connection import neo4j_driver

from app.schema import Pacient

@strawberry.type
class PacientQuery:

    @strawberry.field
    async def pacient(self, info : Info, id:str) -> Pacient:

        query ="MATCH (p:Pacient) WHERE p.uuid = $id  RETURN p  AS pacient "
     
        with neo4j_driver.session() as session:
            db_raw = session.run(query=query, parameters={'id': id})  
            db_data = db_raw.data()[0]['pacient']
            session.close()

        return Pacient(**db_data)