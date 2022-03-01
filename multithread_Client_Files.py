# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 15:48:09 2021

@author: aos82
"""


import socket
import os

space = "<space>"
buffer_size = 1024
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

filename = "Comics.zip"
filesize = os.path.getsize(filename) 

#creates socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((HOST, PORT)) #Connects to the server    
except socket.error as e:
    print(str(e))

rspnd = s.recv(1024)
with open(filename, "rb") as f:
    while True:
        data = f.read(buffer_size)
        if not data:
            break
        rspnd = s.recv(buffer_size)
        print(rspnd.decode('utf-8'))
        s.sendall(data) 
s.close()
