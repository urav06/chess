"""
Movement logic of all the pieces
"""

from itertools import chain, permutations, product
from typing import Generator, Dict, Callable

from engine.constants import BOARD_SIZE
from engine.board import Board
from engine.types import (
    Color, Direction, Location, Move, MoveType, PieceType,
    DIAGONAL_DIRECTIONS, PARALLEL_DIRECTIONS,  # Direction Groups
    CAPTURE, CAPTURE_AND_PROMOTION, PROMOTION,  # MoveTypes
    PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING,  # PieceTypes
    WHITE,  # Colors
)

PROMOTABLE_RANKS = [PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT]


def transform_promotion(move: Move, color: Color) -> Generator[Move, None, None]:
    promotion_row = 0 if color is WHITE else BOARD_SIZE-1
    match move:
        case Move(start, end, MoveType.PASSING) if end.i == promotion_row:
            yield from (
                Move(start, end, PROMOTION, promotion_rank=rank)
                for rank in PROMOTABLE_RANKS
            )
        case Move(start, end, MoveType.CAPTURE, target=target) if end.i == promotion_row:
            yield from (
                Move(start, end, CAPTURE_AND_PROMOTION, target=target, promotion_rank=rank)
                for rank in PROMOTABLE_RANKS
            )
        case _:
            yield move


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
            yield from transform_promotion(
                Move(
                    location, destination, CAPTURE,
                    target=dest_square[1]
                ),
                color
            )

    if board.is_in_bounds(one_ahead) and not board.board[one_ahead[0], one_ahead[1], 3]:
        yield from transform_promotion(Move(location, one_ahead), color)

        if (
            board.board[location[0], location[1], 2] == 0  # Has not moved
            and board.is_in_bounds(two_ahead := location + (2*front))
            and not board.board[two_ahead[0], two_ahead[1], 3]
        ):
            yield Move(location, two_ahead)


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


def bishop_moves(board: Board, location: Location, color: Color) -> Generator[Move, None, None]:
    yield from chain.from_iterable(
        slide_moves(board, location, color, d) for d in DIAGONAL_DIRECTIONS
    )


def rook_moves(board: Board, location: Location, color: Color) -> Generator[Move, None, None]:
    yield from chain.from_iterable(
        slide_moves(board, location, color, d) for d in PARALLEL_DIRECTIONS
    )


def queen_moves(board: Board, location: Location, color: Color) -> Generator[Move, None, None]:
    directions: list[Direction] = PARALLEL_DIRECTIONS + DIAGONAL_DIRECTIONS
    yield from chain.from_iterable(
        slide_moves(board, location, color, d) for d in directions
    )


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


def slide_moves(
    board: Board, location: Location, color: Color, direction: Direction
) -> Generator[Move, None, None]:
    step = 1
    while Board.is_in_bounds(destination := location+(direction*step)):
        dest_square = board.board[destination[0], destination[1]]
        if not dest_square[3]:  # Is not occupied
            yield Move(location, destination)
            step += 1
        elif dest_square[0] != color:  # Enemy
            yield Move(
                location, destination, CAPTURE,
                target=dest_square[1]
            )
            break
        else:  # Friendly
            break


PIECE_LOGIC_MAP: Dict[
    PieceType, Callable[[Board, Location, Color], Generator[Move, None, None]]
] = {
    PAWN: pawn_moves,
    KNIGHT: knight_moves,
    BISHOP: bishop_moves,
    ROOK: rook_moves,
    QUEEN: queen_moves,
    KING: king_moves
}
