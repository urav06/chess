"""
Random Bot.
"""

import random
from typing import Optional

import chess
from bots.basebot import BaseBot


class RandomBot(BaseBot):

    def __init__(self, color: chess.Color, name: Optional[str] = None) -> None:
        super().__init__(color)
        self.name = name or self.name

    def select_move(self, board: chess.Board) -> chess.Move:
        return random.choice(list(board.legal_moves))
