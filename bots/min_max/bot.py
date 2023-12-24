"""
Minmax bot.
"""
import random
from typing import Optional

import chess
from bots.basebot import BaseBot


class MinMaxBot(BaseBot):

    def __init__(self, color: chess.Color, max_depth: int, name: Optional[str] = None) -> None:
        super().__init__(color)
        self.max_depth = max_depth
        self.name = name or f"{self.name}_d{max_depth}"

    def select_move(self, board: chess.Board) -> chess.Move:
        moves = board.legal_moves
        scored_moves: list[tuple[chess.Move, float]] = []
        best_score = float("-inf")
        for move in moves:
            score = self.evaluate(self.seek(board, move), self.max_depth, float("-inf"), float("inf"))
            scored_moves.append((move, score))
            best_score = max(best_score, score)
        if len(scored_moves) == 0:
            raise ValueError("I have no legal moevs!")
        return random.choice([m for m, s in scored_moves if s == best_score])

    def evaluate(self, board: chess.Board, depth: int, a: float, b: float) -> float:

        its_my_turn = board.turn is self.color

        if (outcome := board.outcome()):
            if outcome.winner is None:
                return self.leaf_node_heuristics(board)
            elif outcome.winner is self.color:
                return float("inf")
            elif outcome.winner is (not self.color):
                return float("-inf")
            else:
                raise ValueError(f"Unexpected outcome.winner value: {outcome.winner} for outcome {outcome}")

        if depth == 0:
            return self.leaf_node_heuristics(board)

        scores = []
        for move in board.legal_moves:
            score = self.evaluate(self.seek(board, move), depth-1, a, b)
            scores.append(score)

            if its_my_turn:
                a = max(a, score)
            
            else:
                b = min(b, score)

            if a - b > -2:
                break

        return a if its_my_turn else b


    def leaf_node_heuristics(self, board: chess.Board) -> float:
        weights: dict[chess.PieceType, float] = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 10
        }

        my_piece_score = sum(
            len(board.pieces(p, self.color))*weights[p] for p in chess.PIECE_TYPES
        )
        opponent_piece_score = sum(
            len(board.pieces(p, not self.color))*weights[p] for p in chess.PIECE_TYPES
        )

        return 20 * (my_piece_score - opponent_piece_score)/(my_piece_score + opponent_piece_score)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def seek(board: chess.Board, move: chess.Move) -> chess.Board:
        seek = board.copy(stack=False)
        seek.push(move)
        return seek