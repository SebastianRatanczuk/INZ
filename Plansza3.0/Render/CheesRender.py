import pygame

from Engine import ChessEngine


class Render:
    def __init__(self):
        self.tile_size = 110
        self.window_width = self.tile_size * 8 + 300
        self.window_height = self.tile_size * 8
        self.window_title = "Szaszki"
        self.tile_size_vector = pygame.math.Vector2(self.tile_size, self.tile_size)
        self.light_color = (250, 230, 200)
        self.dark_color = (180, 140, 120)
        self.selected_color = (255, 123, 123)
        self.possible_moves_color = (123, 255, 123)
        self.engine = ChessEngine.GameEngine()
        self.possible_moves = []
        self.valid_moves = self.engine.get_valid_moves()
        self.move_made = False
        self.tile_selected = []
        self.tile_history = []

        self.piece_sprite = {
            1: pygame.image.load('Render/resources/pieces/white/pawn.png'),
            2: pygame.image.load('Render/resources/pieces/white/rook.png'),
            3: pygame.image.load('Render/resources/pieces/white/knight.png'),
            4: pygame.image.load('Render/resources/pieces/white/bishop.png'),
            5: pygame.image.load('Render/resources/pieces/white/queen.png'),
            6: pygame.image.load('Render/resources/pieces/white/king.png'),

            11: pygame.image.load('Render/resources/pieces/black/pawn.png'),
            12: pygame.image.load('Render/resources/pieces/black/rook.png'),
            13: pygame.image.load('Render/resources/pieces/black/knight.png'),
            14: pygame.image.load('Render/resources/pieces/black/bishop.png'),
            15: pygame.image.load('Render/resources/pieces/black/queen.png'),
            16: pygame.image.load('Render/resources/pieces/black/king.png'),
        }

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(self.window_title)
        self.undo_button = Button((self.tile_size * 8, 0), (self.tile_size * 2, self.tile_size), self.screen,
                                  self.selected_color)
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
                                                        (7 - self.tile_selected[1]) * self.tile_size)
            # if self.engine.white_turn:
            #     _tile_render_position = pygame.math.Vector2(self.tile_selected[0] * self.tile_size,
            #                                                 (7 - self.tile_selected[1]) * self.tile_size)
            # else:
            #     _tile_render_position = pygame.math.Vector2((7 - self.tile_selected[0]) * self.tile_size,
            #                                                 self.tile_selected[1] * self.tile_size)
            pygame.draw.rect(self.screen, self.selected_color, (_tile_render_position, self.tile_size_vector))

    def _render_pieces(self):

        for file in range(8):
            for rank in range(8):
                if self.engine.get_board()[file][rank] != 0:
                    self.screen.blit(self.piece_sprite[self.engine.main_board[file][rank].pawn_number],
                                     (5 + file * self.tile_size, 5 + (7 - rank) * self.tile_size))
        # if self.engine.white_turn:
        #     for file in range(8):
        #         for rank in range(8):
        #             if self.engine.get_board()[file][rank] != 0:
        #                 self.screen.blit(self.piece_sprite[self.engine.main_board[file][rank].pawn_number],
        #                                  (5 + file * self.tile_size, 5 + (7 - rank) * self.tile_size))
        # else:
        #     for file in range(8):
        #         for rank in range(8):
        #             if self.engine.get_board()[file][rank] != 0:
        #                 self.screen.blit(self.piece_sprite[self.engine.main_board[file][rank].pawn_number],
        #                                  (5 + (7 - file) * self.tile_size, 5 + rank * self.tile_size))

    def _render_buttons(self):
        self.undo_button.render_button()

    def menu_interface_logic(self, mouse_pos):
        if self.undo_button.get_acton(mouse_pos):
            self.undo_move()

    def undo_move(self):
        self.tile_selected = []
        self.tile_history = []
        self.possible_moves = []
        self.engine.undo_move()
        self.valid_moves = self.engine.get_valid_moves()

    def game_interface_logic(self, mouse_pos):

        new_tile_selection = [mouse_pos[0] // self.tile_size, 7 - (mouse_pos[1] // self.tile_size)]
        # if self.engine.white_turn:
        #     new_tile_selection = [mouse_pos[0] // self.tile_size, 7 - (mouse_pos[1] // self.tile_size)]
        # else:
        #     new_tile_selection = [7 - (mouse_pos[0] // self.tile_size), mouse_pos[1] // self.tile_size]

        if self.tile_selected == [] and self.engine.get_board()[new_tile_selection[0]][new_tile_selection[1]] == 0:
            return

        if self.tile_selected == [] and self.engine.white_turn and not self.engine.main_board[new_tile_selection[0]][
            new_tile_selection[1]].is_white:
            return

        if self.tile_selected == [] and not self.engine.white_turn and self.engine.main_board[new_tile_selection[0]][
            new_tile_selection[1]].is_white:
            return

        if self.tile_selected == new_tile_selection:
            self.tile_selected = []
            self.tile_history = []
            self.possible_moves = []
        elif len(self.tile_history) == 1 and self.engine.main_board[new_tile_selection[0]][
            new_tile_selection[1]] != 0 and (
                self.engine.main_board[self.tile_selected[0]][self.tile_selected[1]].is_white ==
                self.engine.main_board[new_tile_selection[0]][new_tile_selection[1]].is_white):
            self.tile_selected = new_tile_selection
            self.tile_history = []
            self.tile_history.append(self.tile_selected)
        else:
            self.tile_selected = new_tile_selection
            self.tile_history.append(self.tile_selected)

        if len(self.tile_history) == 1:
            self.show_moves()

        if len(self.tile_history) == 2:
            self.make_move()

        if self.move_made:
            self.valid_moves = self.engine.get_valid_moves()
            self.move_made = False

    def show_moves(self):
        self.possible_moves = []
        for move in self.valid_moves:
            if move.start_move == self.tile_history[0]:
                self.possible_moves.append(move)

    def make_move(self):
        move = ChessEngine.Move(self.engine.get_board(), self.tile_history[0], self.tile_history[1])
        if move in self.valid_moves:
            self.engine.move(move)
            self.move_made = True
        self.possible_moves = []
        self.tile_history = []
        self.tile_selected = []

    def _render_possible_moves(self):
        if len(self.possible_moves) == 0:
            return

        for move in self.possible_moves:
            _tile_color = self.possible_moves_color
            _tile_render_position = pygame.math.Vector2((move.end_move[0]) * self.tile_size,
                                                        (7 - move.end_move[1]) * self.tile_size)
            pygame.draw.rect(self.screen, _tile_color, (_tile_render_position, self.tile_size_vector))

        # if self.engine.white_turn:
        #     for move in self.possible_moves:
        #         _tile_color = self.possible_moves_color
        #         _tile_render_position = pygame.math.Vector2((move.end_move[0]) * self.tile_size, (7 - move.end_move[1]) * self.tile_size)
        #         pygame.draw.rect(self.screen, _tile_color, (_tile_render_position, self.tile_size_vector))
        # else:
        #     for move in self.possible_moves:
        #         _tile_color = self.possible_moves_color
        #         _tile_render_position = pygame.math.Vector2((7 - move.end_move[0]) * self.tile_size, (move.end_move[1]) * self.tile_size)
        #         pygame.draw.rect(self.screen, _tile_color, (_tile_render_position, self.tile_size_vector))


class Button:
    def __init__(self, pos, size, screen, color):
        self.pos = pos
        self.size = size
        self.screen = screen
        self.color = color

    def render_button(self):
        pygame.draw.rect(self.screen, self.color, (self.pos, self.size))

    def get_acton(self, mouse_pos):
        return self.pos[0] <= mouse_pos[0] <= self.pos[0] + self.size[0] and \
               self.pos[1] <= mouse_pos[1] <= self.pos[1] + self.size[1]
