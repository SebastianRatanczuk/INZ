import time

import chess.engine
import pygame
from PIL import Image, ImageFilter
from more_itertools import run_length

import ChessEngine
from ChessAI import bestMove
from ChessEngine import Move

ar = []


class Render:
    def __init__(self) -> None:
        self.white_ai = chess.engine.SimpleEngine.popen_uci("resources/troutFish/troutFish.exe")
        self.black_ai = chess.engine.SimpleEngine.popen_uci("resources/troutFish/troutFish.exe")
        self.white_ai.configure(options={"Skill Level": 1})
        self.black_ai.configure(options={"Skill Level": 1})

        self.vs_AI = False
        self.tile_size = 110
        self.tile_size_vector = pygame.math.Vector2(self.tile_size, self.tile_size)
        self.window_width = self.tile_size * 8 + 50
        self.window_height = self.tile_size * 8 + 50
        self.window_title = "Szaszki"
        self.light_color = (250, 230, 200)
        self.dark_color = (180, 140, 120)
        self.selected_color = (255, 123, 123)
        self.possible_moves_color = (123, 255, 123)
        self.engine = ChessEngine.GameEngine()
        self.valid_moves = self.engine.get_valid_moves()
        self.move_made = False
        self.possible_moves = []
        self.tile_selected = []
        self.tile_history = []

        self.player_one = False
        self.player_two = False

        self.piece_sprite = {
            1: pygame.image.load('resources/pieces/white/pawn.png'),
            2: pygame.image.load('resources/pieces/white/rook.png'),
            3: pygame.image.load('resources/pieces/white/knight.png'),
            4: pygame.image.load('resources/pieces/white/bishop.png'),
            5: pygame.image.load('resources/pieces/white/queen.png'),
            6: pygame.image.load('resources/pieces/white/king.png'),

            11: pygame.image.load('resources/pieces/black/pawn.png'),
            12: pygame.image.load('resources/pieces/black/rook.png'),
            13: pygame.image.load('resources/pieces/black/knight.png'),
            14: pygame.image.load('resources/pieces/black/bishop.png'),
            15: pygame.image.load('resources/pieces/black/queen.png'),
            16: pygame.image.load('resources/pieces/black/king.png'),
        }

        self.game_state = 1
        self.game_mode_background = None
        self.game_end_background = None
        self.menu_sprite = {
            "pvp": pygame.image.load('resources/pvp.png'),
            "ai": pygame.image.load('resources/ai.png'),
        }

    def __del__(self):
        self.white_ai.close()
        self.black_ai.close()

    def run(self) -> None:
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption(self.window_title)
        pygame.time.Clock().tick(60)
        self.font = pygame.font.SysFont('Times New Roman Font', 30)
        self.end_font = pygame.font.SysFont('Times New Roman Font', 40)
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self._main_game_loop()

    def _main_game_loop(self) -> None:
        self.running = True
        while self.running:
            self.human_turn = (self.engine.white_turn and self.player_one) or \
                              (not self.engine.white_turn and self.player_two)

            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.running = False

            if self.game_state == 1:
                self._game_mode_selection()
            elif self.game_state == 2:
                self._game_window()
            elif self.game_state == 3:
                self._end_game_screen()

            pygame.display.update()

        pygame.quit()

    def _game_mode_selection(self):

        for event in self.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_menu_logic()

        if self.game_mode_background is None:
            image = Image.open('resources/background.png')
            mode = image.mode
            size = image.size
            data = image.tobytes()
            self.game_mode_background = pygame.image.fromstring(data, size, mode)
            image.close()

        self.screen.blit(self.game_mode_background, (0, 0))
        self.screen.blit(self.menu_sprite['pvp'], (self.window_width * 1 / 3 - 256, self.window_height / 2 - 128))
        self.screen.blit(self.menu_sprite['ai'], (self.window_width * 2 / 3, self.window_height / 2 - 128))

    def _game_window(self):

        for event in self.events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.human_turn:
                self.mouse_logic()
            elif event.type == pygame.KEYDOWN and self.human_turn:
                if event.key == pygame.K_u:
                    self.undo()

        self.game_end_background = None
        self.screen.fill((0, 0, 0))
        self._render_chess_board()
        self._render_possible_moves()
        self._render_pieces()
        pygame.display.update()
        if self.engine.is_game_over():
            self.game_state += 1
        if not self.human_turn:
            if not self.engine.is_game_over():
                # if self.engine.white_turn:
                #     result = self.white_ai.play(self.engine.get_chess_board(), chess.engine.Limit(time=0.1))
                # else:
                #     result = self.black_ai.play(self.engine.get_chess_board(), chess.engine.Limit(time=0.1))
                #
                # move = result.move
                # file1 = move.from_square % 8
                # rank1 = move.from_square // 8
                # file2 = move.to_square % 8
                # rank2 = move.to_square // 8
                # newMove = Move(self.engine.main_board, [file1, rank1], [file2, rank2])
                # self.engine.move(newMove)
                # self.move_made = True
                start = time.time()
                move = bestMove(self.engine)
                stop = time.time()
                ar.append(stop - start)
                if len(ar) > 0:
                    print(sum(ar) / len(ar))
                self.engine.move(move)
                self.valid_moves = self.engine.get_valid_moves()
                self.move_made = True

    def _end_game_screen(self):
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:
                    self.undo()
                    self.game_state -= 1

        if self.game_end_background is None:
            pygame.image.save(self.screen, 'resources/ScreenShot.png')
            image = Image.open('resources/ScreenShot.png').filter(ImageFilter.GaussianBlur(radius=6))
            mode = image.mode
            size = image.size
            data = image.tobytes()
            self.game_end_background = pygame.image.fromstring(data, size, mode)
            image.close()

        self.screen.blit(self.game_end_background, (0, 0))
        self._render_game_over()

    def mouse_logic(self) -> None:
        mouse_pos = pygame.mouse.get_pos()

        if 25 < mouse_pos[0] < 900 and 25 < mouse_pos[1] < 900:
            new_tile = [(mouse_pos[0] - 25) // self.tile_size, 7 - ((mouse_pos[1] - 25) // self.tile_size)]
        else:
            return

        if not self.tile_selected:
            if self.engine.get_piece(new_tile) is None:
                return

            if self.engine.white_turn and not self.engine.get_piece(new_tile).is_white:
                return

            if not self.engine.white_turn and self.engine.get_piece(new_tile).is_white:
                return

        if self.tile_selected == new_tile:
            self.tile_selected = []
            self.tile_history = []
            self.possible_moves = []

        elif len(self.tile_history) == 1 and self.engine.get_piece(new_tile) is not None and (
                self.engine.get_piece(self.tile_selected).is_white ==
                self.engine.get_piece(new_tile).is_white):
            self.tile_selected = new_tile
            self.tile_history = []
            self.tile_history.append(self.tile_selected)
        else:
            self.tile_selected = new_tile
            self.tile_history.append(self.tile_selected)

        if len(self.tile_history) == 1:
            self.show_moves()

        if len(self.tile_history) == 2:
            self.move()

        if self.move_made:
            self.valid_moves = self.engine.get_valid_moves()
            self.move_made = False

    def mouse_menu_logic(self):
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] < self.window_width / 2:
            self.game_state += 1
        else:
            self.game_state += 1

    def _render_game_over(self):
        if self.engine.is_game_over():
            if self.engine.game_status().winner is not None:
                text = "Wygrał " + str("Czarny" if self.engine.game_status().winner else "Biały")
            else:
                text = "Pat"

            textsurface = self.end_font.render(text, True, (255, 0, 122))
            self.screen.blit(textsurface, (255, 255))

    def _render_chess_board(self) -> None:
        for file in range(8):
            for rank in range(8):
                _is_white = (file + rank) % 2 == 0
                _tile_color = self.light_color if _is_white else self.dark_color
                _tile_render_position = pygame.math.Vector2(file * self.tile_size + 25, rank * self.tile_size + 25)
                pygame.draw.rect(self.screen, _tile_color, (_tile_render_position, self.tile_size_vector))

        for i in range(8):
            textsurface = self.font.render(chr(97 + i), True, (255, 255, 255))
            self.screen.blit(textsurface, (75 + i * 110, self.window_height - 22))
            self.screen.blit(textsurface, (75 + i * 110, 2))
            textsurface = self.font.render(str(i + 1), True, (255, 255, 255))
            self.screen.blit(textsurface, (5, 900 - (60 + i * 110)))
            self.screen.blit(textsurface, (910, 900 - (60 + i * 110)))

        if self.tile_selected:
            _tile_render_position = pygame.math.Vector2(
                self.tile_selected[0] * self.tile_size + 25,
                (7 - self.tile_selected[1]) * self.tile_size + 25
            )
            pygame.draw.rect(self.screen, self.selected_color, (_tile_render_position, self.tile_size_vector))

    def _render_pieces(self) -> None:
        for file in range(8):
            for rank in range(8):
                if self.engine.get_piece([file, rank]) is not None:
                    self.screen.blit(
                        self.piece_sprite[self.engine.get_piece([file, rank]).pawn_number],
                        (30 + file * self.tile_size, 25 + (7 - rank) * self.tile_size)
                    )

    def _render_possible_moves(self) -> None:
        if len(self.possible_moves) == 0:
            return

        for move in self.possible_moves:
            file = move.end_move[0]
            rank = move.end_move[1]

            _tile_render_position = pygame.math.Vector2(file * self.tile_size + 25, (7 - rank) * self.tile_size + 25)
            pygame.draw.rect(self.screen, self.possible_moves_color, (_tile_render_position, self.tile_size_vector))

    def show_moves(self) -> None:
        self.possible_moves = []
        for move in self.valid_moves:
            if move.start_move == self.tile_history[0]:
                self.possible_moves.append(move)

    def move(self):
        move = Move(self.engine.main_board, self.tile_history[0], self.tile_history[1])
        for valid_move in self.valid_moves:
            if move == valid_move:
                self.engine.move(valid_move)
                self.move_made = True
                break

        self.possible_moves = []
        self.tile_history = []
        self.tile_selected = []

        fen = self.get_board_fen()
        print(fen)
        # x = szaszki.PyChess(fen)
        # print(x.getBoard())

    def undo(self):
        self.tile_selected = []
        self.tile_history = []
        self.possible_moves = []
        self.engine.undo_move()
        if self.player_one and not self.player_two:
            self.engine.undo_move()
        self.valid_moves = self.engine.get_valid_moves()

    def get_main_board(self):

        x = self.engine.main_board.reshape(8, 8)
        x = list(zip(*x[::-1]))
        x = list(zip(*x[::-1]))
        x = list(zip(*x[::-1]))

        return x

    def get_board_fen(self):
        color = 'w' if self.engine.white_turn else 'b'
        castlng = self.engine.getCastleRights()
        return '/'.join(map(convert_rank, self.get_main_board())) + ' ' + color + ' ' + castlng + ' - 0 1'  # ' w KQkq - 0 1'


def convert_cell(value):
    if value is None:
        return None
    else:
        return value.symbol


def convert_rank(rank):
    return ''.join(
        value * count if value else str(count)
        for value, count in run_length.encode(map(convert_cell, rank))
    )
