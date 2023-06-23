"""
Movement logic of all the pieces
"""

from itertools import chain, permutations, product
from typing import Generator, List, Dict, Callable

from engine.board import Board
from engine.types import (
    DIAGONAL_DIRECTIONS, PARALLEL_DIRECTIONS, Color,
    Direction, Location, Move, MoveType, PieceType
)


def pawn_moves(board: Board, location: Location, color: Color) -> Generator[Move, None, None]:
    front: Direction = Direction.N if color is Color.WHITE else Direction.S
    one_ahead = location + front
    attack_diagonals = [one_ahead+Direction.E, one_ahead+Direction.W]

    for destination in attack_diagonals:
        if (
            board.is_in_bounds(destination)
            and board.is_occupied(destination)
            and (target := board.get_piece(destination)).color is ~color
        ):
            yield Move(location, destination, MoveType.CAPTURE, target)

    if board.is_in_bounds(one_ahead) and not board.is_occupied(one_ahead):
        yield Move(location, one_ahead, MoveType.PASSING)

        if (
            board[location[0], location[1], 2] == 0  # Has not moved
            and board.is_in_bounds(two_ahead := location + (2*front))
            and not board.is_occupied(two_ahead)
        ):
            yield Move(location, two_ahead, MoveType.PASSING)


def knight_moves(board: Board, location: Location, color: Color) -> Generator[Move, None, None]:
    deltas = [-2, -1, 1, 2]
    destination_gen: Generator[Location, None, None] = (
        location+v for v in permutations(deltas, 2) if abs(v[0]) != abs(v[1])
    )
    for destination in filter(Board.is_in_bounds, destination_gen):
        if not board.is_occupied(destination):
            yield Move(location, destination, MoveType.PASSING)
        elif (target := board.get_piece(destination)).color != color:
            yield Move(location, destination, MoveType.CAPTURE, target)


def bishop_moves(board: Board, location: Location, color: Color) -> Generator[Move, None, None]:
    yield from chain.from_iterable(
        slide_moves(board, location, color, d) for d in DIAGONAL_DIRECTIONS
    )


def rook_moves(board: Board, location: Location, color: Color) -> Generator[Move, None, None]:
    yield from chain.from_iterable(
        slide_moves(board, location, color, d) for d in PARALLEL_DIRECTIONS
    )


def queen_moves(board: Board, location: Location, color: Color) -> Generator[Move, None, None]:
    directions: List[Direction] = PARALLEL_DIRECTIONS + DIAGONAL_DIRECTIONS
    yield from chain.from_iterable(
        slide_moves(board, location, color, d) for d in directions
    )


def king_moves(board: Board, location: Location, color: Color) -> Generator[Move, None, None]:
    deltas = [-1, 0, 1]
    destination_gen: Generator[Location, None, None] = (
        location+v for v in product(deltas, deltas) if v != (0, 0)
    )
    for destination in filter(Board.is_in_bounds, destination_gen):
        if not board.is_occupied(destination):
            yield Move(location, destination, MoveType.PASSING)
        elif (target := board.get_piece(destination)).color != color:
            yield Move(location, destination, MoveType.CAPTURE, target)


def slide_moves(
    board: Board, location: Location, color: Color, direction: Direction
) -> Generator[Move, None, None]:
    step = 1
    while Board.is_in_bounds(destination := location+(direction*step)):
        if not board.is_occupied(destination):
            yield Move(location, destination, MoveType.PASSING)
            step += 1
        elif (target := board.get_piece(destination)).color != color:
            yield Move(location, destination, MoveType.CAPTURE, target)
            break
        elif target.color == color:
            break


PIECE_LOGIC_MAP: Dict[
    PieceType, Callable[[Board, Location, Color], Generator[Move, None, None]]
] = {
    PieceType.PAWN: pawn_moves,
    PieceType.KNIGHT: knight_moves,
    PieceType.BISHOP: bishop_moves,
    PieceType.ROOK: rook_moves,
    PieceType.QUEEN: queen_moves,
    PieceType.KING: king_moves
}
