
from bots.neural_network.model import sigmoid
from engine import Game, Color, Move
from bots.basebot import BaseBot


def evaluation_by_heuristics(game: Game):

    param_a = len(game.board.get_pieces(color=Color.WHITE))
    param_b = len(game.board.get_pieces(color=Color.BLACK))
    return (
        sigmoid(
            (param_a - param_b) * (32/(param_a + param_b))
        )
        - 0.5
    ) * 10


class SearchTree(BaseBot):
    def __init__(self, color):
        super().__init__(color)
        self.alpha = float("inf")
        self.beta = float("-inf")
        self.count = 0

    def select_move(self, game: Game) -> Move | None:
        super().select_move(game)
        move, score = self.search_and_evaluation(
            game=game,
            depth=10,
            state=(self.color == Color.WHITE)
        )
        return move

    def search_and_evaluation(
        self, game: Game, depth: int, state: bool
    ):  # state is 0 for max and 1 for min

        self.count = self.count+1
        color = Color.WHITE if state else Color.BLACK
        final_move = None
        if depth == 0:
            x = evaluation_by_heuristics(game)
            return None, x
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
                _, child_score = self.search_and_evaluation(
                    game.seek_move(current_move), depth - 1, state=not state
                )
                check_score = score
                score = max(score, child_score) if state else min(score, child_score)
                if check_score != score:
                    final_move = current_move

            return final_move, score
