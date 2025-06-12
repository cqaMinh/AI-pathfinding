
# algorithms/bfs.py
from collections import deque
import pygame

def bfs_algorithms(draw, grid, start, end):
    queue = deque([start])
    visited = {start}
    came_from = {}

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = queue.popleft()

        if current == end:
            while current in came_from:
                current.make_path()
                current = came_from[current]
            end.make_end()
            draw()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited and not neighbor.is_barrier():
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)
                neighbor.make_open()

        if current != start:
            current.make_closed()

        draw()

    return False
