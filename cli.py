#!/usr/bin/env python3

import argparse

from ea.evolution import Evolution
from ea.store import Store

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--load-gen', type=int)
    parser.add_argument('-f', '--load-file')
    parser.add_argument('-s', '--selection-rate', type=float, default=0.1)
    parser.add_argument('-m', '--mutation-rate', type=float, default=0.01)
    parser.add_argument('-p', '--population_size', type=int, default=100)
    args = parser.parse_args()

    trainer = Evolution()
    trainer.selection_rate = args.selection_rate
    trainer.mutation_rate = args.mutation_rate
    trainer.population_size = args.population_size

    if args.load_gen is not None:
        population = Store.loadGen(args.load_gen)
    elif args.load_file is not None:
        population = Store.loadGen(args.load_file)
    else:
        population = trainer.random_population()

    trainer.save_mode = True
    trainer.genetic_evolution(population)
