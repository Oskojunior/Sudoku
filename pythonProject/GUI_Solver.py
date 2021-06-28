import pygame
import time

pygame.font.init()


class Grid:
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    def __init__(self, rows, cols, width, height, window):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.window = window
        self.squares = [[Square(self.board[i][j], i, j, width, height) for i in range(rows)] for j in range(cols)]

    def draw(self):
        space = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thickness = 3
            else:
                thickness = 1
            pygame.draw.line(self.window, (255, 0, 0), (0, i * space), (self.width, i * space), thickness)
            pygame.draw.line(self.window, (255, 0, 0), (i * space, 0), (i * space, self.height), thickness)

        for i in range(self.rows):
            for j in range(self.cols):
                self.squares[i][j].draw(self.window)


class Square:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.temp = value
        self.selected = False

    def draw(self, window):
        font = pygame.font.SysFont("TimesNewRoman", 40)
        space = self.width / 9
        x = self.col * space
        y = self.row * space
        if self.value != 0:
            text = font.render(str(self.temp), True, (128, 128, 128))
            window.blit(text, (x + 5, y + 5))
        elif not (self.value == 0):
            text = font.render(str(self.value), True, (0, 0, 0))
            window.blit(text, (x + (space / 2 - text.get_width() / 2), y + (space / 2 - text.get_height() / 2)))


def main():
    window = pygame.display.set_mode((500, 600))
    pygame.display.set_caption("Sudoku")
    grid = Grid(9, 9, 500, 600, window)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        grid.draw()
        pygame.display.update()


main()
