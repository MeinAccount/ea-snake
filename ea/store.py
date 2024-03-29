import glob
import pickle
import re
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
    def load_gen(generation: Union[int, str]) -> List[Chromo]:
        return Store.load_file(Path(MODEL_PATH.format(generation)))

    @staticmethod
    def load_file(path: PathLike) -> List[Chromo]:
        with open(path, 'rb') as handler:
            chromo = pickle.load(handler)

        return chromo

    @staticmethod
    def get_latest_gen() -> int:
        regex = MODEL_PATH.format('(\\d+)')
        return max([int(re.match(regex, file).group(1)) for file in glob.glob(MODEL_PATH.format('*'))])
