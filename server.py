import socket
import os
import pickle
import sys

def recvall(c):
    BUFF_SIZE = 4096
    data = b''
    while True:
        part = c.recv(BUFF_SIZE)
        data += part
        if sys.getsizeof(part) < BUFF_SIZE:
            break
    return data

if not os.path.exists("data"):
	os.mkdir("data")
    
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.settimeout(600)
HOST='127.0.0.1'
PORT = 5000
addr = (HOST,PORT)

try:
    s.bind(addr)
except socket.error as error:
    print(error)

while True:
    s.listen()
    print("Server listning",HOST)
    conn,addr = s.accept()
    print("client "+addr[0]+" connected")
    
    data = conn.recv(1024)

    if data == b'list':
        path="data/"
        dir_list = os.listdir(path)
        dir_list = pickle.dumps(dir_list)
        conn.sendall(dir_list)
    
    elif data == b'put':
        conn.send(b'success')
        data = recvall(conn)
        data = pickle.loads(data)
        file = open("data/"+data[0],'wb')
        file.write(data[1])
        file.close()
    
    elif data == b'get':
        conn.send(b'success')
        file_name = conn.recv(1024).decode('UTF-8')
        
        if not os.path.exists('data/'+str(file_name)):
            data = ["Invalid",'0','0']
        else:
            file = open('data/'+str(file_name),"rb").read()
            data = ["Success",str(file_name),file]
        
        data = pickle.dumps(data)
        conn.sendall(data)
        print("F")

    elif data == b'del':
        conn.sendall(b'Success')
        file_name = conn.recv(1024).decode('UTF-8')

        if not os.path.exists('data/'+str(file_name)):
            conn.sendall(b'Invalid')
        else:
            path = 'data/'+str(file_name)
            os.remove(path)
            conn.sendall(b'Success')
    else:
        print(data)
        conn.sendall(b'Invalid')
