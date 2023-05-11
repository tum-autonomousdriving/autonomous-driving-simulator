import socket   
import sys
import cv2

c=socket.socket()                                           # 创建socket对象
c.connect(('localhost',4323))                                #建立连接

vid = cv2.VideoCapture(0)

while True:
    ret, image = vid.read()

    #ab=input('客户端发出：')
    #if ab=='quit':
    #    c.close()                                               #关闭客户端连接
    #    sys.exit(0)
    #else:
        #c.send(ab.encode('utf-8'))                               #发送数据
        #data=c.recv(1024)                                       #接收一个1024字节的数据
        #print('收到：',data.decode('utf-8'))
    image = cv2.resize(image, (640*4, 480*4))
    print(len(image.tobytes()))
    c.send(image.tobytes())