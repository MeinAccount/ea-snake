from typing import Tuple, List

import numpy as np

Chromo = Tuple[np.ndarray, np.ndarray, np.ndarray]

MODEL_FEATURE_COUNT = 7
MODEL_HIDDEN_NEURONS = 100
MODEL_PATH = "dnn_genetic_evolution/gen{}.pickle"


def chromo_predict(chromo: Chromo, angle: float, neighbours_free: List[bool],
                   distance_left: float, distance_forward: float, distance_right: float) -> int:
    act_in = np.array([angle, *neighbours_free, distance_left / 50, distance_forward / 50, distance_right / 50])
    act_hidden = np.clip(np.matmul(act_in, chromo[0]), 0, 10)
    act_hidden2 = np.clip(np.matmul(act_hidden, chromo[1]), 0, 10)
    output = np.matmul(act_hidden2, chromo[2])

    return np.argmax(output) - 1


def random_chromosome(_):
    return (np.random.uniform(-1, 1, (MODEL_FEATURE_COUNT, MODEL_HIDDEN_NEURONS)),
            np.random.uniform(-1, 1, (MODEL_HIDDEN_NEURONS, MODEL_HIDDEN_NEURONS)),
            np.random.uniform(-1, 1, (MODEL_HIDDEN_NEURONS, 3)))
