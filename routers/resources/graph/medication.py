from pyexpat import model
from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from logAssist import logDatabaseComm

# Import internal utilities for database access, authorisation, and schemas
from utils.neo4j_db.connection import neo4j_driver
#from app.authorisation.auth import get_current_active_user, create_password_hash
router = APIRouter()
'''
# Get 
#@router.get("/{pacientID}", response_model=MedicationToTake)
async def GetMedication(pacientID: str, request: Request):
    
    logDatabaseComm(request.client.host, request.url.path, "READ", "Medication")

    query = 'MATCH (p:Pacient)-[r:TAKES]->(m:Medication) WHERE p.id = $id RETURN apoc.map.merge(r, m) AS result'
    with neo4j_driver.session() as session:
        db_raw = session.run(query=query, parameters={'id': pacientID})
        data = db_raw.data()[0]['result']

    return MedicationToTake(**data)'''