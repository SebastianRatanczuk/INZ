from Engine.pieces.Piece import Piece


class Rook(Piece):
    def __init__(self, isWhite):
        number = 2
        pawn_number = number if isWhite else 10 + number
        super().__init__(isWhite, pawn_number)

    def getAllPossibleMoves(self, board):
        print(board)
