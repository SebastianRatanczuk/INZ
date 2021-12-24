//
// Created by sebol on 23.12.2021.
//


#ifndef SZASZKI_BOARD_H
#define SZASZKI_BOARD_H

#include <algorithm>
#include <cctype>
#include <chrono>
#include <functional>
#include <iostream>
#include <map>
#include <random>
#include <string>
#include <utility>
#include <vector>
#include "Move.h"

#include "Enums.h"


class Board {
public:
    char board[NB_SQ]{};

    std::string whiteKingPos;
    std::string blackKingPos;
    Color turn;
    std::vector<Move> moves{};

    bool isGameOver;
    bool isCheckMate;
    bool isStaleMate;
    std::string en_passant;
    bool castle_rights[NB_COLOR][NB_CASTLE]{};

    Board();

    explicit Board(const std::string &);

    char setPieceAt(int row, int col, char piece);

    char getPieceAt(int row, int col);

    char getPieceUci(std::string uci);

    bool isPieceAtPosWhite(int row, int col);

    bool isPieceAtPosBlack(int row, int col);

    static std::string getUci(int row, int col);

    std::vector<Move> generatePawnMoves(int boxNumber);

    std::vector<Move> generateValidMoves();

    std::vector<Move> generateLegalMoves();

    std::vector<Move> generateCastlingMoves();

    void print_board();

    std::string get_board();

    bool checkForCheck();

    bool checkForAttack(const std::string &uci);

    std::vector<Move> KingSideCastle(std::string uci);

    std::vector<Move> QueenSideCastle(std::string uci);

    bool move(std::string uci);

    Move pop();

    std::string translateBoardToFEN();

};


#endif //SZASZKI_BOARD_H
