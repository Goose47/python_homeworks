import curses

from life import GameOfLife
from ui import UI
from time import sleep


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.border('|', '|', '-', '-', '+', '+', '+', '+')

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j] == 1:
                    screen.addstr("*")
                else:
                    screen.addstr(" ")

    def run(self) -> None:
        screen = curses.initscr()
        self.draw_borders(screen)
        curses.curs_set(1)
        self.draw_grid(screen)
        screen.refresh()
        while (self.life.is_changing and
               not self.life.is_max_generations_exceeded):
            self.life.step()
            self.draw_grid(screen)
            screen.refresh()
            sleep(0.5)
        curses.endwin()
