from itertools import chain, permutations, product
from typing import Generator, List, Optional, Dict, Callable

from engine.board import Board
from engine.types import (
    DIAGONAL_DIRECTIONS, PARALLEL_DIRECTIONS, Color,
    Direction, Location, Move, MoveType, Piece, PieceType
)


def pawn_moves(board: Board, location: Location, color: Color) -> Generator[Move, None, None]:
    color = board[location][0]  # TODO: find better way to abstract piece vector
    if color == 0:
        pass
    yield Move(Location(0, 0), Location(0, 0), MoveType.PASSING)


def knight_moves(board: Board, location: Location, color: Color) -> Generator[Move, None, None]:
    deltas = [-2, -1, 1, 2]
    destination_gen: Generator[Location, None, None] = (
        location+v for v in permutations(deltas, 2) if abs(v[0]) != abs(v[1])
    )
    for destination in filter(Board.is_in_bounds, destination_gen):
        target: Optional[Piece] = board.get_square(destination)
        if target is None:
            yield Move(location, destination, MoveType.PASSING)
        elif target.color != color:
            yield Move(location, destination, MoveType.CAPTURE)


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
        target: Optional[Piece] = board.get_square(destination)
        if target is None:
            yield Move(location, destination, MoveType.PASSING)
        elif target.color != color:
            yield Move(location, destination, MoveType.CAPTURE)


def slide_moves(
    board: Board, location: Location, color: Color, direction: Direction
) -> Generator[Move, None, None]:
    step = 1
    while Board.is_in_bounds(destination := location+(direction*step)):
        target: Optional[Piece] = board.get_square(destination)
        if target is None:
            yield Move(location, destination, MoveType.PASSING)
            step += 1
        elif target.color != color:
            yield Move(location, destination, MoveType.CAPTURE)
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
