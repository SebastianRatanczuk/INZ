import copy


class GameEngine:
    def __init__(self):
        self._mainBoard = [
            #    1  2  3  4  5  6  7   8
            [2, 1, 0, 0, 0, 0, 11, 12],  # A   # x1 = pionek
            [3, 1, 0, 0, 0, 0, 11, 13],  # B   # x2 = wieża
            [4, 1, 0, 0, 0, 0, 11, 14],  # C   # x3 = skoczek
            [5, 1, 0, 0, 0, 0, 11, 15],  # D   # x4 = goniec
            [6, 1, 0, 0, 0, 0, 11, 16],  # E   # x5 = dama
            [4, 1, 0, 0, 0, 0, 11, 14],  # F   # x6 = krol
            [3, 1, 0, 0, 0, 0, 11, 13],  # G
            [2, 1, 0, 0, 0, 0, 11, 12],  # H
        ]
        self._whiteTurn = True
        self._log = []

    def move(self, move):
        self._whiteTurn = not self._whiteTurn
        self._mainBoard[move.startMove[0]][move.startMove[1]] = 0
        self._mainBoard[move.endMove[0]][move.endMove[1]] = move.movingPawn
        self._log.append(move)

    def undo_move(self):
        if len(self._log) == 0:
            return
        self._whiteTurn = not self._whiteTurn
        oldMove = self._log.pop()
        self._mainBoard = oldMove.mainBoard

    def getBoard(self):
        return self._mainBoard


class Move:
    def __init__(self, board, startMove, endMove):
        self.mainBoard = copy.deepcopy(board)
        self.startMove = startMove
        self.endMove = endMove
        self.movingPawn = board[startMove[0]][startMove[1]]
        self.targetPawn = board[endMove[0]][endMove[1]]
