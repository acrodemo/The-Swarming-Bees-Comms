"""
Authors:
Ammed Saavedra
Joshua Decker

DeNOVO Team 3, Swarming Bees
Fall 2021 - Spring 2022
CU Denver Senior Capstone Project
"""
#Argument parsing for verbosity
import tqdm
import socket
import os
import time


class Client():
    def __init__(self,HOST: str, PORT: int, buffSize: int, verbose: bool) -> None:
        self.verbose = verbose
        self.HOST = HOST #The server's hostname or IP address
        self.PORT = PORT #The port used by the server
        self.buffSize = buffSize #Number of bytes being read
        self.CLIENT_PATH = "SEND_FILES" #Folder name
        self.space = "<space>" #Encodes spaces
        self.pathExist()
        self.fileName = os.listdir(self.CLIENT_PATH)[0] #Grabs a single file from folder
        self.filePath = self.CLIENT_PATH + "/" + self.fileName #Marks path of file
        self.terminateString = "\t\t Terminate"
        if(self.verbose):
            print(f"File Name: {self.fileName}")
        self.runClient() #Runs client socket function

    def pathExist(self) -> None: #Function to check if folder structure exists. If it does not, create folder
        exist = os.path.exists(self.CLIENT_PATH)
        if not exist:
            os.makedirs(self.CLIENT_PATH)

    def runClient(self) -> None: #Client socket function
        fileSize = os.path.getsize(self.filePath) #Get size of file
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creates socket object of address family .AF_INET and socket type .SOCKET_STREAM

        self.s.connect((self.HOST,self.PORT)) #Connect to server
        self.s.send(f"{self.filePath}{self.space}{fileSize}".encode()) #send file name and file size
        time.sleep(.01)
        if(self.verbose):
            bar = tqdm.tqdm(range(fileSize), f"Sending {self.filePath}", unit="B", unit_scale=True,unit_divisor=256, colour="#00ff00") #Establishes download bar
        with open(self.filePath,"rb") as f: #Open file to send
            while True: #Loop to send file
                data = f.read(self.buffSize) #Reads file in chunks of bytes
                if not data:
                    break
                self.s.sendall(data) #Sends data to server
                if(self.verbose):
                    bar.update(len(data))


        self.s.send(self.terminateString.encode()) #Signal to server transfer is over
        # We begin to read the name of the file the server sends back to check if file was transferred successfully
        length = int(self.s.recv(16).decode()) #Length of filename to read
        data = self.s.recv(length).decode() # Receive file name
        if(self.verbose):
            print("File Sent: ",data)
        self.s.close() #Closing out connection 
        os.remove(self.CLIENT_PATH+"/"+data)


