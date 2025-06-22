from collections import deque
import pygame
import globals

def reconstruct_path_bidirectional(came_from_start, came_from_end, meeting_point, start, end, draw):
    """Reconstruct path from both directions meeting at meeting_point"""
    current = meeting_point
    path_start = []
    while current in came_from_start:
        current = came_from_start[current]
        path_start.append(current)
    
    path_start.reverse()
    
    current = meeting_point
    path_end = []
    while current in came_from_end:
        current = came_from_end[current]
        path_end.append(current)
    
    for spot in path_start:
        if spot != start:
            spot.make_path()
            draw()
    
    meeting_point.make_path()
    draw()
    
    for spot in path_end:
        if spot != end:
            spot.make_path()
            draw()

def bi_directional_search_algorithm(draw, grid, start, end):
    from queue import Queue
    
    globals.state["number_of_node_explored"] = 0
    
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
        yield  # Yield for visualization
        
        if not start_queue.empty():
            current_start = start_queue.get()
            
            if current_start in end_visited:
                print(f"Bidirectional search: Paths met at {current_start.get_pos()}")
                reconstruct_path_bidirectional(came_from_start, came_from_end, current_start, start, end, draw)
                start.make_start()  
                end.make_end()      
                return

            for neighbor in current_start.neighbors:
                if neighbor not in start_visited and not neighbor.is_barrier():
                    start_visited.add(neighbor)
                    came_from_start[neighbor] = current_start
                    start_queue.put(neighbor)
                    if neighbor not in end_visited:
                        neighbor.make_open()  
                    globals.state["number_of_node_explored"] += 1
            
            if current_start != start:
                current_start.make_closed()

        if not end_queue.empty():
            current_end = end_queue.get()
            
            if current_end in start_visited:
                print(f"Bidirectional search: Paths met at {current_end.get_pos()}")
                reconstruct_path_bidirectional(came_from_start, came_from_end, current_end, start, end, draw)
                start.make_start()  
                end.make_end()      
                return

            for neighbor in current_end.neighbors:
                if neighbor not in end_visited and not neighbor.is_barrier():
                    end_visited.add(neighbor)
                    came_from_end[neighbor] = current_end
                    end_queue.put(neighbor)
                    if neighbor not in start_visited:
                        neighbor.make_open()  
                    globals.state["number_of_node_explored"] += 1
            
            if current_end != end:
                current_end.make_closed()

        count_state += 1
        draw()
        print("Bi-directional search algorithm")
        print(f"Number of nodes explored: {globals.state['number_of_node_explored']} at state {count_state}")
        print(f"Start queue size: {start_queue.qsize()}, End queue size: {end_queue.qsize()}")
    
    print("Bidirectional search: No solution found")
    return