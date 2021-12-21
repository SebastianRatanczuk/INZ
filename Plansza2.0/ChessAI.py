import random

import ChessEngine

piece_relative_value = {
    "p": 1,
    "n": 3,
    "b": 3,
    "r": 5,
    "q": 9,
    "k": 0
}

CHECKMATE = 500
MD = 3


def bestMove(engine: ChessEngine.GameEngine) -> ChessEngine.Move:
    global goodMove
    goodMove = random.choice(engine.get_valid_moves())
    findNega(MD, engine, 1 if engine.white_turn else -1, -CHECKMATE, CHECKMATE)
    # min_max(MD, engine)
    print(goodMove.move_pos)
    return goodMove


def min_max(depth: int, engine: ChessEngine.GameEngine):
    global goodMove
    moves = engine.get_valid_moves()
    random.shuffle(moves)
    if depth == 0 or len(moves) == 0:
        return getMaterial(engine)

    if engine.white_turn:
        score = -CHECKMATE
        for move in moves:
            engine.move(move)
            minmax_score = min_max(depth - 1, engine)
            if minmax_score > score:
                score = minmax_score
                if depth == MD:
                    goodMove = move
            engine.undo_move()
    else:
        score = CHECKMATE
        for move in moves:
            engine.move(move)
            minmax_score = min_max(depth - 1, engine)
            if minmax_score < score:
                score = minmax_score
                if depth == MD:
                    goodMove = move
            engine.undo_move()

    return score


def findNega(depth: int, engine: ChessEngine.GameEngine, turn, alfa, beta):
    global goodMove
    moves = engine.get_valid_moves()
    if depth == 0 or len(moves) == 0:
        return getMaterial(engine) * turn
    random.shuffle(moves)
    score = -CHECKMATE

    for move in moves:
        engine.move(move)
        nega_score = -findNega(depth - 1, engine, -turn, -beta, -alfa)
        if nega_score > score:
            score = nega_score
            if depth == MD:
                goodMove = move
        engine.undo_move()
        if score > alfa:
            alfa = score

        if alfa >= beta:
            break

    return score


def getMaterial(engine: ChessEngine.GameEngine):
    if engine.stale_mate:
        return 0
    elif engine.check_mate:
        if engine.white_turn:
            return -CHECKMATE
        else:
            return CHECKMATE
    score = 0

    for square in range(64):
        if engine.main_board[square] is not None:
            piece = engine.main_board[square]
            if piece.is_white:
                score += piece_relative_value[piece.symbol.lower()]
            else:
                score -= piece_relative_value[piece.symbol.lower()]

    return score
