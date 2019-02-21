class Grid:
    def __init__(self, matrix, target_list):
        self.matrix = matrix
        self.target_list = target_list
        self.is_first = True

    def get_probability_at_point(self, point):
        return self.matrix[point[0], point[1]]

    def get_probability_at(self, x, y):
        return self.matrix[x, y]

    def get_neighbor_points_with_danger_list(self, point, last_point):
        return self._get_neighbors_list_of_point(point[0], point[1], last_point)

    def _get_neighbors_list_of_point(self, x, y, last_point):
        neighbors_list = []
        if x > 0:  # left
            point = (x - 1, y)
            neighbors_list.append((point, self.get_probability_at_point(point)))
        if x < len(self.matrix[0]) - 1:  # right
            point = (x + 1, y)
            neighbors_list.append((point, self.get_probability_at_point(point)))
        if y > 0:  # down
            point = (x, y - 1)
            neighbors_list.append((point, self.get_probability_at_point(point)))
        if y < len(self.matrix) - 1:  # up
            point = (x, y + 1)
            neighbors_list.append((point, self.get_probability_at_point(point)))
        if last_point:
            neighbors_list.remove((last_point, self.get_probability_at_point(last_point)))
        return neighbors_list

    def get_targets_list(self):
        return self.target_list

    def __str__(self):
        return str(self.matrix) + '|' + str(self.target_list)
