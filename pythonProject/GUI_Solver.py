import pygame
import time
pygame.font.init()


class Grid:
    grid = [
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
        self.cubes = [[Cube(self.grid[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.update_model()
        self.selected = None
        self.window = window

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def draw(self):
        # Draw Grid Lines
        space = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.window, (0,0,0), (0, i*space), (self.width, i*space), thick)
            pygame.draw.line(self.window, (0, 0, 0), (i * space, 0), (i * space, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.window)

    def solve_sudoku(self):
        self.update_model()
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(self.window, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve_sudoku():
                    return True

                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.window, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, window):
        fnt = pygame.font.SysFont("Times New Roman", 40)

        space = self.width / 9
        x = self.col * space
        y = self.row * space

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128,128,128))
            window.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            window.blit(text, (x + (space/2 - text.get_width()/2), y + (space/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(window, (255,0,0), (x,y, space ,space), 3)

    def draw_change(self, window, correct=True):
        fnt = pygame.font.SysFont("Times New Roman", 40)

        space = self.width / 9
        x = self.col * space
        y = self.row * space

        pygame.draw.rect(window, (255, 255, 255), (x, y, space, space), 0)

        text = fnt.render(str(self.value), 1, (0, 0, 0))
        window.blit(text, (x + (space / 2 - text.get_width() / 2), y + (space / 2 - text.get_height() / 2)))
        if correct:
            pygame.draw.rect(window, (0, 255, 0), (x, y, space, space), 3)
        else:
            pygame.draw.rect(window, (255, 0, 0), (x, y, space, space), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def find_empty(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                return i, j

    return None


def valid(grid, num, location):
    # Check row
    for i in range(len(grid[0])):
        if grid[location[0]][i] == num and location[1] != i:
            return False

    # Check column
    for i in range(len(grid)):
        if grid[i][location[1]] == num and location[0] != i:
            return False

    # Check box
    box_x = location[1] // 3
    box_y = location[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if grid[i][j] == num and (i,j) != location:
                return False

    return True


def show_changes(window, grid, time):
    window.fill((255, 255, 255))
    # Draw time
    fnt = pygame.font.SysFont("Times New Roman", 40)
    text = fnt.render("Time: " + format_time(time), 1, (0, 0, 0))
    window.blit(text, (540 - 160, 560))
    # Draw grid and grid
    grid.draw()


def format_time(secs):
    sec = secs % 60
    minute = secs // 60
    play = " " + str(minute) + ":" + str(sec)
    return play


def main():
    window = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku")
    grid = Grid(9, 9, 540, 540, window)
    run = True
    start = time.time()
    while run:

        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    grid.solve_sudoku()

        show_changes(window, grid, play_time)
        pygame.display.update()


main()
pygame.quit()