import pickle
from pathlib import Path

from ea.dnn import MODEL_PATH

_folder = Path(MODEL_PATH.format("")[:-10])


class Store:
    @staticmethod
    def save(generation, population):
        if not _folder.exists():
            _folder.mkdir(parents=True)

        with open(MODEL_PATH.format(generation), 'wb') as handler:
            pickle.dump(population, handler)

    @staticmethod
    def loadGen(generation):
        path = MODEL_PATH.format(generation)
        path = Path(path)
        if not path.exists():
            return None

        with open(path, 'rb') as handler:
            population = pickle.load(handler)

        return population

    @staticmethod
    def loadFile(path):
        with open(path, 'rb') as handler:
            chromo = pickle.load(handler)

        return chromo
