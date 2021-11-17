# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 15:48:09 2021

@author: aos82
"""


import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

#creates socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT)) #Connects to the server
    s.sendall(b'Are the bees swarming?') #send its message
    data = s.recv(1024) # read the server’s reply and then prints it (1024 bytes) buffer size

print('Received', repr(data))