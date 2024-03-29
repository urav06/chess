"""
Unittests for knight movement logic
"""
import unittest

from engine.types import CAPTURE  # MoveTypes
from engine.types import (BLACK, KNIGHT, ROOK,  # Piece; PieceTypes; Colors
                          WHITE, Location, Piece)
from tests.test_base_piece import BaseTestPiece


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
        self.game.board.place_piece((1, 1), (BLACK, KNIGHT))
        expected = self.moves((1, 1), [(2, 3), (3, 2), (0, 3), (3, 0)])

        self.assert_generated_moves(expected, piece=(Piece(BLACK, KNIGHT), Location(1, 1)))

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
        self.game.board.place_piece((4, 4), (WHITE, KNIGHT))
        expected = self.moves(
            (4, 4), [(5, 6), (6, 5), (2, 3), (3, 2), (5, 2), (6, 3), (3, 6), (2, 5)]
        )

        self.assert_generated_moves(expected, piece=(Piece(WHITE, KNIGHT), Location(4, 4)))

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
        self.game.board.place_piece((3, 2), (BLACK, KNIGHT))
        self.game.board.place_piece((2, 4), (WHITE, KNIGHT))
        self.game.board.place_piece((1, 1), (WHITE, KNIGHT))

        expected = self.moves(
            (3, 2), [(2, 0), (4, 0), (5, 1), (1, 3), (5, 3), (4, 4)]
        ).union(self.moves(
            (3, 2), [(2, 4), (1, 1)],
            move_type=CAPTURE,
            target=KNIGHT
        ))

        self.assert_generated_moves(expected, piece=(Piece(BLACK, KNIGHT), Location(3, 2)))

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
        self.game.board.place_piece((3, 3), (BLACK, KNIGHT))
        self.game.board.place_piece((6, 4), (WHITE, ROOK))
        expected = self.moves(
            (3, 3), [(1, 4), (5, 4)]
        )

        self.assert_generated_moves(expected, piece=(Piece(BLACK, KNIGHT), Location(3, 3)))


if __name__ == "__main__":
    unittest.main()
