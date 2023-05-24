import socket
import numpy as np
import cv2
import time

socket_s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)             # 创建socket对象
socket_s.bind(('localhost',4323))                                      # 绑定地址
socket_s.listen(5)                                                     # 建立5个监听

socket_s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024*1024)
bufsize = socket_s.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
print(bufsize)

while True:
    conn,addr= socket_s.accept()                                       # 等待客户端连接
    while True:
        start = time.time()
        data=conn.recv(1024*1024)

        for i in range(47):
            data = data+conn.recv(1024*1024)
            
        image = np.frombuffer(data, np.uint8).reshape((4096,4096,3))
        #cv2.imshow('server', image)
        #cv2.waitKey(1)
        #dt=data.decode('utf-8')                                 #接收一个1024字节的数据 
        #print('收到：',dt)
        #aa=input('服务器发出：') 
        #if aa=='quit':
        #    conn.close()                                        #关闭来自客户端的连接
        #    s.close()                                           #关闭服务器端连接
        #else:
        #    conn.send(aa.encode('utf-8'))
        print((time.time() - start)*1000, 'ms') 