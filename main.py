import strawberry
from strawberry.types import Info
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import uvicorn
import socket  

from routers import Mutation, Query, WS_Connections

from os import environ
from dotenv import load_dotenv, find_dotenv
from routers.resources.websockets.ws import preloadModels

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
    
    

# ---------------------------------------------   GraphQL   ------------------------------------------------------- #   

if (environ.get('DEVELOPMENT')):
    schema = strawberry.Schema(query=Query, mutation=Mutation)
else: 
    schema = strawberry.Schema(mutation=Mutation)

app.include_router(GraphQLRouter(schema), prefix="/api")

# ---------------------------------------------------------------------------------------------------------------- #

# --------------------------------------------   WebSockets   ---------------------------------------------------- #   

app.include_router(WS_Connections.router, prefix='/ws')

# ---------------------------------------------------------------------------------------------------------------- #   



if __name__ == "__main__":
    uvicorn.run(app)