from functools import lru_cache
import strawberry
from strawberry.types import Info
from fastapi import FastAPI, Request
from strawberry.fastapi import GraphQLRouter
from strawberry.extensions import AddValidationRules
from graphql.validation import NoSchemaIntrospectionCustomRule
import uvicorn
import socket  
import time

from app import Mutation, Query, WS_Connections
from app.resources.commonResponses import VisibleError, MaskErrors, ErrorMessage

from os import environ
from dotenv import load_dotenv, find_dotenv
from app.resources.websockets.ws import preloadModels

from app.auth.jwt_handler import decode_jwt
from logAssist import logRequest

from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

import utils.modelsStorage

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, NoEncryption, PrivateFormat, PublicFormat

#private_key = Ed25519PrivateKey.generate()
#print(private_key.private_bytes(encoding=Encoding.PEM, format=PrivateFormat.PKCS8, encryption_algorithm=NoEncryption()))
#print(private_key.public_key().public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo))

env_loc = find_dotenv('.env')
load_dotenv(env_loc)

app = FastAPI(debug=environ.get('DEVELOPMENT'),
              title=environ.get('APP_NAME'),
              description='...',
              version=0.1,
              docs_url='/docs')
              #redoc_url='/redoc')

#yoloModel, model_context, model_body, emotic_model = None

@app.on_event("startup")
async def startup_event():
    """
    Initialize FastAPI and add variables
    """

    utils.modelsStorage.init()

    utils.modelsStorage.models = preloadModels()

    hostname=socket.gethostname()   
    IPAddr=socket.gethostbyname(hostname) 

    print("***\n" + app.title + "\n***")

    print(">>> Hello There")
    print(">>> General " + IPAddr)
    
    
# ---------------------------------------------------------------------------------------------------------------- #

# --------------------------------------------   Middleware   ---------------------------------------------------- #   
 
if (environ.get('DEVELOPMENT') is False):
    app.add_middleware(HTTPSRedirectMiddleware)

@app.middleware("http")
async def request_middleware(request: Request, call_next):
        
    await logRequest(request.client.host, request.client.port)
   
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# ---------------------------------------------------------------------------------------------------------------- #

# ---------------------------------------------   GraphQL   ------------------------------------------------------- #   

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        AddValidationRules([NoSchemaIntrospectionCustomRule]),
        
    ])

app.include_router(GraphQLRouter(schema), prefix="/api")

# ---------------------------------------------------------------------------------------------------------------- #

# --------------------------------------------   WebSockets   ---------------------------------------------------- #   

app.include_router(WS_Connections.router, prefix='/ws')

# ---------------------------------------------------------------------------------------------------------------- #   



if __name__ == "__main__":
    # workers = 2 x number_of_cores +1 (num_of_threads_per_core x number_of_cores + 1 )
    isDev = environ.get('DEVELOPMENT') != "False"
    uvicorn.run("main:app",host= "0.0.0.0", port=8000, log_level="info", reload=isDev, workers=4, use_colors=isDev, access_log=isDev)