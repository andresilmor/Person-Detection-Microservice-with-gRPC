from pyexpat import model
from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from logAssist import logDatabaseComm

# Import internal utilities for database access, authorisation, and schemas
from utils.neo4j_db.connection import neo4j_driver
#from app.authorisation.auth import get_current_active_user, create_password_hash
from utils.neo4j_db.schema import Pacient

router = APIRouter()

# Get 
@router.get("/{pacientID}", response_model=Pacient)
async def get(pacientID: str, request: Request):
    
    print(pacientID)
    from utils.modelsStorage import models

    for m in models:
        print(type(m))

    logDatabaseComm(request.client.host, request.url._url, "VIEW", "Pacient")
    
    query ="MATCH (pacient:Pacient) WHERE pacient.id = $id RETURN (pacient)"
    
    with neo4j_driver.session() as session:
        db_raw = session.run(query=query, parameters={'id': pacientID})  
        data = db_raw.data()[0]['pacient']
        

    return Pacient(**data)