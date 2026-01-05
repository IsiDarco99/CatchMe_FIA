from environment.grid import GridEnvironment
from agents.catcher import Catcher
from agents.runner import Runner
from game.simulator import GameSimulator

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

env = GridEnvironment(map_data)

# Spawn different power-ups
env.spawn_power_ups(speed_boosts=2, wall_builders=2, ghost_modes=2)
teleport_pos = env.spawn_teleport()

catcher_pos = env.get_random_spawn_position(row_range=(1, 4))
runner_pos = env.get_random_spawn_position(row_range=(14, 17))

catcher = Catcher("catcher", catcher_pos, strategy="astar")
runner = Runner("runner", runner_pos, strategy="greedy")

env.add_agent(catcher.name, catcher.position)
env.add_agent(runner.name, runner.position)

game = GameSimulator(env, catcher, runner, max_turns=100)
game.play()
