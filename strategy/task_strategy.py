import numpy as np

import utils


class TaskStrategy:
    def __init__(self, states_list, initial_state_index):
        self.states_list = states_list
        self.current_state = states_list[initial_state_index]
        self.targets_list = None
        self.path_weight = 0

    def get_path_and_weight_for_grid(self, grid, start_point):
        self.targets_list = list(grid.target_list)
        path = []
        current_point = start_point
        last_point = None
        num_valid_steps = 5 * len(grid.matrix) ** 2
        while self.targets_list:
            tmp_point = self._do_one_step(current_point, grid, path, last_point)
            last_point = current_point
            current_point = tmp_point
            if len(path) >= num_valid_steps:
                return None, np.inf
        return path, self.path_weight

    def _do_one_step(self, current_point, grid, path, last_point):
        self.path_weight += grid.get_probability_at_point(current_point)
        path.append(current_point)
        if current_point in self.targets_list:
            self.targets_list.remove(current_point)
        if not self.targets_list:
            return
        self.current_state, current_point = self._get_next_state_and_point(grid, current_point, last_point)
        return current_point

    def _get_next_state_and_point(self, grid, current_point, last_point):
        neighbors = grid.get_neighbor_points_with_danger_list(current_point, last_point)
        target_point = self._get_closest_target(current_point)
        return self.current_state.get_next_state_and_point(neighbors, target_point)

    def _get_closest_target(self, point):
        dists = [utils.distance(point, target_point) for target_point in self.targets_list]
        min_dist_index = np.argmin(dists)
        return self.targets_list[min_dist_index]
