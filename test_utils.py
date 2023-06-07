import unittest
from engine import Board
from fen_utils import to_fen, from_fen
import numpy.typing as npt
import numpy as np

class TestUtils(unittest.TestCase):

    TEST_TO_FEN =[
      (np.fromfile("test_data.txt"),"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
    ]
    TEST_TO_FEN_FAIL = [
      (np.fromfile("test_data_fail.txt"))
    ]
    TEST_FROM_FEN=[
      ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR",np.fromfile("test_data.txt"))
    ]
    TEST_FROM_FEN_FAIL=[
      ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR/8")
    ]
    def test_to_fen(self):
      pass

    def test_to_fen_invalid(self):
      pass

    def test_from_fen(self):
      pass

    def test_from_fen_invalid(self):
      with self.assertRaises(ValueError):
        from_fen(Board(), "")
