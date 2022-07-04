from unittest import result
import cv2
from Brain.simple_facerec import SimpleFacerec
import face_recognition
import os
import json

''' Comparation between Images
   img = cv2.imread(os.getcwd() + "/Brain/Messi1.webp")
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_encoding = face_recognition.face_encodings(rgb_img)[0]

    img2 = cv2.imread(os.getcwd() + "/Brain/images/Andre Moreira.jpg")
    rgb_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    img_encoding2 = face_recognition.face_encodings(rgb_img2)[0]

    result = face_recognition.compare_faces([img_encoding], img_encoding2)
    #print("Result: ", )
'''

def face_recognize(npimg):
    sfr = SimpleFacerec()
    sfr.load_encoding_images(os.getcwd() + "/Brain/images/")

    #img = cv2.imread(os.getcwd() + "/Brain/" + img)
    img = cv2.imdecode(npimg, 1)

    face_locations, face_names = sfr.detect_known_faces(img)
    result = ""
   
    listDetections = []

    for face_loc, name in zip(face_locations, face_names):
        listDetections.append({'name': name,
                            'box': {'y1': int(face_loc[0]), 'x2':  int(face_loc[1]), 'y2': int(face_loc[2]), 'x1': int(face_loc[3])}})
         #result = '{ "name": "' + name + '", box: { "y1": ' + int(face_loc[0]) + ' } }'

    json_obj_list = []
    json_obj_list.append({'type' : "Person",
                             'list': listDetections })
    json_dump = json.dumps(json_obj_list, indent="\t")
    print(json_dump)
    x =  '{ "name":"John", "age":30, "city":"New York"}'
    result = json.loads(str(json_dump))
    print(result)
    #cv2.imshow("IMG", img)
    #cv2.waitKey(0)
    return result

'''
#Encode faces from a folder
sfr = SimpleFacerec()
sfr.load_encoding_images("images/")


#Load camera
cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()

    #Detect faces
    face_locations, face_names = sfr.detect_known_faces(frame)
    for face_loc, name in zip(face_locations, face_names):
        #print(face_loc) # 4 values, top left, bottom right
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

        cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,200), 2)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
'''