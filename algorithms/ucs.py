from collections import deque
import pygame
import globals

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def ucs_algorithm(draw, grid, start, end):
    from queue import PriorityQueue

    count = 0
    count_state = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0

    open_set_hash = {start}

    while not open_set.empty():
        yield  # Yield for each loop iteration

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return
        count_state += 1
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            globals.state["number_of_node_explored"] += 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((g_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()
        print("Uniform-cost search algorithm")
        print(f"Number of nodes explored: {globals.state['number_of_node_explored']} at state  {count_state}") 

    return