import random
from agents.agent import Agent

class Runner(Agent):
    def __init__(self, name, start_pos, strategy="greedy"):
        super().__init__(name, start_pos)
        self.strategy = strategy
    
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
        directions = ["up", "down", "left", "right"]
        valid = [d for d in directions if env.is_valid_move(self.position, d)]
        
        if not valid:
            return None
        
        if self.strategy == "greedy":
            catcher_pos = env.agents.get("catcher")
            if catcher_pos:
                best_move = None
                max_distance = -1
                
                for direction in valid:
                    next_pos = self.get_next_position(direction)
                    distance = self.manhattan_distance(next_pos, catcher_pos)
                    
                    if distance > max_distance:
                        max_distance = distance
                        best_move = direction
                
                return best_move
        
