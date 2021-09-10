import pygame

import ChessEngine


class Render:
    def __init__(self):

        self.window_width = 880 + 300
        self.window_height = 880
        self.window_title = "Szaszki"

        self.tile_size = 110
        self.tile_size_vector = pygame.math.Vector2(self.tile_size, self.tile_size)

        self.light_color = (250, 230, 200)
        self.dark_color = (180, 140, 120)
        self.selected_color = (255, 123, 123)
        self.engine = ChessEngine.GameEngine()
        self.tile_selected = ()
        self.tile_history = []

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

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(self.window_title)
        self.undoButton = Button((880, 0), (220, 110), self.screen, self.selected_color)
        self._main_game_loop()

    def _main_game_loop(self):
        self.running = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_logic()

            self.screen.fill((0, 0, 0))
            self._render_chess_board()
            self._render_pieces()
            self._render_buttons()

            pygame.display.update()
        pygame.quit()

    def mouse_logic(self):
        mouse_pos = pygame.mouse.get_pos()

        if mouse_pos[0] >= self.tile_size * 8:
            self.menu_interface_logic(mouse_pos)
            return

        self.game_interface_logic(mouse_pos)

    def _render_chess_board(self):
        for file in range(8):
            for rank in range(8):
                _is_white = (file + rank) % 2 == 0
                _tile_color = self.light_color if _is_white else self.dark_color
                _tile_render_position = pygame.math.Vector2(rank * self.tile_size, file * self.tile_size)
                pygame.draw.rect(self.screen, _tile_color, (_tile_render_position, self.tile_size_vector))

        if self.tile_selected:
            _tile_render_position = pygame.math.Vector2(self.tile_selected[0] * self.tile_size,
                                                        self.tile_selected[1] * self.tile_size)
            pygame.draw.rect(self.screen, self.selected_color, (_tile_render_position, self.tile_size_vector))

    def _render_pieces(self):
        for file in range(8):
            for rank in range(8):
                if self.engine.main_board[file][rank] != 0:
                    self.screen.blit(self.piece_sprite[self.engine.main_board[file][rank]],
                                     (5 + file * self.tile_size, 5 + rank * self.tile_size))

    def _render_buttons(self):
        self.undoButton.render_button()

    def menu_interface_logic(self, mouse_pos):
        if self.undoButton.getActon(mouse_pos):
            self.engine.undo_move()

    def game_interface_logic(self, mouse_pos):
        new_tile_selection = (mouse_pos[0] // self.tile_size, mouse_pos[1] // self.tile_size)
        if self.tile_selected == () and self.engine.main_board[new_tile_selection[0]][new_tile_selection[1]] == 0:
            return

        if self.tile_selected == new_tile_selection:
            self.tile_selected = ()
            self.tile_history = []
        else:
            self.tile_selected = new_tile_selection
            self.tile_history.append(self.tile_selected)

        if len(self.tile_history) == 2:
            self.make_move()

    def make_move(self):
        move = ChessEngine.Move(self.engine.main_board, self.tile_history[0], self.tile_history[1])
        self.engine.move(move)
        self.tile_history = []
        self.tile_selected = ()


class Button:
    def __init__(self, pos, size, screen, color):
        self.pos = pos
        self.size = size
        self.screen = screen
        self.color = color

    def render_button(self):
        pygame.draw.rect(self.screen, self.color, (self.pos, self.size))

    def getActon(self, mouse_pos):
        return self.pos[0] <= mouse_pos[0] <= self.pos[0] + self.size[0] and \
               self.pos[1] <= mouse_pos[1] <= self.pos[1] + self.size[1]
