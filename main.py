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

@lru_cache
def validateHash(request):
    operation = request.headers['Hash']
    if (request.method == "POST"):
        if operation == "3466fab4975481651940ed328aa990e4":
            operation = "READ"
        elif operation == "294ce20cdefa29be3be0735cb62e715d":
            operation = "CREATE"
        elif operation == "15a8022d0ed9cd9c2a2e756822703eb4":
            operation = "UPDATE"
        elif operation == "32f68a60cef40faedbc6af20298c1a1e":
            operation = "DELETE"
        else:
            operation = "HEADERS KEY (hash) VALUE CORRUPTED"
            return False, operation
    else: 
        operation = "WEBSOCKET"
    return True, operation


@app.middleware("http")
async def request_middleware(request: Request, call_next):
    #result, operation = validateHash(request)
        
    await logRequest(request.client.host, request.client.port, request.headers['Operation'])
   
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