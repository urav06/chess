
from bots.neural_network.model import sigmoid
from bots.basebot import BaseBot
from engine import Color, Game, Move


class MinMaxProBot(BaseBot):

    def __init__(self, color: Color, max_depth: int) -> None:
        super().__init__(color)
        self.alpha = float('-inf')
        self.beta = float('inf')
        self.max_depth = max_depth

    def select_move(self, game: Game) -> Move | None:
        super().select_move(game)
        move, score = self.evaluate(
            game=game,
            depth=self.max_depth,
        )
        print("Score for Search Tree is", score)
        return move

    def evaluation_by_heuristics(self, game: Game):

        param_a = len(game.board.get_pieces(color=Color.WHITE))
        param_b = len(game.board.get_pieces(color=Color.BLACK))
        return (
            sigmoid(
                (param_a - param_b) * (32/(param_a + param_b))
            )
            - 0.5
        ) * 10

    def evaluate(self, game: Game, depth: int):
        if depth == 0:
            score = self.evaluation_by_heuristics(game)
            my_turn = (game.active_color == self.color) 
            return None, score  

        my_turn = (game.active_color == self.color)
        score = float('-inf') if my_turn else float('inf')
        all_legal_moves = list(game.legal_moves(color=game.active_color))
        final_move = None

        for i, current_move in enumerate(all_legal_moves):
            if score in (float('inf'), float('-inf')):
                pass
            else:
                if my_turn:
                    if depth != self.max_depth and score <= self.beta:
                        break
                else:
                    if score <= self.alpha:
                        break 

            _, child_score = self.evaluate(
                game=game.seek_move(current_move),
                depth=depth-1
                )
            if my_turn and score < child_score:
                score = child_score
                final_move = current_move
            elif not my_turn and score > child_score:
                score = child_score

        if not my_turn and score > self.alpha: 
            self.alpha = score
        if my_turn and score < self.beta: 
            self.beta = score 

        return final_move, score
