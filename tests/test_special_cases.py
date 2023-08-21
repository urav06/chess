import unittest
import logging

from engine.fen_utils import to_fen, from_fen
from engine.game import Game
from engine.types import (
    Location, Move, MoveType, Piece,
    KING, BISHOP, ROOK,  # PieceTypes
    WHITE, BLACK,   # Colors
)


class TestSpecial(unittest.TestCase):

    game: Game

    @classmethod
    def setUpClass(cls) -> None:
        cls.game = Game()

    def setUp(self) -> None:
        self.game.reset()
        self.game.to_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
        self.game.active_pieces