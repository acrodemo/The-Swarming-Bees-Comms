import socket
import os
import threading
import tqdm
import os.path


buffer_size = 1024
HOST = socket.gethostbyname(socket.gethostname())
PORT = 65432      # Port to listen on (non-privileged ports are > 1023) should be an integer from 1-65535 (0 is reserved).
FORM = "utf-8"
SERV_PATH = "RCVD_FILES"
ADDR = (HOST, PORT)
space = "<space>"


def main():
    path_exist()
    print("Server is Opening")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(ADDR) #bind() is used to associate the socket with a specific network interface and port number
    except socket.error as e: #add exception for error
        print(str(e)) #print error message
    s.listen()
    print("Wating for Connection, listening via", (HOST, PORT))
    
    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=work_client, args=(conn,addr))
        thread.start()
        print(f" {threading.activeCount() - 1}")
        
def work_client(conn,addr):
    print("Connected to",(ADDR))
    conn.send("Connected to Base Station Server".encode(FORM))

    recv = conn.recv(buffer_size).decode()
    filename, filesize = recv.split(space)
    filename = os.path.basename(filename)
    filesize = int(filesize)
    save_path = os.path.join(SERV_PATH,filename)

    bar = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=256, colour='#00ff00') # 256 = MB
    with open(save_path, "wb") as f:
        while True: #infinite while loop
            data_read = conn.recv(buffer_size) #reads whatever data the client sends and echoes it back using conn.sendall() (1024 bytes) buffer size
            if not data_read:
                break
            f.write(data_read)
            bar.update(len(data_read))
    check_file_transfer(filename, save_path, conn)
    conn.close()        

def path_exist():
    Exist = os.path.exists(SERV_PATH)
    
    if not Exist:
        os.makedirs(SERV_PATH)
        
def check_file_transfer(filename, save_path, conn):
    file = os.path.exists(save_path)
    if file:
        print(filename)
        conn.send(filename.encode(FORM))
    else:
        conn.send("File not transfered.".encode(FORM))

if __name__ == "__main__":
    main()
