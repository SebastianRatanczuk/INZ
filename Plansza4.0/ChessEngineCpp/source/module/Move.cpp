//
// Created by sebol on 23.12.2021.
//

#include "Move.h"

Move::Move() {}

std::string Move::toString() {
    return moveUci;
}

Move::Move(std::string uci, char movingPawn, char takenPawn, bool isEnpassat,
           bool isCastle, bool isPromotion, char promotedTo) : moveUci(std::move(uci)),
                                                               movingPawn(movingPawn),
                                                               takenPawn(takenPawn),
                                                               isCastle(isCastle),
                                                               isEnpassant(isEnpassat),
                                                               isPromotion(isPromotion),
                                                               promotedTo(promotedTo) {
    startingCol = moveUci[0] - 97;
    startingRow = 8 - (moveUci[1] - 48);
    endingCol = moveUci[2] - 97;
    endingRow = 8 - (moveUci[3] - 48);

    if (isPromotion)
        moveUci = moveUci + promotedTo;
}