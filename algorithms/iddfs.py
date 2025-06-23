from collections import deque
import pygame
import globals

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def iddfs_algorithm(draw, grid, start, end):
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
                draw()

                if dls(neighbor, depth - 1):
                    return True

        if node != start:
            node.make_closed()
        return False

    depth = 0
    while True:
        visited = {start}
        came_from = {}
        globals.state["number_of_node_explored"] = 0  # Reset for this depth

        print(f"[IDDFS] Trying depth = {depth}")
        yield  # Cho phép cập nhật GUI ở mỗi vòng lặp

        if dls(start, depth):
            print(f"Path found at depth {depth}")
            print(f"Nodes explored: {globals.state['number_of_node_explored']}")
            return

        print(f"No path at depth {depth}")
        print(f"Nodes explored: {globals.state['number_of_node_explored']}")

        depth += 1
