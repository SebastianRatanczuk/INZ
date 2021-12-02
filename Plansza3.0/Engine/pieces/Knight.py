from Engine.Move import Move
from Engine.pieces.Piece import Piece


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
                    possible_moves.append(Move(engine.main_board, move, new_move))
                elif engine.main_board[new_move[0]][new_move[1]].is_white != self.is_white:
                    possible_moves.append(Move(engine.main_board, move, new_move))

        return possible_moves
