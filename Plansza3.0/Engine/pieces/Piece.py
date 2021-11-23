from abc import abstractmethod, ABCMeta


class Piece:
    __metaclass__ = ABCMeta

    def __init__(self, isWhite, pawn_number):
        self.isWhite = isWhite
        self.pawn_number = pawn_number
        self.hasMoved = False

    @abstractmethod
    def getAllPossibleMoves(self, board):
        pass
