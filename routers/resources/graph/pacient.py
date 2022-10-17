from unicodedata import name
import strawberry
from utils.neo4j_db.connection import neo4j_driver
from utils.neo4j_db import Entities
from utils.neo4j_db import Relationships
from typing import List


@strawberry.type
class PacientQuery:

    @strawberry.field
    async def pacient(self, info, id:str) -> Entities.Pacient:
        query ="MATCH (pacient:Pacient) WHERE pacient.id = $id RETURN (pacient) AS response"
        with neo4j_driver.session() as session:
            db_raw = session.run(query=query, parameters={'id': id})  
            db_data = db_raw.data()[0]['response']
            session.close()
        print(db_data)
        
        return Entities.Pacient(**db_data)

    
    @strawberry.field
    async def medicationToTake(self, info, id:str) -> Relationships.TAKES:
        query = "MATCH (p:Pacient)-[r:TAKES]->(m:Medication) WHERE p.id = $id RETURN apoc.map.merge(r, m) AS response"
        with neo4j_driver.session() as session:
            db_raw = session.run(query=query, parameters={'id': id})  
            db_data = db_raw.data()[0]['response']
            session.close()
        
        return Relationships.TAKES(**db_data)


