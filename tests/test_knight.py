"""
Unittests for knight movement logic
"""
import unittest

from engine.game import Game
from engine.types import (
    Location, Move, MoveType, Piece,
    KING, KNIGHT, ROOK,# PieceTypes
    WHITE, BLACK, # Colors
)


class TestKnight(unittest.TestCase):

    game: Game

    @classmethod
    def setUpClass(cls) -> None:
        cls.game = Game()

    def setUp(self) -> None:
        self.game.reset()
        self.game.add_piece((0, 4), (BLACK, KING))
        self.game.add_piece((7, 4), (WHITE, KING))

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
        expected_legal_moves = {
            Move(Location(1, 1), Location(*dest))
            for dest in [(2, 3), (3, 2), (0, 3), (3, 0)]
        }

        self.assertSetEqual(
            expected_legal_moves,
            set(self.game.legal_moves(color=BLACK, pieces= ((BLACK, KNIGHT), (1, 1)) ))
        )

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
        self.game.add_piece((4,4), (WHITE, KNIGHT))
        expected_legal_moves = {
            Move(Location(4, 4), Location(*dest))
            for dest in [(5, 6), (6, 5), (2, 3), (3, 2), (5, 2), (6, 3), (3, 6), (2, 5)]
        }

        self.assertSetEqual(
            expected_legal_moves,
            set(self.game.legal_moves(color=WHITE, pieces= ((WHITE, KNIGHT), (4, 4)) ))
        )

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
        expected_legal_moves = {
            *(
                Move(Location(3, 2), Location(*dest))
                for dest in [(2,0), (4, 0), (5, 1), (1, 3), (5, 3), (4, 4)]
            ),
            Move(Location(3, 2), Location(2,4), type=MoveType.CAPTURE, target=Piece(WHITE, KNIGHT)),
            Move(Location(3, 2), Location(1,1), type=MoveType.CAPTURE, target=Piece(WHITE, KNIGHT))
        }

        self.assertSetEqual(
            expected_legal_moves,
            set(self.game.legal_moves(color=BLACK, pieces= ((BLACK, KNIGHT), (3, 2)) ))
        )

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

        expected_legal_moves = {
            Move(start=Location(3, 3), end=Location(1, 4), type=MoveType.PASSING, target=None),
            Move(start=Location(3, 3), end=Location(5, 4), type=MoveType.PASSING, target=None),
        }
        self.assertSetEqual(
            expected_legal_moves,
            set(self.game.legal_moves(color=BLACK, pieces= ((BLACK, KNIGHT), (3, 3)) ))
        )


if __name__ == "__main__":
    unittest.main()
