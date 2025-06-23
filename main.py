import pygame
import math
from queue import PriorityQueue
from algorithms import astar, dfs, bfs, ucs, bi_direction_search, iddfs, idastar, beamsearch 
  
import globals 

pygame.init()

WIDTH =500
GRID_HEIGHT = 500
INSTRUCTION_HEIGHT = 250  # Space for instructions
WIN = pygame.display.set_mode((WIDTH, GRID_HEIGHT + INSTRUCTION_HEIGHT))
pygame.display.set_caption("Path Finding Algorithm visualization")



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
        "1. Uniform_Cost Search (UCS): Press 1",
        "2. Depth-First Search (DFS): Press 2",
        "3. Breadth-First Search (BFS): Press 3",
        "4. A* Search: Press 4",
        "5. Bi-Directional Search: Press 5",
        "6. Iterative Deepening DFS: Press 6",
        "7. Iterative Deepening A*: Press 7",
        "8. Beam Search: Press 8",      
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
'''
def main(win):
    GAP = 20
    HEIGHT = WIDTH
    grid = make_grid(GAP, WIDTH, GRID_HEIGHT)

    algorithm = None  # Generator

    run = True
    time_cost = 0
    start, end = load_map_from_file("map.txt", grid, GAP)
    
    for row in grid:
        for spot in row:
            spot.update_neighbors(grid)
        
    while run:
        draw(win, grid, GAP, WIDTH, GRID_HEIGHT)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end and not algorithm:
                    start_time = pygame.time.get_ticks()
                    algorithm = astar.astar_algorithm(lambda: draw(win, grid, GAP, WIDTH, HEIGHT), grid, start, end)

        if algorithm:
            try:
                next(algorithm)
            except StopIteration:
                algorithm = None
                end_time = pygame.time.get_ticks()
                time_cost = end_time - start_time
                print(f"A* algorithm finished. Time cost: {time_cost} ms")

    pygame.quit()
'''
def main(win):
    GAP = 20
    WIDTH = 500
    GRID_HEIGHT = 500
    HEIGHT = WIDTH

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
                next(algorithm)  # Step-by-step
            except StopIteration:
                algorithm = None  # Done
                end_time = pygame.time.get_ticks()
                total_time = end_time - start_time
                print(f"Total time cost: {total_time} ms")

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
                print("Key name:", pygame.key.name(event.key))


                if event.key == pygame.K_SPACE and start and end and not algorithm:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                if start and end and not algorithm:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                                     pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, 
                                     pygame.K_KP_1, pygame.K_KP_2, pygame.K_KP_3, pygame.K_KP_4,
                                     pygame.K_KP_5, pygame.K_KP_6, pygame.K_KP_7, pygame.K_KP_8]:
                        start_time = pygame.time.get_ticks()

                        if event.key == pygame.K_1 or event.key == pygame.K_KP_1:
                            algorithm = ucs.ucs_algorithm(lambda: draw(win, grid, GRID_HEIGHT // GAP, WIDTH, HEIGHT), grid, start, end)
                        elif event.key == pygame.K_2 or event.key == pygame.K_KP_2:
                            algorithm = dfs.dfs_algorithm(lambda: draw(win, grid, GRID_HEIGHT // GAP, WIDTH, HEIGHT), grid, start, end)
                        elif event.key == pygame.K_3 or event.key == pygame.K_KP_3:
                            algorithm = bfs.bfs_algorithm(lambda: draw(win, grid, GRID_HEIGHT // GAP, WIDTH, HEIGHT), grid, start, end)
                        elif event.key == pygame.K_4 or event.key == pygame.K_KP_4:
                            algorithm = astar.astar_algorithm(lambda: draw(win, grid, GRID_HEIGHT // GAP, WIDTH, HEIGHT), grid, start, end)
                        elif event.key == pygame.K_5 or event.key == pygame.K_KP_5:
                            algorithm = bi_direction_search.bi_directional_search_algorithm(lambda: draw(win, grid, GRID_HEIGHT // GAP, WIDTH, HEIGHT), grid, start, end)
                        elif event.key == pygame.K_6 or event.key == pygame.K_KP_6:
                            algorithm = iddfs.iddfs_algorithm(lambda: draw(win, grid, GRID_HEIGHT // GAP, WIDTH, HEIGHT), grid, start, end)
                        elif event.key == pygame.K_7 or event.key == pygame.K_KP_7:
                            algorithm = idastar.ida_algorithm(lambda: draw(win, grid, GRID_HEIGHT // GAP, WIDTH, HEIGHT), grid, start, end)
                        elif event.key == pygame.K_8 or event.key == pygame.K_KP_8:
                            algorithm = beamsearch.beam_search_algorithm(lambda: draw(win, grid, GRID_HEIGHT // GAP, WIDTH, HEIGHT), grid, start, end)

                        end_time = pygame.time.get_ticks()
                        time_cost = end_time - start_time
                        

                elif event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(GAP, WIDTH, GRID_HEIGHT)
                    algorithm = None
                    paused = False

                elif event.key == pygame.K_p:
                    paused = True

                elif event.key == pygame.K_r:
                    paused = False

    pygame.quit()

main(WIN)
