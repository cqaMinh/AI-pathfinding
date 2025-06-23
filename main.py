import pygame
import math
from queue import PriorityQueue
from algorithms import astar, dfs, bfs, ucs, bi_direction_search, iddfs, idastar, beamsearch 
  
import globals 

pygame.init()

WIDTH = 800
HEIGHT = 500
INSTRUCTION_HEIGHT = 270  # Space for instructions
WIN = pygame.display.set_mode((WIDTH, HEIGHT + INSTRUCTION_HEIGHT))
pygame.display.set_caption("Path Finding Visualizer")



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
		rows = len(grid)
		cols = len(grid[0])
		if self.row < rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])
		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
			self.neighbors.append(grid[self.row - 1][self.col])
		if self.col < cols - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])
		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
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

def draw_instructions(win, HEIGHT):
    font = pygame.font.SysFont("consolas", 18)
    instructions = [
        "Press 1: Uniform_Cost Search (UCS)",
        "Press 2: Depth-First Search (DFS)",
        "Press 3: Breadth-First Search (BFS)",
        "Press 4: A* Search",
        "Press 5: Bi-Directional Search",
        "Press 6: Iterative Deepening DFS",
        "Press 7: Iterative Deepening A*",
        "Press 8: Beam Search", 
        "",
        "SPACE: Pause/Resume     C: Clear",
        "Left Click: Place start/end/barriers",
		"Right Click: Remove start/end/barriers",  
    ]

    for i, text in enumerate(instructions):
        rendered = font.render(text, True, BLACK)
        win.blit(rendered, (10, HEIGHT + 10 + i * 20))

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

import os

def load_map_from_file(filename, grid, gap):
    try:
        path = os.path.join("maps", filename)
        with open(path, 'r') as file:
            lines = file.readlines()
            start = None
            end = None
            for i, line in enumerate(lines):
                for j, char in enumerate(line.strip()):
                    if i < len(grid) and j < len(grid[0]):
                        spot = grid[j][i]
                        if char == 'x':
                            spot.make_barrier()
                        elif char == 's':
                            spot.make_start()
                            start = spot
                        elif char == 'e':
                            spot.make_end()
                            end = spot
                        else:
                            spot.reset()
            return start, end
    except Exception as e:
        print(f"Lỗi khi tải bản đồ: {e}")
        return None, None

def main(win):
	GAP = 20
	ROWS = WIDTH // GAP
	COLS = HEIGHT // GAP

	grid = make_grid(GAP, WIDTH, HEIGHT)
	start = None
	end = None
	algorithm = None
	paused = False

	run = True
	start_time = None

	algo_mapping = {
		pygame.K_1: ucs.ucs_algorithm,
		pygame.K_2: dfs.dfs_algorithm,
		pygame.K_3: bfs.bfs_algorithm,
		pygame.K_4: astar.astar_algorithm,
		pygame.K_5: bi_direction_search.bi_directional_search_algorithm,
		pygame.K_6: iddfs.iddfs_algorithm,
		pygame.K_7: idastar.ida_algorithm,
		pygame.K_8: beamsearch.beam_search_algorithm,
		pygame.K_KP_1: ucs.ucs_algorithm,
		pygame.K_KP_2: dfs.dfs_algorithm,
		pygame.K_KP_3: bfs.bfs_algorithm,
		pygame.K_KP_4: astar.astar_algorithm,
		pygame.K_KP_5: bi_direction_search.bi_directional_search_algorithm,
		pygame.K_KP_6: iddfs.iddfs_algorithm,
		pygame.K_KP_7: idastar.ida_algorithm,
		pygame.K_KP_8: beamsearch.beam_search_algorithm,
	}

	while run:
		draw(win, grid, GAP, WIDTH, HEIGHT)

		if algorithm and not paused:
			try:
				next(algorithm)
			except StopIteration:
				algorithm = None
				end_time = pygame.time.get_ticks()
				total_time = end_time - start_time
				print(f"Total time cost: {total_time} ms")

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]:  # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, GAP)
				if row >= ROWS or col >= COLS:
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
				if row >= ROWS or col >= COLS:
					continue
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				key = event.key
				print("Key name:", pygame.key.name(key))

				# Start algorithm with 1–8 keys
				if key in algo_mapping and start and end and not algorithm:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)
					start_time = pygame.time.get_ticks()
					algorithm = algo_mapping[key](lambda: draw(win, grid, GAP, WIDTH, HEIGHT), grid, start, end)
					paused = False

				# Pause/resume
				elif key == pygame.K_SPACE and algorithm:
					paused = not paused

				# Clear grid
				elif key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(GAP, WIDTH, HEIGHT)
					algorithm = None
					paused = False

	pygame.quit()

main(WIN)
