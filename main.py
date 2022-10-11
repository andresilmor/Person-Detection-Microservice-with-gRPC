from fastapi import FastAPI
import uvicorn
import socket  

from routers import PacientCRUD, MachineLearning

from os import environ
from dotenv import load_dotenv, find_dotenv

env_loc = find_dotenv('.env')
load_dotenv(env_loc)

app = FastAPI(debug=environ.get('DEVELOPMENT'),
              title=environ.get('APP_NAME'),
              description='...',
              version=0.1,
              docs_url='/docs')
              #redoc_url='/redoc')


@app.on_event("startup")
async def startup_event():
    """
    Initialize FastAPI and add variables
    """

    hostname=socket.gethostname()   
    IPAddr=socket.gethostbyname(hostname) 

    print("***\n" + app.title + "\n***")

    print(">>> Hello There")
    print(">>> General " + IPAddr)
    

# ---------------------------------------------   ROUTER   ------------------------------------------------------- #   

app.include_router(
    MachineLearning.router,
    prefix='/brain',
    tags=['ML'],

)

app.include_router(
    PacientCRUD.router,
    prefix='/pacient',
    tags=['Pacient'],

)

    
# ---------------------------------------------------------------------------------------------------------------- #   

if __name__ == "__main__":
    uvicorn.run(app)