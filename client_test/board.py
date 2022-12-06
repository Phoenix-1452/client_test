from piece import Bishop
from piece import King
from piece import Rook
from piece import Pawn
from piece import Queen
from piece import Knight


class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.king = True
        self.board = [[0 for i in range(8)] for j in range(8)]

        self.board[0][0] = Rook(0, 0, "b")
        self.board[0][1] = Knight(0, 1, "b")
        self.board[0][2] = Bishop(0, 2, "b")
        self.board[0][3] = Queen(0, 3, "b")
        self.board[0][4] = King(0, 4, "b")
        self.board[0][5] = Bishop(0, 5, "b")
        self.board[0][6] = Knight(0, 6, "b")
        self.board[0][7] = Rook(0, 7, "b")

        self.board[1][0] = Pawn(1, 0, "b")
        self.board[1][1] = Pawn(1, 1, "b")
        self.board[1][2] = Pawn(1, 2, "b")
        self.board[1][3] = Pawn(1, 3, "b")
        self.board[1][4] = Pawn(1, 4, "b")
        self.board[1][5] = Pawn(1, 5, "b")
        self.board[1][6] = Pawn(1, 6, "b")
        self.board[1][7] = Pawn(1, 7, "b")

        self.board[7][0] = Rook(7, 0, "w")
        self.board[7][1] = Knight(7, 1, "w")
        self.board[7][2] = Bishop(7, 2, "w")
        self.board[7][3] = Queen(7, 3, "w")
        self.board[7][4] = King(7, 4, "w")
        self.board[7][5] = Bishop(7, 5, "w")
        self.board[7][6] = Knight(7, 6, "w")
        self.board[7][7] = Rook(7, 7, "w")

        self.board[6][0] = Pawn(6, 0, "w")
        self.board[6][1] = Pawn(6, 1, "w")
        self.board[6][2] = Pawn(6, 2, "w")
        self.board[6][3] = Pawn(6, 3, "w")
        self.board[6][4] = Pawn(6, 4, "w")
        self.board[6][5] = Pawn(6, 5, "w")
        self.board[6][6] = Pawn(6, 6, "w")
        self.board[6][7] = Pawn(6, 7, "w")

    def draw(self, win, board):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].draw(win, board)

    def select(self, col, row, colorr):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].selected = False

        if self.board[row][col] != 0 and self.board[row][col].color == colorr:
            self.board[row][col].selected = True
            return True
        return False

    def get_color(self, row, col):
        return self.board[col][row].color

    def check_king(self):
        if self.king:
            return True
        else:
            return False

    def check(self, start, end):
        moves = self.board[start[1]][start[0]].valid_moves(self.board)
        if end in moves:
            return True
        else:
            self.board[start[1]][start[0]].selected = False
            return False

    def move(self, start, end, colorr):
        try:

            if self.board[end[1]][end[0]].__class__ == King:
                self.king = False
            self.board[start[1]][start[0]].change_pos((end[1], end[0]))
            self.board[end[1]][end[0]] = self.board[start[1]][start[0]]
            self.board[end[1]][end[0]].selected = False
            if self.board[start[1]][start[0]].__class__ == Pawn:
                self.board[start[1]][start[0]].first = False
                if end[1] == 7 or end[1] == 0:
                    self.board[end[1]][end[0]] = Queen(end[1], end[0], self.board[end[1]][end[0]].color)

            self.board[start[1]][start[0]] = 0
        except:
            pass
