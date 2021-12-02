from abc import abstractmethod, ABCMeta


class Piece:
    __metaclass__ = ABCMeta

    def __init__(self, is_white, pawn_number):
        self.is_white = is_white
        self.pawn_number = pawn_number
        self.has_moved = False

    @abstractmethod
    def get_all_possible_moves(self, engine, move):
        pass
