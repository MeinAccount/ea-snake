from typing import Tuple, List

import numpy as np

MODEL_FEATURE_COUNT = 7
MODEL_HIDDEN_NEURONS = 100
MODEL_PATH = "dnn_genetic_evolution/gen{}.pickle"


def chromo_predict(chromo: Tuple[np.ndarray, np.ndarray], angle: float, neighbours_free: List[bool],
                   distance_left: float, distance_forward: float, distance_right: float) -> int:
    act_in = np.array([angle, *neighbours_free, distance_left, distance_forward, distance_right])
    act_hidden = np.maximum(np.matmul(act_in, chromo[0]), 0)
    output = np.matmul(act_hidden, chromo[1])

    return np.argmax(output) - 1
