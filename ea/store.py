import pickle
from os import PathLike
from pathlib import Path
from typing import List, Union

from ea.dnn import MODEL_PATH, Chromo

_folder = Path(MODEL_PATH.format("")[:-10])


class Store:
    @staticmethod
    def save(generation: Union[int, str], population: List[Chromo]) -> None:
        if not _folder.exists():
            _folder.mkdir(parents=True)

        with open(MODEL_PATH.format(generation), 'wb') as handler:
            pickle.dump(population, handler)

    @staticmethod
    def loadGen(generation: Union[int, str]) -> List[Chromo]:
        return Store.loadFile(Path(MODEL_PATH.format(generation)))

    @staticmethod
    def loadFile(path: PathLike) -> List[Chromo]:
        with open(path, 'rb') as handler:
            chromo = pickle.load(handler)

        return chromo

    @staticmethod
    def loadLatestGen() -> List[Tuple[np.ndarray, np.ndarray]]:
        max_gen = 0
        p = Path(_folder)
        for i in p.iterdir():
            n = str(i).find(".pickle")
            gen = int(str(i)[3:n])
            if max_gen < gen:
                max_gen = gen
        return Store.loadGen(max_gen)
