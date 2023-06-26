"""
Types used in the Chess engine.
"""
from __future__ import annotations
from enum import Enum, IntEnum, auto, IntFlag
from typing import NamedTuple, Union, Tuple, Any, Optional
from typing_extensions import SupportsIndex


class Location(NamedTuple):
    i: int
    j: int

    def __add__(self, __other: Tuple[Any, ...]) -> Location:
        if isinstance(__other, Vector):
            return Location(self.i+__other.i, self.j+__other.j)
        if len(__other) == 2:
            return Location(self.i+__other[0], self.j+__other[1])
        raise NotImplementedError(f"Can't add Location and {__other}")

    def __str__(self) -> str:
        return f"({self.i}, {self.j})"

    def __repr__(self) -> str:
        return str(self)


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


class MoveType(IntFlag):
    PASSING = auto()
    CAPTURE = auto()
    CASTLE = auto()
    PROMOTION = auto()
    CAPTURE_AND_PROMOTION = CAPTURE | PROMOTION

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)


class CastleType(IntEnum):
    QUEENSIDE = auto()
    KINGSIDE = auto()

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)


class Move(NamedTuple):
    start: Location
    end: Location
    type: MoveType = MoveType.PASSING
    target: Optional[Piece] = None
    castle_type: Optional[CastleType] = None
    promotion_rank: Optional[PieceType] = None


class Color(IntEnum):
    BLACK = auto()  # Starts with 1
    WHITE = auto()

    def __invert__(self) -> Color:
        return Color.WHITE if self is Color.BLACK else Color.BLACK

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)


class PieceType(IntEnum):
    PAWN = auto()  # Starts with 1
    KNIGHT = auto()
    BISHOP = auto()
    ROOK = auto()
    QUEEN = auto()
    KING = auto()

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)


class Piece(NamedTuple):
    color: Color
    type: PieceType

# Constants
PARALLEL_DIRECTIONS = [Direction.N, Direction.S, Direction.E, Direction.W]
DIAGONAL_DIRECTIONS = [Direction.NE, Direction.NW, Direction.SE, Direction.SW]

# Aliases
BLACK = Color.BLACK
WHITE = Color.WHITE

PAWN = PieceType.PAWN
KNIGHT = PieceType.KNIGHT
BISHOP = PieceType.BISHOP
ROOK = PieceType.ROOK
QUEEN = PieceType.QUEEN
KING = PieceType.KING

PASSING = MoveType.PASSING
CAPTURE = MoveType.CAPTURE
CASTLE = MoveType.CASTLE
PROMOTION = MoveType.PROMOTION
CAPTURE_AND_PROMOTION = MoveType.CAPTURE_AND_PROMOTION
