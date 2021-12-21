import copy
import dataclasses
import multiprocessing
import time
from typing import Optional, List

import chess
import numpy as np
from numba import prange, jit

num_cores = multiprocessing.cpu_count()


@dataclasses.dataclass
class Status:
    winner: Optional[bool]

    def result(self) -> str:
        return "1/2-1/2" if self.winner is None else ("1-0" if self.winner else "0-1")


class Move:
    def __init__(self, board, start_move, end_move, isEnpassant=False, isCastle=False):
        self.start_move = start_move
        self.end_move = end_move
        self.moving_pawn = board[start_move[0] * 8 + start_move[1]]
        self.target_pawn = board[end_move[0] * 8 + end_move[1]]
        self.move_pos = chr(start_move[0] + 97) + str(start_move[1] + 1) + chr(end_move[0] + 97) + str(end_move[1] + 1)
        self.is_pawn_promotion = False
        self.enpassant = ()

        if isinstance(self.moving_pawn, Pawn):
            if self.moving_pawn.is_white and self.end_move[1] == 7:
                self.is_pawn_promotion = True
            if not self.moving_pawn.is_white and self.end_move[1] == 0:
                self.is_pawn_promotion = True

        self.is_enpassant_move = isEnpassant
        if isEnpassant:
            self.target_pawn = board[end_move[0] * 8 + start_move[1]]

        self.is_castle_move = isCastle

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_pos == other.move_pos


class Piece:

    def __init__(self, is_white, pawn_number, symbol) -> None:
        self.is_white = is_white
        self.pawn_number = pawn_number
        self.symbol = symbol
        self.has_moved = False

    def get_all_possible_moves(self, engine, move) -> List[Move]:
        """Returns all possible moves for given piece"""
        pass


class Pawn(Piece):

    def __init__(self, is_white):
        number = 1
        pawn_number = number if is_white else 10 + number
        symbol = "P" if is_white else "p"
        super().__init__(is_white, pawn_number, symbol)

    def get_all_possible_moves(self, engine, move):
        possible_moves = []
        if self.is_white:
            if move[1] + 1 < 8 and engine.get_piece([move[0], move[1] + 1]) is None:

                possible_moves.append(Move(engine.main_board, move, [move[0], move[1] + 1]))
                if not self.has_moved:
                    if move[1] + 2 < 8 and engine.get_piece([move[0], move[1] + 2]) is None:
                        possible_moves.append(Move(engine.main_board, move, [move[0], move[1] + 2]))

            if move[0] + 1 < 8 and move[1] + 1 < 8 and engine.get_piece([move[0] + 1, move[1] + 1]) is not None and not \
                    engine.get_piece([move[0] + 1, move[1] + 1]).is_white:
                possible_moves.append(Move(engine.main_board, move, [move[0] + 1, move[1] + 1]))
            elif (move[0] + 1, move[1] + 1) == engine.possible_enpassant:
                possible_moves.append(
                    Move(engine.main_board, move, [move[0] + 1, move[1] + 1], True))

            if move[0] - 1 >= 0 and move[1] + 1 < 8 and engine.get_piece([move[0] - 1, move[1] + 1]) is not None and not \
                    engine.get_piece([move[0] - 1, move[1] + 1]).is_white:
                possible_moves.append(Move(engine.main_board, move, [move[0] - 1, move[1] + 1]))
            elif (move[0] - 1, move[1] + 1) == engine.possible_enpassant:
                possible_moves.append(
                    Move(engine.main_board, move, [move[0] - 1, move[1] + 1], True))

        else:
            if move[1] - 1 >= 0 and engine.get_piece([move[0], move[1] - 1]) is None:
                possible_moves.append(Move(engine.main_board, move, [move[0], move[1] - 1]))
                if not self.has_moved:
                    if move[1] - 2 >= 0 and engine.get_piece([move[0], move[1] - 2]) is None:
                        possible_moves.append(Move(engine.main_board, move, [move[0], move[1] - 2]))

            if move[0] + 1 < 8 and move[1] - 1 >= 0 and engine.get_piece([move[0] + 1, move[1] - 1]) is not None and \
                    engine.get_piece([move[0] + 1, move[1] - 1]).is_white:
                possible_moves.append(Move(engine.main_board, move, [move[0] + 1, move[1] - 1]))
            elif (move[0] + 1, move[1] - 1) == engine.possible_enpassant:
                possible_moves.append(
                    Move(engine.main_board, move, [move[0] + 1, move[1] - 1], True))

            if move[0] - 1 >= 0 and move[1] - 0 >= 0 and engine.get_piece([move[0] - 1, move[1] - 1]) is not None and \
                    engine.get_piece([move[0] - 1, move[1] - 1]).is_white:
                possible_moves.append(Move(engine.main_board, move, [move[0] - 1, move[1] - 1]))
            elif (move[0] - 1, move[1] - 1) == engine.possible_enpassant:
                possible_moves.append(
                    Move(engine.main_board, move, [move[0] - 1, move[1] - 1], True))
        return possible_moves


class Rook(Piece):
    def __init__(self, is_white):
        number = 2
        pawn_number = number if is_white else 10 + number
        symbol = "R" if is_white else "r"
        super().__init__(is_white, pawn_number, symbol)

    def get_all_possible_moves(self, engine, move):
        possible_moves = []
        destinations = [[1, 0], [-1, 0], [0, 1], [0, -1]]

        for destination in destinations:
            for i in range(1, 8):
                new_move = [move[0] + i * destination[0], move[1] + i * destination[1]]
                if 0 <= new_move[0] < 8 and 0 <= new_move[1] < 8:
                    if engine.get_piece([new_move[0], new_move[1]]) is None:
                        possible_moves.append(Move(engine.main_board, move, new_move))
                    elif engine.get_piece([new_move[0], new_move[1]]).is_white != self.is_white:
                        possible_moves.append(Move(engine.main_board, move, new_move))
                        break
                    else:
                        break
        return possible_moves


class Bishop(Piece):
    def __init__(self, is_white):
        number = 4
        pawn_number = number if is_white else 10 + number
        symbol = "B" if is_white else "b"
        super().__init__(is_white, pawn_number, symbol)

    def get_all_possible_moves(self, engine, move):
        possible_moves = []
        destinations = [[1, 1], [-1, -1], [-1, 1], [1, -1]]
        for destination in destinations:
            for i in range(1, 8):
                new_move = [move[0] + i * destination[0], move[1] + i * destination[1]]
                if 0 <= new_move[0] < 8 and 0 <= new_move[1] < 8:
                    if engine.get_piece([new_move[0], new_move[1]]) is None:
                        possible_moves.append(Move(engine.main_board, move, new_move))
                    elif engine.get_piece([new_move[0], new_move[1]]).is_white != self.is_white:
                        possible_moves.append(Move(engine.main_board, move, new_move))
                        break
                    else:
                        break
        return possible_moves


class Knight(Piece):
    def __init__(self, is_white):
        number = 3
        pawn_number = number if is_white else 10 + number
        symbol = "N" if is_white else "n"
        super().__init__(is_white, pawn_number, symbol)

    def get_all_possible_moves(self, engine, move):
        possible_moves = []
        destinations = [[1, 2], [-1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, 1], [-2, -1]]
        for destination in destinations:
            new_move = [move[0] + destination[0], move[1] + destination[1]]
            if 0 <= new_move[0] < 8 and 0 <= new_move[1] < 8:
                if engine.get_piece([new_move[0], new_move[1]]) is None:
                    possible_moves.append(Move(engine.main_board, move, new_move))
                elif engine.get_piece([new_move[0], new_move[1]]).is_white != self.is_white:
                    possible_moves.append(Move(engine.main_board, move, new_move))

        return possible_moves


class Queen(Piece):
    def __init__(self, is_white):
        number = 5
        pawn_number = number if is_white else 10 + number
        symbol = "Q" if is_white else "q"
        super().__init__(is_white, pawn_number, symbol)

    def get_all_possible_moves(self, engine, move):
        possible_moves = []
        destinations = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [-1, 1], [1, -1]]
        for destination in destinations:
            for i in range(1, 8):
                new_move = [move[0] + i * destination[0], move[1] + i * destination[1]]
                if 0 <= new_move[0] < 8 and 0 <= new_move[1] < 8:
                    if engine.get_piece([new_move[0], new_move[1]]) is None:
                        possible_moves.append(Move(engine.main_board, move, new_move))
                    elif engine.get_piece([new_move[0], new_move[1]]).is_white != self.is_white:
                        possible_moves.append(Move(engine.main_board, move, new_move))
                        break
                    else:
                        break
        return possible_moves


class King(Piece):
    def __init__(self, is_white):
        number = 6
        pawn_number = number if is_white else 10 + number
        symbol = "K" if is_white else "k"
        super().__init__(is_white, pawn_number, symbol)

    def get_all_possible_moves(self, engine, move):
        possible_moves = []
        destinations = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [-1, 1], [1, -1]]
        for destination in destinations:
            new_move = [move[0] + destination[0], move[1] + destination[1]]
            if 0 <= new_move[0] < 8 and 0 <= new_move[1] < 8:
                if engine.get_piece([new_move[0], new_move[1]]) is None:
                    possible_moves.append(Move(engine.main_board, move, new_move))
                elif engine.get_piece([new_move[0], new_move[1]]).is_white != self.is_white:
                    possible_moves.append(Move(engine.main_board, move, new_move))

        return possible_moves


class GameEngine:

    def __init__(self) -> None:
        self.main_board = np.array([
            Rook(True), Pawn(True), None, None, None, None, Pawn(False), Rook(False),  # A
            Knight(True), Pawn(True), None, None, None, None, Pawn(False), Knight(False),  # B
            Bishop(True), Pawn(True), None, None, None, None, Pawn(False), Bishop(False),  # C
            Queen(True), Pawn(True), None, None, None, None, Pawn(False), Queen(False),  # D
            King(True), Pawn(True), None, None, None, None, Pawn(False), King(False),  # E
            Bishop(True), Pawn(True), None, None, None, None, Pawn(False), Bishop(False),  # F
            Knight(True), Pawn(True), None, None, None, None, Pawn(False), Knight(False),  # G
            Rook(True), Pawn(True), None, None, None, None, Pawn(False), Rook(False),  # H
        ])

        self.white_turn = True
        self._log = []
        self.white_king_pos = [4, 0]
        self.black_king_pos = [4, 7]
        self.check_mate = False
        self.stale_mate = False
        self.possible_enpassant = ()

    def get_piece(self, pos) -> Optional[Piece]:
        return self.main_board[pos[0] * 8 + pos[1]]

    def set_piece(self, pos, piece: Optional[Piece]):
        self.main_board[pos[0] * 8 + pos[1]] = piece

    def move(self, move) -> None:
        self.white_turn = not self.white_turn
        self.set_piece([move.start_move[0], move.start_move[1]], None)
        moving_pawn = copy.deepcopy(move.moving_pawn)
        moving_pawn.has_moved = True
        self.set_piece([move.end_move[0], move.end_move[1]], moving_pawn)
        move.enpassant = copy.deepcopy(self.possible_enpassant)
        self._log.append(move)

        if isinstance(move.moving_pawn, King):
            if move.moving_pawn.is_white:
                self.white_king_pos = move.end_move
            else:
                self.black_king_pos = move.end_move

        if move.is_pawn_promotion:
            self.set_piece([move.end_move[0], move.end_move[1]], Queen(move.moving_pawn.is_white))

        if move.is_enpassant_move:
            self.set_piece([move.end_move[0], move.start_move[1]], None)

        if isinstance(move.moving_pawn, Pawn) and abs(move.start_move[1] - move.end_move[1]) == 2:
            self.possible_enpassant = (move.end_move[0], (move.start_move[1] + move.end_move[1]) // 2)
        else:
            self.possible_enpassant = ()

        if move.is_castle_move:
            if move.end_move[0] - move.start_move[0] == 2:
                oldPiece = self.get_piece([move.end_move[0] + 1, move.end_move[1]])
                self.set_piece([move.end_move[0] - 1, move.end_move[1]], oldPiece)
                self.set_piece([move.end_move[0] + 1, move.end_move[1]], None)
            else:
                oldPiece = self.get_piece([move.end_move[0] - 2, move.end_move[1]])
                self.set_piece([move.end_move[0] + 1, move.end_move[1]], oldPiece)
                self.set_piece([move.end_move[0] - 2, move.end_move[1]], None)

    def undo_move(self) -> None:
        if len(self._log) == 0:
            return
        self.white_turn = not self.white_turn
        old_move = self._log.pop()
        self.set_piece([old_move.start_move[0], old_move.start_move[1]], old_move.moving_pawn)
        self.set_piece([old_move.end_move[0], old_move.end_move[1]], old_move.target_pawn)

        if isinstance(old_move.moving_pawn, King):
            if old_move.moving_pawn.is_white:
                self.white_king_pos = old_move.start_move
            else:
                self.black_king_pos = old_move.start_move

        if old_move.is_enpassant_move:
            self.set_piece([old_move.end_move[0], old_move.end_move[1]], None)
            self.set_piece([old_move.end_move[0], old_move.start_move[1]], old_move.target_pawn)

        self.possible_enpassant = old_move.enpassant

        if old_move.is_castle_move:
            if old_move.end_move[0] - old_move.start_move[0] == 2:
                oldPiece = self.get_piece([old_move.end_move[0] - 1, old_move.end_move[1]])
                self.set_piece([old_move.end_move[0] + 1, old_move.end_move[1]], oldPiece)
                self.set_piece([old_move.end_move[0] - 1, old_move.end_move[1]], None)
            else:
                oldPiece = self.get_piece([old_move.end_move[0] + 1, old_move.end_move[1]])
                self.set_piece([old_move.end_move[0] - 2, old_move.end_move[1]], oldPiece)
                self.set_piece([old_move.end_move[0] + 1, old_move.end_move[1]], None)

    def get_valid_moves(self) -> List[Move]:
        """Returns valid moves"""

        start = time.time()

        tempEnp = self.possible_enpassant
        moves = self.get_possible_moves()

        if self.white_turn:
            castleMoves = self.getCastileMoves(self.white_king_pos)
            for m in castleMoves:
                moves.append(m)
        else:
            castleMoves = self.getCastileMoves(self.black_king_pos)
            for m in castleMoves:
                moves.append(m)

        valid_moves = []
        for i in prange(len(moves)):
            self.move(moves[i])
            self.white_turn = not self.white_turn
            if not self.check_for_check():
                valid_moves.append(moves[i])
            self.white_turn = not self.white_turn
            self.undo_move()

        if len(valid_moves) == 0:
            if self.check_for_check():
                self.check_mate = True
            else:
                self.stale_mate = True
        else:
            self.check_mate = False
            self.stale_mate = False
        self.possible_enpassant = tempEnp
        end = time.time()

        return valid_moves

    @jit(parallel=True, forceobj=True)
    def get_possible_moves(self) -> List[Move]:
        """Returns all legal moves"""
        possible_moves = []
        for square in prange(64):
            if self.main_board[square] is not None and (
                    self.white_turn == self.main_board[square].is_white):
                allMoves = self.get_possible_piece_moves([square // 8, square % 8])
                for move in allMoves:
                    possible_moves.append(move)
        return possible_moves

    def get_possible_piece_moves(self, move) -> List[Move]:
        current_pawn = self.get_piece([move[0], move[1]])
        return current_pawn.get_all_possible_moves(self, move)

    def check_for_check(self) -> bool:
        if self.white_turn:
            return self.check_for_attack(self.white_king_pos)
        else:
            return self.check_for_attack(self.black_king_pos)

    def check_for_attack(self, position) -> bool:
        self.white_turn = not self.white_turn
        enemyMoves = self.get_possible_moves()
        self.white_turn = not self.white_turn

        end_moves = list(map(lambda move: move.end_move, enemyMoves))

        return any(position == move for move in end_moves)

    def getCastileMoves(self, move) -> List[Move]:
        casstleMoves = []
        if self.check_for_check():
            return casstleMoves

        if self.get_piece([move[0], move[1]]).has_moved:
            return casstleMoves

        if self.get_piece([move[0], move[1]]).is_white:
            if isinstance(self.get_piece([0, 0]), Rook) and self.get_piece([0, 0]).has_moved:
                return casstleMoves
            else:
                m = self.getQueensCastle(move)
                if m is not None:
                    casstleMoves.append(m)

            if isinstance(self.get_piece([7, 0]), Rook) and self.get_piece([7, 0]).has_moved:
                return casstleMoves
            else:
                m = self.getKingsCastle(move)
                if m is not None:
                    casstleMoves.append(m)
        else:
            if isinstance(self.get_piece([0, 7]), Rook) and self.get_piece([0, 7]).has_moved:
                return casstleMoves
            else:
                m = self.getQueensCastle(move)
                if m is not None:
                    casstleMoves.append(m)

            if isinstance(self.get_piece([7, 7]), Rook) and self.get_piece([7, 7]).has_moved:
                return casstleMoves
            else:
                m = self.getKingsCastle(move)
                if m is not None:
                    casstleMoves.append(m)

        return casstleMoves

    def getKingsCastle(self, move) -> Move:
        if self.get_piece([move[0] + 1, move[1]]) is None and \
                self.get_piece([move[0] + 2, move[1]]) is None:
            if not self.check_for_attack([move[0] + 1, move[1]]) \
                    and not self.check_for_attack([move[0] + 2, move[1]]):
                return Move(self.main_board, move, [move[0] + 2, move[1]], isCastle=True)

    def getQueensCastle(self, move) -> Move:
        if self.get_piece([move[0] - 1, move[1]]) is None \
                and self.get_piece([move[0] - 2, move[1]]) is None \
                and self.get_piece([move[0] - 3, move[1]]) is None:
            if not self.check_for_attack([move[0] - 1, move[1]]) \
                    and not self.check_for_attack([move[0] - 2, move[1]]):
                return Move(self.main_board, move, [move[0] - 2, move[1]], isCastle=True)

    def is_game_over(self) -> bool:
        return self.check_mate or self.stale_mate

    def game_status(self) -> Optional[Status]:
        if not self.is_game_over():
            return None
        return Status(self.white_turn)

    def get_chess_board(self) -> chess.Board:
        board = chess.Board()
        board.turn = self.white_turn
        for file in range(8):
            for rank in range(8):
                if self.get_piece([file, rank]) is None:
                    board.set_piece_at(file + rank * 8, None)
                else:
                    board.set_piece_at(file + rank * 8, chess.Piece.from_symbol(self.get_piece([file, rank]).symbol))

        return board
