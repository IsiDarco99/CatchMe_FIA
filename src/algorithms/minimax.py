class Minimax:    
    def __init__(self, env, max_depth):
        self.env = env
        self.max_depth = max_depth
        self.directions = ["up", "down", "left", "right"]
    
    def real_path_distance(self, start, goal):
        """
        Calculate real path distance using A* (considers walls).
        Returns number of moves needed, or infinity if no path.
        """
        import heapq
        
        if start == goal:
            return 0
        
        def heuristic(pos):
            # Manhattan distance as heuristic
            return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])
        
        # Priority queue: (f_score, g_score, position)
        open_set = [(heuristic(start), 0, start)]
        visited = {start: 0}  # position -> g_score
        
        while open_set:
            f_score, g_score, pos = heapq.heappop(open_set)
            
            # If we reached the goal
            if pos == goal:
                return g_score
            
            # If we found a better path to this position, skip
            if g_score > visited.get(pos, float('inf')):
                continue
            
            # Explore neighbors
            for direction in self.directions:
                new_pos = self.get_new_position(pos, direction)
                if new_pos and self.is_position_valid(new_pos):
                    new_g_score = g_score + 1
                    
                    # If this is a better path
                    if new_g_score < visited.get(new_pos, float('inf')):
                        visited[new_pos] = new_g_score
                        new_f_score = new_g_score + heuristic(new_pos)
                        heapq.heappush(open_set, (new_f_score, new_g_score, new_pos))
        
        return float('inf')  # No path found
    
    def evaluate_position(self, catcher_pos, runner_pos):
        
        distance_score = self.real_path_distance(catcher_pos, runner_pos)
        
        # Mobility evaluation - penalize positions with few escape routes
        runner_moves = len(self.get_valid_moves(runner_pos))
        catcher_moves = len(self.get_valid_moves(catcher_pos))
        
        # Runner wants more mobility (escape options), Catcher wants to restrict it
        mobility_score = (runner_moves - catcher_moves) * 0.5
        
        # Extra penalty for dead ends (only 1 exit)
        if runner_moves <= 1:
            mobility_score -= 3.0  # Strong penalty for traps
        
        # Power-up evaluation with MUCH lower weights to avoid distractions
        powerup_bonus = 0
        
        for pos, power_type in self.env.power_ups.items():
            runner_dist = self.real_path_distance(runner_pos, pos)
            catcher_dist = self.real_path_distance(catcher_pos, pos)
            
            if power_type == "speed_boost":
                if runner_dist <= 2:
                    powerup_bonus += (3 - runner_dist) * 0.05
                if catcher_dist <= 2:
                    powerup_bonus -= (3 - catcher_dist) * 0.05

            elif power_type == "wall_builder":
                if runner_dist < catcher_dist and runner_dist <= 2:
                    powerup_bonus += 0.1
                elif catcher_dist <= 2:
                    powerup_bonus -= 0.05
            
            elif power_type == "ghost_mode":
                if runner_dist < catcher_dist and runner_dist <= 2:
                    powerup_bonus += 0.08
                elif catcher_dist <= 2:
                    powerup_bonus -= 0.1
            
            elif power_type == "teleport":
                if distance_score <= 3 and runner_dist <= 1:
                    powerup_bonus += 0.15
                elif runner_dist < catcher_dist and runner_dist <= 2:
                    powerup_bonus += 0.08
                elif catcher_dist <= 1:
                    powerup_bonus -= 0.08
        
        # Cap power-up bonus to prevent overwhelming distance
        powerup_bonus = max(-0.5, min(0.5, powerup_bonus))
        
        return distance_score + mobility_score + powerup_bonus
    
    def get_valid_moves(self, pos):
        valid_moves = []
        for direction in self.directions:
            new_pos = self.get_new_position(pos, direction)
            if new_pos and self.is_position_valid(new_pos):
                valid_moves.append((direction, new_pos))
        return valid_moves
    
    def get_new_position(self, pos, direction):
        row, col = pos
        if direction == "up":
            return (row - 1, col)
        elif direction == "down":
            return (row + 1, col)
        elif direction == "left":
            return (row, col - 1)
        elif direction == "right":
            return (row, col + 1)
        return None
    
    def is_position_valid(self, pos):
        row, col = pos
        if 0 <= row < self.env.rows and 0 <= col < self.env.cols:
            if self.env.grid[row, col] == 1:  # Se c'è un muro (1), non è valido
                return False
            if pos in self.env.temporary_walls:
                return False
            return True
        return False
    
    def check_if_trapped(self, runner_pos, catcher_pos, wall_pos):

        original_grid_value = self.env.grid[wall_pos]
        self.env.grid[wall_pos] = 1
        
        distance_with_wall = self.real_path_distance(catcher_pos, runner_pos)
        
        self.env.grid[wall_pos] = original_grid_value
        
        return distance_with_wall <= 5
    
    def minimax(self, catcher_pos, runner_pos, depth, is_maximizing):
        if depth == 0 or catcher_pos == runner_pos:
            return self.evaluate_position(catcher_pos, runner_pos)
        
        if is_maximizing:
            max_eval = float('-inf')
            valid_moves = self.get_valid_moves(runner_pos)
            
            if not valid_moves:
                return self.evaluate_position(catcher_pos, runner_pos)
            
            for direction, new_runner_pos in valid_moves:
                eval_score = self.minimax(catcher_pos, new_runner_pos, depth - 1, False)
                max_eval = max(max_eval, eval_score)
            
            return max_eval
        else:
            min_eval = float('inf')
            valid_moves = self.get_valid_moves(catcher_pos)
            
            if not valid_moves:
                return self.evaluate_position(catcher_pos, runner_pos)
            
            for direction, new_catcher_pos in valid_moves:
                eval_score = self.minimax(new_catcher_pos, runner_pos, depth - 1, True)
                min_eval = min(min_eval, eval_score)
            
            return min_eval
    
    def get_best_action_catcher(self, catcher_pos, runner_pos, catcher_agent):
        actions = []
        
        # Current distance
        current_distance = self.real_path_distance(catcher_pos, runner_pos)
        
        # Normal moves
        for direction in self.directions:
            new_pos = self.get_new_position(catcher_pos, direction)
            if new_pos and self.is_position_valid(new_pos):
                actions.append(("move", direction, new_pos, None))
        
        # Ghost mode: move through walls (excluding borders)
        if catcher_agent.has_item("ghost_mode"):
            for direction in self.directions:
                new_pos = self.get_new_position(catcher_pos, direction)
                if new_pos:
                    row, col = new_pos
                    # Must be inside bounds, not a border
                    if (0 < row < self.env.rows - 1 and 
                        0 < col < self.env.cols - 1):
                        # Check if using ghost mode reduces distance by more than 2
                        new_distance = self.real_path_distance(new_pos, runner_pos)
                        if current_distance - new_distance > 2:
                            actions.append(("use_ghost", direction, new_pos, None))
        
        # Wall builder: place wall to trap runner
        if catcher_agent.has_item("wall_builder"):
            # Try placing walls in adjacent cells
            for direction in self.directions:
                wall_pos = self.get_new_position(catcher_pos, direction)
                if wall_pos and self.env.grid[wall_pos] == 0 and wall_pos not in self.env.temporary_walls:
                    # Check if this wall traps the runner
                    if self.check_if_trapped(runner_pos, catcher_pos, wall_pos):
                        # Stay in place but mark to use wall builder
                        actions.append(("move", None, catcher_pos, wall_pos))
        
        if not actions:
            return ("move", None, None)
        
        # Evaluate all actions using minimax
        best_action = None
        best_value = float('inf')
        
        for action_type, direction, new_pos, wall_pos in actions:
            move_value = self.minimax(new_pos, runner_pos, self.max_depth - 1, True)
            
            if move_value < best_value:
                best_value = move_value
                best_action = (action_type, direction, wall_pos)
        
        return best_action if best_action else ("move", None, None)
    
    def get_best_action_runner(self, catcher_pos, runner_pos, runner_agent):
        actions = []
        
        current_distance = self.real_path_distance(catcher_pos, runner_pos)
        
        for direction in self.directions:
            new_pos = self.get_new_position(runner_pos, direction)
            if new_pos and self.is_position_valid(new_pos):
                actions.append(("move", direction, new_pos, None))
        
        # Ghost mode: move through walls (excluding borders)
        if runner_agent.has_item("ghost_mode"):
            for direction in self.directions:
                new_pos = self.get_new_position(runner_pos, direction)
                if new_pos:
                    row, col = new_pos
                    # Must be inside bounds, not a border
                    if (0 < row < self.env.rows - 1 and 
                        0 < col < self.env.cols - 1):
                        # Check if using ghost mode increases distance by more than 2
                        new_distance = self.real_path_distance(catcher_pos, new_pos)
                        if new_distance - current_distance > 2:
                            actions.append(("use_ghost", direction, new_pos, None))
        
        # Wall builder: place wall to block Catcher
        if runner_agent.has_item("wall_builder"):
            for direction in self.directions:
                wall_pos = self.get_new_position(runner_pos, direction)
                if wall_pos and self.env.grid[wall_pos] == 0 and wall_pos not in self.env.temporary_walls:
                    # Temporarily place wall and check distance change
                    original_value = self.env.grid[wall_pos]
                    self.env.grid[wall_pos] = 1
                    
                    new_distance = self.real_path_distance(catcher_pos, runner_pos)
                    
                    # Restore
                    self.env.grid[wall_pos] = original_value
                    
                    # Use wall if it increases distance by more than 2
                    if new_distance - current_distance > 2:
                        actions.append(("move", None, runner_pos, wall_pos))
        
        if not actions:
            return ("move", None, None)
        
        # Evaluate all actions
        best_action = None
        best_value = float('-inf')
        
        for action_type, direction, new_pos, wall_pos in actions:
            move_value = self.minimax(catcher_pos, new_pos, self.max_depth - 1, False)
            
            if move_value > best_value:
                best_value = move_value
                best_action = (action_type, direction, wall_pos)
        
        return best_action if best_action else ("move", None, None)
