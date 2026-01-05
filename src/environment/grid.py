import numpy as np
import random

class GridEnvironment:
    def __init__(self, map_data):
        self.rows = len(map_data)
        self.cols = len(map_data[0])
        self.grid = np.zeros((self.rows, self.cols), dtype=int)
        self.original_grid = np.copy(self.grid)
        
        for r, line in enumerate(map_data):
            for c, char in enumerate(line):
                if char == "#":
                    self.grid[r, c] = 1
        
        self.original_grid = np.copy(self.grid)
        self.agents = {}
        self.power_ups = {}
        self.temporary_walls = {}
        self.teleport_corners = [(1, 1), (1, self.cols-2), (self.rows-2, 1), (self.rows-2, self.cols-2)]

    def add_agent(self, name, pos):
        if self.grid[pos[0], pos[1]] == 0:
            self.agents[name] = pos
        else:
            raise ValueError("Cell occupied by wall!")

    def is_valid_move(self, pos, direction, ignore_walls=False):
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
            if ignore_walls:
                return True
            return self.grid[row, col] == 0
        return False

    def move_agent(self, name, direction, use_ghost_mode=False):
        if name not in self.agents:
            return False
        pos = self.agents[name]
        
        if self.is_valid_move(pos, direction, ignore_walls=use_ghost_mode):
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
    
    def place_wall(self, pos):
        if 0 <= pos[0] < self.rows and 0 <= pos[1] < self.cols:
            if self.grid[pos[0], pos[1]] == 0:
                self.grid[pos[0], pos[1]] = 1
                self.temporary_walls[pos] = True  # Mark as player-placed wall
                return True
        return False
    
    def teleport_agent(self, name):
        if name in self.agents:
            available_corners = [c for c in self.teleport_corners if c not in self.agents.values()]
            if available_corners:
                self.agents[name] = random.choice(available_corners)
                return True
        return False

    def get_free_cells(self, row_range=None):
        free_cells = []
        start_row = row_range[0] if row_range else 0
        end_row = row_range[1] if row_range else self.rows
        
        for r in range(start_row, end_row):
            for c in range(self.cols):
                if self.grid[r, c] == 0 and (r, c) not in self.agents.values():
                    free_cells.append((r, c))
        return free_cells
    
    def spawn_power_ups(self, speed_boosts=3, wall_builders=2, ghost_modes=2):
        free_cells = self.get_free_cells()
        
        total_powerups = speed_boosts + wall_builders + ghost_modes
        if len(free_cells) < total_powerups:
            return []
        
        spawn_positions = random.sample(free_cells, total_powerups)
        
        idx = 0
        for _ in range(speed_boosts):
            self.power_ups[spawn_positions[idx]] = "speed_boost"
            idx += 1
        for _ in range(wall_builders):
            self.power_ups[spawn_positions[idx]] = "wall_builder"
            idx += 1
        for _ in range(ghost_modes):
            self.power_ups[spawn_positions[idx]] = "ghost_mode"
            idx += 1
        
        return spawn_positions
    
    def spawn_teleport(self):
        center = (self.rows // 2, self.cols // 2)
        self.power_ups[center] = "teleport"
        return center
    
    def get_random_spawn_position(self, row_range=None):
        free_cells = self.get_free_cells(row_range)
        if not free_cells:
            raise ValueError("No free cells available!")
        return random.choice(free_cells)
    
    def collect_power_up(self, pos):
        if pos in self.power_ups:
            power_up_type = self.power_ups[pos]
            if power_up_type != "teleport":
                del self.power_ups[pos]
            return power_up_type
        return None
    
    def print_grid(self):
        display = np.array(self.grid, dtype=str)
        display[display == "0"] = "◾"
        display[display == "1"] = "🧱"
        
        for (r, c), power_type in self.power_ups.items():
            if power_type == "speed_boost":
                display[r, c] = "⚡"
            elif power_type == "wall_builder":
                display[r, c] = "🟫"
            elif power_type == "ghost_mode":
                display[r, c] = "👻"
            elif power_type == "teleport":
                display[r, c] = "🌀"
        
        for pos in self.temporary_walls:
            display[pos[0], pos[1]] = "🚧"
        
        for name, (r, c) in self.agents.items():
            display[r, c] = "🟥" if name == "catcher" else "🟦"
        
        for row in display:
            print(" ".join(row))
        print()
