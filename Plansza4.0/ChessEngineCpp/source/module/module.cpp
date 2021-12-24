#include <algorithm>
#include <cctype>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <string>

#include "Board.h"
#include "Move.h"
#include "Ai.h"


namespace py = pybind11;


PYBIND11_MODULE(szaszki, module) {
    module.doc() = "TES_TEST";

    py::enum_<Color>(module, "PyColor")
            .value("WHITE", Color::white)
            .value("BLACK", Color::black)
            .export_values();

    py::class_<Move>(module, "PyMove")
            .def(py::init())
            .def(py::init<std::string, char, char, bool, bool, bool, char>())
            .def_readonly("uci", &Move::moveUci)
            .def_readonly("movingPawn", &Move::movingPawn)
            .def_readonly("takenPawn", &Move::takenPawn)
            .def_readonly("startingRow", &Move::startingRow)
            .def_readonly("startingCol", &Move::startingCol)
            .def_readonly("endingRow", &Move::endingRow)
            .def_readonly("endingCol", &Move::endingCol)
            .def_readonly("castle_rights", &Move::castle_rights);

    py::class_<Board>(module, "PyChess")
            .def(py::init())
            .def(py::init<std::string>())
            .def("getBoard", &Board::get_board)
            .def("move", &Board::moveUci)
            .def("pop_move", &Board::pop)
            .def("piece_at", &Board::getPieceAt)
            .def("piece_at", &Board::getPieceUci)
            .def("valid_moves", &Board::generateValidMoves)
            .def("generate_fen", &Board::translateBoardToFEN)
            .def_readonly("turn", &Board::turn)
            .def_readonly("move_stack", &Board::moves)
            .def_readonly("en_passant", &Board::en_passant)
            .def_readonly("white_king_pos", &Board::whiteKingPos)
            .def_readonly("black_king_pos", &Board::blackKingPos)
            .def_readonly("castle_rights", &Board::castle_rights)
            .def_readonly("is_game_over", &Board::isGameOver)
            .def_readonly("is_check_mate", &Board::isCheckMate)
            .def_readonly("is_stale_mate", &Board::isStaleMate)
            .def_readonly("surended", &Board::surended);

    py::class_<Ai>(module, "PyAI")
            .def(py::init())
            .def(py::init<std::string, int>())
            .def(py::init<Board, int>())
            .def("get_best_move", &Ai::negaAlfABeta);
}