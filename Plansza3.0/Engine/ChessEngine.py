import copy


def is_white(pawn):
    return pawn < 10 and pawn != 0


def is_black(pawn):
    return pawn > 10


def is_the_same_color(pawn, pawn1):
    if pawn == 0 or pawn1 == 0:
        return False

    if pawn > 10 and pawn1 > 10:
        return True

    if pawn < 10 and pawn1 < 10:
        return True
    return False


class GameEngine:
    def __init__(self):
        self._main_board = [
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
        self.white_turn = True
        self._log = []

    def move(self, move):
        self.white_turn = not self.white_turn
        self._main_board[move.start_move[0]][move.start_move[1]] = 0
        self._main_board[move.end_move[0]][move.end_move[1]] = move.moving_pawn
        self._log.append(move)

    def undo_move(self):
        if len(self._log) == 0:
            return
        self.white_turn = not self.white_turn
        old_move = self._log.pop()
        self._main_board = old_move.main_board

    def get_board(self):
        return self._main_board

    def get_valid_moves(self):
        return self.get_possible_moves()

    def get_possible_moves(self):
        possible_moves = []
        for file in range(8):
            for rank in range(8):
                if (self.white_turn and is_white(self._main_board[file][rank])) or (
                        not self.white_turn and is_black(self._main_board[file][rank])):
                    allMoves = self.get_possible_piece_moves([file, rank])
                    for move in allMoves:
                        possible_moves.append(Move(self._main_board, [file, rank], move))

        return possible_moves

    def get_possible_piece_moves(self, move):
        possible_moves = []
        current_pawn = self._main_board[move[0]][move[1]]

        if current_pawn == 1:
            if move[1] == 1:
                if move[1] + 1 < 8 and self._main_board[move[0]][move[1] + 1] == 0:
                    possible_moves.append([move[0], move[1] + 1])
                    if move[1] + 2 < 8 and self._main_board[move[0]][move[1] + 2] == 0:
                        possible_moves.append([move[0], move[1] + 2])

            if move[0] + 1 < 8 and move[1] + 1 < 8 and is_black(self._main_board[move[0] + 1][move[1] + 1]):
                possible_moves.append([move[0] + 1, move[1] + 1])

            if move[0] - 1 > 0 and move[1] + 1 < 8 and is_black(self._main_board[move[0] - 1][move[1] + 1]):
                possible_moves.append([move[0] - 1, move[1] + 1])

            if move[1] == 4:
                if move[0] + 1 < 8 and is_black(self._main_board[move[0] + 1][move[1]]):
                    possible_moves.append([move[0] + 1, move[1] + 1])

                if move[0] - 1 > 0 and is_black(self._main_board[move[0] - 1][move[1]]):
                    possible_moves.append([move[0] - 1, move[1] + 1])

        if current_pawn == 2:
            for i in range(1, 8):
                if (move[0] + i) > 7 or is_white(self._main_board[move[0] + i][move[1]]):
                    break

                if (move[0] + i) > 7 or is_black(self._main_board[move[0] + i][move[1]]):
                    possible_moves.append([move[0] + i, move[1]])
                    break
                possible_moves.append([move[0] + i, move[1]])

            for i in range(1, 8):
                if (move[0] - i) < 0 or is_white(self._main_board[move[0] - i][move[1]]):
                    break

                if (move[0] - i) < 0 or is_black(self._main_board[move[0] - i][move[1]]):
                    possible_moves.append([move[0] - i, move[1]])
                    break
                possible_moves.append([move[0] - i, move[1]])

            for i in range(1, 8):
                if (move[1] + i) > 7 or is_white(self._main_board[move[0]][move[1] + i]):
                    break

                if (move[1] + i) > 7 or is_black(self._main_board[move[0]][move[1] + i]):
                    possible_moves.append([move[0], move[1] + i])
                    break
                possible_moves.append([move[0], move[1] + i])

            for i in range(1, 8):
                if (move[1] - i) < 0 or is_white(self._main_board[move[0]][move[1] - i]):
                    break

                if (move[1] - i) < 0 or is_black(self._main_board[move[0]][move[1] - i]):
                    possible_moves.append([move[0], move[1] - i])
                    break
                possible_moves.append([move[0], move[1] - i])

        if current_pawn == 3:
            if move[0] + 2 < 8 and move[1] + 1 < 8:
                if not is_white(self._main_board[move[0] + 2][move[1] + 1]):
                    possible_moves.append([move[0] + 2, move[1] + 1])

            if move[0] + 1 < 8 and move[1] + 2 < 8:
                if not is_white(self._main_board[move[0] + 1][move[1] + 2]):
                    possible_moves.append([move[0] + 1, move[1] + 2])

            if move[0] - 2 >= 0 and move[1] - 1 >= 0:
                if not is_white(self._main_board[move[0] - 2][move[1] - 1]):
                    possible_moves.append([move[0] - 2, move[1] - 1])

            if move[0] - 1 >= 0 and move[1] - 2 >= 0:
                if not is_white(self._main_board[move[0] - 1][move[1] - 2]):
                    possible_moves.append([move[0] - 1, move[1] - 2])

            if move[0] - 2 >= 0 and move[1] + 1 < 8:
                if not is_white(self._main_board[move[0] - 2][move[1] + 1]):
                    possible_moves.append([move[0] - 2, move[1] + 1])

            if move[0] - 1 >= 0 and move[1] + 2 < 8:
                if not is_white(self._main_board[move[0] - 1][move[1] + 2]):
                    possible_moves.append([move[0] - 1, move[1] + 2])

            if move[0] + 2 < 8 and move[1] - 1 >= 0:
                if not is_white(self._main_board[move[0] + 2][move[1] - 1]):
                    possible_moves.append([move[0] + 2, move[1] - 1])

            if move[0] + 1 < 8 and move[1] - 2 >= 0:
                if not is_white(self._main_board[move[0] + 1][move[1] - 2]):
                    possible_moves.append([move[0] + 1, move[1] - 2])

        if current_pawn == 4:
            for i in range(1, 8):
                if (move[0] + i) > 7 or (move[1] + i) > 7 or is_white(self._main_board[move[0] + i][move[1] + i]):
                    break

                if (move[0] + i) > 7 or (move[1] + i) > 7 or is_black(self._main_board[move[0] + i][move[1] + i]):
                    possible_moves.append([move[0] + i, move[1] + i])
                    break
                possible_moves.append([move[0] + i, move[1] + i])

            for i in range(1, 8):
                if (move[0] - i) < 0 or (move[1] - i) < 0 or is_white(self._main_board[move[0] - i][move[1] - i]):
                    break

                if (move[0] - i) < 0 or (move[1] - i) < 0 or is_black(self._main_board[move[0] - i][move[1] - i]):
                    possible_moves.append([move[0] - i, move[1] - i])
                    break
                possible_moves.append([move[0] - i, move[1] - i])

            for i in range(1, 8):
                if (move[0] + i) > 7 or (move[1] - i) < 0 or is_white(self._main_board[move[0] + i][move[1] - i]):
                    break

                if (move[0] + i) > 7 or (move[1] - i) < 0 or is_black(self._main_board[move[0] + i][move[1] - i]):
                    possible_moves.append([move[0] + i, move[1] - i])
                    break
                possible_moves.append([move[0] + i, move[1] - i])

            for i in range(1, 8):
                if (move[0] - i) < 0 or (move[1] + i) > 7 or is_white(self._main_board[move[0] - i][move[1] + i]):
                    break

                if (move[0] - i) < 0 or (move[1] + i) > 7 or is_black(self._main_board[move[0] - i][move[1] + i]):
                    possible_moves.append([move[0] - i, move[1] + i])
                    break
                possible_moves.append([move[0] - i, move[1] + i])

        if current_pawn == 5:
            for i in range(1, 8):
                if (move[0] + i) > 7 or (move[1] + i) > 7 or is_white(self._main_board[move[0] + i][move[1] + i]):
                    break

                if (move[0] + i) > 7 or (move[1] + i) > 7 or is_black(self._main_board[move[0] + i][move[1] + i]):
                    possible_moves.append([move[0] + i, move[1] + i])
                    break
                possible_moves.append([move[0] + i, move[1] + i])

            for i in range(1, 8):
                if (move[0] - i) < 0 or (move[1] - i) < 0 or is_white(self._main_board[move[0] - i][move[1] - i]):
                    break

                if (move[0] - i) < 0 or (move[1] - i) < 0 or is_black(self._main_board[move[0] - i][move[1] - i]):
                    possible_moves.append([move[0] - i, move[1] - i])
                    break
                possible_moves.append([move[0] - i, move[1] - i])

            for i in range(1, 8):
                if (move[0] + i) > 7 or (move[1] - i) < 0 or is_white(self._main_board[move[0] + i][move[1] - i]):
                    break

                if (move[0] + i) > 7 or (move[1] - i) < 0 or is_black(self._main_board[move[0] + i][move[1] - i]):
                    possible_moves.append([move[0] + i, move[1] - i])
                    break
                possible_moves.append([move[0] + i, move[1] - i])

            for i in range(1, 8):
                if (move[0] - i) < 0 or (move[1] + i) > 7 or is_white(self._main_board[move[0] - i][move[1] + i]):
                    break

                if (move[0] - i) < 0 or (move[1] + i) > 7 or is_black(self._main_board[move[0] - i][move[1] + i]):
                    possible_moves.append([move[0] - i, move[1] + i])
                    break
                possible_moves.append([move[0] - i, move[1] + i])

            for i in range(1, 8):
                if (move[0] + i) > 7 or is_white(self._main_board[move[0] + i][move[1]]):
                    break

                if (move[0] + i) > 7 or is_black(self._main_board[move[0] + i][move[1]]):
                    possible_moves.append([move[0] + i, move[1]])
                    break
                possible_moves.append([move[0] + i, move[1]])

            for i in range(1, 8):
                if (move[0] - i) < 0 or is_white(self._main_board[move[0] - i][move[1]]):
                    break

                if (move[0] - i) < 0 or is_black(self._main_board[move[0] - i][move[1]]):
                    possible_moves.append([move[0] - i, move[1]])
                    break
                possible_moves.append([move[0] - i, move[1]])

            for i in range(1, 8):
                if (move[1] + i) > 7 or is_white(self._main_board[move[0]][move[1] + i]):
                    break

                if (move[1] + i) > 7 or is_black(self._main_board[move[0]][move[1] + i]):
                    possible_moves.append([move[0], move[1] + i])
                    break
                possible_moves.append([move[0], move[1] + i])

            for i in range(1, 8):
                if (move[1] - i) < 0 or is_white(self._main_board[move[0]][move[1] - i]):
                    break

                if (move[1] - i) < 0 or is_black(self._main_board[move[0]][move[1] - i]):
                    possible_moves.append([move[0], move[1] - i])
                    break
                possible_moves.append([move[0], move[1] - i])

        if current_pawn == 6:
            for i in range(1, 2):
                if (move[0] + i) > 7 or (move[1] + i) > 7 or is_white(self._main_board[move[0] + i][move[1] + i]):
                    break

                if (move[0] + i) > 7 or (move[1] + i) > 7 or is_black(self._main_board[move[0] + i][move[1] + i]):
                    possible_moves.append([move[0] + i, move[1] + i])
                    break
                possible_moves.append([move[0] + i, move[1] + i])

            for i in range(1, 2):
                if (move[0] - i) < 0 or (move[1] - i) < 0 or is_white(self._main_board[move[0] - i][move[1] - i]):
                    break

                if (move[0] - i) < 0 or (move[1] - i) < 0 or is_black(self._main_board[move[0] - i][move[1] - i]):
                    possible_moves.append([move[0] - i, move[1] - i])
                    break
                possible_moves.append([move[0] - i, move[1] - i])

            for i in range(1, 2):
                if (move[0] + i) > 7 or (move[1] - i) < 0 or is_white(self._main_board[move[0] + i][move[1] - i]):
                    break

                if (move[0] + i) > 7 or (move[1] - i) < 0 or is_black(self._main_board[move[0] + i][move[1] - i]):
                    possible_moves.append([move[0] + i, move[1] - i])
                    break
                possible_moves.append([move[0] + i, move[1] - i])

            for i in range(1, 2):
                if (move[0] - i) < 0 or (move[1] + i) > 7 or is_white(self._main_board[move[0] - i][move[1] + i]):
                    break

                if (move[0] - i) < 0 or (move[1] + i) > 7 or is_black(self._main_board[move[0] - i][move[1] + i]):
                    possible_moves.append([move[0] - i, move[1] + i])
                    break
                possible_moves.append([move[0] - i, move[1] + i])

            for i in range(1, 2):
                if (move[0] + i) > 7 or is_white(self._main_board[move[0] + i][move[1]]):
                    break

                if (move[0] + i) > 7 or is_black(self._main_board[move[0] + i][move[1]]):
                    possible_moves.append([move[0] + i, move[1]])
                    break
                possible_moves.append([move[0] + i, move[1]])

            for i in range(1, 2):
                if (move[0] - i) < 0 or is_white(self._main_board[move[0] - i][move[1]]):
                    break

                if (move[0] - i) < 0 or is_black(self._main_board[move[0] - i][move[1]]):
                    possible_moves.append([move[0] - i, move[1]])
                    break
                possible_moves.append([move[0] - i, move[1]])

            for i in range(1, 2):
                if (move[1] + i) > 7 or is_white(self._main_board[move[0]][move[1] + i]):
                    break

                if (move[1] + i) > 7 or is_black(self._main_board[move[0]][move[1] + i]):
                    possible_moves.append([move[0], move[1] + i])
                    break
                possible_moves.append([move[0], move[1] + i])

            for i in range(1, 2):
                if (move[1] - i) < 0 or is_white(self._main_board[move[0]][move[1] - i]):
                    break

                if (move[1] - i) < 0 or is_black(self._main_board[move[0]][move[1] - i]):
                    possible_moves.append([move[0], move[1] - i])
                    break
                possible_moves.append([move[0], move[1] - i])

        if current_pawn == 11:
            if move[1] - 1 >= 0 and self._main_board[move[0]][move[1] - 1] == 0:
                possible_moves.append([move[0], move[1] - 1])
                if move[1] == 6:
                    if move[1] - 2 >= 0 and self._main_board[move[0]][move[1] - 2] == 0:
                        possible_moves.append([move[0], move[1] - 2])

            if move[0] + 1 < 8 and move[1] - 1 >= 0 and is_white(self._main_board[move[0] + 1][move[1] - 1]):
                possible_moves.append([move[0] + 1, move[1] - 1])

            if move[0] - 1 > 0 and move[1] - 0 >= 0 and is_white(self._main_board[move[0] - 1][move[1] - 1]):
                possible_moves.append([move[0] - 1, move[1] - 1])

            if move[1] == 3:
                if move[0] + 1 < 8 and is_white(self._main_board[move[0] + 1][move[1]]):
                    possible_moves.append([move[0] + 1, move[1] - 1])

                if move[0] - 1 > 0 and is_white(self._main_board[move[0] - 1][move[1]]):
                    possible_moves.append([move[0] - 1, move[1] - 1])

        if current_pawn == 12:
            for i in range(1, 8):
                if (move[0] + i) > 7 or is_black(self._main_board[move[0] + i][move[1]]):
                    break

                if (move[0] + i) > 7 or is_white(self._main_board[move[0] + i][move[1]]):
                    possible_moves.append([move[0] + i, move[1]])
                    break
                possible_moves.append([move[0] + i, move[1]])

            for i in range(1, 8):
                if (move[0] - i) < 0 or is_black(self._main_board[move[0] - i][move[1]]):
                    break

                if (move[0] - i) < 0 or is_white(self._main_board[move[0] - i][move[1]]):
                    possible_moves.append([move[0] - i, move[1]])
                    break
                possible_moves.append([move[0] - i, move[1]])

            for i in range(1, 8):
                if (move[1] + i) > 7 or is_black(self._main_board[move[0]][move[1] + i]):
                    break

                if (move[1] + i) > 7 or is_white(self._main_board[move[0]][move[1] + i]):
                    possible_moves.append([move[0], move[1] + i])
                    break
                possible_moves.append([move[0], move[1] + i])

            for i in range(1, 8):
                if (move[1] - i) < 0 or is_black(self._main_board[move[0]][move[1] - i]):
                    break

                if (move[1] - i) < 0 or is_white(self._main_board[move[0]][move[1] - i]):
                    possible_moves.append([move[0], move[1] - i])
                    break
                possible_moves.append([move[0], move[1] - i])

        if current_pawn == 13:
            if move[0] + 2 < 8 and move[1] + 1 < 8:
                if not is_black(self._main_board[move[0] + 2][move[1] + 1]):
                    possible_moves.append([move[0] + 2, move[1] + 1])

            if move[0] + 1 < 8 and move[1] + 2 < 8:
                if not is_black(self._main_board[move[0] + 1][move[1] + 2]):
                    possible_moves.append([move[0] + 1, move[1] + 2])

            if move[0] - 2 >= 0 and move[1] - 1 >= 0:
                if not is_black(self._main_board[move[0] - 2][move[1] - 1]):
                    possible_moves.append([move[0] - 2, move[1] - 1])

            if move[0] - 1 >= 0 and move[1] - 2 >= 0:
                if not is_black(self._main_board[move[0] - 1][move[1] - 2]):
                    possible_moves.append([move[0] - 1, move[1] - 2])

            if move[0] - 2 >= 0 and move[1] + 1 < 8:
                if not is_black(self._main_board[move[0] - 2][move[1] + 1]):
                    possible_moves.append([move[0] - 2, move[1] + 1])

            if move[0] - 1 >= 0 and move[1] + 2 < 8:
                if not is_black(self._main_board[move[0] - 1][move[1] + 2]):
                    possible_moves.append([move[0] - 1, move[1] + 2])

            if move[0] + 2 < 8 and move[1] - 1 >= 0:
                if not is_black(self._main_board[move[0] + 2][move[1] - 1]):
                    possible_moves.append([move[0] + 2, move[1] - 1])

            if move[0] + 1 < 8 and move[1] - 2 >= 0:
                if not is_black(self._main_board[move[0] + 1][move[1] - 2]):
                    possible_moves.append([move[0] + 1, move[1] - 2])

        if current_pawn == 14:
            for i in range(1, 8):
                if (move[0] + i) > 7 or (move[1] + i) > 7 or is_black(self._main_board[move[0] + i][move[1] + i]):
                    break

                if (move[0] + i) > 7 or (move[1] + i) > 7 or is_white(self._main_board[move[0] + i][move[1] + i]):
                    possible_moves.append([move[0] + i, move[1] + i])
                    break
                possible_moves.append([move[0] + i, move[1] + i])

            for i in range(1, 8):
                if (move[0] - i) < 0 or (move[1] - i) < 0 or is_black(self._main_board[move[0] - i][move[1] - i]):
                    break

                if (move[0] - i) < 0 or (move[1] - i) < 0 or is_white(self._main_board[move[0] - i][move[1] - i]):
                    possible_moves.append([move[0] - i, move[1] - i])
                    break
                possible_moves.append([move[0] - i, move[1] - i])

            for i in range(1, 8):
                if (move[0] + i) > 7 or (move[1] - i) < 0 or is_black(self._main_board[move[0] + i][move[1] - i]):
                    break

                if (move[0] + i) > 7 or (move[1] - i) < 0 or is_white(self._main_board[move[0] + i][move[1] - i]):
                    possible_moves.append([move[0] + i, move[1] - i])
                    break
                possible_moves.append([move[0] + i, move[1] - i])

            for i in range(1, 8):
                if (move[0] - i) < 0 or (move[1] + i) > 7 or is_black(self._main_board[move[0] - i][move[1] + i]):
                    break

                if (move[0] - i) < 0 or (move[1] + i) > 7 or is_white(self._main_board[move[0] - i][move[1] + i]):
                    possible_moves.append([move[0] - i, move[1] + i])
                    break
                possible_moves.append([move[0] - i, move[1] + i])

        if current_pawn == 15:
            for i in range(1, 8):
                if (move[0] + i) > 7 or (move[1] + i) > 7 or is_black(self._main_board[move[0] + i][move[1] + i]):
                    break

                if (move[0] + i) > 7 or (move[1] + i) > 7 or is_white(self._main_board[move[0] + i][move[1] + i]):
                    possible_moves.append([move[0] + i, move[1] + i])
                    break
                possible_moves.append([move[0] + i, move[1] + i])

            for i in range(1, 8):
                if (move[0] - i) < 0 or (move[1] - i) < 0 or is_black(self._main_board[move[0] - i][move[1] - i]):
                    break

                if (move[0] - i) < 0 or (move[1] - i) < 0 or is_white(self._main_board[move[0] - i][move[1] - i]):
                    possible_moves.append([move[0] - i, move[1] - i])
                    break
                possible_moves.append([move[0] - i, move[1] - i])

            for i in range(1, 8):
                if (move[0] + i) > 7 or (move[1] - i) < 0 or is_black(self._main_board[move[0] + i][move[1] - i]):
                    break

                if (move[0] + i) > 7 or (move[1] - i) < 0 or is_white(self._main_board[move[0] + i][move[1] - i]):
                    possible_moves.append([move[0] + i, move[1] - i])
                    break
                possible_moves.append([move[0] + i, move[1] - i])

            for i in range(1, 8):
                if (move[0] - i) < 0 or (move[1] + i) > 7 or is_black(self._main_board[move[0] - i][move[1] + i]):
                    break

                if (move[0] - i) < 0 or (move[1] + i) > 7 or is_white(self._main_board[move[0] - i][move[1] + i]):
                    possible_moves.append([move[0] - i, move[1] + i])
                    break
                possible_moves.append([move[0] - i, move[1] + i])

            for i in range(1, 8):
                if (move[0] + i) > 7 or is_black(self._main_board[move[0] + i][move[1]]):
                    break

                if (move[0] + i) > 7 or is_white(self._main_board[move[0] + i][move[1]]):
                    possible_moves.append([move[0] + i, move[1]])
                    break
                possible_moves.append([move[0] + i, move[1]])

            for i in range(1, 8):
                if (move[0] - i) < 0 or is_black(self._main_board[move[0] - i][move[1]]):
                    break

                if (move[0] - i) < 0 or is_white(self._main_board[move[0] - i][move[1]]):
                    possible_moves.append([move[0] - i, move[1]])
                    break
                possible_moves.append([move[0] - i, move[1]])

            for i in range(1, 8):
                if (move[1] + i) > 7 or is_black(self._main_board[move[0]][move[1] + i]):
                    break

                if (move[1] + i) > 7 or is_white(self._main_board[move[0]][move[1] + i]):
                    possible_moves.append([move[0], move[1] + i])
                    break
                possible_moves.append([move[0], move[1] + i])

            for i in range(1, 8):
                if (move[1] - i) < 0 or is_black(self._main_board[move[0]][move[1] - i]):
                    break

                if (move[1] - i) < 0 or is_white(self._main_board[move[0]][move[1] - i]):
                    possible_moves.append([move[0], move[1] - i])
                    break
                possible_moves.append([move[0], move[1] - i])

        if current_pawn == 16:
            for i in range(1, 2):
                if (move[0] + i) > 7 or (move[1] + i) > 7 or is_black(self._main_board[move[0] + i][move[1] + i]):
                    break

                if (move[0] + i) > 7 or (move[1] + i) > 7 or is_white(self._main_board[move[0] + i][move[1] + i]):
                    possible_moves.append([move[0] + i, move[1] + i])
                    break
                possible_moves.append([move[0] + i, move[1] + i])

            for i in range(1, 2):
                if (move[0] - i) < 0 or (move[1] - i) < 0 or is_black(self._main_board[move[0] - i][move[1] - i]):
                    break

                if (move[0] - i) < 0 or (move[1] - i) < 0 or is_white(self._main_board[move[0] - i][move[1] - i]):
                    possible_moves.append([move[0] - i, move[1] - i])
                    break
                possible_moves.append([move[0] - i, move[1] - i])

            for i in range(1, 2):
                if (move[0] + i) > 7 or (move[1] - i) < 0 or is_black(self._main_board[move[0] + i][move[1] - i]):
                    break

                if (move[0] + i) > 7 or (move[1] - i) < 0 or is_white(self._main_board[move[0] + i][move[1] - i]):
                    possible_moves.append([move[0] + i, move[1] - i])
                    break
                possible_moves.append([move[0] + i, move[1] - i])

            for i in range(1, 2):
                if (move[0] - i) < 0 or (move[1] + i) > 7 or is_black(self._main_board[move[0] - i][move[1] + i]):
                    break

                if (move[0] - i) < 0 or (move[1] + i) > 7 or is_white(self._main_board[move[0] - i][move[1] + i]):
                    possible_moves.append([move[0] - i, move[1] + i])
                    break
                possible_moves.append([move[0] - i, move[1] + i])

            for i in range(1, 2):
                if (move[0] + i) > 7 or is_black(self._main_board[move[0] + i][move[1]]):
                    break

                if (move[0] + i) > 7 or is_white(self._main_board[move[0] + i][move[1]]):
                    possible_moves.append([move[0] + i, move[1]])
                    break
                possible_moves.append([move[0] + i, move[1]])

            for i in range(1, 2):
                if (move[0] - i) < 0 or is_black(self._main_board[move[0] - i][move[1]]):
                    break

                if (move[0] - i) < 0 or is_white(self._main_board[move[0] - i][move[1]]):
                    possible_moves.append([move[0] - i, move[1]])
                    break
                possible_moves.append([move[0] - i, move[1]])

            for i in range(1, 2):
                if (move[1] + i) > 7 or is_black(self._main_board[move[0]][move[1] + i]):
                    break

                if (move[1] + i) > 7 or is_white(self._main_board[move[0]][move[1] + i]):
                    possible_moves.append([move[0], move[1] + i])
                    break
                possible_moves.append([move[0], move[1] + i])

            for i in range(1, 2):
                if (move[1] - i) < 0 or is_black(self._main_board[move[0]][move[1] - i]):
                    break

                if (move[1] - i) < 0 or is_white(self._main_board[move[0]][move[1] - i]):
                    possible_moves.append([move[0], move[1] - i])
                    break
                possible_moves.append([move[0], move[1] - i])

        return possible_moves


class Move:
    def __init__(self, board, start_move, end_move):
        self.main_board = copy.deepcopy(board)
        self.start_move = start_move
        self.end_move = end_move
        self.moving_pawn = board[start_move[0]][start_move[1]]
        self.target_pawn = board[end_move[0]][end_move[1]]
        self.move_pos = 1000 * start_move[0] + 100 * start_move[1] + 10 * end_move[0] + end_move[1]

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_pos == other.move_pos
