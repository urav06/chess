from typing import Optional

import numpy as np

from bots.basebot import BaseBot
from bots.neural_network.model import sigmoid
from engine import Color, Game, Move


def seek_move(game: Game, move: Move) -> Game:
    #TODO: Add this as a proper feature in the engine.
    copy_game = Game()
    np.copyto(copy_game.board.board, game.board.board)
    np.copyto(copy_game.seek_board.board, game.seek_board.board)
    copy_game.active_pieces = game.active_pieces.copy()
    copy_game.seek_board_pieces = game.seek_board_pieces.copy()
    copy_game.active_color = game.active_color

    copy_game.execute_move(move)
    copy_game.active_color = ~copy_game.active_color
    return copy_game


class MinMaxBot(BaseBot):

    def __init__(self, color: Color, max_depth: int, name: Optional[str] = None) -> None:
        super().__init__(color)
        self.max_depth = max_depth
        self.name = name or f"minmaxbot_{str(color).lower()}_{max_depth}"

    def select_move(self, game: Game) -> Optional[Move]:
        super().select_move(game)
        moves = game.legal_moves(color=self.color)
        best_move = None
        best_score = float("-inf")
        for move in moves:
            score = self.evaluate(seek_move(game, move), depth=self.max_depth, a=float("-inf"), b=float("inf"))
            if score > best_score:
                best_move = move
                best_score = score
        return best_move

    def leaf_node_heuristics(self, game: Game) -> float:
        my_pieces = game.filter_color_pieces(color=self.color)
        opponent_pieces = game.filter_color_pieces(color=~self.color)

        advantage = (len(my_pieces) - len(opponent_pieces))/(len(my_pieces) + len(opponent_pieces))

        multiplier = 7
        return (sigmoid(multiplier * advantage) - 0.5) * 20

    def evaluate(self, game: Game, depth: int, a: int, b: int) -> float:

        if game.is_in_checkmate(self.color):
            return float("-inf")

        if game.is_in_checkmate(~self.color):
            return float("inf")

        if depth == 0 or game.is_in_stalemate(self.color) or game.is_in_stalemate(~self.color):
            return self.leaf_node_heuristics(game)

        scores = []
        for move in game.legal_moves(color=self.color):
            score = self.evaluate(seek_move(game, move), depth-1, a, b)
            scores.append(score)

            if game.active_color == self.color:
                a = max(a, score)

            else:
                b = min(b, score)

            if a - b < 0:
                break

        return max(scores) if game.active_color == self.color else min(scores)

    def __str__(self) -> str:
        return self.name
 