import multiprocessing
import queue
import threading

import gui
from ea.evolution import Evolution
from game.simulation import dnn_to_handler
from game.state import GameState
from render import App


class QueueHandler:
    current_handler = None

    def __init__(self) -> None:
        self.queue = multiprocessing.Queue()

    def handler(self, state: GameState) -> int:
        if self.current_handler is None:
            return 0

        return self.current_handler(state)

    def update(self):
        try:
            cromo = self.queue.get_nowait()
            self.current_handler = dnn_to_handler(cromo)
            app = App(self.handler, self.update)
            gui.insert(app)
            print("renderer updated")
        except queue.Empty:
            pass


if __name__ == '__main__':
    handler = QueueHandler()


    def worker1():
        trainer = Evolution()
        trainer.genetic_evolution(handler.queue.put)


    thread = threading.Thread(target=worker1)
    thread.start()
    thread2 = threading.Thread(target=gui.test(handler))
    thread2.start()
