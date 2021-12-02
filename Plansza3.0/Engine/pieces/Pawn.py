from Engine.pieces.Piece import Piece


class Pawn(Piece):

    def __init__(self, is_white):
        number = 1
        pawn_number = number if is_white else 10 + number
        super().__init__(is_white, pawn_number)

    def get_all_possible_moves(self, main_board, move):
        from Engine.Move import Move
        from Engine.ChessEngine import GameEngine
        possible_moves = []
        if self.is_white:
            if move[1] + 1 < 8 and main_board[move[0]][move[1] + 1] == 0:

                possible_moves.append(Move(main_board, move, [move[0], move[1] + 1]))
                if not self.has_moved:
                    if move[1] + 2 < 8 and main_board[move[0]][move[1] + 2] == 0:
                        possible_moves.append(Move(main_board, move, [move[0], move[1] + 2]))

            if move[0] + 1 < 8 and move[1] + 1 < 8 and main_board[move[0] + 1][move[1] + 1] != 0 and not \
                    main_board[move[0] + 1][move[1] + 1].is_white:
                possible_moves.append(Move(main_board, move, [move[0] + 1, move[1] + 1]))
            elif [move[0] + 1, move[1] + 1] == GameEngine().possible_enpassant:
                possible_moves.append(Move(main_board, move, [move[0] + 1, move[1] + 1], True))

            if move[0] - 1 >= 0 and move[1] + 1 < 8 and main_board[move[0] - 1][move[1] + 1] != 0 and not \
                    main_board[move[0] - 1][move[1] + 1].is_white:
                possible_moves.append(Move(main_board, move, [move[0] - 1, move[1] + 1]))
            elif [move[0] - 1, move[1] + 1] == GameEngine().possible_enpassant:
                possible_moves.append(Move(main_board, move, [move[0] - 1, move[1] + 1], True))

        else:
            if move[1] - 1 >= 0 and main_board[move[0]][move[1] - 1] == 0:
                possible_moves.append(Move(main_board, move, [move[0], move[1] - 1]))
                if not self.has_moved:
                    if move[1] - 2 >= 0 and main_board[move[0]][move[1] - 2] == 0:
                        possible_moves.append(Move(main_board, move, [move[0], move[1] - 2]))

            if move[0] + 1 < 8 and move[1] - 1 >= 0 and main_board[move[0] + 1][move[1] - 1] != 0 and \
                    main_board[move[0] + 1][move[1] - 1].is_white:
                possible_moves.append(Move(main_board, move, [move[0] + 1, move[1] - 1]))

            if move[0] - 1 >= 0 and move[1] - 0 >= 0 and main_board[move[0] - 1][move[1] - 1] != 0 and \
                    main_board[move[0] - 1][move[1] - 1].is_white:
                possible_moves.append(Move(main_board, move, [move[0] - 1, move[1] - 1]))

        return possible_moves
