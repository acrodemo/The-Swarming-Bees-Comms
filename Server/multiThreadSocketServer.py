"""
Authors:
Ammed Saavedra
Joshua Decker

DeNOVO Team 3, Swarming Bees
Fall 2021 - Spring 2022
CU Denver Senior Capstone Project
"""
import threading
import tqdm
import socket 
import os
import time

class Server():
    def __init__(self,HOST: str, PORT: int, buffSize: int, verbose: bool) -> None:
        self.space = "<space>"
        self.buffSize = buffSize #Bytes to read
        self.HOST = HOST # Standard loopback interface address (localhost); can be a hostname, IP address, or an empty string
        self.PORT = PORT # Port to listen on (non-priveleged ports are > 1023); should be an integer from 1-65535 (0 is reserved)
        self.FORM = "utf-8" # Encoding format
        self.SERV_PATH = "RCVD_FILES" # Folder where received files go
        self.ADDR = (self.HOST,self.PORT)
        self.verbose = verbose
        self.terminateString = "\t\t Terminate".encode(self.FORM)

        #socket.socket creates a socket object that supports the context manager type
        #socket type. AF_INET is the Internet address family for IPv4
        #SOCK_STREAM is the socket type for TCP
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.startServer()

    def startServer(self) -> None: 
        self.pathExist() # Check if received files directory exists, if not, create directory
        if(self.verbose):
            print("Server is Opening")
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # creats socket object of address family .AF_INET and socket type .SOCKET_STREAM
        try:
            self.s.bind(self.ADDR) #bind() is used to associate the socket with a specific network interface and port number
        except socket.error as e: #Add exception for error
            print("Could not open server. Error as follows: ", str(e)) 

        self.s.listen() # Listening for a client requesting connection

        if(self.verbose):
            print("Waiting for connection, listening via: ", self.ADDR)

        while True:
            conn, addr = self.s.accept() #accepts a connection
            thread = threading.Thread(target=self.workClient,args=(conn,addr)) # creates a thread and runs workClient function
            thread.start() # Threading allows multiple clients to connect to server, each client being its own thread
            if(self.verbose):
                print(f"Thread Number: {threading.activeCount() -1}")

    def workClient(self,conn,addr) -> None: #Work client function is used to receive file sent from client
        if (self.verbose):
            print("Connected to: ", (addr))
        recv = conn.recv(self.buffSize).decode() #receives filename and size from file and is decoded
            
        if(self.verbose):
            print(f"Received String: {recv}")

        time.sleep(0.01)
        fileName,fileSize = recv.split(self.space) #splits the filename and filesize info
        fileName = os.path.basename(fileName) # Returns basename of the pathname path

        savePath = os.path.join(self.SERV_PATH,fileName) #Joins the folder name and file name to save file in particular folder
        time.sleep(0.01)
        
        with open(savePath,"wb") as f: #Opens binary file to write to
            while True: #While loop runs until file is completed
                dataRead = conn.recv(self.buffSize)
                if not dataRead or self.terminateString in dataRead: # breaks while loop is data is no longer being sent, or the terminate key has been received
                    alteredData = dataRead[:-len(self.terminateString)] #Remove terminate string from buffer and write data to file
                    f.write(alteredData)
                    break
                f.write(dataRead) #Write data to file
        self.checkFileTransfer(fileName,savePath,conn)
        conn.close() # Close connection


            
    def checkFileTransfer(self,fileName,savePath,conn): # Function to check if file has been transferred
        if(self.verbose):
            print("Checking File Transfer")
        file = os.path.exists(savePath) #Check if file exists in folder
        if file: # If file exists
            if(self.verbose):
                print(f"File transferred successfully: {fileName}")
            time.sleep(0.01)
            conn.send((str(len(fileName))+(16-len(fileName))*' ').encode(self.FORM)) #Begin sending data back to client to confirm transfer - first transfer length of filename for client to listen for
            conn.send(fileName.encode(self.FORM)) # Now send actual filename
        else:
            conn.send(str(21).encode(self.FORM)) 
            conn.send("File not transferred.".encode(self.FORM))
        

    def pathExist(self) -> None: # Check if received files directory exists, if not, create directory
        exist = os.path.exists(self.SERV_PATH)
        if not exist:
            os.makedirs(self.SERV_PATH)

