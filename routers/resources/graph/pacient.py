import imp
from msilib.schema import Error
from unicodedata import name
from unittest import result
from urllib import response
import strawberry
from strawberry.types import Info
from utils.neo4j_db.connection import neo4j_driver
from utils.neo4j_db import Entities, Relationships, SupportMethods

from utils.neo4j_db.schema.entities.medication import Medication
import routers.resources.commonResponses as CommonResponses



MedicationToTakeResponse = strawberry.union(
    "MedicationToTakeResponse",
    [Relationships.Pacient_TAKES_Medication, CommonResponses.ErrorMessage]
)


@strawberry.type
class PacientQuery:

    @strawberry.field
    async def pacient(self, info : Info, id:str) -> Entities.Pacient:

        query ="MATCH (root:Pacient) WHERE root.id = $id"
        filters, returns = SupportMethods.prepareQuery('root', info.selected_fields, 'response')
        query += (filters + 'RETURN ' + returns)     

        with neo4j_driver.session() as session:
            db_raw = session.run(query=query, parameters={'id': id})  
            db_data = db_raw.data()[0]['response']
            session.close()
        print(db_data)
        
        return Entities.Pacient(**db_data)

    
    @strawberry.field
    async def medicationToTake(self, info : Info, id:str) -> list[Relationships.Pacient_TAKES_Medication]:
        
        query = 'MATCH (pacient:Pacient)-[root:TAKES]->(medication:Medication) WHERE pacient.id = $id '
        filters, returns = SupportMethods.prepareQuery('root', info.selected_fields, 'TAKES')
        query += (filters + 'RETURN ' + returns)     

        with neo4j_driver.session() as session:
            db_raw = session.run(query=query, parameters={'id': id})  
           
            db_data = db_raw.data()
            
            session.close()

        return [Relationships.Pacient_TAKES_Medication(**data['TAKES'], medication=(Medication(**data['Medication']) if'Medication' in data else None )) for data in db_data]


