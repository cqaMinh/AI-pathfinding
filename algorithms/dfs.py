from collections import deque
import pygame
import globals

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def dfs_algorithm(draw, grid, start, end):
    stack = [start]
    visited = {start}
    came_from = {}
    count_state = 0

    while stack:
        yield  # Yield for each loop iteration

        current = stack.pop()

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return

        for neighbor in current.neighbors:
            if neighbor not in visited and not neighbor.is_barrier():
                visited.add(neighbor)
                came_from[neighbor] = current
                stack.append(neighbor)
                neighbor.make_open()
                globals.state["number_of_node_explored"] += 1

        count_state += 1
        draw()
        print("Depth-first search algorithm")
        print(f"Number of nodes explored: {globals.state['number_of_node_explored']} at state  {count_state}") 

        if current != start:
            current.make_closed()


    return