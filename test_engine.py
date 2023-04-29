import unittest

from engine import Board


class TestEngine(unittest.TestCase):

    def setUp(self) -> None:
        self.board = Board()
        return super().setUp()
    
    def test_board(self, d) -> None:
        board = Board()
        self.assertEqual(board.board.shape, (8, 8, 4))
        self.assertEqual(board.board.dtype, 'int8')
        self.assertEqual(board.board[0, 0, 0], 0)

    def test_execute_move(self) -> None:
        pass

    def test_get_legal_moves(self) -> None:
        pass

    def test_pawn_moves(self) -> None:
        self.board 
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
