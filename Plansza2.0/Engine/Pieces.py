from abc import abstractmethod, ABCMeta

import Engine.ChessEngine


class Piece:
    __metaclass__ = ABCMeta

    def __init__(self, is_white, pawn_number):
        self.is_white = is_white
        self.pawn_number = pawn_number
        self.has_moved = False

    @abstractmethod
    def get_all_possible_moves(self, engine, move):
        pass


class Pawn(Piece):

    def __init__(self, is_white):
        number = 1
        pawn_number = number if is_white else 10 + number
        super().__init__(is_white, pawn_number)

    def get_all_possible_moves(self, engine, move):
        possible_moves = []
        if self.is_white:
            if move[1] + 1 < 8 and engine.main_board[move[0]][move[1] + 1] == 0:

                possible_moves.append(Engine.ChessEngine.Move(engine.main_board, move, [move[0], move[1] + 1]))
                if not self.has_moved:
                    if move[1] + 2 < 8 and engine.main_board[move[0]][move[1] + 2] == 0:
                        possible_moves.append(Engine.ChessEngine.Move(engine.main_board, move, [move[0], move[1] + 2]))

            if move[0] + 1 < 8 and move[1] + 1 < 8 and engine.main_board[move[0] + 1][move[1] + 1] != 0 and not \
                    engine.main_board[move[0] + 1][move[1] + 1].is_white:
                possible_moves.append(Engine.ChessEngine.Move(engine.main_board, move, [move[0] + 1, move[1] + 1]))
            elif (move[0] + 1, move[1] + 1) == engine.possible_enpassant:
                possible_moves.append(
                    Engine.ChessEngine.Move(engine.main_board, move, [move[0] + 1, move[1] + 1], True))

            if move[0] - 1 >= 0 and move[1] + 1 < 8 and engine.main_board[move[0] - 1][move[1] + 1] != 0 and not \
                    engine.main_board[move[0] - 1][move[1] + 1].is_white:
                possible_moves.append(Engine.ChessEngine.Move(engine.main_board, move, [move[0] - 1, move[1] + 1]))
            elif (move[0] - 1, move[1] + 1) == engine.possible_enpassant:
                possible_moves.append(
                    Engine.ChessEngine.Move(engine.main_board, move, [move[0] - 1, move[1] + 1], True))

        else:
            if move[1] - 1 >= 0 and engine.main_board[move[0]][move[1] - 1] == 0:
                possible_moves.append(Engine.ChessEngine.Move(engine.main_board, move, [move[0], move[1] - 1]))
                if not self.has_moved:
                    if move[1] - 2 >= 0 and engine.main_board[move[0]][move[1] - 2] == 0:
                        possible_moves.append(Engine.ChessEngine.Move(engine.main_board, move, [move[0], move[1] - 2]))

            if move[0] + 1 < 8 and move[1] - 1 >= 0 and engine.main_board[move[0] + 1][move[1] - 1] != 0 and \
                    engine.main_board[move[0] + 1][move[1] - 1].is_white:
                possible_moves.append(Engine.ChessEngine.Move(engine.main_board, move, [move[0] + 1, move[1] - 1]))
            elif (move[0] + 1, move[1] - 1) == engine.possible_enpassant:
                possible_moves.append(
                    Engine.ChessEngine.Move(engine.main_board, move, [move[0] + 1, move[1] - 1], True))

            if move[0] - 1 >= 0 and move[1] - 0 >= 0 and engine.main_board[move[0] - 1][move[1] - 1] != 0 and \
                    engine.main_board[move[0] - 1][move[1] - 1].is_white:
                possible_moves.append(Engine.ChessEngine.Move(engine.main_board, move, [move[0] - 1, move[1] - 1]))
            elif (move[0] - 1, move[1] - 1) == engine.possible_enpassant:
                possible_moves.append(
                    Engine.ChessEngine.Move(engine.main_board, move, [move[0] - 1, move[1] - 1], True))
        return possible_moves


class Rook(Piece):
    def __init__(self, is_white):
        number = 2
        pawn_number = number if is_white else 10 + number
        super().__init__(is_white, pawn_number)

    def get_all_possible_moves(self, engine, move):
        possible_moves = []
        destinations = [[1, 0], [-1, 0], [0, 1], [0, -1]]

        for destination in destinations:
            for i in range(1, 8):
                new_move = [move[0] + i * destination[0], move[1] + i * destination[1]]
                if 0 <= new_move[0] < 8 and 0 <= new_move[1] < 8:
                    if engine.main_board[new_move[0]][new_move[1]] == 0:

                        possible_moves.append(Engine.ChessEngine.Move(engine.main_board, move, new_move))
                    elif engine.main_board[new_move[0]][new_move[1]].is_white != self.is_white:
                        possible_moves.append(Engine.ChessEngine.Move(engine.main_board, move, new_move))
                        break
                    else:
                        break
        return possible_moves


class Bishop(Piece):
    def __init__(self, is_white):
        number = 4
        pawn_number = number if is_white else 10 + number
        super().__init__(is_white, pawn_number)

    def get_all_possible_moves(self, engine, move):
        possible_moves = []
        destinations = [[1, 1], [-1, -1], [-1, 1], [1, -1]]
        for destination in destinations:
            for i in range(1, 8):
                new_move = [move[0] + i * destination[0], move[1] + i * destination[1]]
                if 0 <= new_move[0] < 8 and 0 <= new_move[1] < 8:
                    if engine.main_board[new_move[0]][new_move[1]] == 0:
                        possible_moves.append(Engine.ChessEngine.Move(engine.main_board, move, new_move))
                    elif engine.main_board[new_move[0]][new_move[1]].is_white != self.is_white:
                        possible_moves.append(Engine.ChessEngine.Move(engine.main_board, move, new_move))
                        break
                    else:
                        break
        return possible_moves


class Knight(Piece):
    def __init__(self, is_white):
        number = 3
        pawn_number = number if is_white else 10 + number
        super().__init__(is_white, pawn_number)

    def get_all_possible_moves(self, engine, move):
        possible_moves = []
        destinations = [[1, 2], [-1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, 1], [-2, -1]]
        for destination in destinations:
            new_move = [move[0] + destination[0], move[1] + destination[1]]
            if 0 <= new_move[0] < 8 and 0 <= new_move[1] < 8:
                if engine.main_board[new_move[0]][new_move[1]] == 0:
                    possible_moves.append(Engine.ChessEngine.Move(engine.main_board, move, new_move))
                elif engine.main_board[new_move[0]][new_move[1]].is_white != self.is_white:
                    possible_moves.append(Engine.ChessEngine.Move(engine.main_board, move, new_move))

        return possible_moves


class Queen(Piece):
    def __init__(self, is_white):
        number = 5
        pawn_number = number if is_white else 10 + number
        super().__init__(is_white, pawn_number)

    def get_all_possible_moves(self, engine, move):
        possible_moves = []
        destinations = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [-1, 1], [1, -1]]
        for destination in destinations:
            for i in range(1, 8):
                new_move = [move[0] + i * destination[0], move[1] + i * destination[1]]
                if 0 <= new_move[0] < 8 and 0 <= new_move[1] < 8:
                    if engine.main_board[new_move[0]][new_move[1]] == 0:
                        possible_moves.append(Engine.ChessEngine.Move(engine.main_board, move, new_move))
                    elif engine.main_board[new_move[0]][new_move[1]].is_white != self.is_white:
                        possible_moves.append(Engine.ChessEngine.Move(engine.main_board, move, new_move))
                        break
                    else:
                        break
        return possible_moves


class King(Piece):
    def __init__(self, is_white):
        number = 6
        pawn_number = number if is_white else 10 + number
        super().__init__(is_white, pawn_number)

    def get_all_possible_moves(self, engine, move):
        possible_moves = []
        destinations = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [-1, 1], [1, -1]]
        for destination in destinations:
            new_move = [move[0] + destination[0], move[1] + destination[1]]
            if 0 <= new_move[0] < 8 and 0 <= new_move[1] < 8:
                if engine.main_board[new_move[0]][new_move[1]] == 0:
                    possible_moves.append(Engine.ChessEngine.Move(engine.main_board, move, new_move))
                elif engine.main_board[new_move[0]][new_move[1]].is_white != self.is_white:
                    possible_moves.append(Engine.ChessEngine.Move(engine.main_board, move, new_move))

        return possible_moves
