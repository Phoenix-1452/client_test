from threading import Thread
import pygame
import os
import socket
from board import Board

board = pygame.transform.scale(pygame.image.load(os.path.join("img", "board_alt.png")), (750, 750))
rect = (113, 113, 525, 525)

start = 0
end = 0
startX = rect[0]
startY = rect[1]

def redraw_win():
    global win, bo
    win.blit(board, (0, 0))

    bo.draw(win, bo.board)

    pygame.display.update()


def click(pos):
    x = pos[0]
    y = pos[1]
    if rect[0] < x < rect[0] + rect[2]:
        if rect[1] < y < rect[1] + rect[3]:
            dx = x - rect[0]
            dy = y - rect[0]
            i = int(dx / (rect[2] / 8))
            j = int(dy / (rect[3] / 8))
            return i, j


# server's IP address
# if the server is not on this machine,
# put the private (network) IP address (e.g 192.168.1.2)
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002  # server's port
# initialize TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")


def listen_for_messages():
    global color, turn, d
    while True:
        try:
            msg = s.recv(1024).decode()
            print(msg)
            if msg == "B":
                color = 'b'
                turn = False

            elif msg == "W":
                color = 'w'
                turn = True
            else:
                if len(msg) == 5:
                    d = True
                    i1, i2 = msg[0], msg[1]
                    st = int(i1), int(i2)
                    j1, j2 = msg[2], msg[3]
                    en = int(j1), int(j2)
                    if msg[4] != color:
                        turn = True
                    bo.move(st, en, color)

                    x = 33 + round(startX + (st[0] * rect[2] / 8))
                    y = 33 + round(startY + (st[1] * rect[3] / 8))
                    dx = 33 + round(startX + (en[0] * rect[2] / 8))
                    dy = 33 + round(startY + (en[1] * rect[3] / 8))
                    while d:
                        pygame.draw.circle(win, (0, 0, 255), (x, y), 40, 5)
                        pygame.draw.circle(win, (0, 0, 255), (dx, dy), 40, 5)


        except Exception as e:
            print(f"[!] Error: {e}")
            d = False
            break


width = 750
height = 750
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess Online")
# make a thread that listens for messages to this client & print them
t = Thread(target=listen_for_messages)
# make the thread daemon, so it ends whenever the main thread ends
t.daemon = True
# start the thread
t.start()
data = ' '
bo = Board(8, 8)
clock = pygame.time.Clock()
run = True
flag = False
global color, turn, d
turn = False
dig = 0
start1, end1 = 0, 0

while run:
    clock.tick(60)
    redraw_win()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            d = False
            run = False
            quit()
            pygame.quit()

        elif event.type == pygame.MOUSEBUTTONDOWN and not flag and turn:
            pos = pygame.mouse.get_pos()
            try:
                i, j = click(pos)
                start = i, j
                flag = bo.select(i, j, color)
                print(click(pos))
            except:
                pass
        elif event.type == pygame.MOUSEBUTTONDOWN and flag:
            pos = pygame.mouse.get_pos()
            try:
                i, j = click(pos)
                end = i, j
                moveCheck = bo.check(start, end)
                print(click(pos))
                if moveCheck:
                    bo.move(start, end, color)
                    data = str(start[0]) + str(start[1]) + str(end[0]) + str(end[1]) + str(color)
                    flag = False
                    turn = False
                    d = False
                    if data != ' ':
                        s.send(data.encode())
                else:
                    flag = False
            except:
                pass

# close the socket
s.close()
