
from piece import Pawn, Queen



class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        self.board = [[0 for i in range(8)] for j in range(8)]


        self.board[0][1] = Pawn(0, 1, 'b')
        self.board[0][3] = Pawn(0, 3, 'b')
        self.board[0][5] = Pawn(0, 5, 'b')
        self.board[0][7] = Pawn(0, 7, 'b')

        self.board[1][0] = Pawn(1, 0, 'b')
        self.board[1][2] = Pawn(1, 2, 'b')
        self.board[1][4] = Pawn(1, 4, 'b')
        self.board[1][6] = Pawn(1, 6, 'b')

        self.board[2][1] = Pawn(2, 1, 'b')
        self.board[2][3] = Pawn(2, 3, 'b')
        self.board[2][5] = Pawn(2, 5, 'b')
        self.board[2][7] = Pawn(2, 7, 'b')




        self.board[5][0] = Pawn(5, 0, 'w')
        self.board[5][2] = Pawn(5, 2, 'w')
        self.board[5][4] = Pawn(5, 4, 'w')
        self.board[5][6] = Pawn(5, 6, 'w')

        self.board[6][1] = Pawn(6, 1, 'w')
        self.board[6][3] = Pawn(6, 3, 'w')
        self.board[6][5] = Pawn(6, 5, 'w')
        self.board[6][7] = Pawn(6, 7, 'w')

        self.board[7][0] = Pawn(7, 0, 'w')
        self.board[7][2] = Pawn(7, 2, 'w')
        self.board[7][4] = Pawn(7, 4, 'w')
        self.board[7][6] = Pawn(7, 6, 'w')

    def draw(self, win, board):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].draw(win, board)

    def select(self, col, row):
        #prev_selected = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    #if self.board[i][j]:
                        #prev_selected = (j, i)
                    self.board[i][j].selected = False

        if self.board[row][col] != 0:
            self.board[row][col].selected = True
            return True
        return False

    def get_color(self, row, col):
        return self.board[col][row].color

    def check(self, start, end):
        moves = self.board[start[1]][start[0]].valid_moves(self.board)
        if end in moves:
            return True
        else:
            self.board[start[1]][start[0]].selected = False
            return False

    def move(self, start, end):
        #removed = self.board[end[1]][end[0]]
        self.board[end[1]][end[0]] = self.board[start[1]][start[0]]
        try:
            if self.board[start[1]][start[0]].color == 'w':
                c = abs(start[0] - end[0])
                a = abs(start[0] + end[0]) // 2
                b = abs(start[1] + end[1]) // 2
                self.board[end[1]][end[0]] = Pawn(end[1], end[0], 'w')
                if c == 2 and self.board[b][a].color == 'b':
                    self.board[b][a] = 0

            if self.board[start[1]][start[0]].color == 'b' and self.board[start[1]][start[0]].__class__ == Pawn:

                c = abs(start[0] - end[0])
                a = abs(start[0] + end[0])//2
                b = abs(start[1] + end[1])//2

                self.board[end[1]][end[0]] = Pawn(end[1], end[0], 'b')
                if c == 2 and self.board[b][a].color == 'w':
                    self.board[b][a] = 0
                if end[1] == 7:
                    self.board[end[1]][end[0]] = Queen(end[1], end[0], 'b')
            if self.board[start[1]][start[0]].color == 'b' and self.board[start[1]][start[0]].__class__ == Queen:
                self.board[end[1]][end[0]] = Queen(end[1], end[0], 'b')




            self.board[start[1]][start[0]] = 0



        except:
            pass





        #return removed



