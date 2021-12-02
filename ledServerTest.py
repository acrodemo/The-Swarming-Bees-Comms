import sys
import socket
import selectors
import types

from gpiozero import LED

import time



class Server():
    def __init__(self):
        self.sel = selectors.DefaultSelector()
        self.buffer_size = 1 

        self.led = LED(17)

        self.host, self.port = "10.0.0.246",10000
        self.ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #ls = listen socket , AF_INET=(IPv4), SOCK_STREAM= TCP PORT  
        self.ls.bind((self.host, self.port)) #bind because socket.AF_INET requires 2-tuple (host, TCP port)
        self.ls.listen() #listen() enables a server to connect to accept() connection
        print("listening via", (self.host, self.port))
        self.ls.setblocking(False) # False = non-blocking mode, using with sel.select() allowing to wait for an events of a socket >= 1 (mulitple)
        self.sel.register(self.ls, selectors.EVENT_READ, data=None) #selector.register registers the socket being monitored, unregister REQUIRED once socekt is closed, read mode selected


        self.messageList = []

    def manage_conn(self,key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ: #If socket ready for reading thnen both mask and selectors.EVENT_READ are true
            recv_data = sock.recv(self.buffer_size)
            if recv_data:
                data.outb += recv_data
            else: #client has closed socket
                print("closing connection to", data.addr)
                self.led.off()
                self.sel.unregister(sock) #unregister socket selector stops monitoring
                for y in self.messageList:
                    print("Led going: ",y)
                    self.ledHandler(y,2)
                self.messageList = []
                sock.close()
        if mask & selectors.EVENT_WRITE: #If socket ready for writing then both mask and selector.EVENT_WRITE are true
            if data.outb:
                # print(data.outb[0],data.outb[1])
                state = int.from_bytes(data.outb,'big')
                # length = data.outb[1]
                
                self.messageList.append((state))
                # print("echoing", repr(data.outb), "to", data.addr)
                sent = sock.send(data.outb)  # Data stored in data.outb echoed to client
                data.outb = data.outb[sent:] # Sent bytes are removed from the send buffer
        
    def accept_conn(self,sock): # Should be ready to read due to .EVENT_READ
        conn, addr = sock.accept()  
        print("accepted connection from", addr)
        conn.setblocking(False) # False = non-blocking mode, using with sel.select() allowing to wait for an events of another socket >= 1 (mulitple)
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"") #Format Data (Placeholder, will be used to send image / file data)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE #Check if client is ready for read or write
        self.sel.register(conn, events, data=data)  #Event mask, socket, and data are passed to sel.register()

    def ledHandler(self,state,length):
        if(state==1):
            self.led.on()
            time.sleep(length)
        elif(state==0):
            self.led.off()
            time.sleep(length)



def main():
    server = Server()
    try:
        while True:
            events = server.sel.select(timeout=None) #blocks until socket available for I/O (form:ready file object, timeout = specifies max wait time in secs 
            #returns (key,event) tuples one for each socket
            for key, mask in events: # mask = event mask of operation that is ready
                if key.data is None: #If key.data is none means its the listening socket
                    server.accept_conn(key.fileobj) #accept_Conn module is used to accept connection and and fill in key.data, key.fileobj = socket object
                else:
                    messageList = []
                    server.manage_conn(key, mask) #If key.data != none would mean a client socket has been accepted, and we must manage/service connection
    except KeyboardInterrupt:
        print("caught keyboard interrupt, exiting")
    finally:
        server.sel.close()


if __name__ == "__main__":
    main()