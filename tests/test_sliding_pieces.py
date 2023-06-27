import unittest
import logging

from engine.game import Game
from engine.types import (
    Color, Location, Move, MoveType, Piece, PieceType,
    KING, BISHOP, QUEEN, ROOK,  # PieceTypes
    WHITE, BLACK,   # Colors
)


# class TestSliding(unittest.TestCase):

#     game: Game

    # def setUpClass(cls) -> None:
    #     cls.game = Game()

#     def setUp(self) -> None:
        # self.game.reset()
        # self.game.add_piece((0, 4), (BLACK, KING))
        # self.game.add_piece((7, 4), (WHITE, KING))

#     def test_base_case(self) -> None:
#         pass

#     def test_penetration_case(self) -> None:
#         pass

#     def test_pinned_case(self) -> None:
#         pass

#     def test_capture_case(self) -> None:
#         pass

#     def test_obstruct_case(self) -> None:
#         pass


class TestBishop(unittest.TestCase):

    game: Game

    @classmethod
    def setUpClass(cls) -> None:
        cls.game = Game()

    def setUp(self) -> None:
        self.game.reset()
        self.game.add_piece((0, 4), (BLACK, KING))
        self.game.add_piece((7, 4), (WHITE, KING))
        self.start_loc = Location(1, 1)
        self.piece_info = self.game.add_piece(self.start_loc, (BLACK, BISHOP))

    def test_base_case(self) -> None:

        expected_legal_moves = {
            Move(self.start_loc, Location(*dest))
            for dest in [(0, 0), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)                         
                         , (0, 2), (2, 0)]
        }
        calculated_legal_moves = set(self.game.legal_moves(color=BLACK,
                                                           pieces=self.piece_info))
        logging.debug("Calculated Legal moves are %s", calculated_legal_moves)
        self.assertSetEqual(calculated_legal_moves, expected_legal_moves)

    def test_penetration_case(self) -> None:
        self.game.add_piece((6, 6), (BLACK, ROOK))
        expected_legal_moves = {
            Move(self.start_loc, Location(*dest))
            for dest in [(0, 0), (2, 2), (3, 3), (4, 4), (5, 5), (0, 2), (2, 0) ]
        }
        calculated_legal_moves = set(self.game.legal_moves(color=BLACK,
                                                           pieces=self.piece_info))
        logging.debug("Calculated Legal moves are %s", calculated_legal_moves)
        self.assertSetEqual(calculated_legal_moves, expected_legal_moves)

    def test_pinned_case(self) -> None:
        self.game.add_piece((6, 4), (WHITE, ROOK))
        expected_legal_moves = {
            Move(self.start_loc, Location(*dest))
            for dest in [(4, 4)]
        }
        calculated_legal_moves = set(self.game.legal_moves(color=BLACK,
                                                           pieces=self.piece_info))
        logging.debug("Calculated Legal moves are %s", calculated_legal_moves)
        self.assertSetEqual(calculated_legal_moves, expected_legal_moves)

    def test_capture_case(self) -> None:
        self.game.add_piece((5, 5), (WHITE, ROOK))
        expected_legal_moves = {
            Move(self.start_loc, Location(*dest))
            for dest in [(0, 0), (2, 2), (3, 3), (4, 4), (0, 2), (2, 0)]
        }
        expected_legal_moves.add(Move(self.start_loc, Location(5, 5), MoveType.CAPTURE,
                                      target=Piece(WHITE, ROOK)))

        calculated_legal_moves = set(list(self.game.legal_moves(color=BLACK,
                                                                pieces=self.piece_info)))
        logging.debug("Calculated Legal moves are %s", calculated_legal_moves)
        self.assertSetEqual(calculated_legal_moves, expected_legal_moves)

    def test_obstruct_case(self) -> None:
        self.game.add_piece((4, 4), (BLACK, ROOK))
        expected_legal_moves = {
            Move(self.start_loc, Location(*dest))
            for dest in [(0, 0), (2, 2), (3, 3), (0, 2), (2, 0)]
        }
        calculated_legal_moves = set(self.game.legal_moves(color=BLACK,
                                                           pieces=self.piece_info))
        logging.debug("Calculated Legal moves are %s", calculated_legal_moves)
        self.assertSetEqual(calculated_legal_moves, expected_legal_moves)
