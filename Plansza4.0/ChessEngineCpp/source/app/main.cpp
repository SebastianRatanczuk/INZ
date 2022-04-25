
#include "Board.h"
#include "Ai.h"

using namespace std;

int main() {
    Ai ai = Ai("k7/8/8/8/4K3/8/7R/1Q6 w ---- - 1 0", 1);

    Move a = ai.negaAlfABeta();
    std::cout << a.moveUci << std::endl;

    if (a.moveUci != "h2a2") {
        return -1;
    }

    ai = Ai("k7/8/8/8/4K3/8/7R/1Q6 w ---- - 1 0", 2);

    a = ai.negaAlfABeta();
    std::cout << a.moveUci << std::endl;

    if (a.moveUci != "h2a2") {
        return -1;
    }

    ai = Ai("k7/8/8/8/4K3/8/7R/1Q6 w ---- - 1 0", 3);

    a = ai.negaAlfABeta();
    std::cout << a.moveUci << std::endl;

//    if (a.moveUci != "h2a2") {
//        return 1;
//    }
}