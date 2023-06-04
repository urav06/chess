import unittest

from engine import Board
from engine_types import Move, MoveType, Location, Color
from fen_utils import to_fen, from_fen



class TestEngine(unittest.TestCase):

    TEST_EXECUTE_MOVE = {
        "PASSING": [
            ("rnbqkb1r/pppppppp/8/2n5/8/8/PPPPPPPP/RNBQKBNR", Move((6, 5), (4, 5), MoveType.PASSING), "rnbqkb1r/pppppppp/8/2n5/5P2/8/PPPPP1PP/RNBQKBNR"),
            ("rnbqkb1r/pppppppp/8/2n5/8/8/PPPPPPPP/RNBQKBNR", Move((3,2),(5,3),MoveType.PASSING), "rnbqkb1r/pppppppp/8/8/8/3n4/PPPPPPPP/RNBQKBNR"),
            ("rnbqkb1r/pppppppp/8/8/8/3n4/PPPPPPPP/RNBQKBNR",Move((6,2),(4,2),MoveType.PASSING),"rnbqkb1r/pppppppp/8/8/2P5/3n4/PP1PPPPP/RNBQKBNR")
        ]

    }

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
            # print("In Test Case",test_case,board)
            fen_string = to_fen(board)
            print("Test case is",test_case)
            print("Final output is",fen_string)
            self.assertEqual(fen_string, test_case[2])

    def test_get_legal_moves(self) -> None:
        for test_case in self.TEST_EXECUTE_MOVE['PASSING']:
            board = Board()
            from_fen(board, test_case[0])
            board.generate_possible_moves(Color.WHITE)
            # print("In Test Case",test_case,board)
            fen_string = to_fen(board)
            print("Test case is", test_case)
            print("Final output is", fen_string)
            self.assertEqual(fen_string, test_case[2])

    def test_pawn_moves(self) -> None:
        # self.board
        pass

    def test_knight_moves(self) -> None:
        pass

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
