from typing import Tuple, List

import numpy as np

MODEL_LAYER_COUNT = 20
MODEL_FEATURE_COUNT = 4
MODEL_HIDDEN_NEURONS = MODEL_FEATURE_COUNT * MODEL_LAYER_COUNT ** 2
MODEL_PATH = "dnn_genetic_evolution/gen{}.pickle"


def chromo_predict(chromo: Tuple[np.ndarray, np.ndarray], angle: float, neighbours_free: List[bool]):
    act_in = np.array([angle, *neighbours_free])
    act_hidden = np.maximum(np.matmul(act_in, chromo[0]), 0)
    output = np.matmul(act_hidden, chromo[1])

    return np.argmax(output) - 1
