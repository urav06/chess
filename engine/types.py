"""
Types used in the Chess engine.
"""
from __future__ import annotations
from enum import Enum, IntEnum, auto
from typing import NamedTuple, Union, Tuple, Any, Optional
from typing_extensions import SupportsIndex


class Location(NamedTuple):
    i: int
    j: int

    def __add__(self, __other: Tuple[Any, ...]) -> Location:
        if isinstance(__other, Vector):
            return Location(self.i+__other.i, self.j+__other.j)
        elif len(__other) == 2:
            return Location(self.i+__other[0], self.j+__other[1])
        raise NotImplementedError(f"Can't add Location and {__other}")


class Vector(NamedTuple):
    i: int
    j: int

    def __mul__(self, __value: Union[SupportsIndex, int]) -> Vector:
        if isinstance(__value, int):
            return Vector(self.i*__value, self.j*__value)
        raise NotImplementedError(f"Can't multiply Vector and {type(__value)}")

    def __rmul__(self, __value: Union[SupportsIndex, int]) -> Vector:
        return self.__mul__(__value)


class Direction(Vector, Enum):
    N = Vector(-1, 0)
    S = Vector(1, 0)
    E = Vector(0, 1)
    W = Vector(0, -1)
    NE = Vector(-1, 1)
    NW = Vector(-1, -1)
    SE = Vector(1, 1)
    SW = Vector(1, -1)


class MoveType(IntEnum):
    PASSING = auto()
    CAPTURE = auto()
    CASTLE = auto()
    PROMOTION = auto()


class Move(NamedTuple):
    start: Location
    end: Location
    type: MoveType
    promotion_rank: Optional[PieceType] = None


class Color(IntEnum):
    BLACK = auto()  # Starts with 1
    WHITE = auto()

    def __invert__(self) -> Color:
        return Color.WHITE if self is Color.BLACK else Color.BLACK


class PieceType(IntEnum):
    PAWN = auto()  # Starts with 1
    KNIGHT = auto()
    BISHOP = auto()
    ROOK = auto()
    QUEEN = auto()
    KING = auto()


class Piece(NamedTuple):
    color: Color
    type: PieceType


PARALLEL_DIRECTIONS = [Direction.N, Direction.S, Direction.E, Direction.W]
DIAGONAL_DIRECTIONS = [Direction.NE, Direction.NW, Direction.SE, Direction.SW]
