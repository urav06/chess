from typing import Any
from numpy import ndarray, dtype, floating
from bots.model import sigmoid
from engine import Game, Color, Board


def evaluation_by_heuristics(game: Game):

    param_a = len(game.filter_color_pieces(color=Color.WHITE))
    param_b = len(game.filter_color_pieces(color=Color.BLACK))
    return (
        sigmoid(
            (param_a - param_b) * (32/(param_a + param_b))
        )
        - 0.5
    ) * 10


class SearchTree:
    def __init__(self):
        self.alpha = float("inf")
        self.beta = float("-inf")
        self.count = 0

    def search_and_evaluation(
        self, game: Game, depth: int, state: bool
    ):  # state is 0 for max and 1 for min

        self.count = self.count+1
        color = Color.WHITE if state else Color.BLACK
        if depth == 0:
            x = evaluation_by_heuristics(game)
            return x
        else:
            all_legal_moves = game.legal_moves(color=color)
            score = float("inf")
            if state:
                score = float("-inf")

            for i, current_move in enumerate(all_legal_moves):
                if state:
                    if score in (float("inf"), float("-inf")):
                        pass
                    elif score >= self.alpha:
                        break
                    else:
                        self.alpha = score
                else:
                    if score in (float("inf"), float("-inf")):
                        pass
                    elif score <= self.beta:
                        break
                    else:
                        self.beta = score
                child_score = self.search_and_evaluation(
                    game.seek_move(current_move), depth - 1, state=not state
                )

                score = max(score, child_score) if state else min(score, child_score)

            return score
