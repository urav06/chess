import unittest
from engine import Board
from fen_utils import to_fen, from_fen
import numpy.typing as npt
import numpy as np

class TestUtils(unittest.TestCase):

    TEST_TO_FEN =[
      (np.load("test_data.npy",allow_pickle=True),"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
    ]
    TEST_TO_FEN_FAIL = [
      (np.load("test_data.npy",allow_pickle=True))
    ]
    TEST_FROM_FEN=[
      ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR",np.load("test_data.npy",allow_pickle=True))
    ]
    TEST_FROM_FEN_FAIL=[
      ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR/8")
    ]
    def test_to_fen(self):
      for input, output in self.TEST_TO_FEN:
        board = Board()
        board.board = input
        fen_string=to_fen(board)
        self.assertEqual(fen_string, output)

    def test_to_fen_invalid(self):
      pass

    def test_from_fen(self):
      for input, output in self.TEST_TO_FEN:
        board = Board()
        from_fen(board,input)
        self.assertEqual(board.board,output)

    def test_from_fen_invalid(self):
      for input in self.TEST_TO_FEN_FAIL:
        board = Board()
        with self.assertRaises(ValueError):
          from_fen(board,input)

