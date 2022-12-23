from threading import Thread
import pygame
import os
import socket
from board import Board
import sys
from time import sleep
import pickle
from main import main_menu
pygame.init()
boardd = pygame.transform.scale(pygame.image.load(os.path.join("img", "board_alt.png")), (750, 750))
rect = (113, 113, 525, 525)
global color, turn, d, run, msg, flag
color = ''
start = 0
end = 0
startX = rect[0]
startY = rect[1]


def redraw_win():
    global bo, msg, st, en
    win.blit(boardd, (0, 0))
    bo.draw(win, bo.board)
    if turn and color:
        f1 = pygame.font.Font(None, 36)
        text1 = f1.render(f"Your turn, {colorr}", True,
                          (180, 0, 0))
        win.blit(text1, (10, 10))
    if msg == 'quit':
        f1 = pygame.font.Font(None, 36)
        text2 = f1.render('THE OPPONENT HAS LEFT THE GAME', True,
                          (180, 0, 0))
        win.blit(text2, (10, 30))
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


msg = ' '
data = ''
bo = Board(8, 8)
clock = pygame.time.Clock()
flag = False
run = True
turn = False
d = False
dig = 0
start1, end1 = 0, 0
width = 750
height = 750
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess Online")
BUFFER_SIZE = 8192


def listen_for_messages():
    global color, turn, d, bo, run, msg, flag, st, en, colorr
    d = False
    #game = True
    while True:
        game = bo.check_king()
        try:
            data = s.recv(BUFFER_SIZE)
            msg = pickle.loads(data)
            if msg:
                if msg == "b":
                    colorr = 'Black'
                    color = "b"
                    turn = False
                    print(color)
                elif msg == "w":
                    colorr = 'White'
                    color = "w"
                    turn = True
                    print(color)


                elif msg == 'quit':
                    sleep(3)
                    d = False
                    run = False
                    quit()
                    pygame.quit()
                    s.close()
                elif msg == 'CANT':
                    bo.zxc(int(start[1]), int(start[0]))
                    flag = False
                else:
                    st = msg[1]
                    en = msg[2]
                    bo.board[en[1]][en[0]] = msg[0]
                    bo.board[st[1]][st[0]] = 0
                    if start == st:
                        turn = False
                        flag = False
                    else:
                        d = True
                        turn = True
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



# make a thread that listens for messages to this client & print them
t = Thread(target=listen_for_messages)
# make the thread daemon, so it ends whenever the main thread ends
t.daemon = True
# start the thread
t.start()


while run:
    redraw_win()
    clock.tick(15)

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
                print(click(pos))
                data = str(start[0]) + str(start[1]) + str(end[0]) + str(end[1]) + str(color)

                if data != ' ':
                    print('Send', data)
                    data = data, bo
                    data = pickle.dumps(data)
                    s.send(data)
                    d = False
            except Exception as e:
                print(f"{e}")

# close the socket
s.close()
