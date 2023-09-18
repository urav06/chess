import random

from engine import Game, Color, Move
from bots.basebot import BaseBot

class RandomBot(BaseBot):

    def __init__(self, color: Color) -> None:
        super().__init__(color)

    def select_move(self, game: Game) -> Move:
        super().select_move(game)
        return random.choice(list(game.legal_moves(color=self.color)))