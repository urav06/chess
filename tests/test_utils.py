import unittest

import numpy as np
import numpy.testing as np_testing

from engine import Board
from engine.fen_utils import from_fen, to_fen


class TestUtils(unittest.TestCase):

    CLASSIC_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
    INVALID_RANKS_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR/8"  # 9 ranks

    def test_to_fen_classic(self) -> None:
        board_arr = np.load("tests/data/board_dump.npy")
        expected_fen = self.CLASSIC_FEN
        board = Board()
        board.board = board_arr
        self.assertEqual(to_fen(board), expected_fen)

    def test_from_fen_classic(self) -> None:
        fen = self.CLASSIC_FEN
        expected_board_arr = np.load("tests/data/board_dump.npy")
        board = Board()
        from_fen(board, fen)
        np_testing.assert_array_equal(board.board, expected_board_arr)

    def test_from_fen_invalid_ranks(self) -> None:
        fen_string = self.INVALID_RANKS_FEN
        board = Board()
        with self.assertRaises(ValueError):
            from_fen(board, fen_string)


if __name__ == "__main__":
    unittest.main()