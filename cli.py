#!/usr/bin/env python3

import argparse

from ea.evolution import Evolution

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--resume', type=int)
    parser.add_argument('-s', '--selection-rate', type=float, default=0.1)
    parser.add_argument('-m', '--mutation-rate', type=float, default=0.01)
    parser.add_argument('-p', '--population_size', type=int, default=100)
    args = parser.parse_args()

    trainer = Evolution()
    trainer.load_gen = args.resume
    trainer.selection_rate = args.selection_rate
    trainer.mutation_rate = args.mutation_rate
    trainer.population_size = args.population_size

    trainer.save_mode = True
    trainer.genetic_evolution()
