# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 15:48:09 2021

@author: aos82
"""


import socket
import tqdm
import os
import time

space = "<space>"
buffer_size = 1024

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

filename = "Comics.zip"
filesize = os.path.getsize(filename) 

#creates socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT)) #Connects to the server    
s.send(f"{filename}{space}{filesize}".encode())


bar = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024, colour ='#00ff00')
with open(filename, "rb") as f:

    while True:
        data = f.read(buffer_size)
        if not data:
            break
        
        s.sendall(data)
        bar.update(len(data))
s.close()
