"""
This module contains the neural network model.
"""
from collections.abc import Callable

import numpy as np
import numpy.typing as npt

activation_fx_type = Callable[[npt.NDArray[np.float64]], npt.NDArray[np.float64]]


def sigmoid(x: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
    return 1 / (1 + np.exp(-x))


def relu(x: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
    return np.maximum(0, x)


def sigmoid_derivative(x: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
    return sigmoid(x) * (1 - sigmoid(x))


def relu_derivative(x: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
    return np.where(x <= 0, 0, 1)


class Network:

    def __init__(
        self,
        layers: list[int],
        activation_fx: activation_fx_type,
        activation_fx_derivative: activation_fx_type
    ) -> None:

        self.layers = layers
        self.activation_fx = activation_fx
        self.activation_fx_derivative = activation_fx_derivative

        rng = np.random.default_rng()
        self.biases = [rng.standard_normal((y, 1)) for y in layers[1:]]
        self.weights = [rng.standard_normal((y, x)) for x, y in zip(layers[:-1], layers[1:])]

    def feed_forward(self, activation: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        for bias, weight in zip(self.biases, self.weights):
            activation = self.activation_fx(np.dot(weight, activation) + bias)
        return activation

    def backprop(
        self,
        input: npt.NDArray[np.float64],  # Input vector
        adjustments: npt.NDArray[np.float64],  # Adjustment vector
        eta: float  # Learning rate
    ) -> None:
        delta = -adjustments
        activation = input
        activations = [input]
        zs = []
        for bias, weight in zip(self.biases, self.weights):
            z = np.dot(weight, activation) + bias
            zs.append(z)
            activation = self.activation_fx(z)
            activations.append(activation)

        delta = delta * self.activation_fx_derivative(zs[-1])
        self.biases[-1] = self.biases[-1] - eta*delta
        self.weights[-1] = self.weights[-1] - eta*np.dot(delta, activations[-2].transpose())

        for layer in range(2, len(self.layers)):
            z = zs[-layer]
            afxd = self.activation_fx_derivative(z)
            delta = np.dot(self.weights[-layer+1].transpose(), delta) * afxd
            self.biases[-layer] = self.biases[-layer] - eta*delta
            self.weights[-layer] = self.weights[-layer] - eta*np.dot(delta, activations[-layer-1].transpose())

    def save(self, file: str) -> None:
        data = np.array(
            [
                np.array(self.biases, dtype=object),
                np.array(self.weights, dtype=object),
            ],
            dtype=object
        )
        np.save(f"bots/weights/{file}", data, allow_pickle=True)

    def load(self, file: str) -> None:
        data = np.load(f"bots/weights/{file}.npy", allow_pickle=True)
        self.biases = list(data[0])
        self.weights = list(data[1])
