import socket
import tqdm
import os
import time
space = "<space>"
buffer_size = 1024
HOST = socket.gethostbyname(socket.gethostname())  # The server's hostname or IP address
PORT = 65432        # The port used by the server
CLIENT_PATH = "SEND_FILES" 
filename = "Comics.zip"

def main():
    path_exist()
    file = os.listdir(CLIENT_PATH)
    run_client()
    
    
def run_client ():
    filesize = os.path.getsize(filename) 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT)) #Connects to the server    
    s.send(f"{filename}{space}{filesize}".encode())
    bar = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=256, colour ='#00ff00')
    with open(filename, "rb") as f:
        while True:
            data = f.read(buffer_size)
            if not data:
                break
        
            s.sendall(data)
            bar.update(len(data))
    s.close()
            
def path_exist():
    Exist = os.path.exists(CLIENT_PATH)
    
    if not Exist:
        os.makedirs(CLIENT_PATH)
            

if __name__ == "__main__":
    main()

