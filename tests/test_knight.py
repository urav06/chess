"""
Unittests for knight movement logic
"""
import unittest

from tests.test_base_piece import BaseTestPiece
from engine.types import (
    KNIGHT, ROOK,  # PieceTypes
    WHITE, BLACK,  # Colors
    CAPTURE  # MoveTypes
)


class TestKnight(BaseTestPiece):

    def test_corner_moves(self) -> None:
        """
            Knight in the corner of the board

            ◻  ◼  ◻  ◼  ♚  ◼  ◻  ◼
            ◼  ♞  ◼  ◻  ◼  ◻  ◼  ◻
            ◻  ◼  ◻  ◼  ◻  ◼  ◻  ◼
            ◼  ◻  ◼  ◻  ◼  ◻  ◼  ◻
            ◻  ◼  ◻  ◼  ◻  ◼  ◻  ◼
            ◼  ◻  ◼  ◻  ◼  ◻  ◼  ◻
            ◻  ◼  ◻  ◼  ◻  ◼  ◻  ◼
            ◼  ◻  ◼  ◻  ♔  ◻  ◼  ◻
        """
        self.game.add_piece((1, 1), (BLACK, KNIGHT))
        expected = self.moves((1, 1), [(2, 3), (3, 2), (0, 3), (3, 0)])

        self.assert_generated_moves(expected, piece=((BLACK, KNIGHT), (1, 1)))

    def test_center_moves(self) -> None:
        """
            Knight in center of board

            ◻  ◼  ◻  ◼  ♚  ◼  ◻  ◼
            ◼  ◻  ◼  ◻  ◼  ◻  ◼  ◻
            ◻  ◼  ◻  ◼  ◻  ◼  ◻  ◼
            ◼  ◻  ◼  ◻  ◼  ◻  ◼  ◻
            ◻  ◼  ◻  ◼  ♘  ◼  ◻  ◼
            ◼  ◻  ◼  ◻  ◼  ◻  ◼  ◻
            ◻  ◼  ◻  ◼  ◻  ◼  ◻  ◼
            ◼  ◻  ◼  ◻  ♔  ◻  ◼  ◻
        """
        self.game.add_piece((4, 4), (WHITE, KNIGHT))
        expected = self.moves(
            (4, 4), [(5, 6), (6, 5), (2, 3), (3, 2), (5, 2), (6, 3), (3, 6), (2, 5)]
        )

        self.assert_generated_moves(expected, piece=((WHITE, KNIGHT), (4, 4)))

    def test_capture_moves(self) -> None:
        """
            Knight in center of board, capturing pieces

            ◻  ◼  ◻  ◼  ♚  ◼  ◻  ◼
            ◼  ♘  ◼  ◻  ◼  ◻  ◼  ◻
            ◻  ◼  ◻  ◼  ♘  ◼  ◻  ◼
            ◼  ◻  ♞  ◻  ◼  ◻  ◼  ◻
            ◻  ◼  ◻  ◼  ◻  ◼  ◻  ◼
            ◼  ◻  ◼  ◻  ◼  ◻  ◼  ◻
            ◻  ◼  ◻  ◼  ◻  ◼  ◻  ◼
            ◼  ◻  ◼  ◻  ♔  ◻  ◼  ◻

        """
        self.game.add_piece((3, 2), (BLACK, KNIGHT))
        self.game.add_piece((2, 4), (WHITE, KNIGHT))
        self.game.add_piece((1, 1), (WHITE, KNIGHT))

        expected = self.moves(
            (3, 2), [(2, 0), (4, 0), (5, 1), (1, 3), (5, 3), (4, 4)]
        ).union(self.moves(
            (3, 2), [(2, 4), (1, 1)],
            move_type=CAPTURE,
            target=KNIGHT
        ))

        self.assert_generated_moves(expected, piece=((BLACK, KNIGHT), (3, 2)))

    def test_block_check_moves(self) -> None:
        """
            Knight in center of board, able to block check

            ◻  ◼  ◻  ◼  ♚  ◼  ◻  ◼
            ◼  ◻  ◼  ◻  ◼  ◻  ◼  ◻
            ◻  ◼  ◻  ◼  ◻  ◼  ◻  ◼
            ◼  ◻  ◼  ♞  ◼  ◻  ◼  ◻
            ◻  ◼  ◻  ◼  ◻  ◼  ◻  ◼
            ◼  ◻  ◼  ◻  ◼  ◻  ◼  ◻
            ◻  ◼  ◻  ◼  ♖  ◼  ◻  ◼
            ◼  ◻  ◼  ◻  ♔  ◻  ◼  ◻
        """
        self.game.add_piece((3, 3), (BLACK, KNIGHT))
        self.game.add_piece((6, 4), (WHITE, ROOK))
        expected = self.moves(
            (3, 3), [(1, 4), (5, 4)]
        )

        self.assert_generated_moves(expected, piece=((BLACK, KNIGHT), (3, 3)))


if __name__ == "__main__":
    unittest.main()
