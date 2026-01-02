import random
from agents.agent import Agent
from algorithms.astar import AStar

class Catcher(Agent):
    def __init__(self, name, start_pos, strategy="astar"):
        super().__init__(name, start_pos)
        self.strategy = strategy
        self.astar = None
    
    def choose_action(self, env):
        if self.strategy == "astar":
            if self.astar is None:
                self.astar = AStar(env)
            
            runner_pos = env.agents.get("runner")
            if runner_pos:
                action = self.astar.get_next_action(self.position, runner_pos)
                if action:
                    return action
