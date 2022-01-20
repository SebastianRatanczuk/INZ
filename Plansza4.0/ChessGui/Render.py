import random
import time
from multiprocessing import Process, Queue

import pygame
from PIL import Image, ImageFilter

from resources import szaszki

ai_time = []


class Render:
    def __init__(self):

        self.tile_size = 110
        self.tile_size_vector = pygame.math.Vector2(self.tile_size, self.tile_size)
        self.window_width = self.tile_size * 10 + 50
        self.window_height = self.tile_size * 8 + 50
        self.window_title = "Szaszki"
        self.light_color = (250, 230, 200)
        self.dark_color = (180, 140, 120)
        self.selected_color = (255, 123, 123)
        self.possible_moves_color = (123, 255, 123)
        self.board = szaszki.PyChess("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        # self.board = szaszki.PyChess("r3k2r/8/8/8/8/8/8/4K3 w ---- - 0 1")
        # self.board = szaszki.PyChess("4kR2/8/8/8/8/8/8/R3K3 b ---- - 1 0")
        # self.board = szaszki.PyChess("rnbq2nr/pppp1kpp/8/8/1b3Q2/4P3/PPPP1PPP/RNB1KBNR b KQ-- - 0 1")
        self.depth = 4
        self.tile_history = ""
        self.tile_selected = ""
        self.pawn_promotion = ""
        self.promotion_request = False
        self.legal_moves = []

        self.piece_sprite = {
            'P': pygame.image.load('resources/pieces/white/pawn.png'),
            'R': pygame.image.load('resources/pieces/white/rook.png'),
            'N': pygame.image.load('resources/pieces/white/knight.png'),
            'B': pygame.image.load('resources/pieces/white/bishop.png'),
            'Q': pygame.image.load('resources/pieces/white/queen.png'),
            'K': pygame.image.load('resources/pieces/white/king.png'),

            'p': pygame.image.load('resources/pieces/black/pawn.png'),
            'r': pygame.image.load('resources/pieces/black/rook.png'),
            'n': pygame.image.load('resources/pieces/black/knight.png'),
            'b': pygame.image.load('resources/pieces/black/bishop.png'),
            'q': pygame.image.load('resources/pieces/black/queen.png'),
            'k': pygame.image.load('resources/pieces/black/king.png'),
        }

        self.game_state = 1
        self.game_mode_background = None
        self.game_end_background = None
        self.menu_sprite = {
            "pvp": pygame.image.load('resources/pvp.png'),
            "ai": pygame.image.load('resources/ai.png'),
        }

        self.player_one = True
        self.player_two = False
        self.thinking = False
        self.queue = None
        self.ai_process = None

    def __del__(self):
        pass

    def run(self):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont('Times New Roman Font', 30)
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(self.window_title)
        self._main_game_loop()

    def _main_game_loop(self):
        self.running = True
        while self.running:
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.human_turn = (not self.board.turn.value and self.player_one) or (self.board.turn.value and self.player_two)

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_logic()
            elif event.type == pygame.KEYDOWN and self.human_turn:
                if event.key == pygame.K_u:
                    self.undo_move()

        self.screen.fill((0, 0, 0))
        self._render_chess_board()
        self._render_possible_moves()
        self._render_pieces()
        self._render_other()
        self.game_end_background = None
        pygame.display.update()
        if self.board.is_game_over:
            self.game_state += 1

        self.board.valid_moves()
        if not self.human_turn:
            if not self.board.is_game_over:
                if not self.thinking:
                    self.ai_Move()
                else:
                    if not self.ai_process.is_alive():
                        self.ai_do_move()

        pygame.display.update()

    def _end_game_screen(self):
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:
                    self.undo_move()
                    self.game_state -= 1

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        print(sum(ai_time) / len(ai_time))

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

    def _render_chess_board(self):
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

    def _render_pieces(self):
        for file in range(8):
            for rank in range(8):
                if self.board.piece_at(rank, file) != '.':
                    self.screen.blit(
                        self.piece_sprite[self.board.piece_at(rank, file)],
                        (30 + file * self.tile_size, 25 + rank * self.tile_size)
                    )

    def _render_possible_moves(self):
        for move in self.legal_moves:
            file = move.endingCol
            rank = move.endingRow
            _tile_render_position = pygame.math.Vector2(file * self.tile_size + 25, (rank) * self.tile_size + 25)
            pygame.draw.rect(self.screen, self.possible_moves_color, (_tile_render_position, self.tile_size_vector))
        for move in self.legal_moves:
            file = move.startingCol
            rank = move.startingRow
            _tile_render_position = pygame.math.Vector2(file * self.tile_size + 25, (rank) * self.tile_size + 25)
            pygame.draw.rect(self.screen, self.selected_color, (_tile_render_position, self.tile_size_vector))
            break

    def _render_other(self):
        _tile_render_position = pygame.math.Vector2(930, 0)
        pygame.draw.rect(self.screen, (122, 122, 122), (_tile_render_position, (250, self.window_height)))

    def mouse_menu_logic(self):
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] < self.window_width / 2:
            self.player_one = True
            self.player_two = True
        else:
            k = random.randint(0, 1)
            if k == 0:
                self.player_one = False
                self.player_two = True
            else:
                self.player_one = True
                self.player_two = False
        self.game_state += 1

    def mouse_logic(self):
        mouse_pos = pygame.mouse.get_pos()

        if mouse_pos[0] < 25 or mouse_pos[1] < 25:
            return
        if mouse_pos[0] > 900 or mouse_pos[1] > 900:
            return

        new_tile_selection = chr((mouse_pos[0] - 25) // self.tile_size + 97) + str(
            7 - ((mouse_pos[1] - 25) // self.tile_size) + 1)

        legal_moves = list(self.board.valid_moves())

        self.legal_moves = list(filter(lambda move: str(move.uci).startswith(new_tile_selection), legal_moves))

        if len(self.tile_history) == 0:
            piece = self.board.piece_at(new_tile_selection)
            if piece == ".":
                self.tile_selected = ""
                self.tile_history = ""
                self.legal_moves = []
                return

            if piece.isupper() == self.board.turn.value:
                self.tile_selected = ""
                self.tile_history = ""
                self.legal_moves = []
                return

        if self.tile_selected == new_tile_selection:
            self.tile_selected = ""
            self.tile_history = ""
            self.legal_moves = []
        else:
            self.tile_selected = new_tile_selection
            self.tile_history = self.tile_history + new_tile_selection

        if len(self.tile_history) == 4 and not self.thinking:
            self.move()
            self.tile_history = ""
            self.tile_selected = ""

        if len(self.tile_history) > 4:
            self.tile_history = ""
            self.tile_selected = ""

    def mouse_promotion_logic(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.promotion_request:
            if mouse_pos[0] > 930:
                if 25 < mouse_pos[1] < 25 + 1 * self.tile_size:
                    self.pawn_promotion = "q"
                if 25 + 1 * self.tile_size < mouse_pos[1] < 25 + 2 * self.tile_size:
                    self.pawn_promotion = "b"
                if 25 + 2 * self.tile_size < mouse_pos[1] < 25 + 3 * self.tile_size:
                    self.pawn_promotion = "r"
                if 25 + 3 * self.tile_size < mouse_pos[1] < 25 + 5 * self.tile_size:
                    self.pawn_promotion = "n"

            self.promotion_request = False

    def _render_game_over(self):
        if self.board.is_stale_mate:
            text = "Pat"
        else:
            text = "Wygrał " + str('Biały' if self.board.turn.value else "Czarny")

        textsurface = self.font.render(text, True, (255, 0, 122))
        self.screen.blit(textsurface, (255, 255))

    def move(self):
        move = self.tile_history
        piece = self.board.piece_at(move[0:2])
        if piece != ".":
            if piece == "P":
                if move[1] == "7" and move[3] == "8":
                    item = self.getPromotion()
                    if item == "":
                        return
                    move = (self.tile_history + item)

            if piece == "p":
                if move[1] == "2" and move[3] == "1":
                    item = self.getPromotion()
                    if item == "":
                        return
                    move = (self.tile_history + item)
                    self.pawn_promotion = ""

        valid_moves = self.board.valid_moves()
        if any(valid_move.uci == move for valid_move in valid_moves):
            self.board.move(move)
        self.board.valid_moves()

    def undo_move(self):
        if len(self.board.move_stack) == 0:
            return
        self.board.pop_move()
        if not self.player_two or not self.player_one:
            self.board.pop_move()

        self.promotion_request = False
        self.legal_moves = []
        self.board.valid_moves()

    def getPromotion(self):
        self.promotion_request = True
        self.pawn_promotion = ""
        if self.promotion_request:
            while self.promotion_request:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.mouse_promotion_logic()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_u:
                            self.undo_move()
                self.screen.blit(
                    self.piece_sprite['q'],
                    (55 + 8 * self.tile_size, 25 + 0 * self.tile_size)
                )
                self.screen.blit(
                    self.piece_sprite['b'],
                    (55 + 8 * self.tile_size, 25 + 1 * self.tile_size)
                )
                self.screen.blit(
                    self.piece_sprite['r'],
                    (55 + 8 * self.tile_size, 25 + 2 * self.tile_size)
                )
                self.screen.blit(
                    self.piece_sprite['n'],
                    (55 + 8 * self.tile_size, 25 + 3 * self.tile_size)
                )
                pygame.display.update()
        return self.pawn_promotion

    def ai_Move(self):
        self.thinking = True
        self.queue = Queue()

        self.ai_process = Process(target=ai_Wrapper, args=(self.board.generate_fen(), self.depth, self.queue, ai_time))
        self.ai_process.start()

    def ai_do_move(self):
        ai_move = self.queue.get()
        self.board.move(ai_move[0])

        if not self.board.surended:
            self.board.valid_moves()

        print(self.board.generate_fen())
        self.thinking = False

        ai_time.append(ai_move[1])


def ai_Wrapper(board, depth, queue, ai_time):
    start = time.time()
    ai = szaszki.PyAI(board, depth)
    ai_move = ai.get_best_move()
    stop = time.time()
    if len(ai_time) > 0:
        print(sum(ai_time) / len(ai_time))
    print(ai_move.uci)
    queue.put([ai_move.uci, stop - start])
