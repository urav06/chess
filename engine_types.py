from enum import Enum, auto
from typing import NamedTuple


class Location(NamedTuple):
    i: int
    j: int


class MoveType(Enum):
    PASSING = auto()
    CAPTURE = auto()
    CASTLE = auto()


class Move(NamedTuple):
    start: Location
    end: Location
    type: MoveType


class Color(Enum):
    BLACK = auto()
    WHITE = auto()


class PieceType(Enum):
    PAWN = auto()
    KNIGHT = auto()
    BISHOP = auto()
    ROOK = auto()
    QUEEN = auto()
    KING = auto()


class Piece(NamedTuple):
    color: Color
    type: PieceType
