
from bots.neural_network.model import sigmoid
from bots.basebot import BaseBot
from engine import Color, Game, Move, PieceType


class MinMaxProBot(BaseBot):

    def __init__(self, color: Color, max_depth: int) -> None:
        super().__init__(color)
        self.alpha = float('-inf')
        self.beta = float('inf')
        self.max_depth = max_depth
        self.WEIGHT = {
            PieceType.KING: 100,
            PieceType.QUEEN: 9,
            PieceType.ROOK: 5,
            PieceType.BISHOP: 3,
            PieceType.KNIGHT: 3,
            PieceType.PAWN: 1
        }

    def select_move(self, game: Game) -> Move | None:
        super().select_move(game)
        move, score = self.evaluate(
            game=game,
            depth=self.max_depth,
        )
        print("Score for Search Tree is", score)
        return move

    def evaluation_by_heuristics(self, game: Game):

        board_a = game.board.get_pieces(color=self.color)
        board_b = game.board.get_pieces(color=~self.color)
        param_a = sum(self.WEIGHT[piece.type] for piece, location in board_a)
        param_b = sum(self.WEIGHT[piece.type] for piece, location in board_b)
        return (
            sigmoid(
                (param_a - param_b) * (32/(param_a + param_b))
            )
            - 0.5
        ) * 10

    def evaluate(self, game: Game, depth: int):

        my_turn = (game.active_color == self.color)
        score = float('-inf') if my_turn else float('inf')
        final_move = None

        if depth == 0:
            score = self.evaluation_by_heuristics(game)
            return final_move, score

        if game.is_in_checkmate(self.color):
            print("A")
            return None, float('-inf')
        if game.is_in_checkmate(~self.color):
            print("B")
            return None, float('inf') - 1 

        all_legal_moves = list(game.legal_moves(color=game.active_color))

        final_move = all_legal_moves[0]

        for current_move in all_legal_moves:

            if score not in (float('inf'), float('-inf')):
                if (
                    my_turn
                    and depth != self.max_depth
                    and score <= self.beta
                ):
                    break
                elif not my_turn and score <= self.alpha:
                    break

            _, child_score = self.evaluate(
                game=game.seek_move(current_move),
                depth=depth-1
                )
            if child_score == float("inf")-1:
                final_move = current_move

            # if depth == self.max_depth:
                # print("Turn is", my_turn)
            if my_turn and depth == self.max_depth:
                score = min(score, child_score)
                if score == child_score:
                    final_move = current_move
                continue

            score = max(score, child_score)

        if my_turn:
            self.beta = min(score, self.beta)
        else:
            self.alpha = max(score, self.alpha)

        return final_move, score
