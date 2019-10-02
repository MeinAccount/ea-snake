from typing import Callable, Tuple, List, Iterator
import numpy as np
from ea.dnn import MODEL_FEATURE_COUNT, MODEL_HIDDEN_NEURONS
import click
import pickle
from pathlib import Path
from ea.store import Store


@click.command()
@click.argument('old_path', help="Filename for the old pickle file")
@click.argument('new_path', help="Filename for the new pickle file")
@click.option('--amount', default=3, help='Amount of random rows added to the matrix')
def cli(old_path, new_path, amount):
    """Takes a pickle file and adds amount of rows to the weights matricies of the whole population"""
    p = Path(old_path)
    if not p.exists():
        click.echo("File does not exist")
    new_pop = add_weights_population(Store.loadFile(p))
    Store.save(0, new_pop, path=new_path)
    click.echo('Saved new pickle file in {}'.format(new_path))


def add_weights_population(population: List[Tuple[np.ndarray, np.ndarray]], amount) -> Iterator[
    Tuple[np.ndarray, np.ndarray]]:
    pop = map(lambda x: (x, amount), population)
    return map(add_weights_chromo, pop)


def add_weights_chromo(ch_pop: Tuple[Tuple[np.ndarray, np.ndarray], int]) -> Tuple[np.ndarray, np.ndarray]:
    (chromo, amount) = ch_pop
    a, b = chromo
    # we need a amount x MODEL_HIDDEN_NEURONS matrix
    return np.concatenate(a, np.random.uniform(-1, 1, (amount, MODEL_HIDDEN_NEURONS))), b


if __name__ == "__main__":
    cli()
