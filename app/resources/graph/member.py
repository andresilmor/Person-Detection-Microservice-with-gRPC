import imp

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
    async def memberLogin(self, info : Info, username:str, password: str) -> Entities.Member:
        print(username + " " + password)
        query ="""
        MATCH (c:Member) WHERE c.username = $username AND c.password = $password
            CALL {
                WITH c
                OPTIONAL MATCH (i:Institution)<-[w:WORKS_IN]-(c) 
                    RETURN w{ .* , institution : PROPERTIES(i)} AS Institution
            }
        RETURN apoc.map.removeKeys(c {.*}, ['password', 'username']) AS Member, Institution
        """
     
        with neo4j_driver.session() as session:
            db_raw = session.run(query=query, parameters={'username': username, 'password': password})
            db_data = db_raw.data()
            session.close()
        #if isinstance(db_data['Institution'], tuple): 
        #    return Entities.Member(**db_data['Member'], institution=([Entities.Institution(**data) for data in db_data['Institution']]))
      
        return Entities.Member(**db_data[0]['Member'], token=signJWT(db_data[0]['Member']['uuid'], info.context['request'].client.host)['access_token'], memberOf=([Entities.MemberOf(role=data['Institution']['role'], institution= Entities.Institution(**data['Institution']['institution'])) for data in db_data]))
        