import random
from agents.agent import Agent
from algorithms.minimax import Minimax

class Runner(Agent):
    def __init__(self, name, start_pos, strategy, minimax_depth):
        """
        Initialize Runner agent.
        
        Args:
            name: Agent name
            start_pos: Starting position (row, col)
            strategy: "greedy", "minimax", or "random"
            minimax_depth: Search depth for minimax algorithm (default: 3)
        """
        super().__init__(name, start_pos)
        self.strategy = strategy
        self.minimax = None
        self.minimax_depth = minimax_depth
    
    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def get_next_position(self, direction):
        row, col = self.position
        if direction == "up":
            return (row - 1, col)
        elif direction == "down":
            return (row + 1, col)
        elif direction == "left":
            return (row, col - 1)
        elif direction == "right":
            return (row, col + 1)
        return self.position
    
    def choose_action(self, env):
        catcher_pos = env.agents.get("catcher")
        if not catcher_pos:
            return None
        
        directions = ["up", "down", "left", "right"]
        valid = [d for d in directions if env.is_valid_move(self.position, d)]
        
        if not valid:
            return None
        
        if self.strategy == "greedy":
            best_move = None
            max_distance = -1
            
            for direction in valid:
                next_pos = self.get_next_position(direction)
                distance = self.manhattan_distance(next_pos, catcher_pos)
                
                if distance > max_distance:
                    max_distance = distance
                    best_move = direction
            
            return best_move
        
        elif self.strategy == "minimax":
            if self.minimax is None:
                self.minimax = Minimax(env, max_depth=self.minimax_depth)
            
            result = self.minimax.get_best_action_runner(catcher_pos, self.position, self)
            if result:
                action_type, direction, wall_pos = result
                
                # Use wall builder if needed
                if wall_pos:
                    if self.use_item("wall_builder"):
                        env.place_wall(wall_pos)
                    return None  # Stay in place after placing wall
                
                # Use ghost mode if needed
                if action_type == "use_ghost" and direction:
                    if self.use_item("ghost_mode"):
                        return (direction, True)  # Return with ghost mode flag
                    return direction  # Fallback to normal move
                
                # Normal move
                if direction:
                    return direction
        
        # Fallback to random move
        return random.choice(valid) if valid else None
        
