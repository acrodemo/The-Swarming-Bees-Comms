import sys
import socket
import selectors
import types
import time

sel = selectors.DefaultSelector()
buffer_size = 1024
messages = [b"\x01", b"\x00"]

"""
Inniatiate Connection
"""
def start_conn(host, port, i):
    server_addr = (host, port)
    connid = i + 1
    print("starting connection", connid, "to", server_addr)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #AF_INET=(IPv4), SOCK_STREAM= TCP PORT
    sock.setblocking(False) # False = non-blocking mode, using with sel.select() allowing to wait for an events of a socket >= 1 (mulitple)
    sock.connect_ex(server_addr) #use connect_ex() instead of connect() to avoid blocking error
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    data = types.SimpleNamespace(
        connid=connid,
        msg_total=sum(len(m) for m in messages),
        recv_total=0,
        messages=list(messages),
        outb=b"",
    )
    sel.register(sock, events, data=data)


def manage_conn(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(buffer_size)  # Ready to read
        if recv_data:
            print("received", repr(recv_data), "from connection", data.connid)
            data.recv_total += len(recv_data)
        if not recv_data or data.recv_total == data.msg_total:
            print("closing connection", data.connid)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
        if data.outb:
            print("sending", repr(data.outb), "to connection", data.connid)
            sent = sock.send(data.outb)  # Ready to write
            data.outb = data.outb[sent:]

"""
Event Loop
"""
# if len(sys.argv) != 4:
#     print("usage:", sys.argv[0], "<host> <port> <num_connections>")
#     sys.exit(1)

host, port, num_conns = "10.0.0.246", 10000, 2
start_conn(host,port,1)


while True:
    events = sel.select(timeout=1)
    if events:
        for key, mask in events:
            manage_conn(key, mask)
    # Check for a socket being monitored to continue.
    if not sel.get_map():
        break
