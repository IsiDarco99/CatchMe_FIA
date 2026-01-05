import time

class GameSimulator:
    @staticmethod
    def can_capture(catcher_pos, runner_pos):
        """Check if catcher can capture runner (same position or diagonal)"""
        c_row, c_col = catcher_pos
        r_row, r_col = runner_pos
        
        # Same position
        if c_row == r_row and c_col == r_col:
            return True
        
        # Diagonal adjacent (one step away in both row and col)
        row_diff = abs(c_row - r_row)
        col_diff = abs(c_col - r_col)
        if row_diff == 1 and col_diff == 1:
            return True
        
        return False
    
    def __init__(self, env, catcher, runner, max_turns=50, verbose=True):
        self.env = env
        self.catcher = catcher
        self.runner = runner
        self.max_turns = max_turns
        self.verbose = verbose
        self.turn = 0
        self.metrics = {
            "winner": None,
            "turns": 0,
            "catcher_times": [],
            "runner_times": [],
            "total_time": 0,
            "catcher_nodes_explored": 0,
            "runner_nodes_explored": 0,
        }

    def execute_turn(self, agent, is_catcher=True):
        moves_count = 2 if agent.has_speed_boost() else 1
        agent_name = "catcher" if is_catcher else "runner"
        opponent = self.runner if is_catcher else self.catcher
        
        for move_num in range(moves_count):
            move_start = time.time()
            action = agent.choose_action(self.env)
            move_time = time.time() - move_start
            
            if is_catcher:
                self.metrics["catcher_times"].append(move_time)
            else:
                self.metrics["runner_times"].append(move_time)
            
            if action:
                # Check if action is tuple (direction, use_ghost_mode)
                use_ghost = False
                if isinstance(action, tuple):
                    action, use_ghost = action
                
                self.env.move_agent(agent.name, action, use_ghost_mode=use_ghost)
                agent.position = self.env.agents[agent.name]
            
            power_up = self.env.collect_power_up(agent.position)
            if power_up:
                if power_up == "speed_boost":
                    agent.activate_speed_boost()
                
                elif power_up == "wall_builder":
                    agent.add_to_inventory("wall_builder")
                
                elif power_up == "ghost_mode":
                    agent.add_to_inventory("ghost_mode")
                
                elif power_up == "teleport":
                    self.env.teleport_agent(agent.name)
                    agent.position = self.env.agents[agent.name]
            
            if self.can_capture(self.catcher.position, self.runner.position):
                return "catcher_won"
        
        return None
    
    def run(self):
        """Main game loop"""
        start_time = time.time()
        
        while self.turn < self.max_turns:
            result = self.execute_turn(self.catcher, is_catcher=True)
            if result == "catcher_won":
                self.metrics["winner"] = "catcher"
                self.metrics["turns"] = self.turn + 1
                self.metrics["total_time"] = time.time() - start_time
                
                if self.verbose:
                    print(f"Catcher won in {self.turn+1} turns!")
                    self.env.print_grid()
                return self.metrics
            
            self.catcher.decrease_boost_turns()

            result = self.execute_turn(self.runner, is_catcher=False)
            if result == "catcher_won":
                self.metrics["winner"] = "catcher"
                self.metrics["turns"] = self.turn + 1
                self.metrics["total_time"] = time.time() - start_time
                
                if self.verbose:
                    print(f"Catcher won in {self.turn+1} turns!")
                    self.env.print_grid()
                return self.metrics
            
            self.runner.decrease_boost_turns()
            
            self.env.update_temporary_walls()
            
            if self.verbose:
                self.env.print_grid()
            
            self.turn += 1

        self.metrics["winner"] = "runner"
        self.metrics["turns"] = self.max_turns
        self.metrics["total_time"] = time.time() - start_time
        
        if self.verbose:
            print("Runner won!")
        
        return self.metrics
