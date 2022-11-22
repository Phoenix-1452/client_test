import pygame
import os


b_pawn = pygame.image.load(os.path.join("img", "black_pawn.png"))

w_pawn = pygame.image.load(os.path.join("img", "white_pawn.png"))


b = [b_pawn]
w = [w_pawn]

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



    def isSelected(self):
        return self.selected

    def draw(self, win, board):
        if self.color == 'w':
            drawThis = W[0]
        else:
            drawThis = B[0]


        if self.selected:
            moves = self.valid_moves(board)
            #print(moves)
            for move in moves:
                x = 33 + round(self.startX + (move[0] * self.rect[2] / 8))
                y = 33 + round(self.startY + (move[1] * self.rect[3] / 8))
                pygame.draw.circle(win, (255, 0, 0),(x, y), 10)

        x = 5 + round(self.startX + (self.col * self.rect[2] / 8))
        y = 5 + round(self.startY + (self.row * self.rect[3] / 8))

        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, 55, 55), 2)

        win.blit(drawThis, (x, y))





class Pawn(Piece):

    img = 3
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.first = True
        self.queen = False

    def valid_moves(self, board):
        i = self.row
        j = self.col
        #print(i, j)
        moves = []
        if self.color == 'b':

            if j == 0:
                p = board[i+1][j+1]
                if p == 0:
                    moves.append((j+1, i+1))
            if j == 7:
                p = board[i+1][j-1]
                if p == 0:
                    moves.append((j-1, i+1))

            if j < 7 and j > 0:
                p = board[i+1][j-1]
                if p == 0:
                    moves.append((j-1, i+1))

            if j > 0 and j < 7:
                p = board[i + 1][j + 1]
                if p == 0:
                    moves.append((j + 1, i + 1))

        else:
            if j == 0:
                p = board[i - 1][j + 1]
                if p == 0:
                    moves.append((j + 1, i - 1))
            if j == 7:
                p = board[i - 1][j - 1]
                if p == 0:
                    moves.append((j - 1, i - 1))

            if j < 7 and j > 0:
                p = board[i - 1][j + 1]
                if p == 0:
                    moves.append((j + 1, i - 1))

            if j > 0 and j < 7:
                p = board[i - 1][j - 1]
                if p == 0:
                    moves.append((j - 1, i - 1))



        return moves





