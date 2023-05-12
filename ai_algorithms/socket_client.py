import socket   
import sys
import cv2

                          
socket_c=socket.socket()                                           # 创建socket对象
socket_c.connect(('localhost',4323))                               #建立连接

socket_c.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024*1024)
bufsize = socket_c.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
print(bufsize)

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
    image = cv2.resize(image, (4096, 4096))
    print(len(image.tobytes()))
    socket_c.send(image.tobytes())