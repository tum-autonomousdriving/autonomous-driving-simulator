import time
import socketio
import cv2
import numpy as np
#from torchvision import models
#from torchvision import transforms

#transf = transforms.ToTensor()

from turbojpeg import TurboJPEG, TJPF_BGR 

sioc = socketio.Client()

@sioc.event
def connect():
    print('connected to server')
    sioc.emit(event = 'send_frame', data='connect')

vid = cv2.VideoCapture(0)

end = 0
@sioc.event
def receive_frame_1(data):
    global end
    start = time.time()
    if end != 0:
        print((start-end)*1000,'ms')
    
    #image = np.frombuffer(data, np.uint8)
    #image = TurboJPEG.decode(image)
    #image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED).reshape((4096,4096,3))
    #image = transf(image).unsqueeze(0)
    #model = models.resnet50(pretrained=True)
    #output = model(image)

    if sioc.connected:
        end = time.time()
        ret, image = vid.read()
        image = cv2.resize(image, (2048, 1024))
        sioc.emit('send_frame', data=image.tobytes())
        

@sioc.event
def disconnect():
    quit()

if __name__ == '__main__':
    sioc.connect('http://localhost:5000')
    sioc.wait()