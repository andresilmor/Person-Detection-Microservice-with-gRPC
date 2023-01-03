import strawberry
from strawberry.types import Info
from utils.neo4jDriver.connection import neo4j_driver

from app.schema import Pacient, Medication, MedicationToTake
from typing import Union

from .common.commonResponses import ErrorMessage

from app.auth.jwt_bearer import authorizationRequired

MedicationToTakeResponse = strawberry.union(
    "MedicationToTakeResponse",
    [MedicationToTake, ErrorMessage]
)


@strawberry.type
class MedicationQuery:
    
    @strawberry.field
    async def medicationToTake(self, info : Info, isAvailable:int = None, pacientID:str = None, memberID:str = None, institutionID:str = None) -> Union[list[MedicationToTake], None]:
        varToPass = locals()
        del varToPass['self']
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
                                WHEN 'min' THEN  [ { atTime: took.atTime + duration( { minutes: u.intOfTime } ), quantity: u.quantityPer, timeMeasure: u.timeMeasure, intOfTime: u.intOfTime } ]  
                                WHEN 'h' THEN  [ { atTime: took.atTime  + duration( { hours: u.intOfTime } ), quantity: u.quantityPer, timeMeasure: u.timeMeasure, intOfTime: u.intOfTime } ]  
                                WHEN 'd' THEN  [ { atTime: took.atTime + duration( { days: u.intOfTime } ), quantity: u.quantityPer, timeMeasure: u.timeMeasure, intOfTime: u.intOfTime } ]  
                                WHEN 'm' THEN  [ { atTime: took.atTime + duration( { months: u.intOfTime } ), quantity: u.quantityPer, timeMeasure: u.timeMeasure, intOfTime: u.intOfTime } ]  
                                WHEN 'y' THEN  [ { atTime: took.atTime + duration( { years: u.intOfTime } ), quantity: u.quantityPer, timeMeasure: u.timeMeasure, intOfTime: u.intOfTime } ]  
                            END AS toTake    
                    RETURN PROPERTIES(toTake) as toTake ORDER BY toTake.atTime DESC LIMIT 1
                }
            RETURN toTake, PROPERTIES(p) AS pacient, PROPERTIES(m) AS medication ORDER BY toTake.atTime
            """

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
            return [MedicationToTake(**data['toTake'], pacient=(Pacient(**data['pacient']) if'pacient' in data else None ), medication=(Medication(**data['medication']) if'medication' in data else None )) for data in db_data]
        return await authorizationRequired(info, lambda: func(**varToPass))
