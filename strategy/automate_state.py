import numpy as np


class AutomateState:
    def __init__(self, tolerated_danger_range, score_function):
        self.tolerated_danger_range = tolerated_danger_range
        self.score_function = score_function
        self.next_states = []

    def set_next_states(self, next_states):
        self.next_states = next_states

    def get_next_state_and_point(self, neighbors, target_point):
        best_neighbor = self.get_best_neighbor(neighbors, target_point)
        new_point, danger_prob = best_neighbor
        if danger_prob < self.tolerated_danger_range[0]:
            chosen_state = self.next_states[0]
        elif danger_prob < self.tolerated_danger_range[1]:
            chosen_state = self.next_states[1]
        else:
            chosen_state = self.next_states[2]
        return chosen_state, new_point

    def get_best_neighbor(self, neighbors, target_point):
        scores = [self.score_function(neighbor[0], neighbor[1], target_point) for neighbor in neighbors]
        best_neighbor_index = np.argmin(scores)
        return neighbors[best_neighbor_index]

    def create_copy(self):
        state_copy = AutomateState(self.tolerated_danger_range, self.score_function)
        state_copy.set_next_states(self.next_states)
        return state_copy

    def __str__(self):
        ls = [x.tolerated_danger_range for x in self.next_states]
        return str(self.tolerated_danger_range) + ' | ' + str(ls)
