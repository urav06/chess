"""
Bot class
"""
import numpy as np
import numpy.typing as npt

from engine import Game
from train.utils import generate_input_vector


class Bot:

    def __init__(self, layers: list[int]) -> None:
        input_layer = (8 * 8 * 4) + 150*(3 * 2)
        output_layer = 150
        layers = [input_layer, *layers, output_layer]
        self.layer_count = len(layers)
        self.layers = layers
        self.activation_fx = self.sigmoid
        self.activation_fx_derivative = self.sigmoid_derivative

        rng = np.random.default_rng()
        self.biases = [rng.standard_normal((y, 1)) for y in layers[1:]]
        self.weights = [rng.standard_normal((y, x)) for x, y in zip(layers[:-1], layers[1:])]

    def feed_forward(self, activation: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        """
        Feed forward the activation through the network.

        Note: activation is a numpy array of shape (n, 1)
        where n is the number of neurons in the input layer

        :param activation: activation
        :return: activation
        """
        for bias, weight in zip(self.biases, self.weights):
            activation = self.activation_fx(np.dot(weight, activation) + bias)
        return activation

    def infer_move(self, game: Game) -> npt.NDArray[np.float64]:
        moves = list(game.legal_moves())
        input_vector = generate_input_vector(game.board, moves, self.layers[0])

        index = np.argmax(self.feed_forward(input_vector.reshape((self.layers[0], 1))))
        return moves[index] if index < len(moves) else "Bot picked out of bounds"

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def relu(x):
        return np.maximum(0, x)

    @staticmethod
    def sigmoid_derivative(x):
        return Bot.sigmoid(x) * (1 - Bot.sigmoid(x))

    @staticmethod
    def relu_derivative(x):
        return np.where(x <= 0, 0, 1)
