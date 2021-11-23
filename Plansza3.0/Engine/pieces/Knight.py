from Engine.pieces.Piece import Piece


class Knight(Piece):
    def __init__(self, isWhite):
        number = 3
        pawn_number = number if isWhite else 10 + number
        super().__init__(isWhite, pawn_number)

    def getAllPossibleMoves(self, board):
        print(board)
