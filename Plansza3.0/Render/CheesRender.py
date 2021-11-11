import pygame

from Engine import ChessEngine


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
        self.possibleMovesColor = (123, 255, 123)
        self.engine = ChessEngine.GameEngine()
        self.possibleMoves = []
        self.tile_selected = ()
        self.tile_history = []

        self._whitePlayer = True

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
            self._render_possibleMoves()
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
            if self._whitePlayer:
                _tile_render_position = pygame.math.Vector2(self.tile_selected[0] * self.tile_size,
                                                            (7 - self.tile_selected[1]) * self.tile_size)
            else:
                _tile_render_position = pygame.math.Vector2((7 - self.tile_selected[0]) * self.tile_size,
                                                            self.tile_selected[1] * self.tile_size)
            pygame.draw.rect(self.screen, self.selected_color, (_tile_render_position, self.tile_size_vector))

    def _render_pieces(self):
        if self._whitePlayer:
            for file in range(8):
                for rank in range(8):
                    if self.engine.getBoard()[file][rank] != 0:
                        self.screen.blit(self.piece_sprite[self.engine.getBoard()[file][rank]],
                                         (5 + file * self.tile_size, 5 + (7 - rank) * self.tile_size))
        else:
            for file in range(8):
                for rank in range(8):
                    if self.engine.getBoard()[file][rank] != 0:
                        self.screen.blit(self.piece_sprite[self.engine.getBoard()[file][rank]],
                                         (5 + (7 - file) * self.tile_size, 5 + rank * self.tile_size))

    def _render_buttons(self):
        self.undoButton.render_button()

    def menu_interface_logic(self, mouse_pos):
        if self.undoButton.getActon(mouse_pos):
            self.tile_selected = ()
            self.tile_history = []
            self.possibleMoves = []
            self.engine.undo_move()

    def game_interface_logic(self, mouse_pos):
        if self._whitePlayer:
            new_tile_selection = (mouse_pos[0] // self.tile_size, 7 - (mouse_pos[1] // self.tile_size))
        else:
            new_tile_selection = (7 - (mouse_pos[0] // self.tile_size), mouse_pos[1] // self.tile_size)

        if self.tile_selected == () and self.engine.getBoard()[new_tile_selection[0]][new_tile_selection[1]] == 0:
            return

        if self.tile_selected == new_tile_selection:
            self.tile_selected = ()
            self.tile_history = []
            self.possibleMoves = []
        else:
            self.tile_selected = new_tile_selection
            self.tile_history.append(self.tile_selected)

        if len(self.tile_history) == 1:
            self.showMoves()

        if len(self.tile_history) == 2:
            self.make_move()

    def showMoves(self):
        self.possibleMoves = self.engine.getPossibleMoves(self.tile_history[0])

    def make_move(self):
        move = ChessEngine.Move(self.engine.getBoard(), self.tile_history[0], self.tile_history[1])
        self.engine.move(move)
        self.possibleMoves = []
        self.tile_history = []
        self.tile_selected = ()

    def _render_possibleMoves(self):
        if len(self.possibleMoves) == 0:
            return

        if self._whitePlayer:
            for move in self.possibleMoves:
                _tile_color = self.possibleMovesColor
                _tile_render_position = pygame.math.Vector2(( move[0]) * self.tile_size, (7-move[1]) * self.tile_size)
                pygame.draw.rect(self.screen, _tile_color, (_tile_render_position, self.tile_size_vector))
        else:
            for move in self.possibleMoves:
                _tile_color = self.possibleMovesColor
                _tile_render_position = pygame.math.Vector2((7-move[0]) * self.tile_size, (  move[1]) * self.tile_size)
                pygame.draw.rect(self.screen, _tile_color, (_tile_render_position, self.tile_size_vector))


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
