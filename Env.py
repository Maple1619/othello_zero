import itertools
import numpy as np

class Board:
    def __init__(self, board_size:int):
        self.n = board_size
        self.gameboard = np.zeros((8, 8), int)
        self.initialize()

    def initialize(self):
        self.round=1
        self.winner = -1
        self.move_list=[]
        self.gameboard[0:self.n, 0:self.n] = 0
        self.gameboard[3, 4] = self.gameboard[4, 3] = 1
        self.gameboard[3, 3] = self.gameboard[4, 4] = 2
    
    def add_move(self, loc:tuple):
        
        self.move_list.append(loc)
        x,y = loc

        # 먼저 돌을 두고
        print(self.gameboard)
        print(x, y)
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
                if self.gameboard[tx,ty] == 0:
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
                    if self.gameboard[tx, ty] == 0:
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
        x = self.n - move // self.n -1
        y = move % self.n
        return (x, y)
    
    def location_to_move(self, loc:tuple):
        x, y = loc
        return (self.n-x-1)*self.n+y

board = Board(8)
while True:
    print('Current player: ', board.get_current_player())
    av_move = board.get_available_moves(board.get_current_player())
    print(board.gameboard)
    showboard=board.gameboard.copy()
    print(av_move, end='\t[')
    for m  in av_move:
        m_tp = board.move_to_location(m)
        print(m_tp, end=', ')
        showboard[m_tp]=-1
        
    print(']')
    print(showboard)
    loc = tuple(map(int,input().split()))
    print(loc)
    board.add_move(loc)