import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from environment.grid import GridEnvironment
from agents.catcher import Catcher
from agents.runner import Runner
from game.simulator import GameSimulator
import numpy as np
import json
from datetime import datetime


class Benchmark:
    
    def __init__(self, map_data, max_turns=50):
        self.map_data = map_data
        self.max_turns = max_turns
        self.results = []
    
    def run_experiments(self, catcher_strategy, runner_strategy, num_games=100, 
                       catcher_start=(1, 1), runner_start=(3, 3)):
        print(f"\n{'='*60}")
        print(f"Benchmark: Catcher ({catcher_strategy}) vs Runner ({runner_strategy})")
        print(f"Number of games: {num_games}")
        print(f"{'='*60}\n")
        
        game_results = []
        
        for i in range(num_games):
            env = GridEnvironment(self.map_data)
            
            env.spawn_power_ups(speed_boosts=3, wall_builders=2, ghost_modes=2)
            env.spawn_teleport()
            
            catcher_pos = env.get_random_spawn_position(row_range=(1, 4))
            runner_pos = env.get_random_spawn_position(row_range=(14, 17))
            
            catcher = Catcher("catcher", catcher_pos, strategy=catcher_strategy)
            runner = Runner("runner", runner_pos, strategy=runner_strategy)
            
            env.add_agent(catcher.name, catcher.position)
            env.add_agent(runner.name, runner.position)
            
            game = GameSimulator(env, catcher, runner, max_turns=self.max_turns, verbose=False)
            metrics = game.run()
            
            game_results.append(metrics)
            
            if (i + 1) % 10 == 0:
                print(f"Completed {i + 1}/{num_games} games...")
        
        analysis = self.analyze_results(game_results, catcher_strategy, runner_strategy)
        
        experiment = {
            "timestamp": datetime.now().isoformat(),
            "catcher_strategy": catcher_strategy,
            "runner_strategy": runner_strategy,
            "num_games": num_games,
            "max_turns": self.max_turns,
            "raw_results": game_results,
            "analysis": analysis
        }
        
        self.results.append(experiment)
        
        self.print_analysis(analysis)
        
        return analysis
    
    def analyze_results(self, game_results, catcher_strategy, runner_strategy):
        catcher_wins = sum(1 for g in game_results if g["winner"] == "catcher")
        runner_wins = sum(1 for g in game_results if g["winner"] == "runner")
        
        capture_turns = [g["turns"] for g in game_results if g["winner"] == "catcher"]
        
        catcher_times_flat = [t for g in game_results for t in g["catcher_times"]]
        runner_times_flat = [t for g in game_results for t in g["runner_times"]]
        total_times = [g["total_time"] for g in game_results]
        
        analysis = {
            "catcher_strategy": catcher_strategy,
            "runner_strategy": runner_strategy,
            "total_games": len(game_results),
            
            "catcher_wins": catcher_wins,
            "runner_wins": runner_wins,
            "catcher_win_rate": catcher_wins / len(game_results) * 100,
            "runner_win_rate": runner_wins / len(game_results) * 100,
            
            "avg_capture_turns": np.mean(capture_turns) if capture_turns else None,
            "min_capture_turns": np.min(capture_turns) if capture_turns else None,
            "max_capture_turns": np.max(capture_turns) if capture_turns else None,
            "std_capture_turns": np.std(capture_turns) if capture_turns else None,
            
            "avg_catcher_time_per_move_ms": np.mean(catcher_times_flat) * 1000,
            "avg_runner_time_per_move_ms": np.mean(runner_times_flat) * 1000,
            "avg_total_game_time_s": np.mean(total_times),
            "max_total_game_time_s": np.max(total_times),
            
            "avg_steps_per_game": np.mean([g["turns"] for g in game_results]),
            "std_steps_per_game": np.std([g["turns"] for g in game_results])
        }
        
        return analysis
    
    def print_analysis(self, analysis):
        print(f"\n{'='*60}")
        print(f"EXPERIMENT RESULTS")
        print(f"{'='*60}")
        print(f"Configuration: {analysis['catcher_strategy'].upper()} vs {analysis['runner_strategy'].upper()}")
        print(f"Total games: {analysis['total_games']}")
        print()
        
        print(f"📊 WIN RATE:")
        print(f"  Catcher: {analysis['catcher_wins']}/{analysis['total_games']} ({analysis['catcher_win_rate']:.1f}%)")
        print(f"  Runner:  {analysis['runner_wins']}/{analysis['total_games']} ({analysis['runner_win_rate']:.1f}%)")
        print()
        
        if analysis['avg_capture_turns']:
            print(f"🎯 TURNS TO CAPTURE (when Catcher wins):")
            print(f"  Average: {analysis['avg_capture_turns']:.2f} turns")
            print(f"  Minimum: {analysis['min_capture_turns']} turns")
            print(f"  Maximum: {analysis['max_capture_turns']} turns")
            print(f"  Std Dev: {analysis['std_capture_turns']:.2f}")
            print()
        
        print(f"⏱️  COMPUTATIONAL COST:")
        print(f"  Avg Catcher time per move: {analysis['avg_catcher_time_per_move_ms']:.4f} ms")
        print(f"  Avg Runner time per move:  {analysis['avg_runner_time_per_move_ms']:.4f} ms")
        print(f"  Avg game time:             {analysis['avg_total_game_time_s']:.4f} s")
        print(f"  Max game time:             {analysis['max_total_game_time_s']:.4f} s")
        print()
        
        print(f"📈 STEPS PER EPISODE:")
        print(f"  Average: {analysis['avg_steps_per_game']:.2f} ± {analysis['std_steps_per_game']:.2f}")
        print(f"{'='*60}\n")


if __name__ == "__main__":
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
    
    benchmark = Benchmark(map_data, max_turns=50)
    
    benchmark.run_experiments("minimax", "minimax", num_games=10)
    