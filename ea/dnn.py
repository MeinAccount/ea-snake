from typing import Tuple, List

import numpy as np

Chromo = Tuple[np.ndarray, np.ndarray]

MODEL_FEATURE_COUNT = 4
MODEL_HIDDEN_NEURONS = 100
MODEL_PATH = "dnn_genetic_evolution/gen{}.pickle"


def chromo_predict(chromo: Chromo, angle: float, neighbours_free: List[bool]) -> int:
    act_in = np.array([angle, *neighbours_free])
    act_hidden = np.maximum(np.matmul(act_in, chromo[0]), 0)
    output = np.matmul(act_hidden, chromo[1])

    return np.argmax(output) - 1


def random_chromosome(_):
    return (np.random.uniform(-1, 1, (MODEL_FEATURE_COUNT, MODEL_HIDDEN_NEURONS)),
            np.random.uniform(-1, 1, (MODEL_HIDDEN_NEURONS, 3)))
