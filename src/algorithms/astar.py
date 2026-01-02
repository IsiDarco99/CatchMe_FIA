import heapq

class AStar:
    def __init__(self, env):
        self.env = env
    
    def heuristic(self, pos1, pos2):
        """Distanza di Manhattan come euristica."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def get_neighbors(self, pos):
        """Ritorna le celle vicine valide (no muri)."""
        neighbors = []
        directions = [("up", -1, 0), ("down", 1, 0), ("left", 0, -1), ("right", 0, 1)]
        
        for direction, dr, dc in directions:
            new_pos = (pos[0] + dr, pos[1] + dc)
            if (0 <= new_pos[0] < self.env.rows and 
                0 <= new_pos[1] < self.env.cols and 
                self.env.grid[new_pos[0], new_pos[1]] == 0):
                neighbors.append((direction, new_pos))
        
        return neighbors
    
    def find_path(self, start, goal):
        if start == goal:
            return []
        
        counter = 0
        frontier = [(0, counter, start, [])]
        visited = set()
        
        while frontier:
            f_score, _, current, path = heapq.heappop(frontier)
            
            if current in visited:
                continue
            
            visited.add(current)
            
            if current == goal:
                return path
            
            for direction, neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    g_score = len(path) + 1
                    h_score = self.heuristic(neighbor, goal)
                    f_score = g_score + h_score
                    
                    counter += 1
                    heapq.heappush(frontier, (f_score, counter, neighbor, path + [direction]))
        
        return None
    
    def get_next_action(self, start, goal):
        path = self.find_path(start, goal)
        if path and len(path) > 0:
            return path[0]
        return None
