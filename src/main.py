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
    "#.#...#.#.#.....#",
    "#.#...#.#.......#",
    "#.#####.#.#.....#",
    "#.......#.#.....#",
    "#################"
]

env = GridEnvironment(map_data)

catcher = Catcher("catcher", (1, 1))
runner = Runner("runner", (1, 5))

env.add_agent(catcher.name, catcher.position)
env.add_agent(runner.name, runner.position)

game = GameSimulator(env, catcher, runner)
game.play()
