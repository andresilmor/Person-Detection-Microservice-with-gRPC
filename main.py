import strawberry
from strawberry.types import Info
from fastapi import FastAPI, Request
from strawberry.fastapi import GraphQLRouter
import uvicorn
import socket  
import time

from routers import Mutation, Query, WS_Connections

from os import environ
from dotenv import load_dotenv, find_dotenv
from routers.resources.websockets.ws import preloadModels
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

    utils.modelsStorage.models =preloadModels()

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
    await logRequest(request.client.host, request.client.port, request.headers['hash'])
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# ---------------------------------------------------------------------------------------------------------------- #

# ---------------------------------------------   GraphQL   ------------------------------------------------------- #   

schema = strawberry.Schema(query=Query, mutation=Mutation)

app.include_router(GraphQLRouter(schema), prefix="/api")

# ---------------------------------------------------------------------------------------------------------------- #

# --------------------------------------------   WebSockets   ---------------------------------------------------- #   

app.include_router(WS_Connections.router, prefix='/ws')

# ---------------------------------------------------------------------------------------------------------------- #   



if __name__ == "__main__":
    uvicorn.run(app)