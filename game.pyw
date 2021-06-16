import pygame

from config.screen import SIZE, FPS
from models import Field, Theme, State


def main():
    pygame.init()
    pygame.font.init()

    saros_font = pygame.font.Font('./static/fonts/Saros-Regular.ttf', 72)
    theme = Theme(
        background=(207, 240, 158),
        cell=(168, 219, 168),
        border=(121, 189, 154),
        text=(59, 134, 134),
        font=saros_font
    )

    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()
    
    screen.fill(theme.background)
    pygame.display.set_caption("Tag Game")
    
    field = Field(screen, theme)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if field.state == State.game:
                    field.handle_touch(*event.pos)
                elif field.state == State.win:
                    field.shuffle()
                    field.state = State.game
        
        if field.state == State.win:
            field.draw_victory()
        else:
            field.draw()
        
        field.check_win()
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    

if __name__ == '__main__':
    main()
