from fastapi import APIRouter, Request, WebSocket
from fastapi.responses import HTMLResponse
import base64
import numpy as np
import json
import re


from logAssist import *
from frameRecon import frameRecon

router = APIRouter()
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




@router.get("/test")
async def get(request: Request):
    
    print(request.client.host)
    logWebSocketConnection(request.client.host, request.url._url)
    return HTMLResponse(html)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
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