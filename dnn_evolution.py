import copy
import random

from model import DeepNeuralNetModel
import numpy as np
from constants import Constants

class DNNEvolutionSolver:
    model = DeepNeuralNetModel("/dnn_genetic_evolution/")

    def __init__(self):
        pass

    def move(self, environment):
        predicted_action = self._predict(environment, self.model)
        return predicted_action

    def _predict(self, environment, model):
        predictions = []
        # todo add action class
        actions = [Action.left_neighbor(environment.snake_action), environment.snake_action,
                   Action.right_neighbor(environment.snake_action)]


        for action in actions:
            observation_for_prediction = environment.observation(action)
            predictions.append(
                model.model.predict(np.array(observation_for_prediction).reshape(-1, Constants.MODEL_FEATURE_COUNT, 1))
            )
        best_prediction_index = np.argmax(np.array(predictions))

        return actions[best_prediction_index]

class DNNGeneticEvolutionTrainer:
    generation = 0
    selection_rate = 0.1
    mutation_rate = 0.01
    population_size = 1000
    parents = int(population_size * selection_rate)
    model = DeepNeuralNetModel("/dnn_genetic_evolution/")

    def _genetic_evolution(self):
        population = None
        while True:
            population_size = len(population) if population is not None else self.population_size
            print ("generation: " + str(self.generation) + ", population: " + str(population_size) + ", mutation_rate: " + str(self.mutation_rate))

            # 1. Selection
            parents = self._strongest_parents(population)

            self._save_model(parents)  # Saving main model based on the current best two chromosomes

            # 2. Crossover (Roulette selection)
            pairs = []
            #while len(pairs) != self.population_size:
            #    pairs.append(self._pair(parents))

            # todo higher rank should get higher prob
            # # 2. Crossover (Rank selection)
            pairs = self._combinations(parents)
            random.shuffle(pairs)
            pairs = pairs[:self.population_size]

            base_offsprings = []
            for pair in pairs:
                offsprings = self._crossover(pair[0][0], pair[1][0])
                base_offsprings.append(offsprings[-1])

            # 3. Mutation
            new_population = self._mutation(base_offsprings)
            population = new_population
            self.generation += 1

    def _combinations(self, parents):
        combinations = []
        for i in range(0, len(parents)):
            for j in range(i, len(parents)):
                combinations.append((parents[i], parents[j]))
        return combinations

    def _crossover(self, x, y):
        offspring_x = x
        offspring_y = y
        for i in range(0, Constants.MODEL_FEATURE_COUNT):
            for j in range(0, self.model.hidden_node_neurons):
                if random.choice([True, False]):
                    offspring_x[i][j] = y[i][j]
                    offspring_y[i][j] = x[i][j]
        return offspring_x, offspring_y

    def _mutation(self, base_offsprings):
        offsprings = []
        for offspring in base_offsprings:
            offspring_mutation = copy.deepcopy(offspring)
            for i in range(0, Constants.MODEL_FEATURE_COUNT):
                for j in range(0, self.model.hidden_node_neurons):
                    if np.random.choice([True, False], p=[self.mutation_rate, 1-self.mutation_rate]):
                        offspring_mutation[i][j] = random.uniform(-1, 1)
            offsprings.append(offspring_mutation)
        return offsprings


    def _strongest_parents(self, population):
        if population is None:
            population = self._initial_population()
        scores_for_chromosomes = []
        for i in range(len(population)):
            chromosome = population[i]
            scores_for_chromosomes.append((chromosome, self._gameplay_for_chromosome(chromosome)))
            #if i == len(population)-1:
            #    print "\r"+"\033[K"+"\r",
            #else:
            #    print "\r" + str(i + 1) + " out of " + str(len(population)),

        scores_for_chromosomes.sort(key=lambda x: x[1])
        #print "population: " + str(mean([x[1] for x in scores_for_chromosomes]))

        top_performers = scores_for_chromosomes[-self.parents:]
        top_scores = [x[1] for x in top_performers]
        #print "top " + str(self.selection_rate) + ": " + "(min: " + str(min(top_scores)) + ", avg: " + str(mean(top_scores)) + ", max: " + str(max(top_scores)) + ")"
        #print ""
        return top_performers

    def _gameplay_for_chromosome(self, chromosome):
        self.model.set_weights(chromosome)
        #environment = self.prepare_training_environment()
        while True:
            predicted_action = self._predict(environment)

            # todo: return score if finished
            # - zero score for no finish or

    def _initial_population(self):
        chromosomes = []
        for i in range(0, self.population_size):
            chromosome = []
            for j in range(0, Constants.MODEL_FEATURE_COUNT):
                chromosome.append(self._random_chromosome(self.model.hidden_node_neurons))
            chromosomes.append(chromosome)
        return chromosomes

    def _random_chromosome(self, size):
        chromosome = []
        for i in range(0, size):
            random_value = random.uniform(-1, 1)
            chromosome.append(random_value)
        return chromosome




