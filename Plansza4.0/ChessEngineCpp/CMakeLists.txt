cmake_minimum_required(VERSION 3.16)
project(ChessEngineCpp)
set(CMAKE_CXX_STANDARD 14)

set(APP_SOURCE "${PROJECT_SOURCE_DIR}/source/app")
set(MODULE_SOURCE "${PROJECT_SOURCE_DIR}/source/module")
set(EXTERNALS "${PROJECT_SOURCE_DIR}/externals")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pthread")

# pybind11
add_subdirectory(${EXTERNALS}/pybind11)

# module
pybind11_add_module(
        szaszki
        source/module/module.cpp
        source/module/Board.cpp
        source/module/Board.h
        source/module/Move.cpp
        source/module/Move.h
        source/module/Ai.cpp
        source/module/Ai.h
)

target_include_directories(
        szaszki
        PRIVATE ${MODULE_SOURCE}
)

# app
add_executable(
        szaszkiapp
        source/app/main.cpp
        source/module/Board.cpp
        source/module/Board.h
        source/module/Move.cpp
        source/module/Move.h
        source/module/Ai.cpp
        source/module/Ai.h)

target_include_directories(
        szaszkiapp
        PRIVATE ${APP_SOURCE}
        PRIVATE ${MODULE_SOURCE}
)

target_link_libraries(
        szaszkiapp
        PRIVATE pybind11::embed
)