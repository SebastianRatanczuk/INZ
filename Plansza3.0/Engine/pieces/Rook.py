from Engine.pieces.Piece import Piece


class Rook(Piece):
    def __init__(self, is_white):
        number = 2
        pawn_number = number if is_white else 10 + number
        super().__init__(is_white, pawn_number)

    def get_all_possible_moves(self, main_board, move):
        possible_moves = []
        destinations = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        for destination in destinations:
            for i in range(1, 8):
                new_move = [move[0] + i * destination[0], move[1] + i * destination[1]]
                if 0 <= new_move[0] < 8 and 0 <= new_move[1] < 8:
                    if main_board[new_move[0]][new_move[1]] == 0:
                        possible_moves.append(new_move)
                    elif main_board[new_move[0]][new_move[1]].is_white != self.is_white:
                        possible_moves.append(new_move)
                        break
                    else:
                        break
        return possible_moves
