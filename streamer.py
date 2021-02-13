import argparse

from flask import Flask, render_template, Response
from inference import VideoCamera
app = Flask(__name__)


@app.route('/')
def index():
    # rendering webpage
    return render_template('./index.html')
def gen(camera):
    while True:
        #get camera frame
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/stream')
def video_feed():
    return Response(gen(VideoCamera(input_url)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def parse_args():
    global input_url
    # defining server ip address and port
    parser = argparse.ArgumentParser()
 
    # Adding optional argument
    parser.add_argument("-i", "--input", required=True, help = "select video to stream")
    
    parser.add_argument("-u", "--url", help = "streaming url")

    parser.add_argument("-p", "--port", help = "streaming port")

    # Read arguments from command line
    args = parser.parse_args()
    input_url = args.input
    url = args.url if args.url != None else '0.0.0.0'
    port = args.port if args.port != None else '5000'
    return url, port


if __name__ == '__main__':
    url, port = parse_args()

    app.run(host=url ,port=port, debug=False)