//
// Created by sebol on 23.12.2021.
//

#include "Ai.h"

#include <utility>

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
        return -CHECKMATE;
    }

    int pieceValue = 0;
    int mobilityValue = 0;

    for (int row = 0; row < 8; row++) {
        for (int col = 0; col < 8; ++col) {
            auto piece = board.getPieceAt(row, col);
            if (piece == '.')
                continue;

            if ((board.turn == Color::white) == isupper(piece)) {
                pieceValue += piece_value[(char) tolower(piece)];
                mobilityValue += board.generatePawnMoves(row, col).size();
            } else {
                pieceValue -= piece_value[(char) tolower(piece)];
                mobilityValue -= board.generatePawnMoves(row, col).size();
            }
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

    for (auto move: moves) {
        board.move(&move);
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
    nega(mainDepth, mainBoard, mainBoard.turn == Color::white ? 1 : -1, -CHECKMATE, CHECKMATE);
    if (mainMove.moveUci == "null") {
        std::vector<Move> moves = mainBoard.generateValidMoves();
        if (!moves.empty()) {
            mainMove = moves[0];
        }
    }
    return mainMove;
}

Ai::Ai(Board board, int depth) {
    mainBoard = std::move(board);
    mainDepth = depth;
}
