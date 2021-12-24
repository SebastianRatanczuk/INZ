//
// Created by sebol on 23.12.2021.
//

#ifndef SZASZKI_MOVE_H
#define SZASZKI_MOVE_H

#define NB_SQ 64     // number of squares
#define NB_CASTLE 2  // number of castle types
#define NB_COLOR 2   // number of colors

#include <string>

class Move {
public:
    std::string moveUci = "null";
    char movingPawn;
    char takenPawn;
    bool isEnpassant;
    bool isCastle;
    bool isPromotion;
    char promotedTo;
    int startingRow;
    int startingCol;
    int endingRow;
    int endingCol;
    std::string possibleEnpassant;
    bool castle_rights[NB_COLOR][NB_CASTLE]{};

    Move();

    Move(std::string uci, char movingPawn, char takenPawn, bool isEnpassat = false,
         bool isCastle = false, bool isPromotion = false, char promotedTo = '0');

    std::string toString();


};


#endif //SZASZKI_MOVE_H
