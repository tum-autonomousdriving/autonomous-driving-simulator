# This server used to receive images and current vehicle data from the client, passes the images to a trained classifier to predict new vehicle commands, 
# and then sends these commands back to Unity to control the car for autonomous driving.

# now we only test the communication between the client and server at first, 
# so we just give the fixed command to see wether the car will be controlled and wether the images succesffly recieved
# lately we can also add code to realize autonomous driving

import socketio
# concurrent networking
import eventlet
# web server gateway interface
import eventlet.wsgi
from flask import Flask
import base64
import cv2
import numpy as np
# from io import BytesIO
import time
import os

# Initialize Socket.IO server
sio = socketio.Server()
app = Flask(__name__)

frame_count = 0
frame_count_save = 0
prev_time = 0
fps = 0


@sio.on("send_image")
def on_image(sid, data):
    #make the variables global to calculate the fps 
    global frame_count, frame_count_save, prev_time, fps
    #print("image recieved!")
    img_data = data["image"]
    img_bytes = base64.b64decode(img_data)
    # Decode image from base64 format，将字典里抽取出来的字符串转换为字节串类型
    img = cv2.imdecode(np.frombuffer(img_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)

    # # create a variable to identify every frame of image for the lately image-save
    # frame_count_save += 1

    # Calculate and print fps
    frame_count += 1
    elapsed_time = time.time() - prev_time
    if elapsed_time > 1:
        fps = frame_count / elapsed_time
        print(f"FPS: {fps:.2f}")
        prev_time = time.time()
        frame_count = 0

    # # split the merged image
    # _, width, _ = img.shape
    # single_width = width // 3

    # img1 = img[:, :single_width, :]
    # img2 = img[:, single_width : 2 * single_width, :]
    # img3 = img[:, 2 * single_width :, :]

    # # save the images
    # save_folder = os.path.expanduser("~/Desktop/receivedImage")
    # os.makedirs(save_folder, exist_ok=True)
    # filename = os.path.join(save_folder, f"image{frame_count_save:02d}.jpg")
    # cv2.imwrite(filename, img)

    # show the recieved images on the screen
    if img is not None and img.shape[0] > 0 and img.shape[1] > 0:
        cv2.namedWindow("image from unity", cv2.WINDOW_NORMAL)
        cv2.imshow("image from unity", img)
        key = cv2.waitKey(1)
        if key == 27:
            cv2.destroyAllWindows()
            return
    else:
        print("Invalid image data")

# listen for the event "vehicle_data"
@sio.on("vehicle_data")
def vehicle_command(sid, data):
    # print("data recieved!")
    steering_angle = float(data["steering_angle"])
    throttle = float(data["throttle"])

    if data:
        steering_angle = 0
        throttle = 0.3

        send_control(steering_angle, throttle)
    else:
        # send the data to unityClient
        # sio.emit("manual", data={})
        print("data is empty")


@sio.event
def connect(sid, environ):
    # sid for identifying the client connected表示客户端唯一标识符，environ表示其连接的相关环境信息
    print("Client connected")
    send_control(0, 0)

# Define a data sending function to send processed data back to unity client
def send_control(steering_angle, throttle):
    sio.emit(
        "control_command",
        data={
            "steering_angle": steering_angle.__str__(),
            "throttle": throttle.__str__(),
        },
        skip_sid=True,
    )

@sio.event
def disconnect(sid):
    # implement this function, if disconnected
    print("Client disconnected")


app = socketio.Middleware(sio, app)
# Connect to Socket.IO client
if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(("", 4567)), app)