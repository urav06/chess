from itertools import chain, permutations, product
from typing import Any, Generator, List, Optional, Tuple, Union

import numpy as np
import numpy.typing as npt

from config import BOARD_SIZE, UNICODE_PIECES, UNICODE_SQUARE
from engine_types import (
    DIAGONAL_DIRECTIONS, PARALLEL_DIRECTIONS, Color, Direction,
    Location, Move, MoveType, Piece, PieceType
)


class Board:
    """
    Board.board is an 8x8 matrix of squares.
    Values stored in a square are:
        0: Piece Color
        1: Piece Type
        2: Whether the piece has moved
        3: Whether the square is occupied
    """
    def __init__(self) -> None:
        self.board: npt.NDArray[np.int8] = np.full(
            shape=(BOARD_SIZE, BOARD_SIZE, 4), fill_value=0, dtype=np.int8
        )
        self.active_color = Color.WHITE

    def execute_move(self, move: Move) -> None:
        if move.type is MoveType.PASSING:
            self[move.end] = self[move.start]
            self[move.start] = 0
            self[move.end][2] = 1

        elif move.type is MoveType.CAPTURE:
            pass
        elif move.type is MoveType.CASTLE:
            pass
        else:
            raise ValueError(f'Unknown move type: {move.type}')

    def set_square(self, location: Location, piece: Optional[Piece]) -> None:
        """
        Places or removes a piece.

        :param piece: The piece to place. None to remove any piece.
        :param location: The location to place the piece.
        """
        if piece:
            if self[location][3] == 1:
                raise ValueError(f"{location} already occupied.")
            self[location] = np.array([piece.color, piece.type, 0, 1], dtype=np.int8)
        elif self[location][3] != 0:
            self[location] = 0

    def get_square(self, location: Location) -> Optional[Piece]:
        square: npt.NDArray[np.int8] = self[location]
        if square[3] == 0:
            return None
        return Piece(Color(square[0]), PieceType(square[1]))

    def get_legal_moves(self) -> list[Move]:
        # TODO: rename better + maybe this will be a generator + optimize
        return []

    @staticmethod
    def is_in_bounds(location: Union[Location, Tuple[int, int]]) -> bool:
        return 0 <= location[0] < BOARD_SIZE and 0 <= location[1] < BOARD_SIZE

    def __getitem__(self, location: Location) -> npt.NDArray[np.int8]:
        return self.board[location.i, location.j, :]

    def __setitem__(self, location: Location, value: Any) -> None:
        self.board[location.i, location.j] = value

    def __str__(self) -> str:
        visual: str = ""
        for i, j in product(range(BOARD_SIZE), range(BOARD_SIZE)):
            if (piece := self.get_square(Location(i, j))):
                visual += f" {UNICODE_PIECES[piece.type.name][piece.color.name]} "
            else:
                square_color = Color.BLACK if (i % 2 == 0) ^ (j % 2 == 0) else Color.WHITE
                visual += f" {UNICODE_SQUARE[square_color.name]} "
            if j == BOARD_SIZE - 1:
                visual += "\n"
        return visual

    __repr__ = __str__


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
