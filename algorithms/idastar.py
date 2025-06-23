from collections import deque
import pygame
import globals

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def heuristic(a, b):
        # Manhattan distance
        return abs(a.row - b.row) + abs(a.col - b.col)
def ida_algorithm(draw, grid, start, end):
    def search(node, g, threshold):
        f = g + heuristic(node, end)
        if f > threshold:
            return f  # return new threshold candidate

        if node == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return "FOUND"

        min_threshold = float("inf")
        for neighbor in node.neighbors:
            if neighbor not in visited and not neighbor.is_barrier():
                visited.add(neighbor)
                came_from[neighbor] = node
                neighbor.make_open()
                globals.state["number_of_node_explored"] += 1
                draw()

                result = search(neighbor, g + 1, threshold)
                if result == "FOUND":
                    return "FOUND"
                if isinstance(result, (int, float)):
                    min_threshold = min(min_threshold, result)

        if node != start:
            node.make_closed()
        return min_threshold

    threshold = heuristic(start, end)
    came_from = {}
    iteration = 0

    while True:
        visited = {start}
        globals.state["number_of_node_explored"] = 0  # Reset count each iteration
        result = search(start, 0, threshold)

        print("Iterative Deepening A* algorithm")
        print(f"Number of nodes explored: {globals.state['number_of_node_explored']} at state {iteration}")
        yield  # For visual update step-by-step

        if result == "FOUND":
            print("Path found using IDA*.")
            return
        if result == float("inf"):
            print("No path found.")
            return

        threshold = result  # Increase threshold to next f-cost
        iteration += 1
