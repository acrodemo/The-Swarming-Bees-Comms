import socket
import os
import threading
import tqdm
import os.path
import time

buffer_size = 1024
HOST = "127.0.0.1"#the server's hostname or IP address
PORT = 65432      # Port to listen on (non-privileged ports are > 1023) should be an integer from 1-65535 (0 is reserved).
FORM = "utf-8" #encoding format
SERV_PATH = "RCVD_FILES" #name of folder to put recieved files
ADDR = (HOST, PORT) #combines host name and port
space = "<space>"


def main(): # main function
    path_exist() #runs path exist function
    print("Server is Opening") #message to indicate server is ready to open
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#creates socket object of address family .AF_INET and socket type .SOCKET_STREAM
    try:
        s.bind(ADDR) #bind() is used to associate the socket with a specific network interface and port number
    except socket.error as e: #add exception for error
        print(str(e)) #print error message
    s.listen()#listening for a client requesting connection
    print("Wating for Connection, listening via", (HOST, PORT))
    
    while True:
        conn, addr = s.accept()#accepts a connection
        thread = threading.Thread(target=work_client, args=(conn,addr))#creates a thread and runs workclient functions
        thread.start()#Threading allows multiple clients to connect to server, each client being its own thread.
        print(f"Thread Number: {threading.activeCount() - 1}")
        
def work_client(conn,addr):#work client function is used to recieve file sent from client
    print("Connected to",(ADDR))
    recv = conn.recv(buffer_size).decode() #recieves filename and size from file and is decoded
    print(f"Received String: {recv}")
    time.sleep(0.01)
    filename, filesize = recv.split(space) #splits filename and file size info
    filename = os.path.basename(filename)#returns the basename of the pathname path
    filesize = int(filesize) #changes filezise to an interger
    save_path = os.path.join(SERV_PATH,filename)#joins the folder name and file name to save file in particular folder

    bar = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=256, colour='#00ff00') # 256 = MB, establishes load bar
    with open(save_path, "wb") as f: # opens a filename in binary format
        while True: #infinite while loop
            data_read = conn.recv(buffer_size) #reads whatever data the client sends and echoes it back using conn.sendall() (1024 bytes) buffer size
            time.sleep(0.01)
            if not data_read or "\t\t Terminate" in data_read.decode(): # breaks while loop if data is no longer being sent
                break
            f.write(data_read) #downloads file being sent from client
            bar.update(len(data_read)) #updates bar as data is being sent from client

    check_file_transfer(filename, save_path, conn)#function to check if file has been sent
    conn.close()#closes connection for client        
    

def path_exist():#function to verify if folder exists
    Exist = os.path.exists(SERV_PATH)#uses os librar to verify if a folder exists named SEND_FILES
    
    if not Exist:#if file does not exist, it creates the file using makedirs.
        os.makedirs(SERV_PATH)
        
def check_file_transfer(filename, save_path, conn):#function to check if file has been transfereed
    print("Checking file transfer")
    file = os.path.exists(save_path)#chek if file exists in folder returns true or false
    if file: # if true (file is in folder)
        print(f"{filename}")#prints file name
        conn.send((str(len(filename)) + (16-len(filename))*' ').encode(FORM))
        conn.send(filename.encode(FORM))#sends message back to client with the name of the file
    else:#if false (file not in folder)
        conn.send("File not transfered.".encode(FORM))#sends message back to client that file was not transferred

if __name__ == "__main__":#runs main function
    main()
