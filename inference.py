from provider import *
from facerecognizer import *
import cv2
import os
import numpy as np

def load_db(path):
    db = []
    names = []
    for filename in os.listdir(path):
        encoding = face_encodings(load_image_file(f'{path}/{filename}'))
        db.append(encoding[0])
        names.append(filename.split('.')[0])
    return names, db

def recognize_faces(frame, names, faces):
    rectangles = face_locations(frame)
    for rectangle in rectangles:
        t, r, b, l = rectangle
        frame = cv2.rectangle(frame, (l, t), (r, b), (0,255,0), 2)
        face = frame[t:b, l:r]
        new_encoding = face_encodings(face)
        if len(new_encoding)!=0:
            result = compare_faces(faces, new_encoding[0])
            index = np.where(result)[0]
            person ='Unknown'
            if len(index)!=0:
                person = names[index[0]]
            frame = cv2.putText(frame, person, (l,t), cv2.FONT_HERSHEY_SIMPLEX , 1, (255, 0, 0), 2, cv2.LINE_AA)
    return frame


class VideoCamera(object):

    def __init__(self, url):
        self.video_recv = VideoReceiver(url)
        self.names, self.db = load_db('./faces')

    def get_frame(self):
        frame = self.video_recv.get_frame()
        frame = recognize_faces(frame, self.names, self.db)
        # encode OpenCV raw frame to jpg and displaying it
        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
