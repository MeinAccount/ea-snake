import pickle
from os import PathLike
from pathlib import Path
from typing import Tuple, List, Union

import numpy as np

from ea.dnn import MODEL_PATH

_folder = Path(MODEL_PATH.format("")[:-10])


class Store:
    @staticmethod
    def save(generation: Union[int, str], population: List[Tuple[np.ndarray, np.ndarray]], path=None) -> None:
        if not _folder.exists():
            _folder.mkdir(parents=True)
        if not path:
            path = MODEL_PATH.format(generation)
        with open(path, 'wb') as handler:
            pickle.dump(population, handler)

    @staticmethod
    def loadGen(generation: Union[int, str]) -> List[Tuple[np.ndarray, np.ndarray]]:
        return Store.loadFile(Path(MODEL_PATH.format(generation)))

    @staticmethod
    def loadFile(path: PathLike) -> List[Tuple[np.ndarray, np.ndarray]]:
        with open(path, 'rb') as handler:
            chromo = pickle.load(handler)

        return chromo
