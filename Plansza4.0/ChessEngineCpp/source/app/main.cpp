
#include "Board.h"
#include "Ai.h"

using namespace std;

int main() {
    Ai ai = Ai("4kR2/8/8/8/8/8/8/R3K3 b ---- - 1 0", 1);

    Move a = ai.negaAlfABeta();
    cout << a.moveUci;
}