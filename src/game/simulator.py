class GameSimulator:
    def __init__(self, env, catcher, runner, max_turns=50):
        self.env = env
        self.catcher = catcher
        self.runner = runner
        self.max_turns = max_turns
        self.turn = 0

    def play(self):
        while self.turn < self.max_turns:
            action = self.catcher.choose_action(self.env)
            if action:
                self.env.move_agent(self.catcher.name, action)
                self.catcher.position = self.env.agents[self.catcher.name]

            if self.catcher.position == self.runner.position:
                print(f"Catcher ha vinto in {self.turn+1} turni!")
                self.env.print_grid()
                return

            action = self.runner.choose_action(self.env)
            if action:
                self.env.move_agent(self.runner.name, action)
                self.runner.position = self.env.agents[self.runner.name]

            self.env.print_grid()
            self.turn += 1

        print("Runner ha vinto!")
