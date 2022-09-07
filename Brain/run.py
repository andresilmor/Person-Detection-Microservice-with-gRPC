import base64
from fastapi import FastAPI, WebSocket
import uvicorn
import numpy as np
import socket   
import json
import os
import re
from frameRecon import frameRecon
#import pickle

app = FastAPI(debug=True, title="The Brain")

@app.on_event("startup")
async def startup_event():
    """
    Initialize FastAPI and add variables
    """

    hostname=socket.gethostname()   
    IPAddr=socket.gethostbyname(hostname) 

    print(">>> Hello There")
    print(">>> General " + IPAddr)


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def root():
    recog =  frameRecon("")
    print(recog)
    return {"message": "Hello World"}

@app.websocket("/test")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("check")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(data)
        if (data in ['inside', 'Sending', 'Sended', 'Erro: MediaFrameReference', 'Erro: Exception', 'Erro: SoftwareBitmap', 'Regex']): 
            await websocket.send_text(data)
        else:    
            
            frame = json.loads(data)
            #frame['cameraLocation']['position']['y'] -= 0.100
            b64 = (frame['bytes'] + '===')[0: len(frame['bytes']) + (len(frame['bytes']) % 4)]
            b64 = re.sub(r'/_/g', '/', b64)
            b64 = re.sub(r'/-/g', '+', b64)

            encodeFace = np.fromstring(base64.b64decode(b64), dtype=np.uint8) 
            
            listDetections =  frameRecon(encodeFace)

            print(listDetections)
        

            
            
            #unitCenterX = frame['cameraLocation']['position']['x']
            #unitCenterY = frame['cameraLocation']['position']['y']

            #print("CENTER X: {}, CENTER Y: {}".format(unitCenterX, unitCenterY))

            #   720 - unitCenterX
            #   x       

            #for detection in listDetections:
            #    detection['box']['x1'] = (detection['box']['x1'] * unitCenterX) / 720
            #    detection['box']['x2'] = (detection['box']['x2'] * unitCenterX) / 720
            #    detection['box']['y1'] = (detection['box']['y1'] * unitCenterY) / 468
            #    detection['box']['y2'] = (detection['box']['y2'] * unitCenterY) / 468

            pixelX = 1
            pixelY = 468

            pixelX = 1 - 720
            pixelY = 468 - 468 

             
            '''

       
            listDetections.append({'name': "BOTTOM LEFT",
                                    'box': {'y1': int(0), 'x2':  int(0), 'y2': int(0), 'x1': int(0), 'centerX': (), 'centerY': ((1 * unitCenterY) / 468)}})
            listDetections.append({'name': "BOTTOM RIGHT",
                                    'box': {'y1': int(0), 'x2':  int(0), 'y2': int(0), 'x1': int(0), 'centerX': ((1440 * unitCenterX) / 720), 'centerY': ((1 * unitCenterY) / 468)}})
            listDetections.append({'name': "TOP LEFT",
                                    'box': {'y1': int(0), 'x2':  int(0), 'y2': int(0), 'x1': int(0), 'centerX': ((1 * unitCenterX) / 720), 'centerY': ((936 * unitCenterY) / 468)}})
            listDetections.append({'name': "TOP RIGHT",
                                    'box': {'y1': int(0), 'x2':  int(0), 'y2': int(0), 'x1': int(0), 'centerX': ((1440 * unitCenterX) / 720), 'centerY': ((936 * unitCenterY) / 468)}})
            '''
            
            json_obj_list = []
            json_obj_list.append({'type' : "Person",
                                    'list': listDetections })
            json_dump = json.dumps(json_obj_list, indent="\t")
            
                # TODO 
                # Show normal frame
                # Show frame with draw
                # Show box measures
                
            
            #with open(os.getcwd() + "/Brain/imageToSave.png", "wb") as fh:
            #    fh.write(base64.decodebytes(data))
#            await websocket.send_text("check")
            print(json.loads(str(json_dump)))
            face_recog = "[{'type': 'Person', 'list': [{'name': 'Andre Moreira', 'box': {'y1': 564, 'x2': 908, 'y2': 772, 'x1': 700}}]}] "
            await websocket.send_json(json.loads(str(json_dump)))


if __name__ == "__main__":
    uvicorn.run(app)

