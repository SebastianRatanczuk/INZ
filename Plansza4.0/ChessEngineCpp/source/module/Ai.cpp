//
// Created by sebol on 23.12.2021.
//

#include "Ai.h"
std::mt19937 gen(std::chrono::system_clock::now().time_since_epoch().count());

Ai::Ai() {
    mainBoard = Board();
}

Ai::Ai(const std::string &fen, int depth) {
    mainBoard = Board(fen);
    this->mainDepth = depth;
}

int Ai::boardHeuristic(Board board) {
    if (board.isStaleMate)
        return 0;
    if (board.isCheckMate) {
        if (board.turn == Color::white)
            return CHECKMATE;
        else
            return -CHECKMATE;
    }

    int pieceValue = 0;
    int mobilityValue = 0;

    for (int square = 0; square < 64; square++) {
        auto piece = board.board[square];
        if (piece == '.')
            continue;

        if (board.turn == Color::white && isupper(piece)) {
            pieceValue += piece_value[(char) tolower(piece)];
            mobilityValue += board.generatePawnMoves(square).size();
        } else {
            pieceValue -= piece_value[(char) tolower(piece)];
            mobilityValue -= board.generatePawnMoves(square).size();
        }
    }

    return 12 * pieceValue + mobilityValue;
}

int Ai::nega(int depth, Board &board, int turn, int alfa, int beta) {

    if (depth == 0) {
        return boardHeuristic(board) * turn;
    }

    auto moves = board.generateValidMoves();

    if (moves.empty()) {
        return -CHECKMATE;
    }

    std::shuffle(moves.begin(), moves.end(), gen);
    int score = -CHECKMATE;

    for (const auto &move: moves) {
        board.move(move.moveUci);
        int negaScore = -nega(depth - 1, board, -turn, -beta, -alfa);
        if (negaScore > score) {
            score = negaScore;
            if (this->mainDepth == depth) {
                this->mainMove = move;
            }
        }
        board.pop();

        alfa = std::max(alfa, score);
        if (alfa >= beta)
            break;
    }

    return score;
}

Move Ai::negaAlfABeta() {
    mainMove = mainBoard.generateValidMoves().back();
    nega(mainDepth, mainBoard, mainBoard.turn == Color::white ? 1 : -1, -CHECKMATE, CHECKMATE);
    return mainMove;
}