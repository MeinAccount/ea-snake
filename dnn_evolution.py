import copy
import random
import pickle
import numpy as np
from pathlib import Path

from constants import Constants
from game.simulation import dnn_to_handler, compute_score
from model import DeepNeuralNetModel



class DNNGeneticEvolutionTrainer:
    generation = 0
    selection_rate = 0.1
    mutation_rate = 0.01
    population_size = 100
    parents = int(population_size * selection_rate)

    model = DeepNeuralNetModel()

    load_gen = 1
    save_mode = True

    def _save_population(self, population):
        folder = Path(Constants.MODEL_PATH.format("")[:-10])
        if not folder.exists():
            folder.mkdir(parents=True)

        with open(Constants.MODEL_PATH.format(self.generation), 'wb') as filehandler:
            pickle.dump(population, filehandler)



    def _load_population(self, generation):
        path = Constants.MODEL_PATH.format(generation)
        p = Path(path)
        if not p.exists():
            return None

        with open(p, 'rb') as filehandler:
            population = pickle.load(filehandler)

        return population

    def genetic_evolution(self, best_receiver=lambda x: None):
        population = self._initial_population()
        self._save_population(population)
        while True:
            population_size = len(population) if population is not None else self.population_size
            print("generation: " + str(self.generation) + ", population: " + str(
                population_size) + ", mutation_rate: " + str(self.mutation_rate))

            # 1. Selection
            chosen_parents = self._strongest_parents(population)
            best_receiver(chosen_parents[-1][0])

            # get n possible combinations
            # 2. Crossover (Rank selection)
            pairs = self._get_n_generations(chosen_parents, population_size - self.parents)
            # random.shuffle(pairs)

            base_offsprings = []
            for pair in pairs[:self.population_size]:
                # pair[i] is from _strongest_parents, so (cromo, score)
                base_offsprings.append(self._crossover(pair[0][0], pair[1][0]))

            # 3. Mutation
            self._mutation(base_offsprings)
            #population = new_population
            base_offsprings.extend(map(lambda t: t[0], chosen_parents))
            population = base_offsprings
            self.generation += 1

            if self.save_mode:
                self._save_population(population)

    def _get_n_generations(self, parents, n):
        combinations = []
        for i in range(n):
            r1 = random.randrange(0, len(parents))
            r2 = random.randrange(0, len(parents))
            combinations.append((parents[r1], parents[r2]))

        return combinations

    #def _combinations(self, parents):
    #    combinations = []
    #    for i in range(0, len(parents)):
    #        for j in range(i, len(parents)):
    #            combinations.append((parents[i], parents[j]))
    #    return combinations

    @staticmethod
    def _crossover(x, y):
        return (DNNGeneticEvolutionTrainer._crossover_array(x[0], y[0], Constants.MODEL_FEATURE_COUNT,
                                                       DeepNeuralNetModel.hidden_node_neurons),
                DNNGeneticEvolutionTrainer._crossover_array(x[1], y[1], DeepNeuralNetModel.hidden_node_neurons,
                                                            3
                                                       ))

    @staticmethod
    def _crossover_array(x, y, n, m):
        """crosses two numpy arrays"""
        offspring = copy.deepcopy(x)
        for i in range(n):
            for j in range(m):
                if random.choice([True, False]):
                    offspring[i][j] = y[i][j]
        return offspring

    def _mutation(self, base_offsprings):
        #offsprings = []
        for offspring in base_offsprings:
            #offspring_mutation = copy.deepcopy(offspring)
            #for i in range(0, Constants.MODEL_FEATURE_COUNT):
            #    for j in range(0, DeepNeuralNetModel.hidden_node_neurons):
            #        if np.random.choice([True, False], p=[self.mutation_rate, 1 - self.mutation_rate]):
            #            offspring_mutation[i][j] = random.uniform(-1, 1)
            (x, y) = offspring
            self._mutate_array(x, Constants.MODEL_FEATURE_COUNT,
                                                       DeepNeuralNetModel.hidden_node_neurons)
            self._mutate_array(y, DeepNeuralNetModel.hidden_node_neurons,
                               3,
                               )
            #offsprings.append(offspring_mutation)

        #return offsprings

    def _mutate_array(self, array, n, m):
        for i in range(n):
            for j in range(m):
                if np.random.choice([True, False], p=[self.mutation_rate, 1 - self.mutation_rate]):
                    array[i][j] =  random.uniform(-1, 1)

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
        if self.load_gen or self.load_gen == 0:
            pop = self._load_population(self.load_gen)
            if pop:
                self.generation = self.load_gen
                return pop

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
