from Engine.pieces.Piece import Piece


class Queen(Piece):
    def __init__(self, isWhite):
        number = 5
        pawn_number = number if isWhite else 10 + number
        super().__init__(isWhite, pawn_number)

    def getAllPossibleMoves(self, main_board, move):
        possible_moves = []
        destinations = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [-1, 1], [1, -1]]
        for destination in destinations:
            for i in range(1, 8):
                new_move = [move[0] + i * destination[0], move[1] + i * destination[1]]
                if 0 <= new_move[0] < 8 and 0 <= new_move[1] < 8:
                    if main_board[new_move[0]][new_move[1]] == 0:
                        possible_moves.append(new_move)
                    elif main_board[new_move[0]][new_move[1]].isWhite != self.isWhite:
                        possible_moves.append(new_move)
                        break
                    else:
                        break
        return possible_moves
