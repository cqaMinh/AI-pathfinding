from collections import deque
import pygame
import globals

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def beam_search_algorithm(draw, grid, start, end, beam_width=3):
    queue = deque([start])
    visited = {start}
    came_from = {}
    count_state = 0

    while queue:
        yield  # Yield for each loop iteration

        current_level = []
        for _ in range(min(beam_width, len(queue))):
            current = queue.popleft()
            current_level.append(current)

            if current == end:
                reconstruct_path(came_from, end, draw)
                end.make_end()
                return

            for neighbor in current.neighbors:
                if neighbor not in visited and not neighbor.is_barrier():
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    neighbor.make_open()
                    globals.state["number_of_node_explored"] += 1
                    queue.append(neighbor)

        count_state += 1
        draw()

        for node in current_level:
            if node != start:
                node.make_closed()

    print("Beam search algorithm")
    print(f"Number of nodes explored: {globals.state['number_of_node_explored']} at state {count_state}")
    return