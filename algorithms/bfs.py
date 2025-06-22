
# algorithms/bfs.py
from collections import deque
import pygame
import globals

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def bfs_algorithm(draw, grid, start, end):
    number_of_node_explored = 0
    queue = [start]
    visited = {start}
    came_from = {}

    while queue:
        count_state = 0
        yield  # Yield for each loop iteration

        current = queue.pop(0)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return

        for neighbor in current.neighbors:
            if neighbor not in visited and not neighbor.is_barrier():
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)
                neighbor.make_open()
                globals.state["number_of_node_explored"] += 1

        count_state += 1
        draw()
        print("Breadth-first search algorithm")
        print(f"Number of nodes explored: {globals.state['number_of_node_explored']} at state  {count_state}") 

        if current != start:
            current.make_closed()

    return
