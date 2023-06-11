import unittest
from typing import List, Tuple

import numpy as np
import numpy.typing as npt

from engine import Board
from engine_types import Color
from fen_utils import from_fen, to_fen


class TestUtils(unittest.TestCase):

    TO_FEN_CASES: List[Tuple[npt.NDArray[np.int8], str]] = [
        (np.load("tests/data/board_dump.npy"), "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
    ]
    FROM_FEN_VALID_CASES: List[Tuple[str, npt.NDArray[np.int8]]] = [
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", np.load("tests/data/board_dump.npy"))
    ]
    FROM_FEN_VALID_CASES_2: List[Tuple[str, npt.NDArray[np.int8]]] = [
        (
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            np.load("tests/data/board_dump.npy")
        )
    ]
    FROM_FEN_INVALID_CASES: List[str] = [
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR/8")
    ]

    def test_to_fen(self) -> None:
        for board_arr, expected_fen in self.TO_FEN_CASES:
            board = Board()
            board.board = board_arr
            self.assertEqual(to_fen(board), expected_fen)

    def test_from_fen_valid(self) -> None:
        for fen_string, expected_board_arr in self.FROM_FEN_VALID_CASES:
            board = Board()
            from_fen(board, fen_string)
            self.assertTrue(np.all(board.board == expected_board_arr))

    def test_from_fen_valid_2(self) -> None:
        for fen_string, expected_board_arr in self.FROM_FEN_VALID_CASES_2:
            board = Board()
            from_fen(board, fen_string)
            self.assertTrue(np.all(board.board == expected_board_arr))
            self.assertEqual(board.active_color, Color.WHITE)

    def test_from_fen_invalid(self) -> None:
        for fen_string in self.FROM_FEN_INVALID_CASES:
            with self.assertRaises(ValueError):
                board = Board()
                from_fen(board, fen_string)


if __name__ == "__main__":
    unittest.main()
