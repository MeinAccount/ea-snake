#!/usr/bin/env python3


from pathlib import Path
from typing import Tuple, List, Iterator

import click
import numpy as np

from ea.dnn import MODEL_HIDDEN_NEURONS, Chromo
from ea.store import Store


@click.command()
@click.argument('old_path')
@click.argument('new_path')
@click.option('--amount', default=3, help='Amount of random rows added to the matrix')
def cli(old_path, new_path, amount):
    """ Takes a pickle file and adds amount of rows to the weights matrices of the whole population
    :param old_path: Filename for the old pickle file
    :param new_path: Filename for the new pickle file
    :param amount: Amount of random rows added to the matrix
    """
    p = Path(old_path)
    if not p.exists():
        click.echo("File does not exist")
    # new_pop = add_weights_population(Store.loadFile(p), amount)
    new_pop = add_weights_to_best(Store.loadFile(p), amount)
    Store.save(0, list(new_pop))
    click.echo('Saved new pickle file in {}'.format(new_path))


def add_weights_population(population: List[Tuple[np.ndarray, np.ndarray]], amount) -> Iterator[Chromo]:
    pop = map(lambda x: (x, amount), population)
    return map(add_weights_chromo, pop)


def add_weights_chromo(ch_pop: Tuple[Tuple[np.ndarray, np.ndarray], int]) -> Chromo:
    (chromo, amount) = ch_pop
    x, y = chromo
    # we need a amount x MODEL_HIDDEN_NEURONS matrix
    return np.vstack([x, np.zeros((amount, MODEL_HIDDEN_NEURONS))]), \
           np.identity(MODEL_HIDDEN_NEURONS), y


def add_weights_to_best(population: List[Tuple[np.ndarray, np.ndarray]], amount: int) -> Iterator[Chromo]:
    return map(lambda _: add_weights_chromo((population[0], amount)), range(0, 100))


if __name__ == "__main__":
    cli()
