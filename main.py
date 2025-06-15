import pygame
import math
from queue import PriorityQueue
from algorithms import astar, dfs, bfs

pygame.init()

WIDTH = 800
GRID_HEIGHT = 500
INSTRUCTION_HEIGHT = 100  # Space for instructions
WIN = pygame.display.set_mode((WIDTH, GRID_HEIGHT + INSTRUCTION_HEIGHT))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False


def make_grid(gap, width, height):
    grid = []
    rows = width // gap
    cols = height // gap
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            spot = Spot(i, j, gap, cols)
            grid[i].append(spot)
    return grid

def draw_grid(win, gap, width, height):
    rows = width // gap
    cols = height // gap
    for i in range(cols):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, height))

def draw_instructions(win, grid_height):
    font = pygame.font.SysFont("consolas", 18)
    instructions = [
        "SPACE: Start A*     P: Pause     R: Continue     B: Undo path     C: Clear",
        "Left Click: Place start/end/barriers     Right Click: Remove start/end/barriers",
    ]

    for i, text in enumerate(instructions):
        rendered = font.render(text, True, BLACK)
        win.blit(rendered, (10, grid_height + 10 + i * 25))


def draw(win, grid, gap, width, height):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, gap, width, height)
    draw_instructions(win, height)
    pygame.display.update()


def get_clicked_pos(pos, gap):
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col


def main(win):
    GAP = 20
    grid = make_grid(GAP, WIDTH, GRID_HEIGHT)

    start = None
    end = None
    algorithm = None  # Generator
    paused = False

    run = True
    while run:
        draw(win, grid, GAP, WIDTH, GRID_HEIGHT)

        if algorithm and not paused:
            try:
                next(algorithm)  # Step-by-step A*
            except StopIteration:
                algorithm = None  # Done

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, GAP)
                if row >= WIDTH // GAP or col >= GRID_HEIGHT // GAP:
                    continue
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                elif spot != start and spot != end:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, GAP)
                if row >= WIDTH // GAP or col >= GRID_HEIGHT // GAP:
                    continue
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end and not algorithm:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    from algorithms import astar  # Ensure import here
                    algorithm = astar.astar_algorithm(lambda: draw(win, grid, ROWS, WIDTH), grid, start, end)

                elif event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(GAP, WIDTH)
                    algorithm = None
                    paused = False

                elif event.key == pygame.K_p:
                    paused = True

                elif event.key == pygame.K_r:
                    paused = False

    pygame.quit()

main(WIN)
