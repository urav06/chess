"""
Movement logic of all the pieces. Generates pseudo-legal moves
"""

from itertools import chain, permutations, product
from typing import Generator, Dict, Callable

from engine.bit_utils import apply_mask
from engine.constants import BOARD_SIZE
from engine.board import Board
from engine.types import (
    Color, Direction, Location, Move, MoveType, PieceType,
    DIAGONAL_DIRECTIONS, PARALLEL_DIRECTIONS,  # Direction Groups
    CAPTURE, CAPTURE_AND_PROMOTION, PROMOTION,  # MoveTypes
    PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING,  # PieceTypes
    WHITE,  # Colors
)

class PieceMovement:

    @staticmethod
    def pawn_moves(board: Board, location: Location, color: Color) -> Generator[Move, None, None]:
        front: Direction = Direction.N if color is WHITE else Direction.S
        one_ahead = location + front
        attack_diagonals = [one_ahead+Direction.E, one_ahead+Direction.W]

        for destination in filter(Board.is_in_bounds, attack_diagonals):
            dest_square = board.board[destination[0], destination[1]]
            if (
                dest_square[3]  # Is occupied
                and dest_square[0] != color  # Is enemy
            ):
                yield from PieceMovement._transform_promotion(
                    Move(
                        location, destination, CAPTURE,
                        target=dest_square[1]
                    ),
                    color
                )

        if board.is_in_bounds(one_ahead) and not board.board[one_ahead[0], one_ahead[1], 3]:
            yield from PieceMovement._transform_promotion(Move(location, one_ahead), color)

            if (
                board.board[location[0], location[1], 2] == 0  # Has not moved
                and board.is_in_bounds(two_ahead := location + (2*front))
                and not board.board[two_ahead[0], two_ahead[1], 3]
            ):
                yield Move(location, two_ahead)

    @staticmethod
    def knight_moves(board: Board, location: Location, color: Color) -> Generator[Move, None, None]:
        deltas = [-2, -1, 1, 2]
        destination_gen: Generator[Location, None, None] = (
            location+v for v in permutations(deltas, 2) if abs(v[0]) != abs(v[1])
        )
        for destination in filter(Board.is_in_bounds, destination_gen):
            dest_square = board.board[destination[0], destination[1]]
            if not dest_square[3]:  # Is not occupied
                yield Move(location, destination)
            elif dest_square[0] != color:  # Is enemy
                yield Move(
                    location, destination, CAPTURE,
                    target=dest_square[1]
                )

    @staticmethod
    def bishop_moves(board: Board, location: Location, color: Color) -> Generator[Move, None, None]:
        yield from PieceMovement._slide_moves(board, location, color, "D")

    @staticmethod
    def rook_moves(board: Board, location: Location, color: Color) -> Generator[Move, None, None]:
        yield from PieceMovement._slide_moves(board, location, color, "P")

    @staticmethod
    def queen_moves(board: Board, location: Location, color: Color) -> Generator[Move, None, None]:
        yield from PieceMovement._slide_moves(board, location, color, "C")

    @staticmethod
    def king_moves(board: Board, location: Location, color: Color) -> Generator[Move, None, None]:
        deltas = [-1, 0, 1]
        destination_gen: Generator[Location, None, None] = (
            location+v for v in product(deltas, deltas) if v != (0, 0)
        )
        for destination in filter(Board.is_in_bounds, destination_gen):
            dest_square = board.board[destination[0], destination[1]]
            if not dest_square[3]:  # Is not occupied
                yield Move(location, destination)
            elif dest_square[0] != color:  # Is enemy
                yield Move(
                    location, destination, CAPTURE,
                    target=dest_square[1]
                )

    @staticmethod
    def _transform_promotion(move: Move, color: Color) -> Generator[Move, None, None]:

        promotable_ranks = [PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT]

        promotion_row = 0 if color is WHITE else BOARD_SIZE-1
        match move:
            case Move(start, end, MoveType.PASSING) if end.i == promotion_row:
                yield from (
                    Move(start, end, PROMOTION, promotion_rank=rank)
                    for rank in promotable_ranks
                )
            case Move(start, end, MoveType.CAPTURE, target=target) if end.i == promotion_row:
                yield from (
                    Move(start, end, CAPTURE_AND_PROMOTION, target=target, promotion_rank=rank)
                    for rank in promotable_ranks
                )
            case _:
                yield move

    @staticmethod
    def _slide_moves(
        board: Board, location: Location, color: Color, types: str
    ) -> Generator[Move, None, None]:
        captures, slides = apply_mask(board, location, types)
        yield from (Move(location, Location(*end), CAPTURE, target=PieceType(board[end[0], end[1], 1])) for end in captures)
        yield from (Move(location, Location(*end), MoveType.PASSING) for end in slides)


PIECE_LOGIC_MAP: Dict[
    PieceType, Callable[[Board, Location, Color], Generator[Move, None, None]]
] = {
    PAWN: PieceMovement.pawn_moves,
    KNIGHT: PieceMovement.knight_moves,
    BISHOP: PieceMovement.bishop_moves,
    ROOK: PieceMovement.rook_moves,
    QUEEN: PieceMovement.queen_moves,
    KING: PieceMovement.king_moves
}
