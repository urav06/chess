"""
Unittests for knight movement logic
"""
import unittest
import logging

from engine.game import Game
from engine.types import (
    Color, Location, Move, MoveType, Piece, PieceType,
    KING, KNIGHT,# PieceTypes
    WHITE, BLACK, # Colors
)


class TestKnight(unittest.TestCase):

    game: Game

    @classmethod
    def setUpClass(cls) -> None:
        cls.game = Game()

    def setUp(self) -> None:
        self.game.reset()
        self.game.add_piece((0, 4), (BLACK, KING))
        self.game.add_piece((7, 4), (WHITE, KING))

    def test_all_corner_moves(self) -> None:
        start_loc = Location(1,1)
        piece_info = self.game.add_piece(start_loc, (BLACK, KNIGHT))
        expected_legal_moves = {
            Move(start_loc, Location(*dest))
            for dest in [(2, 3), (3, 2), (0, 3), (3, 0)]
        }
        calculated_legal_moves = set(self.game.legal_moves(color=BLACK, pieces={piece_info}))
        logging.debug("Calculated Legal moves are %s", calculated_legal_moves)
        self.assertSetEqual(calculated_legal_moves, expected_legal_moves)

    def test_all_center_moves(self) -> None:
        start_loc = Location(4, 4)
        piece_info = self.game.add_piece(start_loc, (WHITE, KNIGHT))
        expected_legal_moves = {
            Move(start_loc, Location(*dest))
            for dest in [(5, 6), (6, 5), (2, 3), (3, 2), (5, 2), (6, 3), (3, 6), (2, 5)]
        }
        calculated_legal_moves = set(self.game.legal_moves(color=WHITE, pieces={piece_info}))
        self.assertSetEqual(expected_legal_moves, calculated_legal_moves)

    def test_capture_knight_moves(self) -> None:
        expected_legal_move_list = [
            Move(start=Location(0, 4), end=Location(1, 3), type=MoveType.PASSING, target=None),
            Move(start=Location(0, 4), end=Location(1, 5), type=MoveType.PASSING, target=None),
            Move(start=Location(0, 4), end=Location(1, 4), type=MoveType.PASSING, target=None),
            Move(start=Location(3, 2), end=Location(2, 0), type=MoveType.PASSING, target=None),
            Move(start=Location(3, 2), end=Location(1, 1), type=MoveType.CAPTURE, target=None),
            Move(start=Location(3, 2), end=Location(2, 4), type=MoveType.CAPTURE, target=None),
            Move(start=Location(3, 2), end=Location(4, 0), type=MoveType.PASSING, target=None),
            Move(start=Location(3, 2), end=Location(5, 1), type=MoveType.PASSING, target=None),
            Move(start=Location(3, 2), end=Location(1, 3), type=MoveType.PASSING, target=None),
            Move(start=Location(3, 2), end=Location(5, 3), type=MoveType.PASSING, target=None),
            Move(start=Location(3, 2), end=Location(4, 4), type=MoveType.PASSING, target=None),
        ]
        expected_legal_moves = set(expected_legal_move_list)
        self.game.add_piece((3, 2), Piece(type=PieceType.KNIGHT, color=Color.BLACK))
        self.game.add_piece((2, 4), Piece(type=PieceType.KNIGHT, color=Color.WHITE))
        self.game.add_piece((1, 1), Piece(type=PieceType.KNIGHT, color=Color.WHITE))
        calculate_legal_moves = set(list(self.game.legal_moves(color=Color.BLACK)))
        self.assertSetEqual(expected_legal_moves, calculate_legal_moves)

    def test_check_center_moves(self) -> None:
        expected_legal_move_list = [
            Move(start=Location(0, 4), end=Location(0, 5), type=MoveType.PASSING, target=None),
            Move(start=Location(0, 4), end=Location(0, 3), type=MoveType.PASSING, target=None),
            Move(start=Location(0, 4), end=Location(1, 3), type=MoveType.PASSING, target=None),
            Move(start=Location(0, 4), end=Location(1, 5), type=MoveType.PASSING, target=None),
            Move(start=Location(3, 3), end=Location(1, 4), type=MoveType.PASSING, target=None),
            Move(start=Location(3, 3), end=Location(5, 4), type=MoveType.PASSING, target=None),
        ]
        expected_legal_moves = set(expected_legal_move_list)
        self.game.add_piece((3, 2), Piece(type=PieceType.KNIGHT, color=Color.BLACK))
        self.game.add_piece((6, 4), Piece(type=PieceType.ROOK, color=Color.WHITE))
        calculate_legal_moves = set(list(self.game.legal_moves(color=Color.BLACK)))
        self.assertSetEqual(expected_legal_moves, calculate_legal_moves)


if __name__ == "__main__":
    unittest.main()
