import time
import socketio
import cv2
import numpy as np
from torchvision import models
from torchvision import transforms

transf = transforms.ToTensor()

sioc = socketio.Client()

@sioc.event
def connect():
    print('connected to server')
    sioc.emit(event = 'send_frame')

end = 0
@sioc.event
def receive_frame(data):
    global end
    start = time.time()
    if end != 0:
        print((start-end)*1000,'ms')
    
    image = np.frombuffer(data, np.uint8)
    #image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED).reshape((4096,4096,3))
    #image = transf(image).unsqueeze(0)
    #model = models.resnet50(pretrained=True)
    #output = model(image)

    #sioc.sleep(1)
    if sioc.connected:
        #cv2.imshow('client', image)
        #cv2.waitKey(30)
        #cv2.imwrite(str(time.time())+'.png', image)
        end = time.time()
        sioc.emit('send_frame')
        


#vid = cv2.VideoCapture(0)

'''
@sioc.event
def receive_frame():
    print(222222222222)
    ret, image = vid.read()
    #success, encoded_image = cv2.imencode('.png', image)
    cv2.imshow('client',image)
    cv2.waitKey(1)
    sioc.emit(event = 'send_frame', data = image.tobytes())
    print('已发送')
'''

@sioc.event
def disconnect():
    quit()

if __name__ == '__main__':
    sioc.connect('http://localhost:5000')
    sioc.wait()