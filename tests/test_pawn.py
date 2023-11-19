import unittest

from tests.test_base_piece import BaseTestPiece
from engine.types import (
    Location,
    PAWN,  # PieceTypes
    WHITE, BLACK,   # Colors
    CAPTURE,  # MoveTypes
)


class TestPawn(BaseTestPiece):

    def setUp(self) -> None:
        super().setUp()

    def test_base_case_black(self) -> None:
        self.start_loc = Location(1, 6)
        self.piece_info = self.game.board.place_piece(Location(1, 6), (BLACK, PAWN))
        expected = self.moves(
            (1, 6),
            [
             (2, 6),
             (3, 6)
            ]
            )
        self.assert_generated_moves(
            expected=expected,
            piece=self.piece_info
            )

    def test_base_case_white(self) -> None:
        self.start_loc = Location(6, 6)
        self.piece_info = self.game.board.place_piece(Location(6, 6), (WHITE, PAWN))
        expected = self.moves(
            (6, 6),
            [
             (5, 6),
             (4, 6)
            ]
            )
        self.assert_generated_moves(
            expected=expected,
            piece=self.piece_info
            )

    def test_capture_case_black(self) -> None:
        self.start_loc = Location(1, 6)
        self.piece_info = self.game.board.place_piece(Location(1, 6), (BLACK, PAWN))
        self.game.board.place_piece(Location(2, 5), (WHITE, PAWN))
        expected = self.moves(
            (1, 6),
            [
             (2, 5)
            ]
            )
        self.assert_generated_moves(
            expected=expected,
            piece=self.piece_info
            )

    def test_case_block_black(self) -> None:
        self.start_loc = Location(1, 6)
        self.piece_info = self.game.board.place_piece(Location(1, 6), (BLACK, PAWN))
        self.game.board.place_piece(Location(2, 6), (WHITE, PAWN))
        expected = self.moves(
            (1, 6),
            [
            ]
            )
        self.assert_generated_moves(
            expected=expected,
            piece=self.piece_info
            )


if __name__ == "__main__":
    unittest.main()
