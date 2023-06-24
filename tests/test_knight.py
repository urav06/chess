"""
Unittests for knight movement logic
"""
import unittest
from engine.game import Game
from engine.types import Piece, PieceType, Color,Move,MoveType,Location


class TestKnight(unittest.TestCase):

    def setUp(self) -> None:
        self.default_game = Game()
        self.default_game.add_piece(location=(0, 4),piece=Piece(type=PieceType.KING, color=Color.BLACK))
        self.default_game.add_piece(location=(7, 4), piece=Piece(type=PieceType.KING, color=Color.WHITE))

    def test_all_corner_moves(self):
        expected_legal_move_list = [
            Move(start=Location(1, 1), end=Location(2, 3), type=MoveType.PASSING, target=None),
            Move(start=Location(1, 1), end=Location(3, 2), type=MoveType.PASSING, target=None),
            Move(start=Location(1, 1), end=Location(0, 3), type=MoveType.PASSING, target=None),
            Move(start=Location(1, 1), end=Location(3, 0), type=MoveType.PASSING, target=None),
            Move(start=Location(0, 4), end=Location(0, 5), type=MoveType.PASSING, target=None),
            Move(start=Location(0, 4), end=Location(0, 3), type=MoveType.PASSING, target=None),
            Move(start=Location(0, 4), end=Location(1, 3), type=MoveType.PASSING, target=None),
            Move(start=Location(0, 4), end=Location(1, 5), type=MoveType.PASSING, target=None),
            Move(start=Location(0, 4), end=Location(1, 4), type=MoveType.PASSING, target=None),
        ]
        expected_legal_moves = set(expected_legal_move_list)
        self.default_game.add_piece(location=Location(1, 1), piece=Piece(type=PieceType.KNIGHT, color=Color.BLACK))
        calculated_legal_moves = set(list(self.default_game.legal_moves(color=Color.BLACK)))
        print("Calculated Legal moves is", calculated_legal_moves)
        self.assertSetEqual(calculated_legal_moves, expected_legal_moves)

    def test_all_center_moves(self):
        expected_legal_move_list = [
            Move(start=Location(4, 4), end=Location(5, 6), type=MoveType.PASSING, target=None),
            Move(start=Location(4, 4), end=Location(6, 5), type=MoveType.PASSING, target=None),
            Move(start=Location(4, 4), end=Location(2, 3), type=MoveType.PASSING, target=None),
            Move(start=Location(4, 4), end=Location(3, 2), type=MoveType.PASSING, target=None),
            Move(start=Location(4, 4), end=Location(5, 2), type=MoveType.PASSING, target=None),
            Move(start=Location(4, 4), end=Location(6, 3), type=MoveType.PASSING, target=None),
            Move(start=Location(4, 4), end=Location(3, 6), type=MoveType.PASSING, target=None),
            Move(start=Location(4, 4), end=Location(2, 5), type=MoveType.PASSING, target=None),
            Move(start=Location(7, 4), end=Location(7, 5), type=MoveType.PASSING, target=None),
            Move(start=Location(7, 4), end=Location(7, 3), type=MoveType.PASSING, target=None),
            Move(start=Location(7, 4), end=Location(6, 3), type=MoveType.PASSING, target=None),
            Move(start=Location(7, 4), end=Location(6, 5), type=MoveType.PASSING, target=None),
            Move(start=Location(7, 4), end=Location(6, 4), type=MoveType.PASSING, target=None),
        ]
        expected_legal_moves = set(expected_legal_move_list)
        self.default_game.add_piece(location=Location(4, 4), piece=Piece(type=PieceType.KNIGHT, color=Color.WHITE))
        calculate_legal_moves = set(list(self.default_game.legal_moves(color=Color.WHITE)))
        self.assertSetEqual(expected_legal_moves, calculate_legal_moves)

    def test_capture_knight_moves(self):
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
        self.default_game.add_piece(location=Location(3, 2), piece=Piece(type=PieceType.KNIGHT, color=Color.BLACK))
        self.default_game.add_piece(location=Location(2, 4), piece=Piece(type=PieceType.KNIGHT, color=Color.WHITE))
        self.default_game.add_piece(location=Location(1, 1), piece=Piece(type=PieceType.KNIGHT, color=Color.WHITE))
        calculate_legal_moves = set(list(self.default_game.legal_moves(color=Color.BLACK)))
        self.assertSetEqual(expected_legal_moves, calculate_legal_moves)

        def test_check_center_moves(self):
            expected_legal_move_list = [
            Move(start=Location(0, 4), end=Location(0, 5), type=MoveType.PASSING, target=None),
            Move(start=Location(0, 4), end=Location(0, 3), type=MoveType.PASSING, target=None),
            Move(start=Location(0, 4), end=Location(1, 3), type=MoveType.PASSING, target=None),
            Move(start=Location(0, 4), end=Location(1, 5), type=MoveType.PASSING, target=None),
            Move(start=Location(3, 3), end=Location(1, 4), type=MoveType.PASSING, target=None),
            Move(start=Location(3, 3), end=Location(5, 4), type=MoveType.PASSING, target=None),
        ]
        expected_legal_moves = set(expected_legal_move_list)
        self.default_game.add_piece(location=Location(3, 2), piece=Piece(type=PieceType.KNIGHT, color=Color.BLACK))
        self.default_game.add_piece(location=Location(6, 4), piece=Piece(type=PieceType.ROOK, color=Color.WHITE))
        calculate_legal_moves = set(list(self.default_game.legal_moves(color=Color.BLACK)))
        self.assertSetEqual(expected_legal_moves, calculate_legal_moves)
