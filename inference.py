from provider import *
from facerecognizer import *
import cv2
import os
import numpy as np
import threading
from notification_manager import *
import pandas as pd

def load_db():
    response = requests.get(url="http://localhost:8000/personapp/persons")
    persons = response.json()

    for person in persons:
        person['encoding'] = np.array(eval(person['encoding']))
    return pd.DataFrame(persons)

def recognize_face(rectangle, frame, persons, camera):
    t, r, b, l = rectangle
    frame = cv2.rectangle(frame, (l, t), (r, b), (0,255,0), 2)
    face = frame[t:b, l:r]
    new_encoding = face_encodings(face)
    person_name ='Unknown'
    if len(new_encoding)!=0: # encoded successfully
        encodings = persons['encoding'].tolist()
        result = compare_faces(encodings, new_encoding[0])
        index = np.where(result)[0]
        if len(index)!=0:
            i = index[0]
            person = {
                "id": persons['id'].tolist()[i],
                "first_name": persons['first_name'].tolist()[i],
                "last_name": persons['last_name'].tolist()[i],
                "encoding": persons['encoding'].tolist()[i],
            }
            
            person_name = f"{person['first_name']} {person['last_name']}"
            thread = threading.Thread(target=send_person_detected, args=(person,rectangle, new_encoding[0], camera), daemon=True)
            thread.start()

    frame = cv2.putText(frame, person_name, (l,t), cv2.FONT_HERSHEY_SIMPLEX , 1, (255, 0, 0), 2, cv2.LINE_AA)
    


def recognize_faces(frame, persons, camera):
    rectangles = face_locations(frame)
    snapshot_id = 0
    if len(rectangles)!=0:
        snapshot_id, path = save_snapshot(frame, camera)
        for rectangle in rectangles:
            recognize_face(rectangle, frame, persons, snapshot_id)
        take_snapshot(frame, path)
    return frame


import time

class VideoCamera(object):

    def __init__(self, url, camera):
        self.video_recv = VideoReceiver(url)
        self.db = load_db()
        self.camera = camera

    def get_frame(self):
        start = time.time()
        frame = self.video_recv.get_frame()
        frame = recognize_faces(frame, self.db, self.camera)
        # encode OpenCV raw frame to jpg and displaying it
        _, jpeg = cv2.imencode('.jpg', frame)
        self.video_recv.send_ack()
        print(f"FPS with inference = {time.time() - start}")
        return jpeg.tobytes()
