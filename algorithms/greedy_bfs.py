from queue import PriorityQueue
import pygame
import globals

def h(p1, p2):
    """Manhattan distance heuristic"""
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    """Reconstruct and draw the final path"""
    path_length = 0
    while current in came_from:
        current = came_from[current]
        current.make_path()
        path_length += 1
        draw()
    
    globals.state["total_cost"] = path_length
    return path_length

def greedy_bfs_algorithm(draw, grid, start, end):
    """
    Greedy Best-First Search Algorithm
    Uses only heuristic function h(n) to guide search
    Faster than A* but not guaranteed to find optimal path
    """
    count = 0
    count_state = 0
    globals.state["number_of_node_explored"] = 0
    globals.state["total_cost"] = 0
    
    # Priority queue: (heuristic_cost, count, node)
    open_set = PriorityQueue()
    open_set.put((h(start.get_pos(), end.get_pos()), count, start))
    came_from = {}
    
    # Track nodes in open set for fast lookup
    open_set_hash = {start}
    # Track visited nodes to avoid revisiting
    visited = set()

    while not open_set.empty():
        yield  # Yield for visualization

        current = open_set.get()[2]
        open_set_hash.remove(current)
        
        # Mark as visited
        visited.add(current)
        count_state += 1

        if current == end:
            path_cost = reconstruct_path(came_from, end, draw)
            end.make_end()
            print(f"Greedy BFS found solution!")
            print(f"Path cost: {path_cost}")
            print(f"Total nodes explored: {globals.state['number_of_node_explored']}")
            return

        # Explore neighbors
        for neighbor in current.neighbors:
            # Skip if already visited
            if neighbor in visited:
                continue
                
            # Skip if already in open set
            if neighbor in open_set_hash:
                continue
            
            # Add to path tracking
            came_from[neighbor] = current
            
            # Calculate heuristic cost (only heuristic, no actual cost)
            heuristic_cost = h(neighbor.get_pos(), end.get_pos())
            
            # Add to open set
            count += 1
            open_set.put((heuristic_cost, count, neighbor))
            open_set_hash.add(neighbor)
            neighbor.make_open()
            globals.state["number_of_node_explored"] += 1

        draw()
        print("Greedy Best-First Search")
        print(f"Number of nodes explored: {globals.state['number_of_node_explored']} at state {count_state}")
        print(f"Current heuristic: {h(current.get_pos(), end.get_pos())}")
        
        # Mark current as closed (visited)
        if current != start:
            current.make_closed()

    print("Greedy BFS: No solution found")
    return