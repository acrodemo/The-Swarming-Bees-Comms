# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 13:03:56 2021

@author: aos82
"""

import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost) can be a hostname, IP address, or empty string
PORT = 65432        # Port to listen on (non-privileged ports are > 1023) should be an integer from 1-65535 (0 is reserved).

#socket.socket creates a socket object that supports the context manager type
#socket type. AF_INET is the Internet address family for IPv4
#SOCK_STREAM is the socket type for TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
    s.bind((HOST, PORT)) #bind() is used to associate the socket with a specific network interface and port number
    s.listen() #listen() enables a server to accept() connections
    conn, addr = s.accept() #accept() blocks and waits for an incoming connection
    with conn:
        print('Connected by', addr)
        while True: #infinite while loop
            data = conn.recv(1024) #reads whatever data the client sends and echoes it back using conn.sendall()
            if not data:
                break
            conn.sendall(data)