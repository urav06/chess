from bots.model import sigmoid
from engine import Game, Color, Board


def evaluation_by_heuristics(game: Game) -> int:
    return (
        sigmoid(
            len(game.filter_color_pieces(color=Color.WHITE))
            - len(game.filter_color_pieces(color=Color.BLACK))
        )
        - 0.5
    ) * 10


class SearchTree:
    def __init__(self):
        self.alpha = float("inf")
        self.beta = float("-inf")
        # self.base_values =[]
        # self.cur_val = 0

    def search_and_evaluation(
        self, game: Game, depth: int, state: bool
    ):  # state is 0 for max and 1 for min
        if depth == 0:
            # self.cur_val = (self.cur_val + 1) %4
            x = evaluation_by_heuristics(game)
            # x = self.base_values[self.cur_val]
            return x
        else:
            all_legal_moves = game.legal_moves()
            out_value = float("inf")
            if state:
                out_value = float("-inf")

            for i, current_move in enumerate(all_legal_moves):
                print(depth, i)
                print("Alpha and beta values are", self.alpha, self.beta)
                value = self.search_and_evaluation(
                    game.seek_move(current_move), depth - 1, state=not state
                )
                if state:
                    if value > self.alpha:
                        ...
                    else:
                        self.alpha = value

                else:
                    if value < self.beta:
                        ...
                    else:
                        self.beta = value
                out_value = max(out_value, value) if state else min(out_value,
                                                                    value)

            return out_value
