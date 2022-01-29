import socket
import pickle
import sys
import os
import threading

def recvall(s):
    BUFF_SIZE = 4096
    data = b''
    while True:
        part = s.recv(BUFF_SIZE)
        data += part
        if sys.getsizeof(part) < BUFF_SIZE:
            try:
                pickle.loads(data)
                break
            except:
                pass
    return data

arg = str(sys.argv[1])
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
HOST = '3.234.178.220'
#HOST = '127.0.0.1'
PORT = 5000
s.connect((HOST, PORT))
if arg == "list":
    s.sendall(b'list')
    data = recvall(s)
    data = pickle.loads(data)
    for i in data:
        print(i)
elif arg == "put":
    s.sendall(b'put')
    if s.recv(1024) == b'success':
        if len(sys.argv)<3:
            print("No file name specified")
        elif not os.path.exists(str(sys.argv[2])):
            print("Invalid file name")
        else:
            file_name = sys.argv[2]
            file = open(sys.argv[2],'rb').read()
            data = pickle.dumps([file_name,file])
            s.sendall(data)

elif arg == "get":
    s.sendall(b'get')
    if s.recv(1024) == b'success':
        s.sendall(sys.argv[2].encode())
        data = recvall(s)
        data = pickle.loads(data)
        if data[0] == "Invalid":
            print("File not present on server")
        elif data[0] == "Success":
            file = open(data[1],'wb')
            file.write(data[2])
            file.close()

elif arg == "del":
    s.sendall(b'del')
    if s.recv(1024) == b'Success':
        s.sendall(sys.argv[2].encode())
        data = s.recv(1024)
        if data == b'Success':
            print("File deleted")
        elif data == b'Invalid':
            print("File Not Found")

else:
    s.sendall(arg.encode())
    data = s.recv(1024)
    print(repr(data))
