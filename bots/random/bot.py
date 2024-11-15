"""
Random Bot.
"""

import random
from typing import Optional

from bots.basebot import BaseBot
from engine import Color, Game, Move


class RandomBot(BaseBot):

    def __init__(self, color: Color, name: Optional[str] = None) -> None:
        super().__init__(color)
        self.name = name or self.name

    def select_move(self, game: Game) -> Move:
        super().select_move(game)
        return random.choice(list(game.legal_moves(color=self.color)))
