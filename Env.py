"""
An implementation of the game and the game board

@author: Blaise Wang
modified by: Seunghwan Kang
"""
import itertools
import random
import numpy as np

class Board:
    def __init__(self, board_size:int):
        self.n = board_size
        self.gameboard = np.zeros((8, 8), int)
        self.ob_loc_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 29, 30, 31, 32, 33, 34, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63]
        self.initialize()
    
    def initialize(self):
        self.round=1
        self.winner = -1
        self.move_list=[]
        self.gameboard[0:self.n, 0:self.n] = 0
        self.gameboard[3, 4] = self.gameboard[4, 3] = 1
        self.gameboard[3, 3] = self.gameboard[4, 4] = 2
        self.add_random_obstarcle(5)

    def add_move(self, loc:tuple):
        
        self.move_list.append(loc)
        x,y = loc

        # 먼저 돌을 두고
        self.gameboard[x, y] = 2 if self.round % 2 == 0 else 1

        # 뒤집을 돌이 있는지 찾는다
        directions = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
        # 돌을 둔 위치에서 8방향을 모두 탐색
        for dx, dy in directions:
            tx, ty = x, y
            while self.in_board(tx + dx, ty + dy):
                tx += dx
                ty += dy
                
                # 0을 만났다면-해당 방향으로 존재하는 돌이 없음 -> 방향 탐색 취소
                if self.gameboard[tx,ty] == 0 or self.gameboard[tx, ty] == -1:
                    break
                
                # 돌을 만났고, current_player가 둔 돌과 동일하면
                if self.gameboard[tx, ty] == self.get_current_player():
                    # 돌을 둔 위치까지 반대 방향으로 되돌아가며 돌 뒤집기
                    while tx - dx != x or ty - dy != y:
                        tx -= dx
                        ty -= dy
                        self.gameboard[tx, ty] = self.get_current_player()
                    # 다 뒤집었다면 break으로 더이상 해당 방향을 탐색 할 필요 없기에 break
                    break
        self.round+=1

    def get_available_moves(self, player):

        potential_move_list=[]
        directions = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
        for x, y in list(itertools.product(range(self.n), range(self.n))):
            if self.gameboard[x, y] != 0:
                continue
            for dx, dy in directions:
                flag = False
                tx, ty = x, y
                while self.in_board(tx + dx, ty + dy):
                    tx += dx
                    ty += dy
                    if self.gameboard[tx, ty] == 0 or self.gameboard[tx, ty] == -1:
                        break
                    if player != self.gameboard[tx, ty]:
                        flag = True
                    else:
                        if flag:
                            potential_move_list.append(self.location_to_move((x,y)))
                        break
        return list(set(potential_move_list))

    def in_board(self, x:int, y:int):
        return 0 <= x < self.n and 0 <= y < self.n

    def get_current_player(self):
        return 2 if self.round % 2 == 0 else 1

    def get_opponent_player(self):
        return 2 if self.round % 2 != 0 else 1
    
    def move_to_location(self, move: int):
        x = move // self.n
        y = move % self.n
        return (x, y)
    
    def location_to_move(self, loc:tuple):
        x, y = loc
        return self.n*x + y

    def add_random_obstarcle(self, ob_n):
        self.random_obstarcle = random.sample(self.ob_loc_list, ob_n)
        
        for move in self.random_obstarcle:
            x, y = self.move_to_location(move)
            self.gameboard[x,y] = -1

    def get_current_state(self):
        player = self.get_current_player()
        opponent = self.get_opponent_player()
        # 5 layer로 이루어진 state.
        # 0 layer --> obstarcle
        # 1 layer --> current_player의 돌 위치
        # 2 layer --> opponent_player의 돌 위치
        # 3 layer --> previous move
        # 4 layer --> 1이면 흑, 0이면 백
        square_state = np.zeros((5,self.n,self.n))
        for ob in self.random_obstarcle:
            x, y = self.move_to_location(ob)
            square_state[0,x,y]=1.0
        for (x,y), value in np.ndenumerate(self.gameboard):
            if value == player:
                square_state[1,x,y] = 1.0
            elif value == opponent:
                square_state[2,x,y] = 1.0
        if self.get_move_number() > 0:
            x, y = self.move_liset[self.get_move_number() -1]
            square_state[3,x,y] = 1.0
        if player == 1:
            square_state[4,:,:] = 1.0
        return square_state
 
    def get_move_number(self):
        return len(self.move_list)

    def get_cell_count(self):
        white = 0
        black = 0
        for (x, y), value in np.ndenumerate(self.gameboard):
            black += 1 if value == 1 else 0
            white += 1 if value == 2 else 0
        return black, white

    def has_winner(self):
        if len(self.get_available_moves(self.get_current_player())):
            return -1
        else:
            if len(self.get_available_moves(self.get_opponent_player())):
                self.round+=1
                return -1
            else:
                black, white = self.get_cell_count()
                self.winner = 1 if black > white else 2 if black < white else 0
                return self.winner

    def print_board(self):
        print(self.gameboard)

class Game:
    def __init__(self, board: 'Board'):
        self.board = board

    def start_play(self, args):
        player1, player2, index = args
        if index % 2:
            player1, player2 = player2, player1
        self.board.initialize()
        while self.board.winner == -1:
            player_in_turn = player1 if self.board.get_current_player() == 1 else player2
            # move, _ = player_in_turn.get_action(self.board)

            # to play my self
            av_move = self.board.get_available_moves(self.board.get_current_player())
            print(self.board.gameboard)
            print(av_move, end='\t[')
            for m  in av_move:
                m_tp = self.board.move_to_location(m)
                print(m_tp, end=', ')        
            print(']')
            move = int(input())
            # end of to play my self
            
            loc = self.board.move_to_location(move)
            self.board.add_move(loc)
            winner = self.board.has_winner()
            if winner != -1:
                if not winner:
                    return winner
                if index % 2:
                    return 1 if winner == 2 else 2

    def self_play(self):
        pass
    
if __name__ == '__main__':
    game = Game(Board(8))
    game.start_play([1,2,0])
