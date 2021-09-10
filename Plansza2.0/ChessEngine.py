import copy


class GameEngine:
    def __init__(self):
        self.main_board = [
            [12, 11, 0, 0, 0, 0, 1, 2],
            [13, 11, 0, 0, 0, 0, 1, 3],
            [14, 11, 0, 0, 0, 0, 1, 4],
            [15, 11, 0, 0, 0, 0, 1, 5],
            [16, 11, 0, 0, 0, 0, 1, 6],
            [14, 11, 0, 0, 0, 0, 1, 4],
            [13, 11, 0, 0, 0, 0, 1, 3],
            [12, 11, 0, 0, 0, 0, 1, 2],
        ]
        self.whiteTurn = True
        self.log = []

    def move(self, move):
        self.whiteTurn = not self.whiteTurn
        self.main_board[move.start_move[0]][move.start_move[1]] = 0
        self.main_board[move.end_move[0]][move.end_move[1]] = move.moving_pawn
        self.log.append(move)

    def undo_move(self):
        if len(self.log) == 0:
            return
        self.whiteTurn = not self.whiteTurn
        oldMove = self.log.pop()
        self.main_board = oldMove.main_board


class Move:
    def __init__(self, board, start_move, end_move):
        self.main_board = copy.deepcopy(board)
        self.start_move = start_move
        self.end_move = end_move
        self.moving_pawn = board[start_move[0]][start_move[1]]
        self.target_pawn = board[end_move[0]][end_move[1]]
