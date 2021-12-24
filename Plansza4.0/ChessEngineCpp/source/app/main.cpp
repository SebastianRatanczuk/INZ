
#include "Board.h"
#include "Ai.h"

using namespace std;

int main() {
    Ai ai = Ai("4k3/8/6p1/8/8/1P6/8/4K3 b - - 0 1", 3);
    ai.negaAlfABeta();
    return 0;
}