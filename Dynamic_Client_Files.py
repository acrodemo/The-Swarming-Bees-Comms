import socket #Socket library
import tqdm # status bar
import os #os Library


space = "<space>" # Adds Space
buffer_size = 1024 #number of bytes
HOST = socket.gethostbyname(socket.gethostname())  # The server's hostname or IP address
PORT = 65432        # The port used by the server
CLIENT_PATH = "SEND_FILES" #Folder name

def main(): # main function
    path_exist() #run path exist function
    filename = os.listdir(CLIENT_PATH)[0] #create a list of files in SEND_FILES folder
    print(filename) #prints file name to verify name of file
    run_client(filename) #runs client socket function
    
    
def run_client (filename): #client socket functions 
    filesize = os.path.getsize(filename) #get size of file being transfered
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #creates socket object of address family .AF_INET and socket type .SOCKET_STREAM
    s.connect((HOST, PORT)) #Connects to the server    
    s.send(f"{filename}{space}{filesize}".encode()) #sends file and file size
    bar = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=256, colour ='#00ff00')#establishes download bar
    with open(filename, "rb") as f: # opens a filename in binary format
        while True: #while loop sends file
            data = f.read(buffer_size) #reads file in chunks of bytes
            if not data:# breaks the while loop if nothing is being sent to data variable
                break
        
            s.sendall(data) #sends data to server
            bar.update(len(data)) #updates the download bar as file is sent to server
    s.close() #closes client connection
            
def path_exist(): #function to check if folder structure exists if it does not it creates the folder 
    Exist = os.path.exists(CLIENT_PATH)#uses os librar to verify if a folder exists named SEND_FILES
    
    if not Exist:#if file does not exist, it creates the file using makedirs.
        os.makedirs(CLIENT_PATH)
            

if __name__ == "__main__":#runs main function
    main()

