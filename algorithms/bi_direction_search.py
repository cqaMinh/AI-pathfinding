from collections import deque
import pygame
import globals

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def bi_directional_search_algorithm(draw, grid, start, end):
    from queue import Queue

    start_queue = Queue()
    end_queue = Queue()
    start_queue.put(start)
    end_queue.put(end)

    start_visited = {start}
    end_visited = {end}
    came_from_start = {}
    came_from_end = {}
    count_state = 0

    while not start_queue.empty() and not end_queue.empty():
        yield  # Yield for each loop iteration

        # Expand from the start side
        current_start = start_queue.get()
        if current_start in end_visited:
            reconstruct_path(came_from_start, current_start, draw)
            reconstruct_path(came_from_end, current_start, draw)
            end.make_end()
            return

        for neighbor in current_start.neighbors:
            if neighbor not in start_visited and not neighbor.is_barrier():
                start_visited.add(neighbor)
                came_from_start[neighbor] = current_start
                start_queue.put(neighbor)
                neighbor.make_open()
                globals.state["number_of_node_explored"] += 1

        # Expand from the end side
        current_end = end_queue.get()
        if current_end in start_visited:
            reconstruct_path(came_from_end, current_end, draw)
            reconstruct_path(came_from_start, current_end, draw)
            end.make_end()
            return

        for neighbor in current_end.neighbors:
            if neighbor not in end_visited and not neighbor.is_barrier():
                end_visited.add(neighbor)
                came_from_end[neighbor] = current_end
                end_queue.put(neighbor)
                neighbor.make_open()
                globals.state["number_of_node_explored"] += 1

        count_state += 1
        draw()

        if current_start != start:
            current_start.make_closed()
        if current_end != end:
            current_end.make_closed()

    print("Bi-directional search algorithm")
    print(f"Number of nodes explored: {globals.state['number_of_node_explored']} at state {count_state}")
    
    return