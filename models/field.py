from copy import deepcopy
from random import choice

from pygame import gfxdraw
from pygame.surface import Surface

from config.screen import WIDTH, HEIGHT
from models.theme import Theme
from other import Matrix
from .state import State


def circle(surface, x, y, r, color):
    gfxdraw.aacircle(surface, x, y, r, color)
    gfxdraw.filled_circle(surface, x, y, r, color)


class Field(Matrix):
    def __init__(self, screen: Surface, theme: Theme):
        self.screen = screen
        
        self._width = 4
        self._height = 4
        
        self.shuffle_moves = 2 ** 15
        
        if WIDTH / HEIGHT != self._width / self._height:
            raise ValueError("the ratio of the height and width of the field must be equal "
                             "to the ratio of the height and width of the window")
        
        self._victory_text = "Victory!"
        
        self.cell_edge = int(WIDTH / self._width)
        
        self.theme = theme
        self.border_radius = 10
        self.padding = 5
        
        self.state = State.game
        
        self.original_body = [[
            (x + y * self._width + 1) % (self._width * self._height)
            for x in range(self._width)
        ] for y in range(self._height)]
        
        self.random_body = deepcopy(self.original_body)
        
        super(Field, self).__init__(self.random_body)
    
    def shuffle(self):
        for _ in range(self.shuffle_moves):
            x0, y0 = self.void_cell
            x, y = choice(self.get_movable())
            self[x, y], self[x0, y0] = self[x0, y0], self[x, y]
    
    def handle_touch(self, x: int, y: int):
        field_x = int(x / WIDTH * self._width)
        field_y = int(y / HEIGHT * self._height)
        
        if self.movable(field_x, field_y):
            x0, y0 = self.void_cell
            self[field_x, field_y], self[x0, y0] = self[x0, y0], self[field_x, field_y]
    
    def check_win(self):
        if self.random_body == self.original_body:
            self.state = State.win
    
    @property
    def void_cell(self):
        return self.index(0)
    
    def movable(self, x, y):
        x0, y0 = self.void_cell
        if abs(x0 - x) + abs(y0 - y) == 1:
            return True
        else:
            return False
    
    def get_movable(self):
        x0, y0 = self.void_cell
        
        return list(filter(self.check_cell, [(x0 - 1, y0), (x0 + 1, y0), (x0, y0 - 1), (x0, y0 + 1)]))
    
    def check_cell(self, coordinates: tuple[int, int]):
        x, y = coordinates
        if 0 <= x <= self._width - 1 and 0 <= y <= self._height - 1:
            return True
        else:
            return False
    
    def draw_victory(self):
        self.screen.fill(self.theme.background)
        text = self.theme.font.render(self._victory_text, True, self.theme.text)

        self.screen.blit(text, ((self.screen.get_width() - text.get_rect().width) // 2,
                                (self.screen.get_height() - text.get_rect().height) // 2))
    
    def draw(self):
        
        self.screen.fill(self.theme.background)
        
        for x in range(self._width):
            for y in range(self._height):
                
                if self[x, y] == 0:
                    continue
                
                circle(self.screen, self.cell_edge * x + self.cell_edge // 2,
                       self.cell_edge * y + self.cell_edge // 2, self.cell_edge // 2 - self.padding,
                       self.theme.border)
                
                circle(self.screen, self.cell_edge * x + self.cell_edge // 2,
                       self.cell_edge * y + self.cell_edge // 2,
                       self.cell_edge // 2 - self.padding - self.border_radius, self.theme.cell)
                
                number = self.theme.font.render(str(self[x, y]), True, self.theme.text)
                number_offset_x = (self.cell_edge - number.get_rect().width) // 2
                number_offset_y = (self.cell_edge - number.get_rect().height) // 2
                
                self.screen.blit(number, (x * self.cell_edge + number_offset_x,
                                          y * self.cell_edge + number_offset_y))
