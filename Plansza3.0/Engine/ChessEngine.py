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

    def move(self, move):
        self.white_turn = not self.white_turn
        self.main_board[move.start_move[0]][move.start_move[1]] = 0
        self.main_board[move.end_move[0]][move.end_move[1]] = move.moving_pawn
        move.moving_pawn.hasMoved = True
        self._log.append(move)

    def undo_move(self):
        if len(self._log) == 0:
            return
        self.white_turn = not self.white_turn
        old_move = self._log.pop()
        self.main_board = old_move.main_board

    def get_board(self):
        return self.main_board

    def get_valid_moves(self):
        return self.get_possible_moves()

    def get_possible_moves(self):
        possible_moves = []
        for file in range(8):
            for rank in range(8):
                if (self.white_turn and self.main_board[file][rank] != 0 and self.main_board[file][rank].isWhite) or (
                        not self.white_turn and self.main_board[file][rank] != 0
                        and not self.main_board[file][rank].isWhite):
                    allMoves = self.get_possible_piece_moves([file, rank])
                    for move in allMoves:
                        possible_moves.append(Move(self.main_board, [file, rank], move))

        return possible_moves

    def get_possible_piece_moves(self, move):
        current_pawn = self.main_board[move[0]][move[1]]
        return current_pawn.getAllPossibleMoves(self.main_board, move)


class Move:
    def __init__(self, board, start_move, end_move):
        self.main_board = copy.deepcopy(board)
        self.start_move = start_move
        self.end_move = end_move
        self.moving_pawn = board[start_move[0]][start_move[1]]
        self.target_pawn = board[end_move[0]][end_move[1]]
        self.move_pos = 1000 * start_move[0] + 100 * start_move[1] + 10 * end_move[0] + end_move[1]

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_pos == other.move_pos
