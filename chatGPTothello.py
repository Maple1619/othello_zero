import numpy as np

class Othello:
    def __init__(self):
        self.board = np.zeros((8, 8), dtype=int)
        self.board[3, 3] = self.board[4, 4] = 1
        self.board[3, 4] = self.board[4, 3] = -1
        self.turn = 1

    def get_valid_actions(self, board, turn):
        valid_actions = []
        for i in range(8):
            for j in range(8):
                if self.is_valid_move(board, turn, i, j):
                    valid_actions.append((i, j))
        return valid_actions

    def is_valid_move(self, board, turn, x, y):
        if board[x, y] != 0:
            return False

        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                      (0, 1), (1, -1), (1, 0), (1, 1)]
        for dx, dy in directions:
            if self.check_capture(board, turn, x, y, dx, dy):
                return True
        return False

    def check_capture(self, board, turn, x, y, dx, dy):
        x += dx
        y += dy
        if x < 0 or x >= 8 or y < 0 or y >= 8:
            return False
        if board[x, y] == -turn:
            x += dx
            y += dy
            while x >= 0 and x < 8 and y >= 0 and y < 8:
                if board[x, y] == turn:
                    return True
                if board[x, y] == 0:
                    return False
                x += dx
                y += dy
        return False

    def make_move(self, x, y):
        self.board[x, y] = self.turn
        self.turn = -self.turn

    def get_reward(self, turn):
        black_count = np.count_nonzero(self.board == 1)
        white_count = np.count_nonzero(self.board == -1)
        if turn == 1:
            return black_count - white_count
        else:
            return white_count - black_count

    def is_game_over(self):
        if len(self.get_valid_actions(self.board, self.turn)) == 0:
            if len(self.get_valid_actions(self.board, -self.turn)) == 0:
                return True
            self.turn = -self.turn
        return False

game = Othello()
print(game.get_valid_actions(game.board, game.turn))