from time import time

import numpy as np
import pickle
import utils

from areaMap.grid_generator import GridGenerator
from strategy.random_strategy_generator import RandomStrategyGenerator
from strategy.task_strategy import TaskStrategy


class StrategyBuilder:
    def __init__(self, num_elitisim, score_function, mode, mutate_rate=0.05):
        self.mode = mode
        self.population_size = -1
        self.population = []

        self.num_elitisim = num_elitisim
        self.elitism = {}

        self.score_function = score_function
        self.mutate_rate = mutate_rate

    def init_population(self, population_size):
        self.population_size = population_size
        self.population.extend([RandomStrategyGenerator.generate_random_strategy(self.score_function)
                                for _ in range(population_size)])

    def calc_fitness(self, sample_grid_list):
        scores = []
        for strategy in self.population:
            current_weight = 0
            current_steps = 0
            for grid in sample_grid_list:
                solution_path, weight = strategy.get_path_and_weight_for_grid(grid, (0, 0))
                if solution_path:
                    steps = len(solution_path)
                else:
                    steps = np.inf
                current_weight += weight
                current_steps += steps
            scores.append((current_weight / len(sample_grid_list), current_steps / len(sample_grid_list)))

        scores = zip(scores, self.population)
        scores.sort(key=lambda x: x[0][0])
        _, sorted_population = zip(*scores)
        self.elitism = set(sorted_population[:int(self.num_elitisim / 2)])
        scores.sort(key=lambda x: x[0][1])
        _, sorted_population = zip(*scores)
        self.elitism.update(sorted_population[:int(self.num_elitisim / 2)])

    def select(self):
        return np.random.choice(self.population, size=2)

    def crossover(self, parent_strategy1, parent_strategy2):
        child1 = self._crossover_states(parent_strategy1.states_list, parent_strategy2.states_list)
        child2 = self._crossover_states(parent_strategy2.states_list, parent_strategy1.states_list)
        return child1, child2

    def _crossover_states(self, parent_states1, parent_states2):
        np.random.shuffle(parent_states1)
        num_chosen_states = np.random.randint(1, len(parent_states1))
        chosen_states = parent_states1[:num_chosen_states]
        child_states = []
        for state in chosen_states:
            state_copy = state.create_copy()
            self._obligate_edges_for_chosen_states(chosen_states, state_copy, parent_states2)
            child_states.append(state_copy)
        child_states.extend(parent_states2)
        initial_state_index = np.random.randint(len(child_states))
        return TaskStrategy(child_states, initial_state_index)

    def _obligate_edges_for_chosen_states(self, chosen_states, state_copy, states2):
        for i, connected_state in enumerate(state_copy.next_states):
            if connected_state not in chosen_states:
                new_connected_state = np.random.choice(states2)
                state_copy.next_states[i] = new_connected_state

    def mutate(self, strategy):
        self._mutate_tolerance_range(strategy)
        self._mutate_edges(strategy)
        pass

    def _mutate_tolerance_range(self, strategy):
        if np.random.random() < self.mutate_rate:
            state = np.random.choice(strategy.states_list)
            shift_value = np.random.uniform(-0.01, 0.01)
            state.tolerated_danger_range[0] = self._mutate_to_valid_value(state, shift_value, index=0)
            state.tolerated_danger_range[1] = self._mutate_to_valid_value(state, shift_value, index=1)

    def _mutate_to_valid_value(self, state, shift_value, index):
        return max([min([state.tolerated_danger_range[index] + shift_value, 0]), 1])

    def _mutate_edges(self, strategy):
        if np.random.random() < self.mutate_rate:
            state = np.random.choice(strategy.states_list)
            edge_index_to_change = np.random.randint(3)
            new_state = np.random.choice(strategy.states_list)
            state.next_states[edge_index_to_change] = new_state

    def run(self, dataset, sample_size, num_generations=10):
        for generation in range(num_generations):
            start_time = time()

            np.random.shuffle(dataset)
            dataset_sample = dataset[:sample_size]
            self.calc_fitness(dataset_sample)

            current_population = list(self.elitism)
            while len(current_population) != self.population_size:
                p1, p2 = self.select()
                child1, child2 = self.crossover(p1, p2)
                self.mutate(child1)
                self.mutate(child2)
                current_population.append(child1)
                current_population.append(child2)
            self.population = current_population

            print 'generation {} | time {}'.format(generation, time() - start_time)

    def save_elitisim_to_files(self):
        for i, strategy in enumerate(self.elitism):
            pickle.dump(strategy, open('{}_strategies/strategy_{}'.format(self.mode, i), 'w'))

    @staticmethod
    def load_strategy_from_file(filename):
        return pickle.load(open(filename))


def main():
    num_elitism = 5
    score_func = utils.danger_score
    population_size = 20
    width = 25
    height = 25
    data_size = 10
    sample_size = 1
    num_generations = 10

    builder = StrategyBuilder(num_elitism, score_func, mode='danger')
    builder.init_population(population_size=population_size)
    grid_generator = GridGenerator()
    dataset = [grid_generator.create_grid(width, height) for _ in range(data_size)]
    builder.run(dataset, sample_size=sample_size, num_generations=num_generations)

    builder.save_elitisim_to_files()


def check_strategy(filename1, filename2):
    grid_generator = GridGenerator()
    grid = grid_generator.create_grid(25, 25)
    danger_out = check_strategy_on_grid(grid, filename1)
    print 'first:', danger_out[1]
    time_out = check_strategy_on_grid(grid, filename2)
    print 'second', time_out[1]
    print grid_generator.grid_to_json(grid.matrix, grid.target_list, danger_out, time_out)


def check_strategy_on_grid(grid, filename):
    strategy = StrategyBuilder.load_strategy_from_file(filename)
    return strategy.get_path_and_weight_for_grid(grid, (0, 0))


if __name__ == '__main__':
    # main()
    # check_strategy('danger_strategies/_strategy_0', 'time_strategies/strategy_0_second_try')
    check_strategy('danger_strategies/strategy_0_second_try', 'danger_strategies/strategy_1_second_try')
