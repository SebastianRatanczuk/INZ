
#include "Board.h"
#include "Ai.h"

using namespace std;

int main() {
    Ai ai = Ai("k7/8/8/8/4K3/8/7R/1Q6 w ---- - 0 1", 1);

    Move a = ai.negaAlfABeta();
    cout << a.moveUci;
}