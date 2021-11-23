from Engine.pieces.Piece import Piece


class Pawn(Piece):
    def __init__(self, isWhite):
        number = 1
        pawn_number = number if isWhite else 10 + number
        super().__init__(isWhite, pawn_number)

    def getAllPossibleMoves(self, main_board, move):
        # todo ampersand not implemented
        possible_moves = []
        if self.isWhite:
            if move[1] + 1 < 8 and main_board[move[0]][move[1] + 1] == 0:
                possible_moves.append([move[0], move[1] + 1])
                if not self.hasMoved:
                    if move[1] + 2 < 8 and main_board[move[0]][move[1] + 2] == 0:
                        possible_moves.append([move[0], move[1] + 2])

            if move[0] + 1 < 8 and move[1] + 1 < 8 and main_board[move[0] + 1][move[1] + 1] != 0 and not \
                    main_board[move[0] + 1][move[1] + 1].isWhite:
                possible_moves.append([move[0] + 1, move[1] + 1])

            if move[0] - 1 > 0 and move[1] + 1 < 8 and main_board[move[0] - 1][move[1] + 1] != 0 and not \
                    main_board[move[0] - 1][move[1] + 1].isWhite:
                possible_moves.append([move[0] - 1, move[1] + 1])

        else:
            if move[1] - 1 >= 0 and main_board[move[0]][move[1] - 1] == 0:
                possible_moves.append([move[0], move[1] - 1])
                if not self.hasMoved:
                    if move[1] - 2 >= 0 and main_board[move[0]][move[1] - 2] == 0:
                        possible_moves.append([move[0], move[1] - 2])

            if move[0] + 1 < 8 and move[1] - 1 >= 0 and main_board[move[0] + 1][move[1] - 1] != 0 and \
                    main_board[move[0] + 1][move[1] - 1].isWhite:
                possible_moves.append([move[0] + 1, move[1] - 1])

            if move[0] - 1 > 0 and move[1] - 0 >= 0 and main_board[move[0] - 1][move[1] - 1] != 0 and \
                    main_board[move[0] - 1][move[1] - 1].isWhite:
                possible_moves.append([move[0] - 1, move[1] - 1])

        return possible_moves
