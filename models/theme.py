from dataclasses import dataclass

import pygame.font


@dataclass
class Theme:
    background: tuple[int, int, int]
    cell: tuple[int, int, int]
    border: tuple[int, int, int]
    text: tuple[int, int, int]
    font: pygame.font.Font
