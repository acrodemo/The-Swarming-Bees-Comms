# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 13:03:56 2021

@author: aos82
"""

import socket
import tqdm
import os

space = "<space>"
buffer_size = 1024
HOST = '0.0.0.0'  # Standard loopback interface address (localhost) can be a hostname, IP address, or empty string
PORT = 65432        # Port to listen on (non-privileged ports are > 1023) should be an integer from 1-65535 (0 is reserved).

#socket.socket creates a socket object that supports the context manager type
#socket type. AF_INET is the Internet address family for IPv4
#SOCK_STREAM is the socket type for TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT)) #bind() is used to associate the socket with a specific network interface and port number
s.listen(4) #listen() enables a server to accept() connections
print("listening via", (HOST, PORT))

conn, addr = s.accept() #accept() blocks and waits for an incoming connection
print('Connected by', addr)

recv = conn.recv(buffer_size).decode()
filename, filesize = recv.split(space)
filename = os.path.basename(filename)
filesize = int(filesize)

bar = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=512)
with open(filename, "wb") as f:
    while True: #infinite while loop
        data = s.recv(buffer_size) #reads whatever data the client sends and echoes it back using conn.sendall() (1024 bytes) buffer size
        if not data:
            break
        f.write(data)
        bar.update(len(data))

        f.close()        
        conn.close()
        s.close()