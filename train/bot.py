"""
Bot class
"""
import numpy as np
import numpy.typing as npt

from engine import Game, Move
from engine.types import (
    PASSING, CAPTURE, CASTLE, PROMOTION, CAPTURE_AND_PROMOTION
)


class Bot:

    def __init__(self, layers: list[int]) -> None:
        input_layer = (8 * 8 * 4) + 150*(3 * 2)
        output_layer = 150
        layers = [input_layer, *layers, output_layer]
        self.layer_count = len(layers)
        self.layers = layers

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
            activation = np.dot(weight, activation) + bias
        return activation

    def infer_move(self, game: Game) -> npt.NDArray[np.float64]:
        moves = list(game.legal_moves())
        input_data = np.concatenate((
            game.board.board.reshape(-1),
            np.array(list(map(self.vectorize_move, moves))).reshape(-1),
            np.full((self.layers[0] - 256 - (len(moves)*6)), -1),
        ))

        index = np.argmax(self.feed_forward(input_data.reshape((self.layers[0], 1))))
        return moves[index] if index < len(moves) else "Bot picked out of bounds"



    @staticmethod
    def vectorize_move(move: Move) -> npt.NDArray[np.int8]:
        if move.type is PASSING:
            return np.array([move[0], move[1], [PASSING, 0]])
        elif move.type is CAPTURE:
            return np.array([move[0], move[1], [CAPTURE, move.target]])
        elif move.type is CASTLE:
            return np.array([move[0], move[1], [CASTLE, move.castle_type]])
        elif move.type is PROMOTION:
            return np.array([move[0], move[1], [PROMOTION, move.promotion_rank]])
        elif move.type is CAPTURE_AND_PROMOTION:
            return np.array([move[0], move[1], [CAPTURE_AND_PROMOTION, move.promotion_rank]])
        else:
            raise ValueError(f"Invalid move type: {move.type}")
