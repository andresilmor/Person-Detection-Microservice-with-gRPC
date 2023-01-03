import strawberry
from strawberry.types import Info

from utils.neo4jDriver.connection import neo4j_driver
from app.auth.jwt_handler import signJWT

from app.schema import Member, MemberOf, Institution

@strawberry.type
class MemberQuery:

    @strawberry.field
    async def memberLogin(self, info : Info, username:str, password: str) -> Member:
        query : str ="""
        MATCH (c:Member) WHERE c.username = $username AND c.password = $password
		CALL {
			OPTIONAL MATCH (i:Institution)<-[w:WORKS_IN]-(c) 
				WITH w{ .* , institution : PROPERTIES(i)} AS Institution
				WITH collect(Institution) AS Institutions
				RETURN Institutions
		}
		WITH apoc.map.removeKeys(c {.*}, ['password', 'username']) AS Member, Institutions
		WITH Institutions, Member
		RETURN {member: Member, institutions: Institutions} as member 
        """
     
        with neo4j_driver.session() as session:
            db_raw = session.run(query=query, parameters={'username': username, 'password': password})
            db_data = db_raw.data()
            session.close()
        #if isinstance(db_data['Institution'], tuple): 
        #    return Entities.Member(**db_data['Member'], institution=([Entities.Institution(**data) for data in db_data['Institution']]))
 
        return Member(**db_data[0]['member']["member"], 
            token=signJWT(db_data[0]['member']['member']['uuid'])['access_token'], 
            memberOf=([MemberOf(role=data['role'], institution= Institution(**data['institution'])) for data in db_data[0]['member']['institutions']]))
        