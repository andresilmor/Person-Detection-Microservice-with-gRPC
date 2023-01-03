import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.extensions import AddValidationRules
from fastapi import FastAPI, Request
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from graphql.validation import NoSchemaIntrospectionCustomRule
import uvicorn
import socket  
import time

from app import Mutation, Query, WS_Connections

import os
from dotenv import load_dotenv, find_dotenv
from app.websockets.ws import preloadModels

from app.auth.jwt_handler import decode_jwt
from logAssist import logRequest

import utils.modelsStorage

#private_key = Ed25519PrivateKey.generate()
#print(private_key.private_bytes(encoding=Encoding.PEM, format=PrivateFormat.PKCS8, encryption_algorithm=NoEncryption()))
#print(private_key.public_key().public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo))

env_loc = find_dotenv('.env')
load_dotenv(env_loc)

# ---------------------------------------------------------------------------------------------------------------- #

# --------------------------------------------      NGROK     ---------------------------------------------------- #   
'''
class Settings(BaseSettings):
    # ... The rest of our FastAPI settings

    BASE_URL = "http://localhost:8000"
    USE_NGROK = os.environ.get('USE_NGROK')


settings = Settings()


def init_webhooks(base_url):
    # Update inbound traffic via APIs to use the public-facing ngrok URL
    pass
'''    

app = FastAPI(debug=os.environ.get('DEVELOPMENT'),
              title=os.environ.get('APP_NAME'),
              description='...',
              version=0.1,
              docs_url='/docs')
              #redoc_url='/redoc')

'''
print("=> "+ settings.USE_NGROK)
if settings.USE_NGROK:
    # pyngrok should only ever be installed or initialized in a dev environment when this flag is set
    from pyngrok import ngrok

    # Get the dev server port (defaults to 8000 for Uvicorn, can be overridden with `--port`
    # when starting the server
    port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 8000

    # Open a ngrok tunnel to the dev server
    public_url = ngrok.connect(port).public_url
    logger.info("ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))

    # Update any base URLs or webhooks to use the public ngrok URL
    settings.BASE_URL = public_url
    init_webhooks(public_url)

'''
# ---------------------------------------------------------------------------------------------------------------- #

# --------------------------------------------    Startup     ---------------------------------------------------- #   


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
 
if (os.environ.get('DEVELOPMENT') is False):
    app.add_middleware(HTTPSRedirectMiddleware)

@app.middleware("http")
async def request_middleware(request: Request, call_next):
    #await logRequest(request.client.host, request.client.port)
    #start_time = time.time()
    response = await call_next(request)
    #process_time = time.time() - start_time
    #response.headers["X-Process-Time"] = str(process_time)
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

from app.auth.jwt_handler import decode_jwt

@app.get("/validate")
async def validate_token(request:Request):
    return {"isValid" : await decode_jwt(request.headers["Authorization"])}



if __name__ == "__main__":
    # workers = 2 x number_of_cores +1 (num_of_threads_per_core x number_of_cores + 1 )
    isDev = os.environ.get('DEVELOPMENT') != "False"
    uvicorn.run("main:app",host= "0.0.0.0", port=8000, log_level="info", reload=isDev, workers=4, use_colors=isDev, access_log=isDev)