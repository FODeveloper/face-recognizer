import imagezmq

class VideoReceiver():

    def __init__(self, url="127.0.0.1:8000"):
        self.imageHub = imagezmq.ImageHub(open_port=f"tcp://{url}")

    def get_frame(self):
        (name, frame) = self.imageHub.recv_image()
        self.imageHub.send_reply(b'OK')
        return frame

