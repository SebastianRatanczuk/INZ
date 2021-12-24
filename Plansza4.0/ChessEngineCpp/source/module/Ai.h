//
// Created by sebol on 23.12.2021.
//

#ifndef SZASZKI_AI_H
#define SZASZKI_AI_H

#include "Board.h"
class Ai {
private:
    Board mainBoard;
    int mainDepth = 4;
    std::map<char, int> piece_value = {
            {'p', 1},
            {'n', 3},
            {'b', 3},
            {'r', 5},
            {'q', 10},
            {'k', 0}
    };

    int CHECKMATE = 100000;
    Move mainMove;
    int boardHeuristic(Board board);
    int nega(int depth, Board &board, int turn, int alfa, int beta);
public:
    Ai();
    explicit Ai(const std::string &fen, int depth);
    Move negaAlfABeta();
};


#endif //SZASZKI_AI_H
