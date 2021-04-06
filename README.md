# Install the server
```
pip3 install -r requirements.txt
```

# Install face recognition library with necessary models
```
pip3 install git+https://github.com/ageitgey/face_recognition_models
```

# Run the streamer app
```
python3 streamer.py -u <running-IP> -p <running-port> -i <camera-api-IP:port> -k <camera-id> -n <camera-name> -l <camera-location>
```
* running-IP: which adress you want to run your server, for example 127.0.0.1
* running-port: which port, for example 8080
* camera-api-IP:port : which adress the camera is streaming on(check camera-api repo).
* camera-id: the camera id in the database(in miniface app), to be able to send the notifications for a specific camera(must exist in the database).
* camera-name: it's obvious! (string)
* camera-location: position of the camera(string).

# Before running the server

Ensure you run the database service first. Check the repository of miniface.

## What is Miniface?

Miniface is a simple django REST app that have a database of registered persons.

## How the system works?
1.  it fetch all the persons from the miniface app, using a get request.
2.  Receive a video stream from a camera streamer(for more details check camera-api in my camera-api repository), using imagezmq library.
3.  Detect persons, check if they are in the database. 
4.  Save snapshots if there are persons in the analyzed frame, and send the detected person details to miniface app.