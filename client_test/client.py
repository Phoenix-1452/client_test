import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back
import pygame
import os
import socket
from board import Board
from time import sleep

board = pygame.transform.scale(pygame.image.load(os.path.join("img", "board_alt.png")), (750, 750))
rect = (113, 113, 525, 525)



start = 0
end = 0



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
SERVER_PORT = 5002 # server's port
separator_token = "<SEP>" # we will use this to separate the client name & message

# initialize TCP socket
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")
width = 750
height = 750

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Shashki")

def listen_for_messages():
    while True:
        msg = s.recv(1024).decode()
        i1, i2 = msg[0], msg[1]
        start1 = int(i1), int(i2)
        j1, j2 = msg[2], msg[3]
        end1 = int(j1), int(j2)
        color = bo.get_color(int(i1), int(i2))
        bo.move(start1, end1)



# make a thread that listens for messages to this client & print them
t = Thread(target=listen_for_messages)
# make the thread daemon so it ends whenever the main thread ends
t.daemon = True
# start the thread
t.start()
data = ' '
bo = Board(8, 8)
clock = pygame.time.Clock()
run = True
flag = False
turn = True

dig = 0
start1, end1 = 0, 0
while True:
    # input message we want to send to the server
    clock.tick(60)
    redraw_win()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            quit()
            pygame.quit()

        elif event.type == pygame.MOUSEBUTTONDOWN and not flag:
            pos = pygame.mouse.get_pos()
            try:
                i, j = click(pos)
                start = i, j
                flag = bo.select(i, j)

            except:
                pass
        elif event.type == pygame.MOUSEBUTTONDOWN and flag:
            pos = pygame.mouse.get_pos()
            try:
                i, j = click(pos)
                end = i, j
                moveCheck = bo.check(start, end)
                if moveCheck:
                    bo.move(start, end)
                    data = str(start[0]) + str(start[1]) + str(end[0]) + str(end[1])
                    flag = False

                    turn = True
                    dig += 1
                    if data != ' ':
                        s.send(data.encode())
                else:
                    flag = False

            except:
                pass


# close the socket
s.close()