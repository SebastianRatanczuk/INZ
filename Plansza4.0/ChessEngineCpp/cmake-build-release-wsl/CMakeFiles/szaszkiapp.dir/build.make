# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /mnt/c/Users/sebol/Desktop/INZ/Plansza4.0/ChessEngineCpp

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /mnt/c/Users/sebol/Desktop/INZ/Plansza4.0/ChessEngineCpp/cmake-build-release-wsl

# Include any dependencies generated for this target.
include CMakeFiles/szaszkiapp.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/szaszkiapp.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/szaszkiapp.dir/flags.make

CMakeFiles/szaszkiapp.dir/source/app/main.cpp.o: CMakeFiles/szaszkiapp.dir/flags.make
CMakeFiles/szaszkiapp.dir/source/app/main.cpp.o: ../source/app/main.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/mnt/c/Users/sebol/Desktop/INZ/Plansza4.0/ChessEngineCpp/cmake-build-release-wsl/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/szaszkiapp.dir/source/app/main.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/szaszkiapp.dir/source/app/main.cpp.o -c /mnt/c/Users/sebol/Desktop/INZ/Plansza4.0/ChessEngineCpp/source/app/main.cpp

CMakeFiles/szaszkiapp.dir/source/app/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/szaszkiapp.dir/source/app/main.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /mnt/c/Users/sebol/Desktop/INZ/Plansza4.0/ChessEngineCpp/source/app/main.cpp > CMakeFiles/szaszkiapp.dir/source/app/main.cpp.i

CMakeFiles/szaszkiapp.dir/source/app/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/szaszkiapp.dir/source/app/main.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /mnt/c/Users/sebol/Desktop/INZ/Plansza4.0/ChessEngineCpp/source/app/main.cpp -o CMakeFiles/szaszkiapp.dir/source/app/main.cpp.s

CMakeFiles/szaszkiapp.dir/source/module/Board.cpp.o: CMakeFiles/szaszkiapp.dir/flags.make
CMakeFiles/szaszkiapp.dir/source/module/Board.cpp.o: ../source/module/Board.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/mnt/c/Users/sebol/Desktop/INZ/Plansza4.0/ChessEngineCpp/cmake-build-release-wsl/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object CMakeFiles/szaszkiapp.dir/source/module/Board.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/szaszkiapp.dir/source/module/Board.cpp.o -c /mnt/c/Users/sebol/Desktop/INZ/Plansza4.0/ChessEngineCpp/source/module/Board.cpp

CMakeFiles/szaszkiapp.dir/source/module/Board.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/szaszkiapp.dir/source/module/Board.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /mnt/c/Users/sebol/Desktop/INZ/Plansza4.0/ChessEngineCpp/source/module/Board.cpp > CMakeFiles/szaszkiapp.dir/source/module/Board.cpp.i

CMakeFiles/szaszkiapp.dir/source/module/Board.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/szaszkiapp.dir/source/module/Board.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /mnt/c/Users/sebol/Desktop/INZ/Plansza4.0/ChessEngineCpp/source/module/Board.cpp -o CMakeFiles/szaszkiapp.dir/source/module/Board.cpp.s

CMakeFiles/szaszkiapp.dir/source/module/Move.cpp.o: CMakeFiles/szaszkiapp.dir/flags.make
CMakeFiles/szaszkiapp.dir/source/module/Move.cpp.o: ../source/module/Move.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/mnt/c/Users/sebol/Desktop/INZ/Plansza4.0/ChessEngineCpp/cmake-build-release-wsl/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building CXX object CMakeFiles/szaszkiapp.dir/source/module/Move.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/szaszkiapp.dir/source/module/Move.cpp.o -c /mnt/c/Users/sebol/Desktop/INZ/Plansza4.0/ChessEngineCpp/source/module/Move.cpp

CMakeFiles/szaszkiapp.dir/source/module/Move.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/szaszkiapp.dir/source/module/Move.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /mnt/c/Users/sebol/Desktop/INZ/Plansza4.0/ChessEngineCpp/source/module/Move.cpp > CMakeFiles/szaszkiapp.dir/source/module/Move.cpp.i

CMakeFiles/szaszkiapp.dir/source/module/Move.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/szaszkiapp.dir/source/module/Move.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /mnt/c/Users/sebol/Desktop/INZ/Plansza4.0/ChessEngineCpp/source/module/Move.cpp -o CMakeFiles/szaszkiapp.dir/source/module/Move.cpp.s

CMakeFiles/szaszkiapp.dir/source/module/Ai.cpp.o: CMakeFiles/szaszkiapp.dir/flags.make
CMakeFiles/szaszkiapp.dir/source/module/Ai.cpp.o: ../source/module/Ai.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/mnt/c/Users/sebol/Desktop/INZ/Plansza4.0/ChessEngineCpp/cmake-build-release-wsl/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Building CXX object CMakeFiles/szaszkiapp.dir/source/module/Ai.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/szaszkiapp.dir/source/module/Ai.cpp.o -c /mnt/c/Users/sebol/Desktop/INZ/Plansza4.0/ChessEngineCpp/source/module/Ai.cpp

CMakeFiles/szaszkiapp.dir/source/module/Ai.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/szaszkiapp.dir/source/module/Ai.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /mnt/c/Users/sebol/Desktop/INZ/Plansza4.0/ChessEngineCpp/source/module/Ai.cpp > CMakeFiles/szaszkiapp.dir/source/module/Ai.cpp.i

CMakeFiles/szaszkiapp.dir/source/module/Ai.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/szaszkiapp.dir/source/module/Ai.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /mnt/c/Users/sebol/Desktop/INZ/Plansza4.0/ChessEngineCpp/source/module/Ai.cpp -o CMakeFiles/szaszkiapp.dir/source/module/Ai.cpp.s

# Object files for target szaszkiapp
szaszkiapp_OBJECTS = \
"CMakeFiles/szaszkiapp.dir/source/app/main.cpp.o" \
"CMakeFiles/szaszkiapp.dir/source/module/Board.cpp.o" \
"CMakeFiles/szaszkiapp.dir/source/module/Move.cpp.o" \
"CMakeFiles/szaszkiapp.dir/source/module/Ai.cpp.o"

# External object files for target szaszkiapp
szaszkiapp_EXTERNAL_OBJECTS =

szaszkiapp: CMakeFiles/szaszkiapp.dir/source/app/main.cpp.o
szaszkiapp: CMakeFiles/szaszkiapp.dir/source/module/Board.cpp.o
szaszkiapp: CMakeFiles/szaszkiapp.dir/source/module/Move.cpp.o
szaszkiapp: CMakeFiles/szaszkiapp.dir/source/module/Ai.cpp.o
szaszkiapp: CMakeFiles/szaszkiapp.dir/build.make
szaszkiapp: /usr/lib/x86_64-linux-gnu/libpython3.8.so
szaszkiapp: CMakeFiles/szaszkiapp.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/mnt/c/Users/sebol/Desktop/INZ/Plansza4.0/ChessEngineCpp/cmake-build-release-wsl/CMakeFiles --progress-num=$(CMAKE_PROGRESS_5) "Linking CXX executable szaszkiapp"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/szaszkiapp.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/szaszkiapp.dir/build: szaszkiapp

.PHONY : CMakeFiles/szaszkiapp.dir/build

CMakeFiles/szaszkiapp.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/szaszkiapp.dir/cmake_clean.cmake
.PHONY : CMakeFiles/szaszkiapp.dir/clean

CMakeFiles/szaszkiapp.dir/depend:
	cd /mnt/c/Users/sebol/Desktop/INZ/Plansza4.0/ChessEngineCpp/cmake-build-release-wsl && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /mnt/c/Users/sebol/Desktop/INZ/Plansza4.0/ChessEngineCpp /mnt/c/Users/sebol/Desktop/INZ/Plansza4.0/ChessEngineCpp /mnt/c/Users/sebol/Desktop/INZ/Plansza4.0/ChessEngineCpp/cmake-build-release-wsl /mnt/c/Users/sebol/Desktop/INZ/Plansza4.0/ChessEngineCpp/cmake-build-release-wsl /mnt/c/Users/sebol/Desktop/INZ/Plansza4.0/ChessEngineCpp/cmake-build-release-wsl/CMakeFiles/szaszkiapp.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/szaszkiapp.dir/depend
