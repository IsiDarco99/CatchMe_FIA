import numpy as np

class GridEnvironment:
    def __init__(self, map_data):
        self.rows = len(map_data)
        self.cols = len(map_data[0])
        self.grid = np.zeros((self.rows, self.cols), dtype=int)
        for r, line in enumerate(map_data):
            for c, char in enumerate(line):
                if char == "#":
                    self.grid[r, c] = 1
        self.agents = {}  # nome: agente

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

    def print_grid(self):
        display = np.array(self.grid, dtype=str)
        display[display == "0"] = "."
        display[display == "1"] = "#"
        for name, (r, c) in self.agents.items():
            display[r, c] = name[0].upper()
        for row in display:
            print(" ".join(row))
        print()
