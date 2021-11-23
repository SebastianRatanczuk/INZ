from Engine.pieces.Piece import Piece


class Knight(Piece):
    def __init__(self, isWhite):
        number = 3
        pawn_number = number if isWhite else 10 + number
        super().__init__(isWhite, pawn_number)

    def getAllPossibleMoves(self, main_board, move):
        possible_moves = []
        destinations = [[1, 2], [-1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, 1], [-2, -1]]
        for destination in destinations:
            new_move = [move[0] + destination[0], move[1] + destination[1]]
            if 0 <= new_move[0] < 8 and 0 <= new_move[1] < 8:
                if main_board[new_move[0]][new_move[1]] == 0:
                    possible_moves.append(new_move)
                elif main_board[new_move[0]][new_move[1]].isWhite != self.isWhite:
                    possible_moves.append(new_move)

        return possible_moves
