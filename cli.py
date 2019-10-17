#!/usr/bin/env python3

import argparse

from ea.evolution import Evolution
from ea.store import Store

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--load-gen', type=int)
    parser.add_argument('-l', '--load-latest', dest='load_latest', action='store_true', default=False)
    parser.add_argument('-f', '--load-file')
    parser.add_argument('-s', '--selection-rate', type=float, default=0.1)
    parser.add_argument('-m', '--mutation-rate', type=float, default=0.01)
    parser.add_argument('-p', '--population-size', type=int, default=100)
    parser.add_argument('-sm', '--save-mode', type=bool, default=True)
    args = parser.parse_args()

    trainer = Evolution()
    trainer.selection_rate = args.selection_rate
    trainer.mutation_rate = args.mutation_rate
    trainer.population_size = args.population_size

    if args.load_latest is True:
        print("Loading latest generation")
        gen = Store.get_latest_gen()
        population = Store.load_gen(gen)
        trainer.generation = gen
    elif args.load_gen is not None:
        print("Loading population from generation {}".format(args.load_gen))
        population = Store.load_gen(args.load_gen)
        trainer.generation = args.load_gen
    elif args.load_file is not None:
        print("Loading population from file " + args.load_file)
        population = Store.load_gen(args.load_file)
    else:
        print("Creating random population")
        population = trainer.random_population()

    trainer.save_mode = args.save_mode
    trainer.genetic_evolution(population)
