import pygame
import time
import os

class GameVisualizer:
    
    def __init__(self, env, cell_size=40): # cell_size: Size of each cell in pixels
        pygame.init()
        
        self.env = env
        self.cell_size = cell_size
        self.width = env.cols * cell_size
        self.height = env.rows * cell_size
        
        self.screen = pygame.display.set_mode((self.width, self.height + 100))
        pygame.display.set_caption("CatchMe - Tag Game")
        
        self.colors = {
            "background": (240, 240, 240),
            "wall": (60, 60, 60),
            "temp_wall": (255, 165, 0),
            "free": (255, 255, 255),
            "grid_line": (200, 200, 200),
            "catcher": (255, 50, 50),
            "runner": (50, 150, 255),
            "speed_boost": (255, 215, 0),
            "wall_builder": (139, 90, 43),
            "ghost_mode": (200, 150, 255),
            "teleport": (100, 255, 218),
            "text": (0, 0, 0)
        }
        
        self.font = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 36)
        
        self.timed_message = ""
        self.timed_message_end = 0
        
        # Load icons
        self.icons = self._load_icons()
    
    def set_timed_message(self, message, duration):
        self.timed_message = message
        self.timed_message_end = time.time() + duration
    
    def get_current_message(self):
        if time.time() < self.timed_message_end:
            return self.timed_message
        return ""
    
    def _load_icons(self):
        icons = {}
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icons")
        
        icon_names = [
            "catcher", "runner", "speed_boost", 
            "wall_builder", "ghost_mode", "teleport", "temp_wall"
        ]
        
        for icon_name in icon_names:
            try:
                path = os.path.join(icon_path, f"{icon_name}.png")
                if os.path.exists(path):
                    icon = pygame.image.load(path)
                    size = int(self.cell_size)
                    icon = pygame.transform.scale(icon, (size, size))
                    icons[icon_name] = icon
                else:
                    icons[icon_name] = None
            except Exception as e:
                print(f"Warning: Could not load icon {icon_name}.png: {e}")
        
        return icons
        
    def draw_grid(self):
        self.screen.fill(self.colors["background"])
        
        for r in range(self.env.rows):
            for c in range(self.env.cols):
                x = c * self.cell_size
                y = r * self.cell_size
                
                if self.env.grid[r, c] == 1:
                    color = self.colors["wall"]
                else:
                    color = self.colors["free"]
                
                pygame.draw.rect(self.screen, color, (x, y, self.cell_size, self.cell_size))
                
                pygame.draw.rect(self.screen, self.colors["grid_line"], 
                               (x, y, self.cell_size, self.cell_size), 1)
        
        for pos in self.env.temporary_walls:
            r, c = pos
            x = c * self.cell_size
            y = r * self.cell_size
            
            if self.icons["temp_wall"]:
                icon_rect = self.icons["temp_wall"].get_rect(center=(x + self.cell_size // 2, y + self.cell_size // 2))
                self.screen.blit(self.icons["temp_wall"], icon_rect)
            else:
                pygame.draw.rect(self.screen, self.colors["temp_wall"], 
                               (x, y, self.cell_size, self.cell_size))
        
        for pos, power_type in self.env.power_ups.items():
            r, c = pos
            x = c * self.cell_size
            y = r * self.cell_size
            center_x = x + self.cell_size // 2
            center_y = y + self.cell_size // 2
            
            icon = self.icons.get(power_type)
            if icon:
                icon_rect = icon.get_rect(center=(center_x, center_y))
                self.screen.blit(icon, icon_rect)
            else:
                if power_type == "speed_boost":
                    pygame.draw.circle(self.screen, self.colors["speed_boost"], (center_x, center_y), self.cell_size // 3)
                    text = self.font.render("S", True, self.colors["text"])
                elif power_type == "wall_builder":
                    pygame.draw.rect(self.screen, self.colors["wall_builder"], 
                                   (center_x - self.cell_size // 4, center_y - self.cell_size // 4, 
                                    self.cell_size // 2, self.cell_size // 2))
                    text = self.font.render("W", True, self.colors["text"])
                elif power_type == "ghost_mode":
                    pygame.draw.circle(self.screen, self.colors["ghost_mode"], (center_x, center_y), self.cell_size // 3)
                    text = self.font.render("G", True, self.colors["text"])
                elif power_type == "teleport":
                    pygame.draw.circle(self.screen, self.colors["teleport"], (center_x, center_y), self.cell_size // 3)
                    text = self.font.render("T", True, self.colors["text"])
                
                text_rect = text.get_rect(center=(center_x, center_y))
                self.screen.blit(text, text_rect)
        
        for name, (r, c) in self.env.agents.items():
            x = c * self.cell_size
            y = r * self.cell_size
            center_x = x + self.cell_size // 2
            center_y = y + self.cell_size // 2
            
            icon = self.icons.get(name)
            if icon:
                icon_rect = icon.get_rect(center=(center_x, center_y))
                self.screen.blit(icon, icon_rect)
            else:
                if name == "catcher":
                    pygame.draw.circle(self.screen, self.colors["catcher"], (center_x, center_y), self.cell_size // 3)
                    text = self.font_large.render("C", True, (255, 255, 255))
                else:
                    pygame.draw.circle(self.screen, self.colors["runner"], (center_x, center_y), self.cell_size // 3)
                    text = self.font_large.render("R", True, (255, 255, 255))
                
                text_rect = text.get_rect(center=(center_x, center_y))
                self.screen.blit(text, text_rect)
    
    def draw_info(self, turn, catcher, runner, message=""):
        info_y = self.env.rows * self.cell_size + 10
        
        turn_text = self.font.render(f"Turn: {turn}", True, self.colors["text"])
        self.screen.blit(turn_text, (10, info_y))
        
        catcher_text = f"Catcher: "
        if catcher.has_speed_boost():
            catcher_text += f"⚡({catcher.speed_boost_turns}) "
        if catcher.has_item("wall_builder"):
            catcher_text += f"W:{catcher.inventory['wall_builder']} "
        if catcher.has_item("ghost_mode"):
            catcher_text += f"G:{catcher.inventory['ghost_mode']} "
        
        text = self.font.render(catcher_text, True, self.colors["catcher"])
        self.screen.blit(text, (10, info_y + 30))
        
        runner_text = f"Runner: "
        if runner.has_speed_boost():
            runner_text += f"⚡({runner.speed_boost_turns}) "
        if runner.has_item("wall_builder"):
            runner_text += f"W:{runner.inventory['wall_builder']} "
        if runner.has_item("ghost_mode"):
            runner_text += f"G:{runner.inventory['ghost_mode']} "
        
        text = self.font.render(runner_text, True, self.colors["runner"])
        self.screen.blit(text, (10, info_y + 55))
        
        if message:
            msg_text = self.font.render(message, True, self.colors["text"])
            self.screen.blit(msg_text, (self.width // 2 - 100, info_y + 30))
    
    def draw_end_screen(self, winner, turns):
        button_width = 150
        button_height = 50
        button_x = self.width // 2 - button_width // 2
        button_y = self.height // 2 + 60
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        return True
            
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            if winner == "catcher":
                text = self.font_large.render(f"CATCHER WINS!", True, self.colors["catcher"])
            else:
                text = self.font_large.render(f"RUNNER WINS!", True, self.colors["runner"])
            
            text_rect = text.get_rect(center=(self.width // 2, self.height // 2 - 20))
            self.screen.blit(text, text_rect)
            
            turns_text = self.font.render(f"Turns: {turns}", True, (255, 255, 255))
            turns_rect = turns_text.get_rect(center=(self.width // 2, self.height // 2 + 20))
            self.screen.blit(turns_text, turns_rect)
            
            mouse_pos = pygame.mouse.get_pos()
            button_color = (100, 200, 100) if button_rect.collidepoint(mouse_pos) else (70, 170, 70)
            pygame.draw.rect(self.screen, button_color, button_rect, border_radius=10)
            pygame.draw.rect(self.screen, (255, 255, 255), button_rect, 3, border_radius=10)
            
            reset_text = self.font_large.render("Reset", True, (255, 255, 255))
            reset_rect = reset_text.get_rect(center=button_rect.center)
            self.screen.blit(reset_text, reset_rect)
            
            pygame.display.flip()
    
    def update(self, turn, catcher, runner, message=""):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
        
        display_message = message if message else self.get_current_message()
        
        self.draw_grid()
        self.draw_info(turn, catcher, runner, display_message)
        pygame.display.flip()
        
        return True
    
    def close(self):
        pygame.quit()
