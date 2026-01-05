class Agent:
    def __init__(self, name, start_pos):
        self.name = name
        self.position = start_pos
        self.speed_boost_turns = 0

        self.inventory = {
            "wall_builder": 0,
            "ghost_mode": 0
        }

    def activate_speed_boost(self):
        self.speed_boost_turns = 3
    
    def add_to_inventory(self, item_type):
        if item_type in self.inventory:
            self.inventory[item_type] += 1
            return True
        return False
    
    def has_item(self, item_type):
        return self.inventory.get(item_type, 0) > 0
    
    def use_item(self, item_type):
        if self.has_item(item_type):
            self.inventory[item_type] -= 1
            return True
        return False
    
    def has_speed_boost(self):
        return self.speed_boost_turns > 0
    
    def decrease_boost_turns(self):
        if self.speed_boost_turns > 0:
            self.speed_boost_turns -= 1

    def choose_action(self, env):
        raise NotImplementedError
