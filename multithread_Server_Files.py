# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 13:03:56 2021

@author: aos82
"""

import socket
import tqdm
import os
import time
from _thread import *

space = "<space>"
buffer_size = 1024
HOST = '0.0.0.0'  # Standard loopback interface address (localhost) can be a hostname, IP address, or empty string
PORT = 65432      # Port to listen on (non-privileged ports are > 1023) should be an integer from 1-65535 (0 is reserved).
Threadnumb = 0

#socket.socket creates a socket object that supports the context manager type
#socket type. AF_INET is the Internet address family for IPv4
#SOCK_STREAM is the socket type for TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((HOST, PORT)) #bind() is used to associate the socket with a specific network interface and port number
except socket.error as e: #add exception for error
    print(str(e)) #print error message
    
print("Wating for Connection, listening via", (HOST, PORT))
s.listen(5) #listen() enables a server to accept() connections
start = time.time()

def client_thread(connection):
    connection.send(str.encode('Base Station Server'))
    bar = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=256, colour='#00ff00') # 256 = MB
    with open(filename, "wb") as f:
        while True:
            data_read = connection.recv(buffer_size) #reads whatever data the client sends and echoes it back using conn.sendall() (1024 bytes) buffer size
            reply = 'Server Speak: ' + data_read.decode('utf-8')
            if not data_read:
                break
            connection.sendall(str.encode(reply))
            f.write(data_read)
            bar.update(len(data_read))
    connection.close()

while True:        
    client, addr = s.accept() #accept() blocks and waits for an incoming connection
    print('Connected to: ', addr[0] + ':' + str(addr[1]))
    start_new_thread(client_thread, (client, ))
    Threadnumb += 1
    print('Thread Number: ' + str(Threadnumb))
    s.close()

end = time.time()
time = end-start
xfr_rate = filesize / time

print('\n\nTime = {:.4}s \nFile size = {:.8} MB \nTransfer rate = {:.4} MB/s\n'.format(time, filesize/(1024*1024), xfr_rate/(1024*1024)))