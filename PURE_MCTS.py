"""
An implementation of the Monte Carlo tree node
A pure implementation of the Monte Carlo Tree Search

@author: Junxiao Song
modified by: Blaise Wang
modified by: Seunghwan Kang
"""

import copy
import numpy as np
from operator import itemgetter

from Env import Board

class Node():
    def __init__(self, parent, prior_p):
        self._parent = parent
        self.children = {}  # a map from action to TreeNode
        self._N = 0
        self._Q = 0
        self._u = 0
        self._W = 0
        self._P = prior_p

    def select(self, c_puct):
        # TEST
        for tmp in self.children.items():
            # print('printtest',tmp[1].get_value(c_puct))
            break
        # TEST END
        return max(self.children.items(), key=lambda act_node: act_node[1].get_value(c_puct))
    
    def expand(self, action_priors):
        """ 자식 노드 생성하며 Tree 확장
        action_priors : policy function에서 나온 output (a list of tuples of actions / prior probability)
        """
        for action, prob in action_priors:
            if action not in self.children:
                self.children[action] = Node(self, prob)
             
    def update(self, leaf_value):
        self._N += 1
        self._W += leaf_value
        self._Q = self._W / self._N
    
    def update_recursive(self, leaf_value):
        if self._parent:
            self._parent.update_recursive(-leaf_value)
        self.update(leaf_value)

    def get_value(self, c_puct):
        # TEST
        # print('self.u',self._u)
        # print('c_puct', c_puct)
        # print('self._P', self._P)
        # print('self._parent._N',self._parent._N)
        # print('self._N', self._N)

        # TEST END
        self._u = c_puct * self._P * np.sqrt(self._parent._N / (1+self._N))
        return self._Q + self._u
    
    def is_leaf(self):
        return self.children=={}
    
    def is_root(self):
        return self._parent is None


def roll_out_policy_func(board: 'Board'):
    # 현재 board에서 둘 수 있는 경우를 random하게 수행
    # roll out randomly
    return zip(board.get_available_moves(board.get_current_player()),
               np.random.rand(len(board.get_available_moves(board.get_current_player()))))


def policy_value_func(board: 'Board'):
    """state (Board)를 입력으로 하고 (action, probabilities)를 output으로 하는 함수.
    추후에는 Model이 policy_value_func을 대체한다."""
    # 정규분포된 확률 반환, pure MCTS에는 0점 부여
    # return uniform probabilities and 0 score for pure MCTS
    return zip(board.get_available_moves(board.get_current_player()), np.ones(len(board.get_available_moves(board.get_current_player()))) / len(
        board.get_available_moves(board.get_current_player()))), 0


class MCTS():
    # def __init__(self, policy_value_function, c_puct = 5, n_play_out = 10000):
    def __init__(self, policy_value_function, c_puct = 5, n_play_out = 1000):
        """Arguments:
        policy_value_func -- a function that takes in a board state and outputs a list of (action, probabilities)
            tuples and also a score in [-1, 1] (i.e. the expected value of the end game score from 
            the current player's perspective) for the current player. --> 결국엔 model임.
        c_puct -- a number in (0, inf) that controls how quickly exploration converges to the
            maximum-value policy, where a higher value means relying on the prior more
        """
        self._root = Node(None, 1.0)
        self._policy = policy_value_function
        self._c_puct = c_puct
        self._n_play_out = n_play_out

    def _play_out(self, state: 'Board'):
        """Run a single play out from the root to the leaf, getting a value at the leaf and
        propagating it back through its parents. State is modified in-place, so a copy must be
        provided.
        Arguments:
        state -- a copy of the state.
        """
        node = self._root
        # print(node)
        while True:
            if node.is_leaf():
                # leaf 노드라면
                break
            action, node = node.select(self._c_puct)
            x, y = state.move_to_location(action)
            state.add_move((x, y))
    
        action_probabilities, _ = self._policy(state)


        if state.has_winner() == -1:
            # 게임이 안끝났으면 expand
            node.expand(action_probabilities)

        # Evaluate the leaf node by random roll out
        # 게임이 끝나지 않았다면 무작위로 게임이 끝날때 까지 진행하여 leaf노드를 선택
        leaf_value = self._evaluate_roll_out(state)
        # print('leaf_value : ', leaf_value)
        # Update value and visit count of nodes in this traversal.
        node.update_recursive(-leaf_value)
        # print('update recursive fin')
        # print(node)


    @staticmethod
    def _evaluate_roll_out(state: 'Board', limit=1000):
        """
        roll out policy (추후에는 Model이 대체)를 사용해서 게임이 끝날때 까지 진행한다.
        현재 플레이어가 이긴다면 +1, 진다면 -1, 비긴다면 0을 반환한다.
        """
        winner = -1
        player = state.get_current_player()
        for i in range(limit):
            winner = state.has_winner()
            if winner != -1:
                # 게임이 끝났다면
                break
            max_action = max(roll_out_policy_func(state), key=itemgetter(1))[0]
            x, y = state.move_to_location(max_action)
            state.add_move((x, y))

        if winner == 0:  # tie
            return 0
        else:
            return 1 if winner == player else -1

    def get_move(self, state:'Board'):
        """
        가능한 모든 경우의 수를 가지뻗어나가고, 가장 많이 방문한 action을 반환한다.
        state: game Board의 정보를 가지고 있다. 현재 돌의 상태, 플레이하는 사람 등 게임의 상태를 가지고 있음
        return: 가장 많이 방문한 action
        """
        # [self._play_out(copy.deepcopy(state)) for _ in range(self._n_play_out)]
        # TEST
        [self._play_out(copy.deepcopy(state)) for _ in range(self._n_play_out)]
        # TEST END
        # print('Root',self._root)
        return max(self._root.children.items(), key=lambda act_node: act_node[1]._N)[0]
    
    def update_with_move(self, last_move: int):
        """Step forward in the tree, keeping everything we already know about the subtree.
        """
        if last_move in self._root.children:
            self._root = self._root.children[last_move]
            self._root._parent = None
        else:
            self._root = Node(None, 1.0)

class MCTSPlayer:
    def __init__(self, c_puct=5, n_play_out=2000):
        self.mcts = MCTS(policy_value_func, c_puct, n_play_out)

    def get_action(self, board: 'Board'):
        if board.winner == -1:
            self.move = self.mcts.get_move(board)
            self.mcts.update_with_move(-1)
            return self.move
        
if __name__=='__main__':
    gboard = Board(8)
    mcts_player = MCTSPlayer()
    print(gboard.has_winner())
    while gboard.has_winner() == -1:
        gboard.print_board()
        print('current player: ', gboard.get_current_player())
        next_move = mcts_player.get_action(gboard)
        gboard.add_move(gboard.move_to_location(next_move))
    print(f"The Winner is player no.{gboard.has_winner()}")

    