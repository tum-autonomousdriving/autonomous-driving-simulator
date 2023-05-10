import time
import socketio
import cv2
import numpy as np
#from torchvision import models
#from torchvision import transforms

#transf = transforms.ToTensor()

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

    if sioc.connected:
        end = time.time()
        sioc.emit('send_frame')
        

@sioc.event
def disconnect():
    quit()

if __name__ == '__main__':
    sioc.connect('http://localhost:5000')
    sioc.wait()