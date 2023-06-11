import unittest

from engine import Board, knight_moves
from engine.types import Move, MoveType, Location, Color
from engine.fen_utils import to_fen, from_fen
import numpy as np



class TestEngine(unittest.TestCase):

    TEST_EXECUTE_MOVE = {
        "PASSING": [
            ("rnbqkb1r/pppppppp/8/2n5/8/8/PPPPPPPP/RNBQKBNR", Move(Location(6, 5),Location(4, 5), MoveType.PASSING), "rnbqkb1r/pppppppp/8/2n5/5P2/8/PPPPP1PP/RNBQKBNR"),
            ("rnbqkb1r/pppppppp/8/2n5/8/8/PPPPPPPP/RNBQKBNR", Move(Location(3,2),Location(5,3),MoveType.PASSING), "rnbqkb1r/pppppppp/8/8/8/3n4/PPPPPPPP/RNBQKBNR"),
            ("rnbqkb1r/pppppppp/8/8/8/3n4/PPPPPPPP/RNBQKBNR",Move(Location(6,2),Location(4,2),MoveType.PASSING),"rnbqkb1r/pppppppp/8/8/2P5/3n4/PP1PPPPP/RNBQKBNR")
        ]
    }
    TEST_KNIGHT_MOVE = [
            ("N7/8/8/8/8/8/8/8",(0,0),[Move(Location(0,0),Location(1,2),MoveType.PASSING),
                                 Move(Location(0, 0), Location(2, 1), MoveType.PASSING)]),
            ("N7/8/1p6/8/8/8/8/8",(0,0), [Move(Location(0, 0), Location(2, 1), MoveType.CAPTURE),
                                  Move(Location(0, 0), Location(1, 2), MoveType.PASSING)] ),
            (" N7 / 2P5 / 1P6 / 8 / 8 / 8 / 8 / 8",(0,0),[]),
            ("8/8/8/3N4/8/8/8/8",(3,4),[ Move(Location(3, 4), Location(1, 5), MoveType.PASSING),
                                   Move(Location(3, 4), Location(1, 3), MoveType.PASSING),
                                   Move(Location(3, 4), Location(2, 6), MoveType.PASSING),
                                   Move(Location(3, 4), Location(2, 2), MoveType.PASSING),
                                   Move(Location(3, 4), Location(4, 6), MoveType.PASSING),
                                   Move(Location(3, 4), Location(4, 2), MoveType.PASSING),
                                   Move(Location(3, 4), Location(5, 5), MoveType.PASSING),
                                   Move(Location(3, 4), Location(5, 3), MoveType.PASSING)]),
            # ("8/8/1r6/2N5/8/8/P1B5/1KR5",(2,4),[Move(Location(2, 4), Location(1, 6), MoveType.PASSING),
            #                               Move(Location(2,4),Location(1,2),MoveType.CAPTURE)]),
            # ("8/8/1r6/2N5/8/8/P1B5/1KR5",(2,3),[Move(Location(2,3),Location(1,5),MoveType.PASSING)]),
            # ("8/8/1r6/2N5/8/8/P1B5/1KR5",(2,3),[]),

        ]
    TEST_BISHOP_MOVE = [
      ("B7/8/8/8/8/8/8/8",),
      ("8/8/8/8/8/8/8/B7",),
      ("8/8/8/8/3B4/8/8/8",),
      ("8/8/8/3B4/8/8/8/8 ")
    ]

    TEST_KING_MOVE = {

    }
    TEST_QUEEN_MOVE = {

    }
    TEST_ROOK_MOVE = {

    }

    # TODO - Make Move of MoveType - Passing/Capture/Castle

    def setUp(self) -> None:

        board = Board()
        self.board = board
        return super().setUp()
    
    def test_board(self) -> None:
        board = Board()
        self.assertEqual(board.board.shape, (8, 8, 4))
        self.assertEqual(board.board.dtype, 'int8')
        self.assertEqual(board.board[0, 0, 0], 0)

    def test_execute_move(self) -> None:
        for test_case in self.TEST_EXECUTE_MOVE['PASSING']:
            board = Board()
            from_fen(board, test_case[0])
            board.execute_move(test_case[1])
            fen_string = to_fen(board)
            self.assertEqual(fen_string, test_case[2])

    def test_get_legal_moves(self) -> None:
        pass

    def test_pawn_moves(self) -> None:
        # self.board
        pass

    def test_knight_moves(self) -> None:
        for input,loc,output in self.TEST_KNIGHT_MOVE:
          board = Board()
          from_fen(board,input)
          calc_output =list(knight_moves(board,Location(*loc),Color.WHITE))
          calculated_output = set(calc_output)
          actual_output = set(output)
          self.assertSetEqual(actual_output,calculated_output)

    def test_bishop_moves(self) -> None:
        pass

    def test_rook_moves(self) -> None:
        pass

    def test_queen_moves(self) -> None:
        pass

    def test_king_moves(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
