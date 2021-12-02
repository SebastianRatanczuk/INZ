import Engine.pieces.Pawn as Pawn


class Move:
    def __init__(self, board, start_move, end_move, enpassant=False):
        self.start_move = start_move
        self.end_move = end_move
        self.moving_pawn = board[start_move[0]][start_move[1]]
        self.target_pawn = board[end_move[0]][end_move[1]]
        self.move_pos = 1000 * start_move[0] + 100 * start_move[1] + 10 * end_move[0] + end_move[1]
        self.is_pawn_promotion = False

        if isinstance(self.moving_pawn, Pawn.Pawn):
            if self.moving_pawn.is_white and self.end_move[1] == 7:
                self.is_pawn_promotion = True
            if not self.moving_pawn.is_white and self.end_move[1] == 0:
                self.is_pawn_promotion = True

        self.is_enpassant_move = enpassant
        if enpassant:
            self.target_pawn = board[end_move[0]][start_move[1]]

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_pos == other.move_pos
