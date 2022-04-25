//
// Created by sebol on 23.12.2021.
//

#include <thread>
#include <string>
#include "Board.h"

// trim from start
static inline std::string &ltrim(std::string &s) {
    s.erase(s.begin(), std::find_if(s.begin(), s.end(),
                                    std::not1(std::ptr_fun<int, int>(std::isspace))));
    return s;
}

// trim from end
static inline std::string &rtrim(std::string &s) {
    s.erase(std::find_if(s.rbegin(), s.rend(),
                         std::not1(std::ptr_fun<int, int>(std::isspace))).base(), s.end());
    return s;
}

// trim from both ends
static inline std::string &trim(std::string &s) {
    return ltrim(rtrim(s));
}

Board::Board() {

    isStaleMate = isCheckMate = isGameOver = false;
    whiteKingPos = "e1";
    blackKingPos = "e8";

    std::string fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";

    whiteKingPos = "e1";
    blackKingPos = "e8";
    for (char &i: board) i = '.';
    const size_t size = fen.size();
    size_t iter = 0;
    int index = 0;

    for (; (iter < size) && (fen[iter] != ' '); iter++) {
        if (fen[iter] == '/')
            continue;

        if (isdigit(fen[iter]))
            index += (fen[iter] - '0');

        else {
            board[index] = fen[iter];
            ++index;
        }
    }

    turn = fen[iter + 1] == 'w' ? Color::white : Color::black;

    for (iter += 3; (iter < size) && (fen[iter] != ' '); iter++) {

        if (fen[iter] == 'k')
            castle_rights[Color::black][Castle::king_side] = true;

        else if (fen[iter] == 'K')
            castle_rights[Color::white][Castle::king_side] = true;

        else if (fen[iter] == 'q')
            castle_rights[Color::black][Castle::queen_side] = true;

        else if (fen[iter] == 'Q')
            castle_rights[Color::white][Castle::queen_side] = true;
    }
    std::string tmp = fen.substr(iter + 1, 2);
    en_passant = trim(tmp);
}

Board::Board(const std::string &fen) {
    isStaleMate = isCheckMate = isGameOver = false;

    whiteKingPos = "e1";
    blackKingPos = "e8";
    for (char &i: board) i = '.';
    const size_t size = fen.size();
    size_t iter = 0;
    int index = 0;

    for (; (iter < size) && (fen[iter] != ' '); iter++) {
        if (fen[iter] == '/')
            continue;

        if (isdigit(fen[iter]))
            index += (fen[iter] - '0');

        else {
            board[index] = fen[iter];
            ++index;
        }
    }

    turn = fen[iter + 1] == 'w' ? Color::white : Color::black;

    for (iter += 3; (iter < size) && (fen[iter] != ' '); iter++) {

        if (fen[iter] == 'k')
            castle_rights[Color::black][Castle::king_side] = true;

        else if (fen[iter] == 'K')
            castle_rights[Color::white][Castle::king_side] = true;

        else if (fen[iter] == 'q')
            castle_rights[Color::black][Castle::queen_side] = true;

        else if (fen[iter] == 'Q')
            castle_rights[Color::white][Castle::queen_side] = true;
    }

    en_passant = fen.substr(iter + 1, 2);
}

char Board::setPieceAt(int row, int col, char piece) {
    if (row > 7 || row < 0 || col > 7 || col < 0)
        throw std::out_of_range("OutOfBounds");
    return board[row * 8 + col] = piece;
}

char Board::getPieceAt(int row, int col) {
    if (row > 7 || row < 0 || col > 7 || col < 0)
        throw std::out_of_range("OutOfBounds");
    return board[row * 8 + col];
}

char Board::getPieceUci(std::string uci) {
    int col = uci[0] - 97;
    int row = 8 - (uci[1] - 48);

    return getPieceAt(row, col);
}

bool Board::isPieceAtPosWhite(int row, int col) {
    auto piece = getPieceAt(row, col);

    if (piece == '.')
        return false;

    return (bool)isupper(piece);
}

bool Board::isPieceAtPosBlack(int row, int col) {
    auto piece = getPieceAt(row, col);

    if (piece == '.')
        return false;

    return !(bool)isupper(piece);
}

std::string Board::getUci(int row, int col) {
    return char(col + 97) + std::to_string(8 - row);
}

std::vector<Move> Board::generatePawnMoves(int row, int col) {
    std::vector<Move> listOfMoves;

    std::string startingUci = getUci(row, col);

    switch (board[row * 8 + col]) {
        case 'P': {
            if (row - 1 > 0) {
                if (getPieceAt(row - 1, col) == '.') { //przestrzen wolna nad pionkiem
                    listOfMoves.emplace_back(startingUci + getUci(row - 1, col), getPieceAt(row, col),
                                             getPieceAt(row - 1, col));
                    if (row == 6) { //podwojny ruch
                        if (getPieceAt(row - 2, col) == '.')
                            listOfMoves.emplace_back(startingUci + getUci(row - 2, col), getPieceAt(row, col),
                                                     getPieceAt(row - 2, col));
                    }
                }
            }

            if (row - 1 > 0 && col - 1 >= 0) {
                if (isPieceAtPosBlack(row - 1, col - 1)) {
                    listOfMoves.emplace_back(startingUci + getUci(row - 1, col - 1), getPieceAt(row, col),
                                             getPieceAt(row - 1, col - 1));
                }
                if (en_passant == getUci(row - 1, col - 1)) {
                    listOfMoves.emplace_back(startingUci + getUci(row - 1, col - 1), getPieceAt(row, col),
                                             getPieceAt(row - 1, col - 1), true, false, false, '0');
                }
            }

            if (row - 1 > 0 && col + 1 < 8) {
                if (isPieceAtPosBlack(row - 1, col + 1)) {
                    listOfMoves.emplace_back(startingUci + getUci(row - 1, col + 1), getPieceAt(row, col),
                                             getPieceAt(row - 1, col + 1));
                }
                if (en_passant == getUci(row - 1, col + 1)) {
                    listOfMoves.emplace_back(startingUci + getUci(row - 1, col + 1), getPieceAt(row, col),
                                             getPieceAt(row - 1, col + 1), true, false, false, '0');
                }
            }

            if (row - 1 == 0) {
                if (getPieceAt(row - 1, col) == '.') { //przestrzen wolna nad pionkiem

                    listOfMoves.emplace_back(startingUci + getUci(row - 1, col), getPieceAt(row, col),
                                             getPieceAt(row - 1, col), false, false, true, 'q');
                    listOfMoves.emplace_back(startingUci + getUci(row - 1, col), getPieceAt(row, col),
                                             getPieceAt(row - 1, col), false, false, true, 'b');
                    listOfMoves.emplace_back(startingUci + getUci(row - 1, col), getPieceAt(row, col),
                                             getPieceAt(row - 1, col), false, false, true, 'r');
                    listOfMoves.emplace_back(startingUci + getUci(row - 1, col), getPieceAt(row, col),
                                             getPieceAt(row - 1, col), false, false, true, 'n');

                }
                if (col - 1 >= 0)
                    if (isPieceAtPosBlack(row - 1, col - 1)) {
                        listOfMoves.emplace_back(startingUci + getUci(row - 1, col - 1), getPieceAt(row, col),
                                                 getPieceAt(row - 1, col - 1), false, false, true, 'q');
                        listOfMoves.emplace_back(startingUci + getUci(row - 1, col - 1), getPieceAt(row, col),
                                                 getPieceAt(row - 1, col - 1), false, false, true, 'b');
                        listOfMoves.emplace_back(startingUci + getUci(row - 1, col - 1), getPieceAt(row, col),
                                                 getPieceAt(row - 1, col - 1), false, false, true, 'r');
                        listOfMoves.emplace_back(startingUci + getUci(row - 1, col - 1), getPieceAt(row, col),
                                                 getPieceAt(row - 1, col - 1), false, false, true, 'n');
                    }

                if (col + 1 < 8)
                    if (isPieceAtPosBlack(row - 1, col + 1)) {
                        listOfMoves.emplace_back(startingUci + getUci(row - 1, col + 1), getPieceAt(row, col),
                                                 getPieceAt(row - 1, col + 1), false, false, true, 'q');
                        listOfMoves.emplace_back(startingUci + getUci(row - 1, col + 1), getPieceAt(row, col),
                                                 getPieceAt(row - 1, col + 1), false, false, true, 'b');
                        listOfMoves.emplace_back(startingUci + getUci(row - 1, col + 1), getPieceAt(row, col),
                                                 getPieceAt(row - 1, col + 1), false, false, true, 'r');
                        listOfMoves.emplace_back(startingUci + getUci(row - 1, col + 1), getPieceAt(row, col),
                                                 getPieceAt(row - 1, col + 1), false, false, true, 'n');
                    }
            }

            break;
        }
        case 'R': {
            int directions[4][2] = {{1,  0},
                                    {-1, 0},
                                    {0,  1},
                                    {0,  -1}};

            for (auto direction: directions) {
                for (int i = 1; i < 8; i++) {
                    int newRow = row + direction[0] * i;
                    int newCol = col + direction[1] * i;

                    if (0 <= newRow && newRow < 8 && 0 <= newCol && newCol < 8) {
                        if (getPieceAt(newRow, newCol) == '.')
                            listOfMoves.emplace_back(startingUci + getUci(newRow, newCol), getPieceAt(row, col),
                                                     getPieceAt(newRow, newCol));
                        else if (isPieceAtPosBlack(newRow, newCol)) {
                            listOfMoves.emplace_back(startingUci + getUci(newRow, newCol), getPieceAt(row, col),
                                                     getPieceAt(newRow, newCol));
                            break;
                        } else {
                            break;
                        }
                    }
                }
            }
            break;
        }
        case 'N': {
            int jumps[8][2] = {{1,  2},
                               {-1, 2},
                               {2,  1},
                               {2,  -1},
                               {1,  -2},
                               {-1, -2},
                               {-2, 1},
                               {-2, -1}};

            for (auto jump: jumps) {
                int newRow = row + jump[0];
                int newCol = col + jump[1];

                if (0 <= newRow && newRow < 8 && 0 <= newCol && newCol < 8) {
                    if (!isPieceAtPosWhite(newRow, newCol)) {
                        listOfMoves.emplace_back(startingUci + getUci(newRow, newCol), getPieceAt(row, col),
                                                 getPieceAt(newRow, newCol));
                    }
                }
            }
            break;
        }
        case 'B': {
            int directions[4][2] = {{1,  1},
                                    {-1, -1},
                                    {-1, 1},
                                    {1,  -1}};

            for (auto direction: directions) {
                for (int i = 1; i < 8; i++) {
                    int newRow = row + direction[0] * i;
                    int newCol = col + direction[1] * i;

                    if (0 <= newRow && newRow < 8 && 0 <= newCol && newCol < 8) {
                        if (getPieceAt(newRow, newCol) == '.')
                            listOfMoves.emplace_back(startingUci + getUci(newRow, newCol), getPieceAt(row, col),
                                                     getPieceAt(newRow, newCol));
                        else if (isPieceAtPosBlack(newRow, newCol)) {
                            listOfMoves.emplace_back(startingUci + getUci(newRow, newCol), getPieceAt(row, col),
                                                     getPieceAt(newRow, newCol));
                            break;
                        } else {
                            break;
                        }
                    }
                }
            }
            break;
        }
        case 'Q': {
            int directions[8][2] = {{1,  1},
                                    {-1, -1},
                                    {-1, 1},
                                    {1,  -1},
                                    {1,  0},
                                    {-1, 0},
                                    {0,  1},
                                    {0,  -1}};

            for (auto direction: directions) {
                for (int i = 1; i < 8; i++) {
                    int newRow = row + direction[0] * i;
                    int newCol = col + direction[1] * i;

                    if (0 <= newRow && newRow < 8 && 0 <= newCol && newCol < 8) {
                        if (getPieceAt(newRow, newCol) == '.')
                            listOfMoves.emplace_back(startingUci + getUci(newRow, newCol), getPieceAt(row, col),
                                                     getPieceAt(newRow, newCol));
                        else if (isPieceAtPosBlack(newRow, newCol)) {
                            listOfMoves.emplace_back(startingUci + getUci(newRow, newCol), getPieceAt(row, col),
                                                     getPieceAt(newRow, newCol));
                            break;
                        } else {
                            break;
                        }
                    }
                }
            }
            break;
        }
        case 'K': {
            int jumps[8][2] = {{1,  0},
                               {-1, 0},
                               {0,  1},
                               {0,  -1},
                               {1,  1},
                               {-1, -1},
                               {-1, 1},
                               {1,  -1}};

            for (auto jump: jumps) {
                int newRow = row + jump[0];
                int newCol = col + jump[1];

                if (0 <= newRow && newRow < 8 && 0 <= newCol && newCol < 8) {
                    if (!isPieceAtPosWhite(newRow, newCol)) {
                        listOfMoves.emplace_back(startingUci + getUci(newRow, newCol), getPieceAt(row, col),
                                                 getPieceAt(newRow, newCol));
                    }
                }
            }
            break;
        }
        case 'p': {
            if (row + 1 < 7) {
                if (getPieceAt(row + 1, col) == '.') { //przestrzen wolna nad pionkiem
                    listOfMoves.emplace_back(startingUci + getUci(row + 1, col), getPieceAt(row, col),
                                             getPieceAt(row + 1, col));
                    if (row == 1) { //podwojny ruch
                        if (getPieceAt(row + 2, col) == '.')
                            listOfMoves.emplace_back(startingUci + getUci(row + 2, col), getPieceAt(row, col),
                                                     getPieceAt(row + 2, col));
                    }
                }
            }

            if (row + 1 < 7 && col - 1 >= 0) {
                if (isPieceAtPosWhite(row + 1, col - 1)) {
                    listOfMoves.emplace_back(startingUci + getUci(row + 1, col - 1), getPieceAt(row, col),
                                             getPieceAt(row + 1, col - 1));
                }

                if (en_passant == getUci(row + 1, col - 1)) {
                    listOfMoves.emplace_back(startingUci + getUci(row + 1, col - 1), getPieceAt(row, col),
                                             getPieceAt(row + 1, col - 1), true, false, false, '0');
                }
            }

            if (row + 1 < 7 && col + 1 < 8) {
                if (isPieceAtPosWhite(row + 1, col + 1)) {
                    listOfMoves.emplace_back(startingUci + getUci(row + 1, col + 1), getPieceAt(row, col),
                                             getPieceAt(row + 1, col + 1));
                }

                if (en_passant == getUci(row + 1, col + 1)) {
                    listOfMoves.emplace_back(startingUci + getUci(row + 1, col + 1), getPieceAt(row, col),
                                             getPieceAt(row + 1, col + 1), true, false, false, '0');
                }
            }

            if (row + 1 == 7) {
                if (getPieceAt(row + 1, col) == '.') { //przestrzen wolna nad pionkiem

                    listOfMoves.emplace_back(startingUci + getUci(row + 1, col), getPieceAt(row, col),
                                             getPieceAt(row + 1, col), false, false, true, 'q');
                    listOfMoves.emplace_back(startingUci + getUci(row + 1, col), getPieceAt(row, col),
                                             getPieceAt(row + 1, col), false, false, true, 'b');
                    listOfMoves.emplace_back(startingUci + getUci(row + 1, col), getPieceAt(row, col),
                                             getPieceAt(row + 1, col), false, false, true, 'r');
                    listOfMoves.emplace_back(startingUci + getUci(row + 1, col), getPieceAt(row, col),
                                             getPieceAt(row + 1, col), false, false, true, 'n');

                }
                if (col - 1 >= 0)
                    if (isPieceAtPosWhite(row + 1, col - 1)) {
                        listOfMoves.emplace_back(startingUci + getUci(row + 1, col - 1), getPieceAt(row, col),
                                                 getPieceAt(row + 1, col - 1), false, false, true, 'q');
                        listOfMoves.emplace_back(startingUci + getUci(row + 1, col - 1), getPieceAt(row, col),
                                                 getPieceAt(row + 1, col - 1), false, false, true, 'b');
                        listOfMoves.emplace_back(startingUci + getUci(row + 1, col - 1), getPieceAt(row, col),
                                                 getPieceAt(row + 1, col - 1), false, false, true, 'r');
                        listOfMoves.emplace_back(startingUci + getUci(row + 1, col - 1), getPieceAt(row, col),
                                                 getPieceAt(row + 1, col - 1), false, false, true, 'n');
                    }

                if (col + 1 < 8)
                    if (isPieceAtPosWhite(row + 1, col + 1)) {
                        listOfMoves.emplace_back(startingUci + getUci(row + 1, col + 1), getPieceAt(row, col),
                                                 getPieceAt(row + 1, col + 1), false, false, true, 'q');
                        listOfMoves.emplace_back(startingUci + getUci(row + 1, col + 1), getPieceAt(row, col),
                                                 getPieceAt(row + 1, col + 1), false, false, true, 'b');
                        listOfMoves.emplace_back(startingUci + getUci(row + 1, col + 1), getPieceAt(row, col),
                                                 getPieceAt(row + 1, col + 1), false, false, true, 'r');
                        listOfMoves.emplace_back(startingUci + getUci(row + 1, col + 1), getPieceAt(row, col),
                                                 getPieceAt(row + 1, col + 1), false, false, true, 'n');
                    }
            }
            break;
        }
        case 'r': {
            int directions[4][2] = {{1,  0},
                                    {-1, 0},
                                    {0,  1},
                                    {0,  -1}};

            for (auto direction: directions) {
                for (int i = 1; i < 8; i++) {
                    int newRow = row + direction[0] * i;
                    int newCol = col + direction[1] * i;

                    if (0 <= newRow && newRow < 8 && 0 <= newCol && newCol < 8) {
                        if (getPieceAt(newRow, newCol) == '.')
                            listOfMoves.emplace_back(startingUci + getUci(newRow, newCol), getPieceAt(row, col),
                                                     getPieceAt(newRow, newCol));
                        else if (isPieceAtPosWhite(newRow, newCol)) {
                            listOfMoves.emplace_back(startingUci + getUci(newRow, newCol), getPieceAt(row, col),
                                                     getPieceAt(newRow, newCol));
                            break;
                        } else {
                            break;
                        }
                    }
                }
            }
            break;
        }
        case 'n': {
            int jumps[8][2] = {{1,  2},
                               {-1, 2},
                               {2,  1},
                               {2,  -1},
                               {1,  -2},
                               {-1, -2},
                               {-2, 1},
                               {-2, -1}};

            for (auto jump: jumps) {
                int newRow = row + jump[0];
                int newCol = col + jump[1];

                if (0 <= newRow && newRow < 8 && 0 <= newCol && newCol < 8) {
                    if (!isPieceAtPosBlack(newRow, newCol)) {
                        listOfMoves.emplace_back(startingUci + getUci(newRow, newCol), getPieceAt(row, col),
                                                 getPieceAt(newRow, newCol));
                    }
                }
            }
            break;
        }
        case 'b': {
            int directions[4][2] = {{1,  1},
                                    {-1, -1},
                                    {-1, 1},
                                    {1,  -1}};

            for (auto direction: directions) {
                for (int i = 1; i < 8; i++) {
                    int newRow = row + direction[0] * i;
                    int newCol = col + direction[1] * i;

                    if (0 <= newRow && newRow < 8 && 0 <= newCol && newCol < 8) {
                        if (getPieceAt(newRow, newCol) == '.')
                            listOfMoves.emplace_back(startingUci + getUci(newRow, newCol), getPieceAt(row, col),
                                                     getPieceAt(newRow, newCol));
                        else if (isPieceAtPosWhite(newRow, newCol)) {
                            listOfMoves.emplace_back(startingUci + getUci(newRow, newCol), getPieceAt(row, col),
                                                     getPieceAt(newRow, newCol));
                            break;
                        } else {
                            break;
                        }
                    }
                }
            }
            break;
        }
        case 'q': {
            int directions[8][2] = {{1,  1},
                                    {-1, -1},
                                    {-1, 1},
                                    {1,  -1},
                                    {1,  0},
                                    {-1, 0},
                                    {0,  1},
                                    {0,  -1}};

            for (auto direction: directions) {
                for (int i = 1; i < 8; i++) {
                    int newRow = row + direction[0] * i;
                    int newCol = col + direction[1] * i;

                    if (0 <= newRow && newRow < 8 && 0 <= newCol && newCol < 8) {
                        if (getPieceAt(newRow, newCol) == '.')
                            listOfMoves.emplace_back(startingUci + getUci(newRow, newCol), getPieceAt(row, col),
                                                     getPieceAt(newRow, newCol));
                        else if (isPieceAtPosWhite(newRow, newCol)) {
                            listOfMoves.emplace_back(startingUci + getUci(newRow, newCol), getPieceAt(row, col),
                                                     getPieceAt(newRow, newCol));
                            break;
                        } else {
                            break;
                        }
                    }
                }
            }
            break;
        }
        case 'k': {
            int jumps[8][2] = {{1,  0},
                               {-1, 0},
                               {0,  1},
                               {0,  -1},
                               {1,  1},
                               {-1, -1},
                               {-1, 1},
                               {1,  -1}};

            for (auto jump: jumps) {
                int newRow = row + jump[0];
                int newCol = col + jump[1];

                if (0 <= newRow && newRow < 8 && 0 <= newCol && newCol < 8) {
                    if (!isPieceAtPosBlack(newRow, newCol)) {
                        listOfMoves.emplace_back(startingUci + getUci(newRow, newCol), getPieceAt(row, col),
                                                 getPieceAt(newRow, newCol));
                    }
                }
            }
            break;
        }
    }

    return listOfMoves;
}

//sequentialValidMoves
std::vector<Move> Board::generateValidMoves() {
    std::string tmpEnpassant = en_passant;

    auto legalMoves = generateLegalMoves();

    std::vector<Move> validMoves;

    auto castleMoves = generateCastlingMoves();

    if (!castleMoves.empty())
        validMoves.insert(validMoves.end(), castleMoves.begin(), castleMoves.end());

    for (auto legalMove: legalMoves) {
        Board copy(*this);
        copy.move(&legalMove);
        copy.turn = static_cast<Color>(!copy.turn);
        if (!copy.checkForCheck())
            validMoves.push_back(legalMove);
        copy.turn = static_cast<Color>(!copy.turn);
        copy.pop();
    }

    en_passant = tmpEnpassant;

    if (validMoves.empty()) {
        isGameOver = true;
        if (checkForCheck()) {
            isCheckMate = true;
        } else {
            isStaleMate = true;
        }
    } else {
        isGameOver = false;
        isStaleMate = false;
        isCheckMate = false;
    }
    return validMoves;
}

//parallelValidMoves
std::vector<Move> Board::generateValidMovesAlternative() {
    std::string tmpEnpassant = en_passant;

    auto legalMoves = generateLegalMoves();

    std::vector<Move> validMoves;

    auto castleMoves = generateCastlingMoves();

    if (!castleMoves.empty())
        validMoves.insert(validMoves.end(), castleMoves.begin(), castleMoves.end());

    auto arraySize = legalMoves.size();
    auto threadCount = 4;
    auto threads = std::vector<std::thread>(threadCount);
    auto threadArraySize = arraySize / threadCount;

    std::vector<std::vector<Move>> results(threadCount);

    for (size_t i = 0; i < threadCount; i++) {
        threads[i] =
                std::thread(
                        [this](size_t threadNumber, size_t iStart, size_t iEnd, std::vector<Move> &legalMoves,
                               std::vector<std::vector<Move>> &validMoves) {
                            for (size_t i = iStart; i < iEnd; i++) {
                                Board newBoard(*this);
                                newBoard.move(&legalMoves[i]);
                                newBoard.turn = static_cast<Color>(!newBoard.turn);
                                if (!newBoard.checkForCheck()) {
                                    validMoves[threadNumber].push_back(legalMoves[i]);
                                }
                                newBoard.turn = static_cast<Color>(!newBoard.turn);
                                newBoard.pop();
                            }
                        },

                        i,
                        threadArraySize * i,
                        threadArraySize * (i + 1) + ((i + 1) != threadCount ? 0 : arraySize % threadCount),
                        std::ref(legalMoves),
                        std::ref(results)
                );
    }

    std::for_each(threads.begin(), threads.end(), [](std::thread &thread) { thread.join(); });
    for (size_t i = 0; i < threadCount; i++) {
        if (!results[i].empty())
            validMoves.insert(validMoves.end(), results[i].begin(), results[i].end());
    }


    en_passant = tmpEnpassant;

    if (validMoves.empty()) {
        isGameOver = true;
        if (checkForCheck()) {
            isCheckMate = true;
        } else {
            isStaleMate = true;
        }
    } else {
        isGameOver = false;
        isStaleMate = false;
        isCheckMate = false;
    }

    return validMoves;
}

std::vector<Move> Board::generateLegalMoves() {
    std::vector<Move> legalMoves;

    for (int row = 0; row < 8; row++) {
        for (int col = 0; col < 8; col++) {
            auto piece = getPieceAt(row, col);
            if (piece == '.')
                continue;

            if ((bool)isupper(piece) != (turn == Color::white)) {
                continue;
            }
            std::vector<Move> result = generatePawnMoves(row, col);
            if (!result.empty())
                legalMoves.insert(legalMoves.end(), result.begin(), result.end());
        }
    }

    return legalMoves;
}

std::vector<Move> Board::generateCastlingMoves() {
    std::vector<Move> castleMoves;
    if (checkForCheck()) {
        return castleMoves;
    }

    if (castle_rights[turn][Castle::king_side]) {
        if (turn == Color::white) {
            auto king = KingSideCastle(whiteKingPos);
            if (!king.empty()) {
                castleMoves.insert(castleMoves.end(), king.begin(), king.end());
            }
        } else {
            auto king = KingSideCastle(blackKingPos);
            if (!king.empty()) {
                castleMoves.insert(castleMoves.end(), king.begin(), king.end());
            }
        }
    }

    if (castle_rights[turn][Castle::queen_side]) {
        if (turn == Color::white) {
            auto king = QueenSideCastle(whiteKingPos);
            if (!king.empty()) {
                castleMoves.insert(castleMoves.end(), king.begin(), king.end());
            }
        } else {
            auto king = QueenSideCastle(blackKingPos);
            if (!king.empty()) {
                castleMoves.insert(castleMoves.end(), king.begin(), king.end());
            }
        }
    }

    return castleMoves;
}

void Board::print_board() {
    for (int i = 0; i < NB_SQ; i++) {
        if (i % 8 == 0) std::cout << '\n';
        std::cout << board[i] << ' ';
    }
    std::cout << '\n';
}

std::string Board::get_board() {

    std::string str;
    for (int i = 0; i < NB_SQ; i++) {
        if (i % 8 == 0)
            str += '\n';
        str += board[i];
    }
    return str;
}

bool Board::checkForCheck() {
    turn = static_cast<Color>(!turn);
    auto enemyMoves = generateLegalMoves();
    turn = static_cast<Color>(!turn);
    for (const auto &enemyMove: enemyMoves) {
        if (enemyMove.takenPawn == ((turn == Color::white) ? 'K' : 'k')) {
            return true;
        }
    }
    return false;

}

bool Board::checkForAttack(const std::string &uci) {
    turn = static_cast<Color>(!turn);
    auto enemyMoves = generateLegalMoves();
    turn = static_cast<Color>(!turn);//

    for (const auto &enemyMove: enemyMoves) {
        if (enemyMove.moveUci.substr(2, 2) == uci) {
            return true;
        }
    }
    return false;
}

std::vector<Move> Board::KingSideCastle(std::string uci) {
    std::vector<Move> list;
    int col = uci[0] - 97;
    int row = 8 - (uci[1] - 48);
    if (getPieceAt(row, col + 1) == '.' & getPieceAt(row, col + 2) == '.') {
        std::string pos1 = getUci(row, col + 1);
        std::string pos2 = getUci(row, col + 2);
        if (!checkForAttack(pos1) && !checkForAttack(pos2)) {
            list.emplace_back(uci + pos2, getPieceUci(uci), getPieceUci(pos2), false, true, false, '0');
        }
    }

    return list;
}

std::vector<Move> Board::QueenSideCastle(std::string uci) {
    std::vector<Move> list;
    int col = uci[0] - 97;
    int row = 8 - (uci[1] - 48);
    if (getPieceAt(row, col - 1) == '.' && getPieceAt(row, col - 2) == '.' && getPieceAt(row, col - 3) == '.') {
        std::string pos1 = getUci(row, col - 1);
        std::string pos2 = getUci(row, col - 2);
        if (!checkForAttack(pos1) && !checkForAttack(pos2)) {
            list.emplace_back(uci + pos2, getPieceUci(uci), getPieceUci(pos2), false, true, false, '0');
        }
    }

    return list;
}

bool Board::move(Move *move) {

    move->castle_rights[Color::white][Castle::king_side] = castle_rights[Color::white][Castle::king_side];
    move->castle_rights[Color::white][Castle::queen_side] = castle_rights[Color::white][Castle::queen_side];
    move->castle_rights[Color::black][Castle::king_side] = castle_rights[Color::black][Castle::king_side];
    move->castle_rights[Color::black][Castle::queen_side] = castle_rights[Color::black][Castle::queen_side];

    setPieceAt(move->endingRow, move->endingCol, move->movingPawn);
    setPieceAt(move->startingRow, move->startingCol, '.');

    if (move->isPromotion) {
        char promotedTo = move->moveUci[4];
        if (turn == Color::white)
            promotedTo = toupper(promotedTo);
        setPieceAt(move->endingRow, move->endingCol, promotedTo);
    }
    move->possibleEnpassant = en_passant;

    if ((move->movingPawn == 'P' || move->movingPawn == 'p') && (abs(move->startingRow - move->endingRow) == 2)) {
        en_passant = getUci((move->startingRow + move->endingRow) / 2, move->startingCol);
    } else {
        en_passant = "-";
    }

    if (move->isEnpassant) {
        move->takenPawn = getPieceAt(move->startingRow, move->endingCol);
        setPieceAt(move->startingRow, move->endingCol, '.');
    }

    if (move->movingPawn == 'K') {
        castle_rights[Color::white][Castle::king_side] = false;
        castle_rights[Color::white][Castle::queen_side] = false;
        whiteKingPos = move->moveUci.substr(2, 2);
    } else if (move->movingPawn == 'k') {
        castle_rights[Color::black][Castle::king_side] = false;
        castle_rights[Color::black][Castle::queen_side] = false;
        blackKingPos = move->moveUci.substr(2, 2);
    }

    if (move->movingPawn == 'R') {
        if (move->startingRow == 7) {
            if (move->startingCol == 0) {
                castle_rights[Color::white][Castle::queen_side] = false;
            } else if (move->startingCol == 7) {
                castle_rights[Color::white][Castle::king_side] = false;
            }
        }
    }

    if (move->movingPawn == 'r') {
        if (move->startingRow == 0) {
            if (move->startingCol == 0) {
                castle_rights[Color::black][Castle::queen_side] = false;
            } else if (move->startingCol == 7) {
                castle_rights[Color::black][Castle::king_side] = false;
            }
        }
    }

    if (move->isCastle) {
        if (move->endingCol - move->startingCol == 2) {
            char oldPiece = getPieceAt(move->endingRow, move->endingCol + 1);
            setPieceAt(move->endingRow, move->endingCol - 1, oldPiece);
            setPieceAt(move->endingRow, move->endingCol + 1, '.');
        } else {
            char oldPiece = getPieceAt(move->endingRow, move->endingCol - 2);
            setPieceAt(move->endingRow, move->endingCol + 1, oldPiece);
            setPieceAt(move->endingRow, move->endingCol - 2, '.');
        }
    }


    moves.push_back(*move);
    turn = static_cast<Color>(!turn);

    return true;
}

bool Board::moveUci(std::string uci) {

    if (uci == "null") {
        isGameOver = true;
        isCheckMate = true;
        surended = true;
        return true;
    }
    auto validMoves = generateLegalMoves();
    auto castleMoves = generateCastlingMoves();

    if (!castleMoves.empty())
        validMoves.insert(validMoves.end(), castleMoves.begin(), castleMoves.end());

    auto move = std::find_if(validMoves.begin(), validMoves.end(),
                             [&](Move const &move) { return move.moveUci == uci; });
    if (move == std::end(validMoves))
        return false;

    move->castle_rights[Color::white][Castle::king_side] = castle_rights[Color::white][Castle::king_side];
    move->castle_rights[Color::white][Castle::queen_side] = castle_rights[Color::white][Castle::queen_side];
    move->castle_rights[Color::black][Castle::king_side] = castle_rights[Color::black][Castle::king_side];
    move->castle_rights[Color::black][Castle::queen_side] = castle_rights[Color::black][Castle::queen_side];

    setPieceAt(move->endingRow, move->endingCol, move->movingPawn);
    setPieceAt(move->startingRow, move->startingCol, '.');

    if (move->isPromotion) {
        char promotedTo = move->moveUci[4];
        if (turn == Color::white)
            promotedTo = toupper(promotedTo);
        setPieceAt(move->endingRow, move->endingCol, promotedTo);
    }
    move->possibleEnpassant = en_passant;

    if ((move->movingPawn == 'P' || move->movingPawn == 'p') && (abs(move->startingRow - move->endingRow) == 2)) {
        en_passant = getUci((move->startingRow + move->endingRow) / 2, move->startingCol);
    } else {
        en_passant = "-";
    }

    if (move->isEnpassant) {
        move->takenPawn = getPieceAt(move->startingRow, move->endingCol);
        setPieceAt(move->startingRow, move->endingCol, '.');
    }

    if (move->movingPawn == 'K') {
        castle_rights[Color::white][Castle::king_side] = false;
        castle_rights[Color::white][Castle::queen_side] = false;
        whiteKingPos = move->moveUci.substr(2, 2);
    } else if (move->movingPawn == 'k') {
        castle_rights[Color::black][Castle::king_side] = false;
        castle_rights[Color::black][Castle::queen_side] = false;
        blackKingPos = move->moveUci.substr(2, 2);
    }

    if (move->movingPawn == 'R') {
        if (move->startingRow == 7) {
            if (move->startingCol == 0) {
                castle_rights[Color::white][Castle::queen_side] = false;
            } else if (move->startingCol == 7) {
                castle_rights[Color::white][Castle::king_side] = false;
            }
        }
    }

    if (move->movingPawn == 'r') {
        if (move->startingRow == 0) {
            if (move->startingCol == 0) {
                castle_rights[Color::black][Castle::queen_side] = false;
            } else if (move->startingCol == 7) {
                castle_rights[Color::black][Castle::king_side] = false;
            }
        }
    }

    if (move->isCastle) {
        if (move->endingCol - move->startingCol == 2) {
            char oldPiece = getPieceAt(move->endingRow, move->endingCol + 1);
            setPieceAt(move->endingRow, move->endingCol - 1, oldPiece);
            setPieceAt(move->endingRow, move->endingCol + 1, '.');
        } else {
            char oldPiece = getPieceAt(move->endingRow, move->endingCol - 2);
            setPieceAt(move->endingRow, move->endingCol + 1, oldPiece);
            setPieceAt(move->endingRow, move->endingCol - 2, '.');
        }
    }


    moves.push_back(*move);
    turn = static_cast<Color>(!turn);

    return true;
}

Move Board::pop() {
    if (moves.empty())
        return {};

    Move move = moves.back();
    moves.pop_back();
    en_passant = move.possibleEnpassant;


    setPieceAt(move.startingRow, move.startingCol, move.movingPawn);
    setPieceAt(move.endingRow, move.endingCol, move.takenPawn);

    if (move.isEnpassant) {
        setPieceAt(move.endingRow, move.endingCol, '.');
        setPieceAt(move.startingRow, move.endingCol, move.takenPawn);
    }

    if (move.movingPawn == 'K') {
        whiteKingPos = move.moveUci.substr(0, 2);
    } else if (move.movingPawn == 'k') {
        blackKingPos = move.moveUci.substr(0, 2);
    }

    if (move.isCastle) {
        if (move.endingCol - move.startingCol == 2) {
            char oldPiece = getPieceAt(move.endingRow, move.endingCol - 1);
            setPieceAt(move.endingRow, move.endingCol + 1, oldPiece);
            setPieceAt(move.endingRow, move.endingCol - 1, '.');
        } else {
            char oldPiece = getPieceAt(move.endingRow, move.endingCol + 1);
            setPieceAt(move.endingRow, move.endingCol - 2, oldPiece);
            setPieceAt(move.endingRow, move.endingCol + 1, '.');
        }
    }

    castle_rights[Color::white][Castle::king_side] = move.castle_rights[Color::white][Castle::king_side];
    castle_rights[Color::white][Castle::queen_side] = move.castle_rights[Color::white][Castle::queen_side];
    castle_rights[Color::black][Castle::king_side] = move.castle_rights[Color::black][Castle::king_side];
    castle_rights[Color::black][Castle::queen_side] = move.castle_rights[Color::black][Castle::queen_side];


    turn = static_cast<Color>(!turn);
    return move;
}

std::string Board::translateBoardToFEN() {
    std::string fen;
    for (int row = 0; row < 8; row++) {
        int empty = 0;
        std::string rankFen;
        for (int col = 0; col < 8; col++) {
            char piece = getPieceAt(row, col);
            if (piece == '.')
                empty++;
            else {
                if (empty != 0)
                    rankFen += std::to_string(empty);

                rankFen += piece;
                empty = 0;
            }
        }
        if (empty != 0) rankFen += std::to_string(empty);
        fen += rankFen;
        // add row separator. If last then add a space
        if (row != 8 - 1) {
            fen += "/";
        } else {
            fen += " ";
        }
    }

    std::string player = (turn == Color::white) ? "w" : "b";
    std::string castle;

    if (castle_rights[Color::white][Castle::king_side])
        castle += "K";
    else
        castle += "-";

    if (castle_rights[Color::white][Castle::queen_side])
        castle += "Q";
    else
        castle += "-";

    if (castle_rights[Color::black][Castle::king_side])
        castle += "k";
    else
        castle += "-";

    if (castle_rights[Color::black][Castle::queen_side])
        castle += "q";
    else
        castle += "-";

    return fen + player + " " + castle + " " + en_passant + " 0 1";
}