class Agent:
    def __init__(self, name, start_pos):
        self.name = name
        self.position = start_pos

    def choose_action(self, env):
        raise NotImplementedError
