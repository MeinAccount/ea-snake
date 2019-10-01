import copy

import numpy as np

from constants import Constants
from game.simulation import dnn_to_handler, compute_score
from model import DeepNeuralNetModel


class DNNGeneticEvolutionTrainer:
    generation = 0
    selection_rate = 0.1
    mutation_rate = 0.01
    population_size = 100
    parents = int(population_size * selection_rate)

    def _save_population(self, population):
        model = DeepNeuralNetModel()
        for i in population:
            model.set_weights(i)
            model.save(Constants.MODEL_PATH.format(self.generation, hash(i)))

    def genetic_evolution(self, best_receiver=lambda x: None):
        population = self._initial_population()
        while True:
            population_size = len(population) if population is not None else self.population_size
            print("generation: " + str(self.generation) + ", population: " + str(
                population_size) + ", mutation_rate: " + str(self.mutation_rate))

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

    @staticmethod
    def _crossover(x, y):
        return (DNNGeneticEvolutionTrainer._crossover_array(x[0], y[0]),
                DNNGeneticEvolutionTrainer._crossover_array(x[1], y[1]))

    @staticmethod
    def _crossover_array(x, y):
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

    def _strongest_parents(self, population):
        scores_for_chromosomes = []
        for chromo in population:
            score = compute_score(dnn_to_handler(chromo))
            scores_for_chromosomes.append((chromo, score))
            print(score)

        scores_for_chromosomes.sort(key=lambda x: x[1])

        top_performers = scores_for_chromosomes[-self.parents:]
        top_scores = [x[1] for x in top_performers]
        print(top_scores)

        return top_performers

    def _initial_population(self):
        population = []
        for i in range(0, self.population_size):
            population.append((self._random_chromosome(Constants.MODEL_FEATURE_COUNT,
                                                       DeepNeuralNetModel.hidden_node_neurons),
                               self._random_chromosome(DeepNeuralNetModel.hidden_node_neurons, 3)))

        return population

    @staticmethod
    def _random_chromosome(n, m):
        return np.random.uniform(-1, 1, (n, m))


if __name__ == '__main__':
    trainer = DNNGeneticEvolutionTrainer()
    trainer.genetic_evolution()
