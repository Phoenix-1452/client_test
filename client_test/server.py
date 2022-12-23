import socket
from threading import Thread
from board import Board
import pickle

# server's IP address
SERVER_HOST = "localhost"
SERVER_PORT = 5002 # port we want to use
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
#bo = Board(8, 8)
BUFFER_SIZE = 4096

def listen_for_client(cs):
    """
    This function keep listening for a message from `cs` socket
    Whenever a message is received, broadcast it to all other connected clients
    """
    global msg, id, client_socket

    while True:
        try:

            data = cs.recv(BUFFER_SIZE)
            rec = pickle.loads(data)
            if rec:
                # keep listening for a message from `cs` socket
                bo = rec[1]
                msg = rec[0]
                i1, i2 = msg[0], msg[1]
                start = int(i1), int(i2)
                j1, j2 = msg[2], msg[3]
                end = int(j1), int(j2)
                color = msg[4]
                moveCheck = bo.check(start, end)
                if moveCheck:
                    bo.move(start, end, color)
                    data = (bo.board[end[1]][end[0]], start, end)
                    data = pickle.dumps(data)
                    for client_socket in client_sockets:
                        # and send the message
                        if cs == client_socket:
                            id = client_sockets.index(cs) + 1
                            if id % 2 == 0:
                                client_sockets[id - 2].send(data)
                                client_sockets[id - 1].send(data)
                            else:
                                client_sockets[id - 1].send(data)
                                client_sockets[id].send(data)
                else:
                    msg = pickle.dumps("CANT")
                    cs.send(msg)


        except Exception as e:
            # client no longer connected
            # remove it from the set
            print(f"[!] Error zxc: {e}")

            ind = client_sockets.index(cs) + 1
            print('Вышел: ', ind)
            data = pickle.dumps('quit')

            if ind % 2 == 0:
                client_sockets[ind - 2].send(data)
            else:
                client_sockets[ind].send(data)

            break

            """if ind % 2 == 0:

                client_sockets.pop(ind)
                client_sockets.pop(ind-1)

            else:
                client_sockets.pop(ind)
                client_sockets.pop(ind+1)"""




while True:
    global l_sockets
    # we keep listening for new connections all the time
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")
    # add the new connected client to connected sockets
    client_sockets.append(client_socket)
    print('Осталось ', len(client_sockets))
    #print(*client_sockets, sep='\n')
    try:
        if len(client_sockets) % 2 == 0 and len(client_sockets) > 0:
            l_sockets = len(client_sockets)
            client_sockets[l_sockets-1].send(pickle.dumps('b'))
            client_sockets[l_sockets-2].send(pickle.dumps('w'))
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
