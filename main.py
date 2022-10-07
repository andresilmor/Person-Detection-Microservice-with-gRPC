from fastapi import FastAPI
import uvicorn
import socket  

from config import Settings
from apiRouter import MachineLearning

app = FastAPI(debug=Settings().development,
              title=Settings().app_name,
              description='...',
              version=0.1,
              docs_url='/docs',
              redoc_url='/redoc')


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

    
# ---------------------------------------------------------------------------------------------------------------- #   

if __name__ == "__main__":
    uvicorn.run(app)