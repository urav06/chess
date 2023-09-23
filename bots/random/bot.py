import random
from typing import Optional

from bots.basebot import BaseBot
from engine import Color, Game, Move


class RandomBot(BaseBot):

    def __init__(self, color: Color) -> None:
        super().__init__(color)

    def select_move(self, game: Game) -> Optional[Move]:
        super().select_move(game)
        return random.choice(list(game.legal_moves(color=self.color)))