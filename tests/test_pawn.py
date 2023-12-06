import unittest

from tests.test_base_piece import BaseTestPiece
from engine.types import (
    Location,
    PAWN, KING, ROOK,  # PieceTypes
    WHITE, BLACK,   # Colors
    CAPTURE,  # MoveTypes
)


class TestPawn(BaseTestPiece):

    def setUp(self)->None:
        return super().setUp()

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
        return self.assert_generated_moves(
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
        return self.assert_generated_moves(
            expected=expected,
            piece=self.piece_info
            )

    def test_capture_case_black(self) -> None:
        self.start_loc = Location(1, 6)
        self.piece_info = self.game.board.place_piece(Location(1, 6), (BLACK, PAWN))
        self.game.board.place_piece(Location(2, 5), (WHITE, PAWN))
        expected_passing = self.moves(
            (1, 6),
            [
             (2, 6),
             (3, 6)
            ]
            )
        expected_capture = self.moves(
            (1, 6),
            [(2, 5)],
            move_type=CAPTURE,
            target=PAWN,
        )
        expected = expected_passing | expected_capture
        return self.assert_generated_moves(
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
        return self.assert_generated_moves(
            expected=expected,
            piece=self.piece_info
            )

    def test_case_promote_black(self) -> bool:
        self.start_loc = Location(1, 6)
        self.piece_info = self.game.board.place_piece(Location(1, 6), (BLACK, PAWN))
        legal_moves = self.game.legal_moves(
            color=BLACK,
            piece=self.piece_info
            )
        return True

    def test_case_pinned_case_black(self) -> None:
        self.start_loc = Location(1, 6)
        self.game.board.place_piece(Location(3, 6), (BLACK, KING))
        black_pawn = self.game.board.place_piece(Location(2, 6), (BLACK, PAWN))
        self.game.board.place_piece(Location(1, 6), (WHITE, ROOK))
        expected = self.moves(
            (2, 6),
            []
            )
        return self.assert_generated_moves(
            expected=expected,
            piece=black_pawn,
        )


if __name__ == "__main__":
    unittest.main()
