import copy


def isWhite(pawn):
    return pawn < 10 and pawn != 0


def isBlack(pawn):
    return pawn > 10


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
        self.whiteTurn = True
        self._log = []

    def move(self, move):
        self.whiteTurn = not self.whiteTurn
        self._mainBoard[move.startMove[0]][move.startMove[1]] = 0
        self._mainBoard[move.endMove[0]][move.endMove[1]] = move.movingPawn
        self._log.append(move)

    def undo_move(self):
        if len(self._log) == 0:
            return
        self.whiteTurn = not self.whiteTurn
        oldMove = self._log.pop()
        self._mainBoard = oldMove.mainBoard

    def getBoard(self):
        return self._mainBoard

    def getValidMoves(self):
        return self.getPossibleMoves()

    def getPossibleMoves(self):
        possibleMoves = []
        for file in range(8):
            for rank in range(8):
                if (self.whiteTurn and isWhite(self._mainBoard[file][rank])) or (
                        not self.whiteTurn and isBlack(self._mainBoard[file][rank])):
                    allMoves = self.getPossiblePieceMoves([file, rank])
                    for move in allMoves:
                        possibleMoves.append(Move(self._mainBoard, [file, rank], move))

        return possibleMoves

    def getPossiblePieceMoves(self, move):
        possibleMoves = []
        currentPawn = self._mainBoard[move[0]][move[1]]

        if currentPawn == 1:
            if move[1] == 1:
                if move[1] + 1 < 8 and self._mainBoard[move[0]][move[1] + 1] == 0:
                    possibleMoves.append([move[0], move[1] + 1])
                    if move[1] + 2 < 8 and self._mainBoard[move[0]][move[1] + 2] == 0:
                        possibleMoves.append([move[0], move[1] + 2])

            if move[0] + 1 < 8 and move[1] + 1 < 8 and isBlack(self._mainBoard[move[0] + 1][move[1] + 1]):
                possibleMoves.append([move[0] + 1, move[1] + 1])

            if move[0] - 1 > 0 and move[1] + 1 < 8 and isBlack(self._mainBoard[move[0] - 1][move[1] + 1]):
                possibleMoves.append([move[0] - 1, move[1] + 1])

            if move[1] == 4:
                if move[0] + 1 < 8 and isBlack(self._mainBoard[move[0] + 1][move[1]]):
                    possibleMoves.append([move[0] + 1, move[1] + 1])

                if move[0] - 1 > 0 and isBlack(self._mainBoard[move[0] - 1][move[1]]):
                    possibleMoves.append([move[0] - 1, move[1] + 1])

        if currentPawn == 2:
            for i in range(1, 8):
                if (move[0] + i) > 7 or isWhite(self._mainBoard[move[0] + i][move[1]]):
                    break

                if (move[0] + i) > 7 or isBlack(self._mainBoard[move[0] + i][move[1]]):
                    possibleMoves.append([move[0] + i, move[1]])
                    break
                possibleMoves.append([move[0] + i, move[1]])

            for i in range(1, 8):
                if (move[0] - i) < 0 or isWhite(self._mainBoard[move[0] - i][move[1]]):
                    break

                if (move[0] - i) < 0 or isBlack(self._mainBoard[move[0] - i][move[1]]):
                    possibleMoves.append([move[0] - i, move[1]])
                    break
                possibleMoves.append([move[0] - i, move[1]])

            for i in range(1, 8):
                if (move[1] + i) > 7 or isWhite(self._mainBoard[move[0]][move[1] + i]):
                    break

                if (move[1] + i) > 7 or isBlack(self._mainBoard[move[0]][move[1] + i]):
                    possibleMoves.append([move[0], move[1] + i])
                    break
                possibleMoves.append([move[0], move[1] + i])

            for i in range(1, 8):
                if (move[1] - i) < 0 or isWhite(self._mainBoard[move[0]][move[1] - i]):
                    break

                if (move[1] - i) < 0 or isBlack(self._mainBoard[move[0]][move[1] - i]):
                    possibleMoves.append([move[0], move[1] - i])
                    break
                possibleMoves.append([move[0], move[1] - i])

        if currentPawn == 3:
            if move[0] + 2 < 8 and move[1] + 1 < 8:
                if not isWhite(self._mainBoard[move[0] + 2][move[1] + 1]):
                    possibleMoves.append([move[0] + 2, move[1] + 1])

            if move[0] + 1 < 8 and move[1] + 2 < 8:
                if not isWhite(self._mainBoard[move[0] + 1][move[1] + 2]):
                    possibleMoves.append([move[0] + 1, move[1] + 2])

            if move[0] - 2 >= 0 and move[1] - 1 >= 0:
                if not isWhite(self._mainBoard[move[0] - 2][move[1] - 1]):
                    possibleMoves.append([move[0] - 2, move[1] - 1])

            if move[0] - 1 >= 0 and move[1] - 2 >= 0:
                if not isWhite(self._mainBoard[move[0] - 1][move[1] - 2]):
                    possibleMoves.append([move[0] - 1, move[1] - 2])

            if move[0] - 2 >= 0 and move[1] + 1 < 8:
                if not isWhite(self._mainBoard[move[0] - 2][move[1] + 1]):
                    possibleMoves.append([move[0] - 2, move[1] + 1])

            if move[0] - 1 >= 0 and move[1] + 2 < 8:
                if not isWhite(self._mainBoard[move[0] - 1][move[1] + 2]):
                    possibleMoves.append([move[0] - 1, move[1] + 2])

            if move[0] + 2 < 8 and move[1] - 1 >= 0:
                if not isWhite(self._mainBoard[move[0] + 2][move[1] - 1]):
                    possibleMoves.append([move[0] + 2, move[1] - 1])

            if move[0] + 1 < 8 and move[1] - 2 >= 0:
                if not isWhite(self._mainBoard[move[0] + 1][move[1] - 2]):
                    possibleMoves.append([move[0] + 1, move[1] - 2])

        if currentPawn == 4:
            for i in range(1, 8):
                if (move[0] + i) > 7 or (move[1] + i) > 7 or isWhite(self._mainBoard[move[0] + i][move[1] + i]):
                    break

                if (move[0] + i) > 7 or (move[1] + i) > 7 or isBlack(self._mainBoard[move[0] + i][move[1] + i]):
                    possibleMoves.append([move[0] + i, move[1] + i])
                    break
                possibleMoves.append([move[0] + i, move[1] + i])

            for i in range(1, 8):
                if (move[0] - i) < 0 or (move[1] - i) < 0 or isWhite(self._mainBoard[move[0] - i][move[1] - i]):
                    break

                if (move[0] - i) < 0 or (move[1] - i) < 0 or isBlack(self._mainBoard[move[0] - i][move[1] - i]):
                    possibleMoves.append([move[0] - i, move[1] - i])
                    break
                possibleMoves.append([move[0] - i, move[1] - i])

            for i in range(1, 8):
                if (move[0] + i) > 7 or (move[1] - i) < 0 or isWhite(self._mainBoard[move[0] + i][move[1] - i]):
                    break

                if (move[0] + i) > 7 or (move[1] - i) < 0 or isBlack(self._mainBoard[move[0] + i][move[1] - i]):
                    possibleMoves.append([move[0] + i, move[1] - i])
                    break
                possibleMoves.append([move[0] + i, move[1] - i])

            for i in range(1, 8):
                if (move[0] - i) < 0 or (move[1] + i) > 7 or isWhite(self._mainBoard[move[0] - i][move[1] + i]):
                    break

                if (move[0] - i) < 0 or (move[1] + i) > 7 or isBlack(self._mainBoard[move[0] - i][move[1] + i]):
                    possibleMoves.append([move[0] - i, move[1] + i])
                    break
                possibleMoves.append([move[0] - i, move[1] + i])

        if currentPawn == 5:
            for i in range(1, 8):
                if (move[0] + i) > 7 or (move[1] + i) > 7 or isWhite(self._mainBoard[move[0] + i][move[1] + i]):
                    break

                if (move[0] + i) > 7 or (move[1] + i) > 7 or isBlack(self._mainBoard[move[0] + i][move[1] + i]):
                    possibleMoves.append([move[0] + i, move[1] + i])
                    break
                possibleMoves.append([move[0] + i, move[1] + i])

            for i in range(1, 8):
                if (move[0] - i) < 0 or (move[1] - i) < 0 or isWhite(self._mainBoard[move[0] - i][move[1] - i]):
                    break

                if (move[0] - i) < 0 or (move[1] - i) < 0 or isBlack(self._mainBoard[move[0] - i][move[1] - i]):
                    possibleMoves.append([move[0] - i, move[1] - i])
                    break
                possibleMoves.append([move[0] - i, move[1] - i])

            for i in range(1, 8):
                if (move[0] + i) > 7 or (move[1] - i) < 0 or isWhite(self._mainBoard[move[0] + i][move[1] - i]):
                    break

                if (move[0] + i) > 7 or (move[1] - i) < 0 or isBlack(self._mainBoard[move[0] + i][move[1] - i]):
                    possibleMoves.append([move[0] + i, move[1] - i])
                    break
                possibleMoves.append([move[0] + i, move[1] - i])

            for i in range(1, 8):
                if (move[0] - i) < 0 or (move[1] + i) > 7 or isWhite(self._mainBoard[move[0] - i][move[1] + i]):
                    break

                if (move[0] - i) < 0 or (move[1] + i) > 7 or isBlack(self._mainBoard[move[0] - i][move[1] + i]):
                    possibleMoves.append([move[0] - i, move[1] + i])
                    break
                possibleMoves.append([move[0] - i, move[1] + i])

            for i in range(1, 8):
                if (move[0] + i) > 7 or isWhite(self._mainBoard[move[0] + i][move[1]]):
                    break

                if (move[0] + i) > 7 or isBlack(self._mainBoard[move[0] + i][move[1]]):
                    possibleMoves.append([move[0] + i, move[1]])
                    break
                possibleMoves.append([move[0] + i, move[1]])

            for i in range(1, 8):
                if (move[0] - i) < 0 or isWhite(self._mainBoard[move[0] - i][move[1]]):
                    break

                if (move[0] - i) < 0 or isBlack(self._mainBoard[move[0] - i][move[1]]):
                    possibleMoves.append([move[0] - i, move[1]])
                    break
                possibleMoves.append([move[0] - i, move[1]])

            for i in range(1, 8):
                if (move[1] + i) > 7 or isWhite(self._mainBoard[move[0]][move[1] + i]):
                    break

                if (move[1] + i) > 7 or isBlack(self._mainBoard[move[0]][move[1] + i]):
                    possibleMoves.append([move[0], move[1] + i])
                    break
                possibleMoves.append([move[0], move[1] + i])

            for i in range(1, 8):
                if (move[1] - i) < 0 or isWhite(self._mainBoard[move[0]][move[1] - i]):
                    break

                if (move[1] - i) < 0 or isBlack(self._mainBoard[move[0]][move[1] - i]):
                    possibleMoves.append([move[0], move[1] - i])
                    break
                possibleMoves.append([move[0], move[1] - i])

        if currentPawn == 6:
            for i in range(1, 2):
                if (move[0] + i) > 7 or (move[1] + i) > 7 or isWhite(self._mainBoard[move[0] + i][move[1] + i]):
                    break

                if (move[0] + i) > 7 or (move[1] + i) > 7 or isBlack(self._mainBoard[move[0] + i][move[1] + i]):
                    possibleMoves.append([move[0] + i, move[1] + i])
                    break
                possibleMoves.append([move[0] + i, move[1] + i])

            for i in range(1, 2):
                if (move[0] - i) < 0 or (move[1] - i) < 0 or isWhite(self._mainBoard[move[0] - i][move[1] - i]):
                    break

                if (move[0] - i) < 0 or (move[1] - i) < 0 or isBlack(self._mainBoard[move[0] - i][move[1] - i]):
                    possibleMoves.append([move[0] - i, move[1] - i])
                    break
                possibleMoves.append([move[0] - i, move[1] - i])

            for i in range(1, 2):
                if (move[0] + i) > 7 or (move[1] - i) < 0 or isWhite(self._mainBoard[move[0] + i][move[1] - i]):
                    break

                if (move[0] + i) > 7 or (move[1] - i) < 0 or isBlack(self._mainBoard[move[0] + i][move[1] - i]):
                    possibleMoves.append([move[0] + i, move[1] - i])
                    break
                possibleMoves.append([move[0] + i, move[1] - i])

            for i in range(1, 2):
                if (move[0] - i) < 0 or (move[1] + i) > 7 or isWhite(self._mainBoard[move[0] - i][move[1] + i]):
                    break

                if (move[0] - i) < 0 or (move[1] + i) > 7 or isBlack(self._mainBoard[move[0] - i][move[1] + i]):
                    possibleMoves.append([move[0] - i, move[1] + i])
                    break
                possibleMoves.append([move[0] - i, move[1] + i])

            for i in range(1, 2):
                if (move[0] + i) > 7 or isWhite(self._mainBoard[move[0] + i][move[1]]):
                    break

                if (move[0] + i) > 7 or isBlack(self._mainBoard[move[0] + i][move[1]]):
                    possibleMoves.append([move[0] + i, move[1]])
                    break
                possibleMoves.append([move[0] + i, move[1]])

            for i in range(1, 2):
                if (move[0] - i) < 0 or isWhite(self._mainBoard[move[0] - i][move[1]]):
                    break

                if (move[0] - i) < 0 or isBlack(self._mainBoard[move[0] - i][move[1]]):
                    possibleMoves.append([move[0] - i, move[1]])
                    break
                possibleMoves.append([move[0] - i, move[1]])

            for i in range(1, 2):
                if (move[1] + i) > 7 or isWhite(self._mainBoard[move[0]][move[1] + i]):
                    break

                if (move[1] + i) > 7 or isBlack(self._mainBoard[move[0]][move[1] + i]):
                    possibleMoves.append([move[0], move[1] + i])
                    break
                possibleMoves.append([move[0], move[1] + i])

            for i in range(1, 2):
                if (move[1] - i) < 0 or isWhite(self._mainBoard[move[0]][move[1] - i]):
                    break

                if (move[1] - i) < 0 or isBlack(self._mainBoard[move[0]][move[1] - i]):
                    possibleMoves.append([move[0], move[1] - i])
                    break
                possibleMoves.append([move[0], move[1] - i])

        if currentPawn == 11:
            if move[1] - 1 >= 0 and self._mainBoard[move[0]][move[1] - 1] == 0:
                possibleMoves.append([move[0], move[1] - 1])
                if move[1] == 6:
                    if move[1] - 2 >= 0 and self._mainBoard[move[0]][move[1] - 2] == 0:
                        possibleMoves.append([move[0], move[1] - 2])

            if move[0] + 1 < 8 and move[1] - 1 >= 0 and isWhite(self._mainBoard[move[0] + 1][move[1] - 1]):
                possibleMoves.append([move[0] + 1, move[1] - 1])

            if move[0] - 1 > 0 and move[1] - 0 >= 0 and isWhite(self._mainBoard[move[0] - 1][move[1] - 1]):
                possibleMoves.append([move[0] - 1, move[1] - 1])

            if move[1] == 3:
                if move[0] + 1 < 8 and isWhite(self._mainBoard[move[0] + 1][move[1]]):
                    possibleMoves.append([move[0] + 1, move[1] - 1])

                if move[0] - 1 > 0 and isWhite(self._mainBoard[move[0] - 1][move[1]]):
                    possibleMoves.append([move[0] - 1, move[1] - 1])

        if currentPawn == 12:
            for i in range(1, 8):
                if (move[0] + i) > 7 or isBlack(self._mainBoard[move[0] + i][move[1]]):
                    break

                if (move[0] + i) > 7 or isWhite(self._mainBoard[move[0] + i][move[1]]):
                    possibleMoves.append([move[0] + i, move[1]])
                    break
                possibleMoves.append([move[0] + i, move[1]])

            for i in range(1, 8):
                if (move[0] - i) < 0 or isBlack(self._mainBoard[move[0] - i][move[1]]):
                    break

                if (move[0] - i) < 0 or isWhite(self._mainBoard[move[0] - i][move[1]]):
                    possibleMoves.append([move[0] - i, move[1]])
                    break
                possibleMoves.append([move[0] - i, move[1]])

            for i in range(1, 8):
                if (move[1] + i) > 7 or isBlack(self._mainBoard[move[0]][move[1] + i]):
                    break

                if (move[1] + i) > 7 or isWhite(self._mainBoard[move[0]][move[1] + i]):
                    possibleMoves.append([move[0], move[1] + i])
                    break
                possibleMoves.append([move[0], move[1] + i])

            for i in range(1, 8):
                if (move[1] - i) < 0 or isBlack(self._mainBoard[move[0]][move[1] - i]):
                    break

                if (move[1] - i) < 0 or isWhite(self._mainBoard[move[0]][move[1] - i]):
                    possibleMoves.append([move[0], move[1] - i])
                    break
                possibleMoves.append([move[0], move[1] - i])

        if currentPawn == 13:
            if move[0] + 2 < 8 and move[1] + 1 < 8:
                if not isBlack(self._mainBoard[move[0] + 2][move[1] + 1]):
                    possibleMoves.append([move[0] + 2, move[1] + 1])

            if move[0] + 1 < 8 and move[1] + 2 < 8:
                if not isBlack(self._mainBoard[move[0] + 1][move[1] + 2]):
                    possibleMoves.append([move[0] + 1, move[1] + 2])

            if move[0] - 2 >= 0 and move[1] - 1 >= 0:
                if not isBlack(self._mainBoard[move[0] - 2][move[1] - 1]):
                    possibleMoves.append([move[0] - 2, move[1] - 1])

            if move[0] - 1 >= 0 and move[1] - 2 >= 0:
                if not isBlack(self._mainBoard[move[0] - 1][move[1] - 2]):
                    possibleMoves.append([move[0] - 1, move[1] - 2])

            if move[0] - 2 >= 0 and move[1] + 1 < 8:
                if not isBlack(self._mainBoard[move[0] - 2][move[1] + 1]):
                    possibleMoves.append([move[0] - 2, move[1] + 1])

            if move[0] - 1 >= 0 and move[1] + 2 < 8:
                if not isBlack(self._mainBoard[move[0] - 1][move[1] + 2]):
                    possibleMoves.append([move[0] - 1, move[1] + 2])

            if move[0] + 2 < 8 and move[1] - 1 >= 0:
                if not isBlack(self._mainBoard[move[0] + 2][move[1] - 1]):
                    possibleMoves.append([move[0] + 2, move[1] - 1])

            if move[0] + 1 < 8 and move[1] - 2 >= 0:
                if not isBlack(self._mainBoard[move[0] + 1][move[1] - 2]):
                    possibleMoves.append([move[0] + 1, move[1] - 2])

        if currentPawn == 14:
            for i in range(1, 8):
                if (move[0] + i) > 7 or (move[1] + i) > 7 or isBlack(self._mainBoard[move[0] + i][move[1] + i]):
                    break

                if (move[0] + i) > 7 or (move[1] + i) > 7 or isWhite(self._mainBoard[move[0] + i][move[1] + i]):
                    possibleMoves.append([move[0] + i, move[1] + i])
                    break
                possibleMoves.append([move[0] + i, move[1] + i])

            for i in range(1, 8):
                if (move[0] - i) < 0 or (move[1] - i) < 0 or isBlack(self._mainBoard[move[0] - i][move[1] - i]):
                    break

                if (move[0] - i) < 0 or (move[1] - i) < 0 or isWhite(self._mainBoard[move[0] - i][move[1] - i]):
                    possibleMoves.append([move[0] - i, move[1] - i])
                    break
                possibleMoves.append([move[0] - i, move[1] - i])

            for i in range(1, 8):
                if (move[0] + i) > 7 or (move[1] - i) < 0 or isBlack(self._mainBoard[move[0] + i][move[1] - i]):
                    break

                if (move[0] + i) > 7 or (move[1] - i) < 0 or isWhite(self._mainBoard[move[0] + i][move[1] - i]):
                    possibleMoves.append([move[0] + i, move[1] - i])
                    break
                possibleMoves.append([move[0] + i, move[1] - i])

            for i in range(1, 8):
                if (move[0] - i) < 0 or (move[1] + i) > 7 or isBlack(self._mainBoard[move[0] - i][move[1] + i]):
                    break

                if (move[0] - i) < 0 or (move[1] + i) > 7 or isWhite(self._mainBoard[move[0] - i][move[1] + i]):
                    possibleMoves.append([move[0] - i, move[1] + i])
                    break
                possibleMoves.append([move[0] - i, move[1] + i])

        if currentPawn == 15:
            for i in range(1, 8):
                if (move[0] + i) > 7 or (move[1] + i) > 7 or isBlack(self._mainBoard[move[0] + i][move[1] + i]):
                    break

                if (move[0] + i) > 7 or (move[1] + i) > 7 or isWhite(self._mainBoard[move[0] + i][move[1] + i]):
                    possibleMoves.append([move[0] + i, move[1] + i])
                    break
                possibleMoves.append([move[0] + i, move[1] + i])

            for i in range(1, 8):
                if (move[0] - i) < 0 or (move[1] - i) < 0 or isBlack(self._mainBoard[move[0] - i][move[1] - i]):
                    break

                if (move[0] - i) < 0 or (move[1] - i) < 0 or isWhite(self._mainBoard[move[0] - i][move[1] - i]):
                    possibleMoves.append([move[0] - i, move[1] - i])
                    break
                possibleMoves.append([move[0] - i, move[1] - i])

            for i in range(1, 8):
                if (move[0] + i) > 7 or (move[1] - i) < 0 or isBlack(self._mainBoard[move[0] + i][move[1] - i]):
                    break

                if (move[0] + i) > 7 or (move[1] - i) < 0 or isWhite(self._mainBoard[move[0] + i][move[1] - i]):
                    possibleMoves.append([move[0] + i, move[1] - i])
                    break
                possibleMoves.append([move[0] + i, move[1] - i])

            for i in range(1, 8):
                if (move[0] - i) < 0 or (move[1] + i) > 7 or isBlack(self._mainBoard[move[0] - i][move[1] + i]):
                    break

                if (move[0] - i) < 0 or (move[1] + i) > 7 or isWhite(self._mainBoard[move[0] - i][move[1] + i]):
                    possibleMoves.append([move[0] - i, move[1] + i])
                    break
                possibleMoves.append([move[0] - i, move[1] + i])

            for i in range(1, 8):
                if (move[0] + i) > 7 or isBlack(self._mainBoard[move[0] + i][move[1]]):
                    break

                if (move[0] + i) > 7 or isWhite(self._mainBoard[move[0] + i][move[1]]):
                    possibleMoves.append([move[0] + i, move[1]])
                    break
                possibleMoves.append([move[0] + i, move[1]])

            for i in range(1, 8):
                if (move[0] - i) < 0 or isBlack(self._mainBoard[move[0] - i][move[1]]):
                    break

                if (move[0] - i) < 0 or isWhite(self._mainBoard[move[0] - i][move[1]]):
                    possibleMoves.append([move[0] - i, move[1]])
                    break
                possibleMoves.append([move[0] - i, move[1]])

            for i in range(1, 8):
                if (move[1] + i) > 7 or isBlack(self._mainBoard[move[0]][move[1] + i]):
                    break

                if (move[1] + i) > 7 or isWhite(self._mainBoard[move[0]][move[1] + i]):
                    possibleMoves.append([move[0], move[1] + i])
                    break
                possibleMoves.append([move[0], move[1] + i])

            for i in range(1, 8):
                if (move[1] - i) < 0 or isBlack(self._mainBoard[move[0]][move[1] - i]):
                    break

                if (move[1] - i) < 0 or isWhite(self._mainBoard[move[0]][move[1] - i]):
                    possibleMoves.append([move[0], move[1] - i])
                    break
                possibleMoves.append([move[0], move[1] - i])

        if currentPawn == 16:
            for i in range(1, 2):
                if (move[0] + i) > 7 or (move[1] + i) > 7 or isBlack(self._mainBoard[move[0] + i][move[1] + i]):
                    break

                if (move[0] + i) > 7 or (move[1] + i) > 7 or isWhite(self._mainBoard[move[0] + i][move[1] + i]):
                    possibleMoves.append([move[0] + i, move[1] + i])
                    break
                possibleMoves.append([move[0] + i, move[1] + i])

            for i in range(1, 2):
                if (move[0] - i) < 0 or (move[1] - i) < 0 or isBlack(self._mainBoard[move[0] - i][move[1] - i]):
                    break

                if (move[0] - i) < 0 or (move[1] - i) < 0 or isWhite(self._mainBoard[move[0] - i][move[1] - i]):
                    possibleMoves.append([move[0] - i, move[1] - i])
                    break
                possibleMoves.append([move[0] - i, move[1] - i])

            for i in range(1, 2):
                if (move[0] + i) > 7 or (move[1] - i) < 0 or isBlack(self._mainBoard[move[0] + i][move[1] - i]):
                    break

                if (move[0] + i) > 7 or (move[1] - i) < 0 or isWhite(self._mainBoard[move[0] + i][move[1] - i]):
                    possibleMoves.append([move[0] + i, move[1] - i])
                    break
                possibleMoves.append([move[0] + i, move[1] - i])

            for i in range(1, 2):
                if (move[0] - i) < 0 or (move[1] + i) > 7 or isBlack(self._mainBoard[move[0] - i][move[1] + i]):
                    break

                if (move[0] - i) < 0 or (move[1] + i) > 7 or isWhite(self._mainBoard[move[0] - i][move[1] + i]):
                    possibleMoves.append([move[0] - i, move[1] + i])
                    break
                possibleMoves.append([move[0] - i, move[1] + i])

            for i in range(1, 2):
                if (move[0] + i) > 7 or isBlack(self._mainBoard[move[0] + i][move[1]]):
                    break

                if (move[0] + i) > 7 or isWhite(self._mainBoard[move[0] + i][move[1]]):
                    possibleMoves.append([move[0] + i, move[1]])
                    break
                possibleMoves.append([move[0] + i, move[1]])

            for i in range(1, 2):
                if (move[0] - i) < 0 or isBlack(self._mainBoard[move[0] - i][move[1]]):
                    break

                if (move[0] - i) < 0 or isWhite(self._mainBoard[move[0] - i][move[1]]):
                    possibleMoves.append([move[0] - i, move[1]])
                    break
                possibleMoves.append([move[0] - i, move[1]])

            for i in range(1, 2):
                if (move[1] + i) > 7 or isBlack(self._mainBoard[move[0]][move[1] + i]):
                    break

                if (move[1] + i) > 7 or isWhite(self._mainBoard[move[0]][move[1] + i]):
                    possibleMoves.append([move[0], move[1] + i])
                    break
                possibleMoves.append([move[0], move[1] + i])

            for i in range(1, 2):
                if (move[1] - i) < 0 or isBlack(self._mainBoard[move[0]][move[1] - i]):
                    break

                if (move[1] - i) < 0 or isWhite(self._mainBoard[move[0]][move[1] - i]):
                    possibleMoves.append([move[0], move[1] - i])
                    break
                possibleMoves.append([move[0], move[1] - i])

        return possibleMoves


class Move:
    def __init__(self, board, startMove, endMove):
        self.mainBoard = copy.deepcopy(board)
        self.startMove = startMove
        self.endMove = endMove
        self.movingPawn = board[startMove[0]][startMove[1]]
        self.targetPawn = board[endMove[0]][endMove[1]]
        self.movePos = 1000 * startMove[0] + 100 * startMove[1] + 10 * endMove[0] + endMove[1]

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.movePos == other.movePos
