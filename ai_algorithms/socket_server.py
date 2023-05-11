import socket
import numpy as np
import cv2

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)             # 创建socket对象
s.bind(('localhost',4323))                                      # 绑定地址
s.listen(5)                                                     # 建立5个监听

while True:
    conn,addr= s.accept()                                       # 等待客户端连接

    bufsize = conn.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)

    while True:
        cv2.waitKey(100)
        data=conn.recv(640*4*480*4*3)
            
        image = np.frombuffer(data, np.uint8).reshape((480*4,640*4,3))
        cv2.imshow('server', image)
        cv2.waitKey(1)
        #dt=data.decode('utf-8')                                 #接收一个1024字节的数据 
        #print('收到：',dt)
        #aa=input('服务器发出：') 
        #if aa=='quit':
        #    conn.close()                                        #关闭来自客户端的连接
        #    s.close()                                           #关闭服务器端连接
        #else:
        #    conn.send(aa.encode('utf-8'))