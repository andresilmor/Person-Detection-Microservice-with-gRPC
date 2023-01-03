from fastapi import APIRouter, Request, WebSocket
from fastapi.responses import HTMLResponse
import base64
import numpy as np
import json
import re

from frameRecon import frameRecon
from models.experimental import attempt_load
from emotic import Emotic 
import torch
import os

router = APIRouter()

def preloadModels():
    yoloModel = attempt_load("weights/yolov7x.pt", "cpu")

    model_context = torch.load(os.path.join("models/emotic",'model_context1.pth')).to("cpu")
    model_body = torch.load(os.path.join("models/emotic",'model_body1.pth')).to("cpu")

    emotic_state_dict = torch.load(os.path.join("models/emotic",'model_emotic1.pt'))
    emotic_model = Emotic(2048,2048)
    emotic_model.load_state_dict(emotic_state_dict)

    model_context.eval()
    model_body.eval()
    emotic_model.eval()
    return [yoloModel, model_context, model_body, emotic_model]

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
    var ws = new WebSocket("wss://4d74-193-136-194-58.eu.ngrok.io/ws/test");
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

@router.get("/")
async def get():
    return HTMLResponse(html)

@router.websocket("/test")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

@router.websocket("/live")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("oi")
    while True:
        data = await websocket.receive_text()
        print("oi2")
        print(data)
        if (data in ['Connection Opened','inside', 'Sending', 'Sended', 'Erro: MediaFrameReference', 'Erro: Exception', 'Erro: SoftwareBitmap', 'Regex']): 
            await websocket.send_text(f"Ignore")
        #await websocket.send_text(data)
        else:    
            
            frame = json.loads(data)
            
            b64 = (frame['bytes'] + '===')[0: len(frame['bytes']) + (len(frame['bytes']) % 4)]
            b64 = re.sub(r'/_/g', '/', b64)
            b64 = re.sub(r'/-/g', '+', b64)

            encodeFace = np.fromstring(base64.b64decode(b64), dtype=np.uint8) 
            
            
            listDetections =  frameRecon(encodeFace)

            json_obj_list = []
            json_obj_list.append({'type' : "Person",
                                    'list': listDetections })
            json_dump = json.dumps(json_obj_list, indent="\t")
       

            print(json.loads(str(json_dump)))
            face_recog = "[{'type': 'Person', 'list': [{'name': 'Andre Moreira', 'box': {'y1': 564, 'x2': 908, 'y2': 772, 'x1': 700}}]}] "
            await websocket.send_json(json.loads(str(json_dump)))
