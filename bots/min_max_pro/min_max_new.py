"""
MinMax Pro Bot Main File
"""
import chess
from typing import Optional
from bots.neural_network.model import sigmoid
from bots.basebot import BaseBot


class MinMaxProBot(BaseBot):
    def __init__(
        self, color: chess.Color, max_depth: int, name: Optional[str] = None
    ) -> None:
        super().__init__(color)
        self.alpha = float("-inf")
        self.beta = float("inf")
        self.max_depth = max_depth
        self.name = name or f"{self.name}_d{max_depth}"
        self.weight = {
            chess.KING: 100,
            chess.QUEEN: 9,
            chess.ROOK: 5,
            chess.BISHOP: 3,
            chess.KNIGHT: 3,
            chess.PAWN: 1,
        }

    def select_move(self, board: chess.Board) -> chess.Move:
        # super().select_move(board)
        move, score = self.evaluate(
            board=board,
            depth=self.max_depth,
        )
        if move is None:
            raise ValueError("I have no legal moves!")
        return move

    def evaluation_by_heuristics(self, board: chess.Board):
        param_a = sum(
            len(board.pieces(piece_type=p, color=self.color))*self.weight[p]
            for p in chess.PIECE_TYPES
            )
        param_b = sum(
            len(board.pieces(piece_type=p, color=~self.color))*self.weight[p]
            for p in chess.PIECE_TYPES
            )
        # param_a = sum(self.weight[piece.type] for piece, _,_ in board_a)
        # param_b = sum(self.weight[piece.type] for piece, _, _ in board_b)
        return (sigmoid((param_a - param_b) * (32 / (param_a + param_b))) - 0.5) * 10

    def evaluate(self, board: chess.Board, depth: int):
        my_turn = board.turn is self.color
        score = float("-inf") if my_turn else float("inf")
        final_move = None

        if depth == 0:
            score = self.evaluation_by_heuristics(board=board)
            return final_move, score

        all_legal_moves = list(board.legal_moves)
        final_move = all_legal_moves[0]

        for current_move in all_legal_moves:
            if score not in (float("inf"), float("-inf")):
                if my_turn and depth != self.max_depth and score <= self.beta:
                    break
                if not my_turn and score <= self.alpha:
                    break

            # if game.is_in_checkmate(self.color):
            #     print("A")
            #     return None, float('-inf')
            # if game.is_in_checkmate(~self.color):
            #     print("B")
            #     return current_move, float('inf')

            _, child_score = self.evaluate(
                board=self.seek_move(board=board,
                                     move=current_move),
                depth=depth - 1
            )

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

    @staticmethod
    def seek_move(board: chess.Board, move: chess.Move) -> chess.Board:
        seek = board.copy(stack=False)
        seek.push(move)
        return seek
