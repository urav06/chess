"""
Base test case for all pieces.
"""
import unittest

from engine import Game
from engine.types import (
    BLACK , WHITE,  # Colors
    KING,  # PieceTypes
)

class BaseTestPiece(unittest.TestCase):

    game: Game

    @classmethod
    def setUpClass(cls) -> None:
        cls.game = Game()

    def setUp(self) -> None:
        self.game.reset()
        self.game.add_piece((0, 4), (BLACK, KING))
        self.game.add_piece((7, 4), (WHITE, KING))
