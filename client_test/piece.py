import pygame
import os

b_pawn = pygame.image.load(os.path.join("img", "black_pawn.png"))
b_queen = pygame.image.load(os.path.join("img", "black_queen.png"))
w_pawn = pygame.image.load(os.path.join("img", "white_pawn.png"))
w_queen = pygame.image.load(os.path.join("img", "white_queen.png"))

b = [b_pawn, b_queen]
w = [w_pawn, w_queen]

B = []
W = []

for img in b:
    B.append(pygame.transform.scale(img, (55, 55)))

for img in w:
    W.append(pygame.transform.scale(img, (55, 55)))


class Piece:
    img = -1
    rect = (113, 113, 525, 525)
    startX = rect[0]
    startY = rect[1]

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.selected = False
        self.queen = False

    def isSelected(self):
        return self.selected

    def draw(self, win, board):
        if self.color == 'w':
            drawThis = W[self.img]
        else:
            drawThis = B[self.img]

        if self.selected:
            moves = self.valid_moves(board)
            # print(moves)
            for move in moves:
                x = 33 + round(self.startX + (move[0] * self.rect[2] / 8))
                y = 33 + round(self.startY + (move[1] * self.rect[3] / 8))
                pygame.draw.circle(win, (255, 0, 0), (x, y), 10)

        x = 5 + round(self.startX + (self.col * self.rect[2] / 8))
        y = 5 + round(self.startY + (self.row * self.rect[3] / 8))

        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, 55, 55), 2)

        win.blit(drawThis, (x, y))

class Queen(Piece):
    img = 1

    def __init__(self, row, col, color):
        super().__init__(row, col, color)

    def valid_moves(self, board):
        i = self.row
        j = self.col
        dig = 8
        # print(j, i)
        moves = []
        if self.color == 'b':

            try:
                for x in range(8):
                    for y in range(8):
                        moves.append((x, y))
            except:
                pass

        return moves


class Pawn(Piece):
    img = 0

    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.queen = False




    def watch(self, pos, board):
        rd = pos[0]+1, pos[1]+1
        lu = pos[0]-1, pos[1]-1
        ru = pos[0]-1, pos[1]+1
        ld = pos[0]+1, pos[1]-1



    def valid_moves(self, board):
        i = self.row
        j = self.col
        dig = 8
        # print(j, i)
        moves = []
        if self.color == 'b':

            try:
                if not board[i + 1][j - 1] and (j - 1 > -1) and (i + 1 < 8):
                    moves.append((j - 1, i + 1))
                else:
                    if board[i + 1][j - 1].color == 'w' and (board[i + 2][j - 2] == 0) and (j - 2 > -1) and (i + 2 < 8):
                        moves.append((j - 2, i + 2))
                        pos = (i+2, j-2)
                        self.watch(pos, board)
                        #print("zxc", pos)

            except:
                pass
            try:
                if not board[i + 1][j + 1] and (i + 1 < 8 > j + 1):
                    moves.append((j + 1, i + 1))
                else:
                    if board[i + 1][j + 1].color == 'w' and (board[i + 2][j + 2] == 0):
                        moves.append((j + 2, i + 2))

            except:
                pass

        if self.color == 'w':
            try:
                if not board[i - 1][j + 1] and (j + 1 < 8) and (i - 1 > -1):
                    moves.append((j + 1, i - 1))
                else:
                    if board[i - 1][j + 1].color == 'b' and (board[i - 2][j + 2] == 0) and (i-2>-1) and(j+2<8):
                        moves.append((j + 2, i - 2))
            except:
                pass

            try:
                if not board[i - 1][j - 1] and (j - 1 > -1 < i - 1):
                    moves.append((j - 1, i - 1))
                else:
                    if board[i - 1][j - 1].color == 'b' and (board[i - 2][j - 2] == 0):
                        moves.append((j - 2, i - 2))
            except:
                pass



        return moves
