import random
from agents.agent import Agent
from algorithms.astar import AStar
from algorithms.minimax import Minimax

class Catcher(Agent):
    def __init__(self, name, start_pos, strategy, minimax_depth):
        super().__init__(name, start_pos)
        self.strategy = strategy
        self.astar = None
        self.minimax = None
        self.minimax_depth = minimax_depth
    
    def choose_action(self, env):
        runner_pos = env.agents.get("runner")
        if not runner_pos:
            return None
        
        if self.strategy == "astar":
            if self.astar is None:
                self.astar = AStar(env)
            
            action = self.astar.get_next_action(self.position, runner_pos)
            if action:
                return action
        
        elif self.strategy == "minimax":
            if self.minimax is None:
                self.minimax = Minimax(env, max_depth=self.minimax_depth)
            
            result = self.minimax.get_best_action_catcher(self.position, runner_pos, self)
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
        
        valid_directions = []
        for direction in ["up", "down", "left", "right"]:
            if env.is_valid_move(self.position, direction):
                valid_directions.append(direction)
        
        if valid_directions:
            return random.choice(valid_directions)
        
        return None
