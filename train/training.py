import numpy as np
import numpy.typing as npt

from train.bot import Bot
from train.utils import generate_input_vector
from engine import Game
from engine.types import (
    WHITE,  # Colors
    KNIGHT  # PieceTypes
)
from train.constants import eta


def cost_derivative() -> npt.NDArray[np.float64]:
    return np.array([0])


def trainzzzzz():
    game = Game()
    bot = Bot([256, 180])
    moves = list(game.legal_moves())
    input_vector = generate_input_vector(game.board, moves, bot.layers[0])
    backpropogation(bot, input_vector, 0.1)


def backpropogation(bot: Bot, vectorized_input: npt.NDArray[np.int8]):
    activation = vectorized_input
    activations = [vectorized_input]
    zs = []
    for bias, weight in zip(bot.biases, bot.weights):
        z = np.dot(weight, activation) + bias
        zs.append(z)
        activation = bot.activation_fx(z)
        activations.append(activation)

    delta = cost_derivative() * bot.activation_fx_derivative(zs[-1])

    bot.biases[-1] = bot.biases[-1] - eta * delta
    bot.weights[-1] = bot.weights[-1] - eta * np.dot(delta, activations[-2].transpose())

    for layer in range(2, bot.layer_count):
        z = zs[-layer]
        afxp = bot.activation_fx_derivative(z)
        delta = np.dot(bot.weights[-layer+1].transpose(), delta) * afxp
        bot.biases[-layer] = bot.biases[-layer] - eta * delta
        bot.weights[-layer] = bot.weights[-layer] - eta * np.dot(delta, activations[-layer-1].transpose())


if __name__ == "__main__":
    trainzzzzz()
