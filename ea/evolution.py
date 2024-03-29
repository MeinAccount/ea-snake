import copy
import multiprocessing
from typing import List, Callable

import numpy as np

from ea.dnn import Chromo, random_chromosome
from ea.store import Store
from game.simulation import dnn_to_handler, av_score


class Evolution:
    generation = 0
    selection_rate = 0.1
    mutation_rate = 0.01
    population_size = 50
    parents = int(population_size * selection_rate)

    save_mode = False

    def __init__(self) -> None:
        self.pool = multiprocessing.Pool()

    def genetic_evolution(self, population: List[Chromo],
                          best_receiver: Callable[[Chromo], None] = lambda x: None) -> None:
        while True:
            population_size = len(population) if population is not None else self.population_size
            print("generation: {0}, population: {1}, mutation_rate: {2}".format(
                str(self.generation), str(population_size), str(self.mutation_rate)))

            # 1. Selection
            chosen_parents = self._strongest_parents(population)
            best_receiver(chosen_parents[-1][0])

            # get n possible combinations
            # 2. Crossover (Rank selection)
            base_offsprings = np.apply_along_axis(
                lambda x: self._crossover(chosen_parents[x[0]][0], chosen_parents[x[1]][0]), 1,
                np.random.randint(0, len(chosen_parents), (self.population_size - self.parents, 2)))

            # 3. Mutation
            self._mutation(base_offsprings)

            # 4. store population
            population = np.ndarray.tolist(base_offsprings)
            population.extend(map(lambda t: t[0], chosen_parents))
            self.generation += 1

            if self.save_mode:
                Store.save(self.generation, population)

    @staticmethod
    def _crossover(x: Chromo, y: Chromo) -> Chromo:
        return Evolution._crossover_array(x[0], y[0]), Evolution._crossover_array(x[1], y[1])

    @staticmethod
    def _crossover_array(x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """crosses two numpy arrays"""
        mask = np.random.choice([True, False], x.shape)
        offspring = copy.deepcopy(x)
        offspring[mask] = y[mask]

        return offspring

    def _mutation(self, base_offsprings):
        for offspring in base_offsprings:
            (x, y) = offspring
            self._mutate_array(x)
            self._mutate_array(y)

    def _mutate_array(self, array):
        mask = np.random.choice([True, False], array.shape, p=[self.mutation_rate, 1 - self.mutation_rate])
        array[mask] = np.random.uniform(-1, 1, array.shape)[mask]  # TODO: perhaps generate less random data

    @staticmethod
    def _score_chromo(chromo):
        return chromo, av_score(dnn_to_handler(chromo), 3)

    def _strongest_parents(self, population):
        scores_for_chromosomes = self.pool.map(self._score_chromo, population)
        scores_for_chromosomes.sort(key=lambda x: x[1])

        top_performers = scores_for_chromosomes[-self.parents:]
        print([x[1] for x in top_performers])

        return top_performers

    def random_population(self) -> List[Chromo]:
        return list(map(random_chromosome, range(0, self.population_size)))
