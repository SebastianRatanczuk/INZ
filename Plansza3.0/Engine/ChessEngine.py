import copy

from Engine.pieces.Bishop import Bishop
from Engine.pieces.King import King
from Engine.pieces.Knight import Knight
from Engine.pieces.Pawn import Pawn
from Engine.pieces.Queen import Queen
from Engine.pieces.Rook import Rook


class GameEngine:
    def __init__(self):
        self.main_board = [
            [Rook(True), Pawn(True), 0, 0, 0, 0, Pawn(False), Rook(False)],  # A
            [Knight(True), Pawn(True), 0, 0, 0, 0, Pawn(False), Knight(False)],  # B
            [Bishop(True), Pawn(True), 0, 0, 0, 0, Pawn(False), Bishop(False)],  # C
            [Queen(True), Pawn(True), 0, 0, 0, 0, Pawn(False), Queen(False)],  # D
            [King(True), Pawn(True), 0, 0, 0, 0, Pawn(False), King(False)],  # E
            [Bishop(True), Pawn(True), 0, 0, 0, 0, Pawn(False), Bishop(False)],  # F
            [Knight(True), Pawn(True), 0, 0, 0, 0, Pawn(False), Knight(False)],  # G
            [Rook(True), Pawn(True), 0, 0, 0, 0, Pawn(False), Rook(False)],  # H
        ]
        self.white_turn = True
        self._log = []
        self.white_king_pos = [4, 0]
        self.black_king_pos = [4, 7]
        self.check_mate = False
        self.stale_mate = False
        self.possible_enpassant = []

    def move(self, move):
        self.white_turn = not self.white_turn
        self.main_board[move.start_move[0]][move.start_move[1]] = 0
        moving_pawn = copy.deepcopy(move.moving_pawn)
        moving_pawn.has_moved = True
        self.main_board[move.end_move[0]][move.end_move[1]] = moving_pawn
        self._log.append(move)

        if isinstance(move.moving_pawn, King):
            if move.moving_pawn.is_white:
                self.white_king_pos = move.end_move
            else:
                self.black_king_pos = move.end_move

        if move.is_pawn_promotion:
            self.main_board[move.end_move[0]][move.end_move[1]] = Queen(move.moving_pawn.is_white)

    def undo_move(self):
        if len(self._log) == 0:
            return
        self.white_turn = not self.white_turn
        old_move = self._log.pop()
        self.main_board[old_move.start_move[0]][old_move.start_move[1]] = old_move.moving_pawn
        self.main_board[old_move.end_move[0]][old_move.end_move[1]] = old_move.target_pawn

        if isinstance(old_move.moving_pawn, King):
            if old_move.moving_pawn.is_white:
                self.white_king_pos = old_move.start_move
            else:
                self.black_king_pos = old_move.start_move

    def get_board(self):
        return self.main_board

    def get_valid_moves(self):
        moves = self.get_possible_moves()
        for i in range(len(moves) - 1, -1, -1):
            self.move(moves[i])
            self.white_turn = not self.white_turn
            if self.check_for_check():
                moves.remove(moves[i])
            self.white_turn = not self.white_turn
            self.undo_move()

        if len(moves) == 0:
            if self.check_for_check():
                self.check_mate = True
            else:
                self.stale_mate = True
        else:
            self.check_mate = False
            self.stale_mate = False
        return moves

    def get_possible_moves(self):
        possible_moves = []
        for file in range(8):
            for rank in range(8):
                if (self.white_turn and self.main_board[file][rank] != 0 and self.main_board[file][rank].is_white) or (
                        not self.white_turn and self.main_board[file][rank] != 0
                        and not self.main_board[file][rank].is_white):
                    allMoves = self.get_possible_piece_moves([file, rank])
                    for move in allMoves:
                        possible_moves.append(move)

        return possible_moves

    def get_possible_piece_moves(self, move):
        current_pawn = self.main_board[move[0]][move[1]]
        return current_pawn.get_all_possible_moves(self.main_board, move)

    def check_for_check(self):
        if self.white_turn:
            return self.check_for_attack(self.white_king_pos)
        else:
            return self.check_for_attack(self.black_king_pos)

    def check_for_attack(self, position):
        self.white_turn = not self.white_turn
        enemyMoves = self.get_possible_moves()
        self.white_turn = not self.white_turn

        for move in enemyMoves:
            if move.end_move == position:
                return True
        return False
