# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 15:48:09 2021

@author: aos82
"""


import socket
import tqdm
import os
space = "<space>"
buffer_size = 1024

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

filename = "GPS_Data.txt"
filesize = os.path.getsize(filename) 
print(int(filesize))

#creates socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT)) #Connects to the server    
s.send(f"{filename}{space}{filesize}".encode())

bar = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=512)
while True:
    # read the bytes from the file
    f = open(filename,'rb')
    data = f.read(buffer_size)
    while data:
        s.sendall(data)
        data = f.read(buffer_size)
        bar.update(len(data))
    f.close()