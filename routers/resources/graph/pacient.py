from unicodedata import name
from unittest import result
from urllib import response
import strawberry
from utils.neo4j_db.connection import neo4j_driver
from utils.neo4j_db import Entities
from utils.neo4j_db import Relationships
from typing import List

from utils.neo4j_db.schema.entities.medication import Medication


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
    async def medicationToTake(self, info, id:str) -> Relationships.Pacient_TAKES_Medication:
        query = "MATCH (p:Pacient)-[r:TAKES]->(m:Medication) WHERE p.id = $id RETURN PROPERTIES(r) AS TAKES, PROPERTIES(m) AS medication"
        with neo4j_driver.session() as session:
            db_raw = session.run(query=query, parameters={'id': id})  
            db_data = db_raw.data()[0]
            
            session.close()
        
        return Relationships.Pacient_TAKES_Medication(**db_data['TAKES'], medication=Medication(**db_data['medication']))


