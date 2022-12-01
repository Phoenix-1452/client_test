import socket
from threading import Thread
from board import Board

# server's IP address
SERVER_HOST = "localhost"
SERVER_PORT = 5002 # port we want to use
separator_token = "<SEP>" # we will use this to separate the client name & message
# initialize list/set of all connected client's sockets
client_sockets = []
# create a TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# make the port as reusable port
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the socket to the address we specified
s.bind((SERVER_HOST, SERVER_PORT))
# listen for upcoming connections
s.listen()
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
bo = Board(8, 8)


def listen_for_client(cs):
    """
    This function keep listening for a message from `cs` socket
    Whenever a message is received, broadcast it to all other connected clients
    """
    global msg
    while True:
        try:

            # keep listening for a message from `cs` socket
            msg = cs.recv(1024).decode()

            for client_socket in client_sockets:
                # and send the message
                if cs == client_socket:
                    id = client_sockets.index(cs) + 1
                    if id % 2 == 0:
                        client_sockets[id-2].send(msg.encode())
                    else:
                        client_sockets[id].send(msg.encode())

        except Exception as e:
            # client no longer connected
            # remove it from the set
            print(f"[!] Error: {e}")
            for client_socket in client_sockets:
                client_sockets.remove(client_socket)
            break


while True:
    # we keep listening for new connections all the time
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")
    # add the new connected client to connected sockets
    client_sockets.append(client_socket)
    try:
        if len(client_sockets) % 2 == 0 and len(client_sockets) > 0:
            l = len(client_sockets)
            client_sockets[l-1].send('B'.encode())
            client_sockets[l-2].send('W'.encode())
    except Exception as e:
        print(f"[!] Error: {e}")

    # start a new thread that listens for each client's messages
    t = Thread(target=listen_for_client, args=(client_socket,))
    # make the thread daemon, so it ends whenever the main thread ends
    t.daemon = True
    # start the thread
    t.start()


# close client sockets
for cs in client_sockets:
    cs.close()
# close server socket
s.close()