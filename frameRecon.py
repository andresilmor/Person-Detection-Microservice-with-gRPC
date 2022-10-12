import argparse
import time
from pathlib import Path
import cv2
import torch
import numpy as np
import torch.backends.cudnn as cudnn
from torchvision import transforms
from numpy import random
import base64
from PIL import Image, ImageOps
from deepface import DeepFace as df
from retinaface import RetinaFace as rt
import matplotlib.pyplot as plt
from io import BytesIO
from emotic import Emotic 
import torchvision.models as t_models
from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path
from utils.plots import plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized, TracedModel
import os


def letterbox(img, new_shape=(640, 640), color=(114, 114, 114), auto=True, scaleFill=False, scaleup=True, stride=32):
    # Resize and pad image while meeting stride-multiple constraints
    shape = img.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:  # only scale down, do not scale up (for better test mAP)
        r = min(r, 1.0)

    # Compute padding
    ratio = r, r  # width, height ratios
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - \
        new_unpad[1]  # wh padding
    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding
    elif scaleFill:  # stretch
        dw, dh = 0.0, 0.0
        new_unpad = (new_shape[1], new_shape[0])
        ratio = new_shape[1] / shape[1], new_shape[0] / \
            shape[0]  # width, height ratios

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    if shape[::-1] != new_unpad:  # resize
        img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    img = cv2.copyMakeBorder(
        img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return img, ratio, (dw, dh)


def processImagesForEmotic(context_norm, body_norm, npimg, image_context=None, image_body=None, bbox=None):
    ''' Prepare context and body image. 
    :param context_norm: List containing mean and std values for context images. 
    :param body_norm: List containing mean and std values for body images. 
    :param image_context_path: Path of the context image. 
    :param image_context: Numpy array of the context image.
    :param image_body: Numpy array of the body image. 
    :param bbox: List to specify the bounding box to generate the body image. bbox = [x1, y1, x2, y2].
    :return: Transformed image_context tensor and image_body tensor.
    '''
    
    image_context = npimg[...,::-1].copy()

    if bbox is not None:
        image_body = image_context[bbox[1]:bbox[3],bbox[0]:bbox[2]].copy()
    
 
    image_context = cv2.resize(image_context, (224,224))
    image_body = cv2.resize(image_body, (128,128))
  
    
    test_transform = transforms.Compose([transforms.ToPILImage(),transforms.ToTensor()])
    context_norm = transforms.Normalize(context_norm[0], context_norm[1])  
    body_norm = transforms.Normalize(body_norm[0], body_norm[1])

    image_context = context_norm(test_transform(image_context)).unsqueeze(0)
    image_body = body_norm(test_transform(image_body)).unsqueeze(0)

    return image_context, image_body 


def detectObjects(npimg, yoloModel = None):
    classes_to_filter = ["bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork",
                         "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch", "potted plant", "bed", "dining table", "toilet", "mouse", "remote", "keyboard", "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"]  # You can give list of classes to filter by name, Be happy you don't have to put class number. ['train','person' ]

    opt = {

        # Path to weights file default weights are for nano model
        "weights": "weights/yolov7x.pt",
        "yaml": "data/coco.yaml",
        "img-size": 640,  # default image size
        "conf-thres": 0.25,  # confidence threshold for inference.
        "iou-thres": 0.45,  # NMS IoU threshold for inference.
        "device": 'cpu',  # device to run our model i.e. 0 or 0,1,2,3 or cpu
        "classes": classes_to_filter  # list of classes to filter or None

    }

    with torch.no_grad():
        weights, imgsz = opt['weights'], opt['img-size']
        set_logging()
        device = select_device(opt['device'])
        half = device.type != 'cpu'
        if (yoloModel is None):
            model = attempt_load(weights, map_location=device)  # load FP32 model
        else:
            model = yoloModel
        stride = int(model.stride.max())  # model stride
        imgsz = check_img_size(imgsz, s=stride)  # check img_size
        if half:
            model.half()

        names = model.module.names if hasattr(model, 'module') else model.names
        colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]
        if device.type != 'cpu':
            model(torch.zeros(1, 3, imgsz, imgsz).to(
                device).type_as(next(model.parameters())))

        img = letterbox(npimg, imgsz, stride=stride)[0]
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference
        t1 = time_synchronized()
        pred = model(img, augment=False)[0]

        # Apply NMS
        classes = None
        if opt['classes']:
            classes = []
            for class_name in opt['classes']:
                classes.append(names.index(class_name))

        if classes:
            classes = [i for i in range(len(names)) if i not in classes]

        pred = non_max_suppression(
            pred, opt['conf-thres'], opt['iou-thres'], classes=classes, agnostic=False)
        t2 = time_synchronized()
        persons = {"persons": []}
        filtering = {"filter": []}
        for i, det in enumerate(pred):
            s = ''
            s += '%gx%g ' % img.shape[2:]  # print string
            gn = torch.tensor(npimg.shape)[[1, 0, 1, 0]]
            if len(det):
                det[:, :4] = scale_coords(
                    img.shape[2:], det[:, :4], npimg.shape).round()

                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    # add to string
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "

                for *xyxy, conf, cls in reversed(det):
                    label = f'{names[int(cls)]} {conf:.2f}'
                    plot_one_box(xyxy, npimg, label=label,
                                 color=colors[int(cls)], line_thickness=3)
                    if (label.startswith(('laptop', 'cell', 'tv'))):
                        filtering["filter"].append({"box": {"x1": int(np.array(xyxy)[0]), "y1": int(np.array(
                            xyxy)[1]), "x2": int(np.array(xyxy)[2]), "y2": int(np.array(xyxy)[3])}})

                    else:
                        persons["persons"].append({"box": {"x1": int(np.array(xyxy)[0]), "y1": int(np.array(xyxy)[
                                                  1]), "x2": int(np.array(xyxy)[2]), "y2": int(np.array(xyxy)[3])}})

        return filtering, persons
    

def recognizeEmotions(npimg, personBox):
    thresholds_path = "thresholds"
    model_path = "models/emotic"
    
    cat = ['Affection', 'Anger', 'Annoyance', 'Anticipation', 'Aversion', 'Confidence', 'Disapproval', 'Disconnection', \
            'Disquietment', 'Doubt/Confusion', 'Embarrassment', 'Engagement', 'Esteem', 'Excitement', 'Fatigue', 'Fear','Happiness', \
            'Pain', 'Peace', 'Pleasure', 'Sadness', 'Sensitivity', 'Suffering', 'Surprise', 'Sympathy', 'Yearning']
    cat2ind = {}
    ind2cat = {}
    for idx, emotion in enumerate(cat):
        cat2ind[emotion] = idx
        ind2cat[idx] = emotion
        
    vad = ['Valence', 'Arousal', 'Dominance']
    ind2vad = {}
    for idx, continuous in enumerate(vad):
        ind2vad[idx] = continuous
        
    context_mean = [0.4690646, 0.4407227, 0.40508908]
    context_std = [0.2514227, 0.24312855, 0.24266963]
    body_mean = [0.43832874, 0.3964344, 0.3706214]
    body_std = [0.24784276, 0.23621225, 0.2323653]
    context_norm = [context_mean, context_std]
    body_norm = [body_mean, body_std]

    
    device = torch.device("cuda:%s" %(str(0)) if torch.cuda.is_available() else "cpu")
    thresholds = torch.FloatTensor(np.load(os.path.join(thresholds_path, 'emotic_thresholds.npy'))).to(device) 
    model_context = torch.load(os.path.join(model_path,'model_context1.pth')).to(device)
    model_body = torch.load(os.path.join(model_path,'model_body1.pth')).to(device)
    #emotic_model = torch.load(os.path.join(model_path,'model_emotic1.pth')).to(device)
    emotic_state_dict = torch.load(os.path.join(model_path,'model_emotic1.pt'))


    #https://github.com/pytorch/pytorch/issues/7812
    #https://pytorch.org/docs/master/notes/serialization.html

    emotic_model = Emotic(2048,2048)
    #emotic_model = Emotic(512,512)
    emotic_model.load_state_dict(emotic_state_dict)

    model_context.eval()
    model_body.eval()
    emotic_model.eval()
    models = [model_context, model_body, emotic_model]

    bbox = [int(personBox[0]), int(personBox[1]), int(personBox[2]), int(personBox[3])] # x1 y1 x2 y2
    image_context = None
    image_body = None
    image_context, image_body = processImagesForEmotic(context_norm, body_norm, npimg, image_context=image_context, image_body=image_body, bbox=bbox)
    
    model_context, model_body, emotic_model = models

    with torch.no_grad():
        image_context = image_context.to(device)
        image_body = image_body.to(device)
        
        pred_context = model_context(image_context)
        pred_body = model_body(image_body)
        pred_cat, pred_cont = emotic_model(pred_context, pred_body)
        pred_cat = pred_cat.squeeze(0)
        pred_cont = pred_cont.squeeze(0).to("cpu").data.numpy()

        bool_cat_pred = torch.gt(pred_cat, thresholds)
    
    cat_emotions = list()
    for i in range(len(bool_cat_pred)):
        if bool_cat_pred[i] == True:
            cat_emotions.append(ind2cat[i])

    if True:
        print ('\n Image predictions')
        print ('Continuous Dimnesions Predictions') 
        for i in range(len(pred_cont)):
            print ('Continuous %10s %.5f' %(ind2vad[i], 10*pred_cont[i]))
        print ('Categorical Emotion Predictions')
        for emotion in cat_emotions:
            print ('Categorical %16s' %(emotion))
    
    pred_cat = cat_emotions
    pred_cont = 10*pred_cont
    
    
    #pred_cat, pred_cont = infer(context_norm, body_norm, ind2cat, ind2vad, device, thresholds, models, npimg, bbox=bbox)
        
    resp = {'continuous' : [], 'categorical' : []}
        
    write_line = list()
    for emotion in pred_cat:
        write_line.append(emotion)
        resp['categorical'].append(emotion)
    for continuous in pred_cont:
        write_line.append(str('%.4f' %(continuous)))
        resp['continuous'].append(str('%.4f' %(continuous))) # Valence Arousal Dominance
    write_line = ' '.join(write_line) 
    
    return resp


def rectContains(rect, pt):
    return rect[0] < pt[0] < rect[0]+rect[2] and rect[1] < pt[1] < rect[1]+rect[3]


def toIgnore(person, filtering):
    for filter in filtering['filter']:
        if (rectContains((filter['box']['x1'], filter['box']['y1'], filter['box']['x2'], filter['box']['y2']), person)):
            return True


def frameRecon(encodeFace = "", yoloModel = None):
    '''
    img = cv2.imread('abel.jpg')

    jpg_img = cv2.imencode('.jpg', img)
    b64_string = base64.b64encode(jpg_img[1]).decode('utf-8')
    encodeFace = np.frombuffer(base64.b64decode(b64_string), dtype=np.uint8)
    '''

    img = Image.open(BytesIO(bytearray(encodeFace)))
    img.save(os.getcwd() + "/frame.png")
    npimg = cv2.imdecode(encodeFace, 1)

    npimgClean = np.copy(npimg)

    filtering, persons = detectObjects(npimg, yoloModel)

    #print("FILTERING")
    #print(filtering)
    #print("PERSONS")
    #print(persons)

    response =  []

    for person in persons['persons']:
        print( person['box'])
        personCenterX = int(person['box']['x1'] + ((person['box']['x2'] - person['box']['x1']) * 0.5))
        personCenterY = int(person['box']['y1'] + ((person['box']['y2'] - person['box']['y1']) * 0.5))
        #if (toIgnore((personCenterX, personCenterY), filtering)):
        #    continue
        faces = rt.detect_faces(
            npimg[person['box']['y1']:person['box']['y2'], person['box']['x1']:person['box']['x2']])
        if (len(faces) == 1):
            facial_area = faces['face_1']['facial_area']
            #[ {'type': 'Person', 'list':[{'name': 'Abel Ferraz', 'box': {'y1': 656, 'x2': 1184, 'y2': 848, 'x1': 980 } } ] } ]
            
            #cv2.imshow("DAD", npimg[person['box']['y1'] + facial_area[1]:person['box']['y1'] +
            #           facial_area[3], person['box']['x1'] + facial_area[0]:person['box']['x1'] + facial_area[2]])
            #cv2.waitKey(0)
            resp = df.find(img_path=npimg[person['box']['y1']:person['box']['y2'], person['box']['x1']:person['box']['x2']],
                           db_path='database/', model_name='ArcFace', enforce_detection=False, prog_bar=False, silent=True)

            identity = str(resp.iloc[:1]['identity'])
            id = identity[identity.find("/") + 1: identity.rfind("/")] 
            
            response.append({'id': id, 'bodyCenter' : {'x' : int(personCenterX), 'y' : int(personCenterY)}, 'faceRect' : {'x1' : int(person['box']['x1'] + facial_area[0]), 'y1' : int(person['box']['y1'] + facial_area[1]), 'x2' : int(person['box']['x1'] + facial_area[2]), 'y2' : int(person['box']['y1'] +
                       facial_area[3])}, 'emotions' : recognizeEmotions(npimgClean, [person['box']['x1'], person['box']['y1'], person['box']['x2'], person['box']['y2']])})
    return response


if __name__ == '__main__':
    frameRecon()
