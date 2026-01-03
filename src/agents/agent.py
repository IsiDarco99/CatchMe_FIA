class Agent:
    def __init__(self, name, start_pos):
        self.name = name
        self.position = start_pos
        self.speed_boost_turns = 0

    def activate_speed_boost(self):
        self.speed_boost_turns = 3
    
    def has_speed_boost(self):
        return self.speed_boost_turns > 0
    
    def decrease_boost_turns(self):
        if self.speed_boost_turns > 0:
            self.speed_boost_turns -= 1

    def choose_action(self, env):
        raise NotImplementedError
