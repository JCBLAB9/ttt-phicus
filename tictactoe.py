class TicTacToe:
    def __init__(self):
        self.board = [['-' for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.status = "in progress"

    def reset(self):
        self.__init__()

    def display_board(self):
        return self.board

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def is_valid_move(self, row, col):
        if 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == '-':
            return True
        return False

    def make_move(self, row, col):
        if self.is_valid_move(row, col):
            self.board[row][col] = self.current_player
            if self.check_winner():
                self.status = f"{self.current_player} wins"
                return self.status
            elif self.is_draw():
                self.status = "draw"
                return self.status
            else:
                self.switch_player()
                return "move accepted"
        return "invalid move"

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != '-':
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != '-':
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '-':
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '-':
            return True
        return False

    def is_draw(self):
        for row in self.board:
            for cell in row:
                if cell == '-':
                    return False
        return True
