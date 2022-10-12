from fastapi import APIRouter, Request, WebSocket
from fastapi.responses import HTMLResponse
import base64
import numpy as np
import json
import re

from logAssist import logWebSocketConnection

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
    return [yoloModel, model_context, model_body, emotic_model]

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
            
            listDetections =  frameRecon(encodeFace, yoloModel)

            json_obj_list = []
            json_obj_list.append({'type' : "Person",
                                    'list': listDetections })
            json_dump = json.dumps(json_obj_list, indent="\t")
       

            print(json.loads(str(json_dump)))
            face_recog = "[{'type': 'Person', 'list': [{'name': 'Andre Moreira', 'box': {'y1': 564, 'x2': 908, 'y2': 772, 'x1': 700}}]}] "
            await websocket.send_json(json.loads(str(json_dump)))