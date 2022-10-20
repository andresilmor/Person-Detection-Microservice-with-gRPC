import imp
from msilib.schema import Error
from unicodedata import name
from unittest import result
from urllib import response
import strawberry
from strawberry.types import Info
from utils.neo4j_db.connection import neo4j_driver
from utils.neo4j_db import Entities
from utils.neo4j_db import Relationships

from utils.neo4j_db.schema.entities.medication import Medication
import routers.resources.commonResponses as CommonResponses



MedicationToTakeResponse = strawberry.union(
    "MedicationToTakeResponse",
    [Relationships.Pacient_TAKES_Medication, CommonResponses.ErrorMessage]
)

def prepareQuery(parent, selected_fields, returnAs):
    queryFilter = ' UNWIND apoc.any.properties(' + parent + ',['
    childs = []
    for field in selected_fields:
       
        for selection in field.selections:
            if len(selection.selections) == 0:
                queryFilter += (', \"' + selection.name + '\"')
            else:
                childs.append(selection)

    queryFilter += (']) AS ' + returnAs + ' ')

    for index in range(len(childs)):
        newFilter, newReturn = prepareQuery(childs[index].name,[childs[index]], str(childs[index].name).capitalize())
        queryFilter += newFilter
        returnAs += (', ' + newReturn)

    return queryFilter, returnAs

@strawberry.type
class PacientQuery:

    @strawberry.field
    async def pacient(self, info : Info, id:str) -> Entities.Pacient:
        query ="MATCH (pacient:Pacient) WHERE pacient.id = $id RETURN (pacient) AS response"
        with neo4j_driver.session() as session:
            db_raw = session.run(query=query, parameters={'id': id})  
            db_data = db_raw.data()[0]['response']
            session.close()
        print(db_data)
        
        return Entities.Pacient(**db_data)

    
    @strawberry.field
    async def medicationToTake(self, info : Info, id:str) -> list[Relationships.Pacient_TAKES_Medication]:
        query = 'MATCH (pacient:Pacient)-[root:TAKES]->(medication:Medication) WHERE pacient.id = $id '
        filters, returns = prepareQuery('root', info.selected_fields, 'TAKES')
        query += (filters + 'RETURN ' + returns)     

        '''for field in info.selected_fields:
            for selection in field.selections:
                print(selection)
                if len(selection.selections) > 0:
                    print("oui")
'''         
        print('\n')
        print (query)
        print('\n')
        with neo4j_driver.session() as session:
            db_raw = session.run(query=query, parameters={'id': id})  
           
            db_data = db_raw.data()
            
            session.close()
        print(db_data)
        #Relationships.Pacient_TAKES_Medication(**db_data['TAKES'], medication=Medication(**db_data['medication']))
        return [Relationships.Pacient_TAKES_Medication(**data['TAKES'], medication=(Medication(**data['Medication']) if'Medication' in data else None )) for data in db_data]


