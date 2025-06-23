# algorithms/theta.py
import pygame
import math
from queue import PriorityQueue
import globals

def heuristic(p1, p2):
    """Calculate Manhattan distance heuristic for grid-based movement"""
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def get_distance(p1, p2):
    """Calculate Manhattan distance between two points"""
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def line_of_sight(grid, start_spot, end_spot):
    """Check if there's a clear line of sight between two spots using Bresenham's line algorithm"""
    x0, y0 = start_spot.row, start_spot.col
    x1, y1 = end_spot.row, end_spot.col
    
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    
    err = dx - dy
    
    while True:
        # Check if current position is within grid bounds
        if x0 < 0 or x0 >= len(grid) or y0 < 0 or y0 >= len(grid[0]):
            return False
        
        # Check if current position is a barrier
        if grid[x0][y0].is_barrier():
            return False
        
        # If we've reached the end point
        if x0 == x1 and y0 == y1:
            break
        
        e2 = 2 * err
        
        if e2 > -dy:
            err -= dy
            x0 += sx
        
        if e2 < dx:
            err += dx
            y0 += sy
    
    return True

def get_manhattan_path(start_spot, end_spot):
    """Get points following Manhattan distance (only horizontal/vertical movement)"""
    points = []
    x0, y0 = start_spot.row, start_spot.col
    x1, y1 = end_spot.row, end_spot.col
    
    # Start from the starting point
    current_x, current_y = x0, y0
    points.append((current_x, current_y))
    
    # Move horizontally first, then vertically
    # (You can change this to vertical first if preferred)
    
    # Horizontal movement
    while current_x != x1:
        if current_x < x1:
            current_x += 1
        else:
            current_x -= 1
        points.append((current_x, current_y))
    
    # Vertical movement
    while current_y != y1:
        if current_y < y1:
            current_y += 1
        else:
            current_y -= 1
        points.append((current_x, current_y))
    
    return points

def reconstruct_path(came_from, current, draw, grid):
    """Reconstruct and draw the final path with Manhattan-style movement"""
    path_spots = []
    
    # Collect the key path points
    while current in came_from:
        path_spots.append(current)
        current = came_from[current]
    path_spots.append(current)  # Add the start point
    
    # Reverse to get path from start to end
    path_spots.reverse()
    
    # Draw Manhattan path segments between consecutive path points
    total_distance = 0
    for i in range(len(path_spots) - 1):
        start_spot = path_spots[i]
        end_spot = path_spots[i + 1]
        
        # Calculate Manhattan distance for this segment
        manhattan_dist = abs(start_spot.row - end_spot.row) + abs(start_spot.col - end_spot.col)
        total_distance += manhattan_dist
        
        # Get all points on the Manhattan path between start and end
        manhattan_points = get_manhattan_path(start_spot, end_spot)
        
        # Mark all points on the path (except start and end nodes)
        for point in manhattan_points:
            row, col = point
            if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
                spot = grid[row][col]
                if not spot.is_start() and not spot.is_end():
                    spot.make_path()
    
    # Final draw to show complete path
    draw()
    
    globals.state["total_cost"] = total_distance
    print(f"Path segments: {len(path_spots) - 1}")
    print(f"Total path length (Manhattan): {total_distance}")
    
    return total_distance

def theta_algorithm(draw, grid, start, end):
    """Theta* pathfinding algorithm implementation"""
    count = 0
    globals.state["number_of_node_explored"] = 0  # Reset counter
    globals.state["total_cost"] = 0  # Reset cost
    
    # Priority queue for open set
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    
    # Dictionaries to track path and costs
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())
    
    # Set to track what's in the open set
    open_set_hash = {start}
    
    while not open_set.empty():
        yield  # Yield for each iteration
        
        # Get the spot with lowest f_score
        current = open_set.get()[2]
        open_set_hash.remove(current)
        
        # Goal reached
        if current == end:
            reconstruct_path(came_from, end, draw, grid)
            end.make_end()
            start.make_start()
            print(f"Theta* algorithm completed!")
            print(f"Total nodes explored: {globals.state['number_of_node_explored']}")
            print(f"Total path cost: {globals.state['total_cost']:.2f}")
            return
        
        # Process neighbors
        for neighbor in current.neighbors:
            if neighbor.is_barrier():
                continue
            
            # Standard A* path cost
            temp_g_score = g_score[current] + get_distance(current.get_pos(), neighbor.get_pos())
            parent_to_use = current
            
            # Theta* optimization: check line of sight to parent
            if current in came_from and line_of_sight(grid, came_from[current], neighbor):
                # Direct path from parent to neighbor
                parent = came_from[current]
                direct_g_score = g_score[parent] + get_distance(parent.get_pos(), neighbor.get_pos())
                
                if direct_g_score < temp_g_score:
                    temp_g_score = direct_g_score
                    parent_to_use = parent
            
            # Update scores if we found a better path
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = parent_to_use
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())
                
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    if not neighbor.is_end():
                        neighbor.make_open()
                    globals.state["number_of_node_explored"] += 1
        
        # Only draw every few iterations to improve performance
        if globals.state["number_of_node_explored"] % 5 == 0:
            draw()
            print(f"Theta* algorithm - Nodes explored: {globals.state['number_of_node_explored']}")
        
        # Mark current as closed
        if current != start:
            current.make_closed()
    
    print("Theta* algorithm: No path found!")
    return