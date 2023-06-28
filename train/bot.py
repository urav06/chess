"""
Bot class
"""
import numpy as np
import numpy.typing as npt


class Bot:

    def __init__(self, layers: list[int]) -> None:
        self.layer_count = len(layers)
        self.layers = layers

        rng = np.random.default_rng()
        self.biases = np.array(
            [rng.standard_normal((y, 1)) for y in layers[1:]],
            dtype=object
        )
        self.weights = np.array(
            [rng.standard_normal((y, x)) for x, y in zip(layers[:-1], layers[1:])],
            dtype=object
        )

    def feed_forward(self, activation: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        """
        Feed forward the activation through the network.

        Note: activation is a numpy array of shape (n, 1)
        where n is the number of neurons in the input layer

        :param activation: activation
        :return: activation
        """
        for bias, weight in zip(self.biases, self.weights):
            activation = np.dot(weight, activation) + bias
        return activation
