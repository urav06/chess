from typing import Optional

import numpy as np
import numpy.typing as npt

from bots.neural_network.model import Network, sigmoid, sigmoid_derivative, activation_fx_type
from engine import Board, Game, Move


class NNBot:

    def __init__(
        self,
        hidden_layers: list[int],
        activation_fx: Optional[activation_fx_type] = None,
        activation_fx_derivative: Optional[activation_fx_type] = None
    ):
        self.input_layer = (64 * 4) + (150 * 6)  # 64 squares + 150 moves
        self.output_layer = 150  # 150 moves
        self.network = Network(
            [self.input_layer, *hidden_layers, self.output_layer],
            activation_fx or sigmoid,
            activation_fx_derivative or sigmoid_derivative
        )

    def select_move(self, game: Game) -> int:
        moves: list[Move] = list(game.legal_moves())
        input_vector = self.generate_input_vector(game, moves).astype(np.float64)
        output_vector = self.network.feed_forward(input_vector)
        return np.argmax(output_vector)  # type: ignore

    def train(self, board: Board, moves: list[Move], eta: float) -> None:
        input_vector = self.generate_input_vector(board, moves).astype(np.float64)
        delta = np.concatenate((
            np.zeros((len(moves), 1)),
            np.full((self.output_layer-len(moves), 1), -1),
        ))
        self.network.backprop(input_vector, delta, eta)

    def generate_input_vector(self, board: Board, moves: list[Move]) -> npt.NDArray[np.int8]:
        return np.concatenate((
            board.board.reshape(-1, 1),
            self.serialize_moves(moves).reshape(-1, 1),
            np.full((self.input_layer - (64 * 4) - (len(moves) * 6), 1), -1)
        ))

    @staticmethod
    def serialize_moves(moves: list[Move]) -> npt.NDArray[np.int8]:
        return np.array([
            [
                move.start,
                move.end,
                (move.type, move.promotion_rank or move.castle_type or move.target or 0)
            ]
            for move in moves
        ])
