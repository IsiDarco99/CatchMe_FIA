import time

class GameSimulator:
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
                self.env.move_agent(agent.name, action)
                agent.position = self.env.agents[agent.name]
            
            power_up = self.env.collect_power_up(agent.position)
            if power_up == "speed_boost":
                agent.activate_speed_boost()
            
            if self.catcher.position == self.runner.position:
                return "catcher_won"
        
        
        return None

    def play(self):
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

            if self.verbose:
                self.env.print_grid()
                if self.catcher.has_speed_boost():
                    print(f"Catcher speed boost: {self.catcher.speed_boost_turns} turns left")
                if self.runner.has_speed_boost():
                    print(f"Runner speed boost: {self.runner.speed_boost_turns} turns left")
            
            self.turn += 1

        self.metrics["winner"] = "runner"
        self.metrics["turns"] = self.max_turns
        self.metrics["total_time"] = time.time() - start_time
        
        if self.verbose:
            print("Runner won!")
        
        return self.metrics
