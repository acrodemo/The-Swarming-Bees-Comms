# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 16:20:07 2021

@author: aos82
"""

#command line arguments needed include: <host> <port> i.e 127.0.0.1 65432

import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()
buffer_size = 1024

"""
Accept the connection
"""
def accept_conn(sock): # Should be ready to read due to .EVENT_READ
    conn, addr = sock.accept()  
    print("accepted connection from", addr)
    conn.setblocking(False) # False = non-blocking mode, using with sel.select() allowing to wait for an events of another socket >= 1 (mulitple)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"") #Format Data (Placeholder, will be used to send image / file data)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE #Check if client is ready for read or write
    sel.register(conn, events, data=data)  #Event mask, socket, and data are passed to sel.register()


def manage_conn(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ: #If socket ready for reading thnen both mask and selectors.EVENT_READ are true
        recv_data = sock.recv(buffer_size)
        if recv_data:
            data.outb += recv_data
        else: #client has closed socket
            print("closing connection to", data.addr)
            sel.unregister(sock) #unregister socket selector stops monitoring
            sock.close()
    if mask & selectors.EVENT_WRITE: #If socket ready for writing then both mask and selector.EVENT_WRITE are true
        if data.outb:
            print("echoing", repr(data.outb), "to", data.addr)
            sent = sock.send(data.outb)  # Data stored in data.outb echoed to client
            data.outb = data.outb[sent:] # Sent bytes are removed from the send buffer


if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

"""
Listen Socket
"""
host, port = sys.argv[1], int(sys.argv[2]) #command line arguments
ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #ls = listen socket , AF_INET=(IPv4), SOCK_STREAM= TCP PORT  
ls.bind((host, port)) #bind because socket.AF_INET requires 2-tuple (host, TCP port)
ls.listen() #listen() enables a server to connect to accept() connection
print("listening via", (host, port))
ls.setblocking(False) # False = non-blocking mode, using with sel.select() allowing to wait for an events of a socket >= 1 (mulitple)
sel.register(ls, selectors.EVENT_READ, data=None) #selector.register registers the socket being monitored, unregister REQUIRED once socekt is closed, read mode selected


"""
Event Loop
"""
try:
    while True:
        events = sel.select(timeout=None) #blocks until socket available for I/O (form:ready file object, timeout = specifies max wait time in secs 
        #returns (key,event) tuples one for each socket
        for key, mask in events: # mask = event mask of operation that is ready
            if key.data is None: #If key.data is none means its the listening socket
                accept_conn(key.fileobj) #accept_Conn module is used to accept connection and and fill in key.data, key.fileobj = socket object
            else:
                manage_conn(key, mask) #If key.data != none would mean a client socket has been accepted, and we must manage/service connection
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()