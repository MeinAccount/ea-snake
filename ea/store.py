import pickle
from pathlib import Path

from ea.dnn import MODEL_PATH


class DNNStore:
    @staticmethod
    def save(generation, population):
        folder = Path(MODEL_PATH.format("")[:-10])
        if not folder.exists():
            folder.mkdir(parents=True)

        with open(MODEL_PATH.format(generation), 'wb') as handler:
            pickle.dump(population, handler)

    @staticmethod
    def load(generation):
        path = MODEL_PATH.format(generation)
        p = Path(path)
        if not p.exists():
            return None

        with open(p, 'rb') as handler:
            population = pickle.load(handler)

        return population
