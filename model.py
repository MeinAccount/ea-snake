import os

import numpy as np
import tflearn
from tflearn import input_data, fully_connected, regression

from constants import Constants

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Disables TF warnings


class DeepNeuralNetModel:
    # __metaclass__ = Singleton
    hidden = None
    hidden_node_neurons = Constants.MODEL_FEATURE_COUNT * Constants.MODEL_LAYER_COUNT ** 2

    def __init__(self):
        network = input_data(shape=[None, Constants.MODEL_FEATURE_COUNT, 1])
        self.hidden = network = fully_connected(network, self.hidden_node_neurons, activation='relu6')
        network = fully_connected(network, 3, activation='linear')
        network = regression(network, optimizer='adam', loss='mean_square')
        self.model = tflearn.DNN(network)

    def save(self, path):
        self.model.save(path)

    def load(self, path):
        self.model.load(path)

    def get_weights(self):
        return self.model.get_weights(self.hidden.W)

    def set_weights(self, weights):
        self.model.set_weights(self.hidden.W, weights)

    def predict(self, angle, neighbours_free):
        """
        :param angle: angle to apple in [-1, 1)
        :param neighbours_free: list of three bools denoting [left free, forward free, right free]
        :return: direction with (left: -1, forward: 0, right: 1)
        """
        pred = self.model.predict(np.array([angle, *neighbours_free]).reshape((1, 4, 1)))
        return np.argmax(pred) - 1
