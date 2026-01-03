import numpy as np
import random

class GridEnvironment:
    def __init__(self, map_data):
        self.rows = len(map_data)
        self.cols = len(map_data[0])
        self.grid = np.zeros((self.rows, self.cols), dtype=int)
        for r, line in enumerate(map_data):
            for c, char in enumerate(line):
                if char == "#":
                    self.grid[r, c] = 1
        self.agents = {}  # name: position
        self.power_ups = {}  # position: power_up_type

    def add_agent(self, name, pos):
        if self.grid[pos[0], pos[1]] == 0:
            self.agents[name] = pos
        else:
            raise ValueError("Cella occupata da muro!")

    def is_valid_move(self, pos, direction):
        row, col = pos
        if direction == "up":
            row -= 1
        elif direction == "down":
            row += 1
        elif direction == "left":
            col -= 1
        elif direction == "right":
            col += 1
        else:
            return False
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row, col] == 0
        return False

    def move_agent(self, name, direction):
        if name not in self.agents:
            return False
        pos = self.agents[name]
        if self.is_valid_move(pos, direction):
            row, col = pos
            if direction == "up":
                row -= 1
            elif direction == "down":
                row += 1
            elif direction == "left":
                col -= 1
            elif direction == "right":
                col += 1
            self.agents[name] = (row, col)
            return True
        return False

    def get_free_cells(self, row_range=None):
        """Get all free cells (no walls, no agents)."""
        free_cells = []
        start_row = row_range[0] if row_range else 0
        end_row = row_range[1] if row_range else self.rows
        
        for r in range(start_row, end_row):
            for c in range(self.cols):
                if self.grid[r, c] == 0 and (r, c) not in self.agents.values():
                    free_cells.append((r, c))
        return free_cells
    
    def spawn_power_ups(self, num_power_ups=3, power_up_type="speed_boost"):
        """Spawn power-ups randomly in free cells."""
        free_cells = self.get_free_cells()
        
        if len(free_cells) < num_power_ups:
            num_power_ups = len(free_cells)
        
        spawn_positions = random.sample(free_cells, num_power_ups)
        
        for pos in spawn_positions:
            self.power_ups[pos] = power_up_type
        
        return spawn_positions
    
    def get_random_spawn_position(self, row_range=None):
        free_cells = self.get_free_cells(row_range)        
        return random.choice(free_cells)
    
    def collect_power_up(self, pos):
        if pos in self.power_ups:
            power_up_type = self.power_ups[pos]
            del self.power_ups[pos]
            return power_up_type
        return None
    
    def print_grid(self):
        display = np.array(self.grid, dtype=str)
        display[display == "0"] = "◾"
        display[display == "1"] = "🧱"
        
        for (r, c), power_type in self.power_ups.items():
            display[r, c] = "⚡"
        
        for name, (r, c) in self.agents.items():
            display[r, c] = "🟥" if name == "catcher" else "🟦"
        
        for row in display:
            print(" ".join(row))
        print()
