import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from environment.grid import GridEnvironment
from agents.catcher import Catcher
from agents.runner import Runner
from visualization.game_visualizer import GameVisualizer
from game.simulator import GameSimulator
import time

map_data = [
    "#################",
    "#...............#",
    "#.#####...#.#...#",
    "#.#.......#.#...#",
    "#.#.###.###.###.#",
    "#.#.#...........#",
    "#.#.#...###.###.#",
    "#.........#.#...#",
    "#...###...#.#...#",
    "#...###.........#",
    "#...###...#######",
    "#.........#.....#",
    "#.#...#.#.#...#.#",
    "#.#...#.#.#...#.#",
    "#.#####.#.....#.#",
    "#.......#.....#.#",
    "#################"
]

def run_visual_demo(turn_delay): # turn_delay: Seconds to wait between turns
    
    env = GridEnvironment(map_data)
    
    env.spawn_power_ups(speed_boosts=2, wall_builders=2, ghost_modes=2)
    env.spawn_teleport()
    
    catcher_pos = env.get_random_spawn_position(row_range=(1, 4))
    runner_pos = env.get_random_spawn_position(row_range=(14, 17))
    
    print(f"Catcher spawned at: {catcher_pos}")
    print(f"Runner spawned at: {runner_pos}")
    
    catcher = Catcher("catcher", catcher_pos, strategy="minimax", minimax_depth=6)
    runner = Runner("runner", runner_pos, strategy="minimax", minimax_depth=6)
    
    env.add_agent(catcher.name, catcher.position)
    env.add_agent(runner.name, runner.position)
    
    visualizer = GameVisualizer(env, cell_size=40)
    
    max_turns = 100
    turn = 0
    message = ""
    
    if not visualizer.update(turn, catcher, runner, "Game Start!"):
        return
    time.sleep(2)
    
    while turn < max_turns:
        moves_count = 2 if catcher.has_speed_boost() else 1
        
        for _ in range(moves_count):
            action = catcher.choose_action(env)
            if action:
                # Check if action is tuple (direction, use_ghost_mode)
                use_ghost = False
                if isinstance(action, tuple):
                    action, use_ghost = action
                
                env.move_agent(catcher.name, action, use_ghost_mode=use_ghost)
                catcher.position = env.agents[catcher.name]
            
            power_up = env.collect_power_up(catcher.position)
            if power_up:
                message = f"Catcher collected {power_up}!"
                if power_up == "speed_boost":
                    catcher.activate_speed_boost()
                elif power_up in ["wall_builder", "ghost_mode"]:
                    catcher.add_to_inventory(power_up)
                elif power_up == "teleport":
                    env.teleport_agent(catcher.name)
                    catcher.position = env.agents[catcher.name]
                    message = f"Catcher teleported to {catcher.position}!"
                
                visualizer.set_timed_message(message, duration=3.0)
            
            if catcher.position == runner.position:
                visualizer.update(turn + 1, catcher, runner, "CATCHER CAUGHT RUNNER!")
                return visualizer.draw_end_screen("catcher", turn + 1)
            
            if not visualizer.update(turn, catcher, runner, message):
                return False
            time.sleep(turn_delay / 2)
        
        catcher.decrease_boost_turns()
        message = ""
        
        moves_count = 2 if runner.has_speed_boost() else 1
        
        for _ in range(moves_count):
            action = runner.choose_action(env)
            if action:
                # Check if action is tuple (direction, use_ghost_mode)
                use_ghost = False
                if isinstance(action, tuple):
                    action, use_ghost = action
                
                env.move_agent(runner.name, action, use_ghost_mode=use_ghost)
                runner.position = env.agents[runner.name]
            
            power_up = env.collect_power_up(runner.position)
            if power_up:
                message = f"Runner collected {power_up}!"
                if power_up == "speed_boost":
                    runner.activate_speed_boost()
                elif power_up in ["wall_builder", "ghost_mode"]:
                    runner.add_to_inventory(power_up)
                elif power_up == "teleport":
                    env.teleport_agent(runner.name)
                    runner.position = env.agents[runner.name]
                    message = f"Runner teleported to {runner.position}!"
                
                visualizer.set_timed_message(message, duration=3.0)
            
            if GameSimulator.can_capture(catcher.position, runner.position):
                visualizer.update(turn + 1, catcher, runner, "CATCHER CAUGHT RUNNER!")
                return visualizer.draw_end_screen("catcher", turn + 1)
            
            if not visualizer.update(turn, catcher, runner, message):
                return False
            time.sleep(turn_delay / 2)
        
        runner.decrease_boost_turns()
        message = ""
        
        if not visualizer.update(turn, catcher, runner):
            return False
        
        time.sleep(turn_delay)
        turn += 1
    
    visualizer.update(turn, catcher, runner, "TIME'S UP!")
    return visualizer.draw_end_screen("runner", max_turns)

if __name__ == "__main__":
    print("="*60)
    print("CATCHME - TAG GAME DEMO")
    print("="*60)
    
    while True:
        reset = run_visual_demo(turn_delay=0.1)
        if not reset:
            break