import chess
import chess.engine
import pygame


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
        self.board = chess.Board()
        self.tile_history = ""
        self.tile_selected = ""
        self.pawn_promotion = ""
        self.promotion_request = False
        self.legal_moves = []
        self.engine = chess.engine.SimpleEngine.popen_uci("resources/troutFish/troutFish.exe")

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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_logic()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_u:
                        self.undo_move()

            self.screen.fill((0, 0, 0))
            self._render_chess_board()
            self._render_possible_moves()
            self._render_pieces()
            self._render_other()

            if self.board.is_game_over():
                self._render_game_over()

            pygame.display.update()
        pygame.quit()

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
                if self.board.piece_at(file + rank * 8) is not None:
                    self.screen.blit(
                        self.piece_sprite[self.board.piece_at(file + rank * 8).symbol()],
                        (30 + file * self.tile_size, 25 + (7 - rank) * self.tile_size)
                    )

    def _render_possible_moves(self):
        for move in self.legal_moves:
            file = move.to_square % 8
            rank = move.to_square // 8
            _tile_render_position = pygame.math.Vector2(file * self.tile_size + 25, (7 - rank) * self.tile_size + 25)
            pygame.draw.rect(self.screen, self.possible_moves_color, (_tile_render_position, self.tile_size_vector))
        for move in self.legal_moves:
            file = move.from_square % 8
            rank = move.from_square // 8
            _tile_render_position = pygame.math.Vector2(file * self.tile_size + 25, (7 - rank) * self.tile_size + 25)
            pygame.draw.rect(self.screen, self.selected_color, (_tile_render_position, self.tile_size_vector))
            break

    def _render_other(self):
        _tile_render_position = pygame.math.Vector2(930, 0)
        pygame.draw.rect(self.screen, (122, 122, 122), (_tile_render_position, (250, self.window_height)))

    def mouse_logic(self):
        mouse_pos = pygame.mouse.get_pos()

        if mouse_pos[0] < 25 or mouse_pos[1] < 25:
            return
        if mouse_pos[0] > 900 or mouse_pos[1] > 900:
            return

        new_tile_selection = chr((mouse_pos[0] - 25) // self.tile_size + 97) + str(
            7 - ((mouse_pos[1] - 25) // self.tile_size) + 1)

        legal_moves = list(self.board.legal_moves)
        self.legal_moves = list(filter(lambda move: str(move).startswith(new_tile_selection), legal_moves))

        if len(self.tile_history) == 0:
            if self.board.piece_at(
                    (mouse_pos[0] - 25) // self.tile_size + 8 * (7 - (mouse_pos[1] - 25) // self.tile_size)) is None:
                self.tile_selected = ""
                self.tile_history = ""
                self.legal_moves = []
                return

            if self.board.color_at((mouse_pos[0] - 25) // self.tile_size + 8 * (
                    7 - (mouse_pos[1] - 25) // self.tile_size)) != self.board.turn:
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

        if len(self.tile_history) == 4:
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
                    self.pawn_promotion = "r"

            self.promotion_request = False

    def move(self):
        move = chess.Move.from_uci(self.tile_history)

        if self.board.piece_at(move.from_square) is not None:
            if self.board.piece_at(move.from_square).symbol() == "P":
                if move.from_square // 8 == 6 and move.to_square // 8 == 7:
                    item = self.getPromotion()
                    if item == "":
                        return
                    move = chess.Move.from_uci(self.tile_history + item)

            if self.board.piece_at(move.from_square).symbol() == "p":
                if move.from_square // 8 == 1 and move.to_square // 8 == 0:
                    item = self.getPromotion()
                    if item == "":
                        return
                    move = chess.Move.from_uci(self.tile_history + item)
                    self.pawn_promotion = ""

        if move in self.board.legal_moves:
            self.board.push(move)

        if not self.board.is_game_over():
            result = self.engine.play(self.board, chess.engine.Limit(time=0.1))
            self.board.push(result.move)

    def undo_move(self):
        if len(self.board.move_stack) == 0:
            return
        self.board.pop()
        self.promotion_request = False
        self.legal_moves = []

    def _render_game_over(self):
        if self.board.outcome().termination.value == 1:
            text = "Wygrał " + str('Biały' if self.board.outcome().winner else "Czarny")
        else:
            text = "Pat"
        textsurface = self.font.render(text, True, (255, 0, 122))
        self.screen.blit(textsurface, (255, 255))

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
