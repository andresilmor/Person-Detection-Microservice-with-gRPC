import imp
from msilib.schema import Error
from unicodedata import name
from unittest import result
from urllib import response
import strawberry
from strawberry.types import Info
from utils.neo4j_db.connection import neo4j_driver
from utils.neo4j_db import Entities

from app.auth.jwt_handler import signJWT, token_response

@strawberry.type
class CaregiverQuery:

    @strawberry.field
    async def caregiverLogin(self, info : Info, username:str, password: str) -> Entities.Caregiver:

        query ="""
        MATCH (c:Caregiver) WHERE c.username = $username AND c.password = $password
            CALL {
                WITH c
                OPTIONAL MATCH (i:Institution)<-[:WORKS_IN]-(c) RETURN PROPERTIES(i) AS Institution
            }
        RETURN apoc.map.removeKeys(c {.*}, ['password', 'username']) AS Caregiver, Institution
        """
     
        with neo4j_driver.session() as session:
            db_raw = session.run(query=query, parameters={'username': username, 'password': password})
            db_data = db_raw.data()[0]
            session.close()
        if isinstance(db_data['Institution'], tuple): 
            return Entities.Caregiver(**db_data['Caregiver'], institution=([Entities.Institution(**data) for data in db_data['Institution']]))
        return Entities.Caregiver(**db_data['Caregiver'], token=signJWT(db_data['Caregiver']['uuid'], info.context['request'].client.host)['access_token'], institution=([Entities.Institution(**db_data['Institution'])]))
        