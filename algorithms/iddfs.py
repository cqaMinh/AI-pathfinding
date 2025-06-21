from collections import deque
import pygame
import globals

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def iddfs_algorithm(draw, grid, start, end, max_depth=10):
    def dls(node, depth):
        if node == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True
        if depth == 0:
            return False

        for neighbor in node.neighbors:
            if neighbor not in visited and not neighbor.is_barrier():
                visited.add(neighbor)
                came_from[neighbor] = node
                neighbor.make_open()
                globals.state["number_of_node_explored"] += 1

                if dls(neighbor, depth - 1):
                    return True

        if node != start:
            node.make_closed()
        return False

    for depth in range(max_depth):
        visited = {start}
        came_from = {}
        yield  # Yield for each loop iteration

        if dls(start, depth):
            print("Depth-limited search algorithm")
            print(f"Number of nodes explored: {globals.state['number_of_node_explored']} at max depth {max_depth}")
            return
        
    print("No path found within the maximum depth limit.")

    
    return