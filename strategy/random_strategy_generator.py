import random
import numpy as np

from strategy.automate_state import AutomateState
from strategy.task_strategy import TaskStrategy


class RandomStrategyGenerator:
    def __init__(self):
        pass

    @staticmethod
    def generate_random_strategy(score_function, max_states=5):
        num_states = random.randint(3, max_states)
        states = []

        # vertices
        for _ in range(num_states):
            tolerated_danger_range = sorted(np.random.random(2))
            states.append(AutomateState(tolerated_danger_range, score_function))

        # edges
        for state in list(states):
            np.random.shuffle(states)
            next_states = states[:3]
            state.set_next_states(next_states)

        initial_state_index = np.random.randint(num_states)
        return TaskStrategy(states, initial_state_index)
