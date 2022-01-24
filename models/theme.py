from dataclasses import dataclass

from pygame.font import Font


@dataclass
class Theme:
    background: tuple[int, int, int]
    cell: tuple[int, int, int]
    border: tuple[int, int, int]
    text: tuple[int, int, int]
    font: Font
