"""
Test the sliding pieces (Bishop, Rook, Queen) for legal moves.
"""

import unittest

from engine.types import CAPTURE  # MoveTypes
from engine.types import (BISHOP, BLACK, ROOK, WHITE,  # PieceTypes; Colors
                          Location)
from tests.test_base_piece import BaseTestPiece


class TestBishop(BaseTestPiece):

    def setUp(self) -> None:
        super().setUp()
        self.start_loc = Location(1, 1)
        self.piece_info = self.game.board.place_piece(Location(1, 1), (BLACK, BISHOP))

    def test_base_case(self) -> None:
        expected = self.moves(
            (1, 1), [(0, 0), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (0, 2), (2, 0)]
        )
        self.assert_generated_moves(expected, piece=self.piece_info)

    def test_penetration_case(self) -> None:
        self.game.board.place_piece((6, 6), (BLACK, ROOK))
        expected = self.moves(
            (1, 1), [(0, 0), (2, 2), (3, 3), (4, 4), (5, 5), (0, 2), (2, 0)]
        )

        self.assert_generated_moves(expected, piece=self.piece_info)

    def test_pinned_case(self) -> None:
        self.game.board.place_piece((6, 4), (WHITE, ROOK))
        expected = self.moves((1, 1), [(4, 4)])

        self.assert_generated_moves(expected, piece=self.piece_info)

    def test_capture_case(self) -> None:
        self.game.board.place_piece((5, 5), (WHITE, ROOK))
        expected = self.moves(
            (1, 1), [(0, 0), (2, 2), (3, 3), (4, 4), (0, 2), (2, 0)],
        ).union(self.moves(
            (1, 1), [(5, 5)], move_type=CAPTURE, target=ROOK
        ))

        self.assert_generated_moves(expected, piece=self.piece_info)

    def test_obstruct_case(self) -> None:
        self.game.board.place_piece((4, 4), (BLACK, ROOK))
        expected = self.moves((1, 1), [(0, 0), (2, 2), (3, 3), (0, 2), (2, 0)])

        self.assert_generated_moves(expected, piece=self.piece_info)


if __name__ == "__main__":
    unittest.main()
