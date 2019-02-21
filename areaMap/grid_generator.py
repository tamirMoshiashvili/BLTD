import json
import random

import numpy

import utils
from areaMap.Grid import Grid


class GridGenerator:

    def __init__(self):
        self.grid = None

    @staticmethod
    def get_all_neighbors_list_of_point(upper_border, lower_border, left_border, right_border):
        neighbors_list = []
        for i in range(left_border, right_border):
            for j in range(upper_border, lower_border):
                neighbors_list.append((i, j))
        return neighbors_list

    def update(self, neighbor, danger_point, val):
        if self.grid[neighbor] == 0:
            self.grid[neighbor] = self.grid[danger_point] - val
        else:
            self.grid[neighbor] = ((self.grid[neighbor] + self.grid[danger_point] - val) / 2 + self.grid[
                danger_point] - val) / 2

    def fill_one_neighbor(self, neighbor, danger_point, scale):
        dist = utils.distance(neighbor, danger_point)
        if dist <= scale:
            self.update(neighbor, danger_point, dist / 50)

    def fill_neighbors(self, current_point, width, height):
        scale = int(width / 10)
        x = current_point[0]
        y = current_point[1]
        upper_border = max(0, y - scale)
        lower_border = min(y + scale, height)
        left_border = max(0, x - scale)
        right_border = min(x + scale, width)
        neighbors = self.get_all_neighbors_list_of_point(upper_border, lower_border, left_border, right_border)
        for n in neighbors:
            self.fill_one_neighbor(n, current_point, scale)
        return self.grid

    def fill_all_else(self, width, height):
        for i in range(height):
            for j in range(width):
                if self.grid[i, j] == 0.0:
                    self.grid[i, j] = random.uniform(0.0, 0.2)

    def create_grid(self, width, height):
        num_special_points = int(width / 5)
        targets_list = GridGenerator.create_points_list(width, height, num_special_points)
        self.grid = numpy.zeros((width, height))
        danger_list = GridGenerator.create_points_list(width, height, num_special_points)
        for danger_point in danger_list:
            self.grid[danger_point] = random.uniform(0.8, 1.0)
            self.fill_neighbors(danger_point, width, height)
        self.fill_all_else(width, height)
        return Grid(self.grid, targets_list)

    @staticmethod
    def create_points_list(width, length, num_of_points):
        x_positions = random.sample(range(width - 1), num_of_points)
        y_positions = random.sample(range(length - 1), num_of_points)
        targets = [(x_positions[i], y_positions[i]) for i in range(num_of_points)]
        return targets

    def grid_to_json(self, matrix, targets_list, path_and_weight_danger, path_and_weight_steps):
        dict_for_json = {
            "grid": matrix.tolist(),
            "targets_list": targets_list,
            "starting_point": [0, 0],
            "danger_output": path_and_weight_danger,
            "time_output" : path_and_weight_steps
        }
        return json.dumps(dict_for_json)


if __name__ == '__main__':
    g = GridGenerator()
    grid = g.create_grid(25, 25)
    matrix, ls = grid.matrix, grid.target_list

    import matplotlib.pyplot as plt

    plt.imshow(matrix)
    plt.show()
