import utils
from areaMap.grid_generator import GridGenerator
from strategy.random_strategy_generator import RandomStrategyGenerator


def main():
    print "hello"
    width = 50

    grid_generator = GridGenerator()
    grid = grid_generator.create_grid(width, width)

    path_and_weight_less_danger = get_path_to_grid_with_function(grid, utils.danger_score)
    path, weight = path_and_weight_less_danger
    print weight
    # print path
    path_and_weight_less_steps = get_path_to_grid_with_function(grid, utils.dist_score)
    print grid_generator.grid_to_json(grid.matrix, grid.target_list, path_and_weight_less_danger, path_and_weight_less_steps)


def get_path_to_grid_with_function(grid, score_func):
    strategy = RandomStrategyGenerator.generate_random_strategy(score_func)
    return strategy.get_path_and_weight_for_grid(grid, (0, 0))


if __name__ == '__main__':
    main()
