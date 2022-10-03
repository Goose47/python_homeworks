import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.width = cell_size * self.life.cols
        self.height = cell_size * self.life.rows
        self.screen_size = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.grid = self.life.curr_generation

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        for row_index, row in enumerate(self.grid):
            for col_index, el in enumerate(row):
                if el:
                    color = pygame.Color('green')
                else:
                    color = pygame.Color('white')

                pygame.draw.rect(
                    self.screen,
                    color,
                    (col_index * self.cell_size, row_index * self.cell_size, self.cell_size, self.cell_size)
                )

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        running = True
        pause = False

        while running and self.life.is_changing and not self.life.is_max_generations_exceeded:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYUP and event.key == K_p:
                    pause = not pause
                elif pause and event.type == MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    row = y // self.cell_size
                    col = x // self.cell_size
                    self.grid[row][col] = (self.grid[row][col] + 1) % 2
            self.draw_grid()
            self.draw_lines()

            if not pause:
                self.life.step()

            self.grid = self.life.curr_generation
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


if __name__ == '__main__':
    game = GameOfLife((15, 15))
    gui = GUI(game)

    gui.run()
