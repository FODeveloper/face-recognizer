import requests
import os
import datetime
import cv2

SNAPSHOT_PATH = os.path.join(os.getcwd(), 'snapshots')


def save_snapshot(frame, camera):

    snapshot = {
        "path": os.path.join(SNAPSHOT_PATH, f"{camera['position']}-{datetime.datetime.now()}.jpg"),
        "camera": camera['id']
    }
    save_snapshot = requests.post("http://127.0.0.1:8000/alertapp/snapshots/", json=snapshot)
    if save_snapshot.status_code == 400:
        print("Problem in saving snapshots")
        return 0
    return save_snapshot.json()['id'], snapshot['path']


def send_person_detected(person, boundingbox, encoding, snapshot_id):
    t, r, b, l = boundingbox

    detected_person = {
        "bb_tlx": l,
        "bb_tly": t,
        "bb_brx": r,
        "bb_bry": b,
        "new_encoding": f"{encoding.tolist()}",
        "person": person['id'],
        "Snapshot": snapshot_id
    }
    
    save_detect_person = requests.post("http://127.0.0.1:8000/alertapp/detectedpersons/", json=detected_person)

def take_snapshot(frame, path):
    cv2.imwrite(path, frame)