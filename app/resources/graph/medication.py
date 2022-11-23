import imp
from msilib.schema import Error
from unicodedata import name
from unittest import result
from urllib import response
import strawberry
from strawberry.types import Info
from utils.neo4j_db.connection import neo4j_driver
from utils.neo4j_db import Entities, Relationships, SupportMethods
from typing import Union

import app.resources.commonResponses as CommonResponses
import app.resources.customResponses as CustomResponses

from app.auth.jwt_bearer import jwtBearer, authorizationRequired
from fastapi import Depends

MedicationToTakeResponse = strawberry.union(
    "MedicationToTakeResponse",
    [Relationships.Medication_UNDER_Receipt, CommonResponses.ErrorMessage]
)


@strawberry.type
class MedicationQuery:
    
    @strawberry.field
    async def medicationToTake(self, info : Info, isAvailable:int = None, pacientID:str = None, memberID:str = None, institutionID:str = None) -> Union[list[CustomResponses.MedicationToTake], None]:
        varToPass = locals()
        del varToPass['self']
        print("\nBefore token")
        async def func(info : Info, isAvailable:int = None, pacientID:str = None, memberID:str = None, institutionID:str = None):
            query = """
            MATCH (p)<-[:RESPONSIBLE_OF]-(c:Member)-[w:WORKS_IN]->(i:Institution)<-[:UNDER_CARE_OF]-(p:Pacient)<-[:PRESCRIBED_FOR]-(:Receipt)<-[u:UNDER]-(m:Medication)    
            WHERE True = True """

            parameters = {}
            if (isAvailable != None):
                query += """AND u.isAvailable = $isAvailable """
                parameters["isAvailable"] = True if isAvailable == 1 else False
            if (pacientID != None):
                query += """AND p.uuid = $pacientID """
                parameters["pacientID"] = pacientID
            if (memberID != None):
                query += """AND c.uuid = $memberID """
                parameters["memberID"] = memberID
            if (institutionID != None):
                query += """AND i.uuid = $institutionID """
                parameters["institutionID"] = institutionID
                
            query += """
                CALL {
                    WITH m, u
                    OPTIONAL MATCH (:Pacient)-[took:TOOK]->(m2:Medication)
                        WHERE m2.uuid = m.uuid 
                            UNWIND CASE u.timeMeasure
                                WHEN 'min' THEN  [ { atTime: took.atTime + duration( { minutes: u.intOfTime } ), quantity: u.quantityPer } ]  
                                WHEN 'h' THEN  [ { atTime: took.atTime  + duration( { hours: u.intOfTime } ), quantity: u.quantityPer } ]  
                                WHEN 'd' THEN  [ { atTime: took.atTime + duration( { days: u.intOfTime } ), quantity: u.quantityPer } ]  
                                WHEN 'm' THEN  [ { atTime: took.atTime + duration( { months: u.intOfTime } ), quantity: u.quantityPer } ]  
                                WHEN 'y' THEN  [ { atTime: took.atTime + duration( { years: u.intOfTime } ), quantity: u.quantityPer } ]  
                            END AS toTake    
                    RETURN PROPERTIES(toTake) as toTake ORDER BY toTake.atTime DESC LIMIT 1
                }
            RETURN toTake, PROPERTIES(p) AS pacient, PROPERTIES(m) AS medication ORDER BY toTake.atTime
            """

            print("\nHere\n")

            with neo4j_driver.session() as session:
                db_raw = session.run(query=query, parameters=parameters)  
                db_data = db_raw.data() 
                session.close()
                
            '''
            query = 'MATCH (pacient:Pacient)-[root:TAKES]->(medication:Medication) WHERE pacient.id = $id '
            filters, returns = SupportMethods.prepareQuery('root', info.selected_fields, 'TAKES')
            query += (filters + 'RETURN ' + returns)     
            print (query)
            '''

            print("\n" + str(db_data) +"\n")
            return [CustomResponses.MedicationToTake(**data['toTake'], pacient=(Entities.Pacient(**data['pacient']) if'pacient' in data else None ), medication=(Entities.Medication(**data['medication']) if'medication' in data else None )) for data in db_data]
        return await authorizationRequired(info, lambda: func(**varToPass))

