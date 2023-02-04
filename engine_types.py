from __future__ import annotations

from enum import Enum, Flag, auto
from typing import NamedTuple, Union

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
        valid_range = range(0, BOARD_SIZE)
        return self.i in valid_range and self.j in valid_range

    def get_relative(
        self,
        direction: Union[Direction, tuple[int, int]],
        step: int = 1
    ) -> Location:
        """
        Returns a location in a particular direction relative to this location.
        """
        if type(direction) is Direction:
            direction_value: tuple[int, int] = direction.value
        elif type(direction) is tuple:
            direction_value = direction
        return Location(self.i+direction_value[0]*step, self.j+direction_value[1]*step)

    def __repr__(self) -> str:
        return f"({self.i},{self.j})"
