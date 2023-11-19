"""
Minmax bot.
"""
import random
from typing import Optional

from bots.basebot import BaseBot
from engine import Color, Game, Move, PieceType


class MinMaxBot(BaseBot):

    def __init__(self, color: Color, max_depth: int, name: Optional[str] = None) -> None:
        super().__init__(color)
        self.max_depth = max_depth
        self.name = name or f"{self.name}_d{max_depth}"

    def select_move(self, game: Game) -> Optional[Move]:
        super().select_move(game)
        moves = game.legal_moves(color=self.color)
        scored_moves: list[tuple[Move, float]]  = []
        best_score = float("-inf")
        for move in moves:
            score = self.evaluate(
                game.seek_move(move), depth=self.max_depth, a=float("-inf"), b=float("inf")
            )
            scored_moves.append((move, score))
            if score > best_score:
                best_score = score
        return random.choice([move for move, score in scored_moves if score == best_score])

    def leaf_node_heuristics(self, game: Game) -> float:

        piece_weights: dict[PieceType, float] = {
            PieceType.PAWN: 1,
            PieceType.KNIGHT: 3,
            PieceType.BISHOP: 3,
            PieceType.ROOK: 5,
            PieceType.QUEEN: 9,
            PieceType.KING: 100
        }

        my_pieces = game.board.get_pieces(color=self.color)
        opponent_pieces = game.board.get_pieces(color=~self.color)

        advantage = (
            (
                sum(map(lambda x: piece_weights[x[0].type], my_pieces))
                - sum(map(lambda x: piece_weights[x[0].type], opponent_pieces))
            ) / (
                sum(map(lambda x: piece_weights[x[0].type], my_pieces))
                + sum(map(lambda x: piece_weights[x[0].type], opponent_pieces))
            )
        )
        return advantage * 20

    def evaluate(self, game: Game, depth: int, a: int, b: int) -> float:

        its_my_turn = game.active_color == self.color

        if game.is_in_checkmate(game.active_color):
            return float("-inf") if its_my_turn else float("inf")

        if depth == 0 or game.is_in_stalemate(game.active_color):
            return self.leaf_node_heuristics(game)

        scores = []
        for move in game.legal_moves(color=game.active_color):
            score = self.evaluate(game.seek_move(move), depth-1, a, b)
            scores.append(score)

            if its_my_turn:
                a = max(a, score)

            else:
                b = min(b, score)

            if a - b < 0:
                break

        return max(scores) if its_my_turn else min(scores)

    def __str__(self) -> str:
        return self.name
 