from __future__ import annotations

from enum import Enum, Flag, auto
from typing import NamedTuple

from config import BOARD_SIZE


class Color(Enum):
    """
    The two colors in chess: black and white.
    """
    BLACK = 1
    WHITE = -1

    def __invert__(self) -> Color:
        return Color(self.value*-1)


class SlidingVariation(Flag):
    """
    Denotes parallel movement & diagonal movement of sliding pieces.
    """
    PARALLEL = auto()
    DIAGONAL = auto()


class MoveType(Enum):
    """
    Denotes the type of the move.

    PASSING: A piece moves without capturing.
    CAPTURE: A piece captures an opponent piece.
    CASTLE: The move where the king castles.
    """
    PASSING = auto()
    CAPTURE = auto()
    CASTLE = auto()


class Direction(Enum):
    """
    Denotes the 8 eight directions on the chess board.
    Absolute w.r.t. the board. Independednt of Color.
    """
    NORTH = N = (-1, 0)
    SOUTH = S = (1, 0)
    EAST = E = (0, 1)
    WEST = W = (0, -1)
    NORTHEAST = NE = (-1, 1)
    NORTHWEST = NW = (-1, -1)
    SOUTHEAST = SE = (1, 1)
    SOUTHWEST = SW = (1, -1)


PARALLEL_DIRECTIONS: list[Direction] = [Direction.N, Direction.S, Direction.E, Direction.W]
DIAGONAL_DIRECTIONS: list[Direction] = [Direction.NE, Direction.NW, Direction.SE, Direction.SW]


class Location(NamedTuple):
    """
    i: Vertical. Denoting Rank. 0 to 7
    j: Horizontal. Denoting File. 0 to 7
    """
    i: int
    j: int

    def is_in_bounds(self) -> bool:
        return 0 <= self.i < BOARD_SIZE and 0 <= self.j < BOARD_SIZE

    def get_relative(
        self,
        direction: tuple[int, int],
        step: int = 1
    ) -> Location:
        """
        Returns a location in a particular direction relative to this location.
        """
        return Location(self.i+direction[0]*step, self.j+direction[1]*step)

    def __repr__(self) -> str:
        return f"({self.i},{self.j})"
