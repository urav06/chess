from abc import ABC, abstractmethod
from enum import Enum, Flag, auto
from typing import Union, TYPE_CHECKING

import config
if TYPE_CHECKING:
    from board import Board

class Color(Enum):
    BLACK = "black"
    WHITE = "white"

class BoundMoveVariationFlag(Flag):
    """
    Denotes parallel movement & diagonal movement
    """
    PARALLEL = auto()
    DIAGONAL = auto()


class Location():
    """
    i: Vertical. Denoting Rank. 0 to 7
    j: Horizontal. Denoting File. 0 to 7
    """
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j

    def __repr__(self) -> str:
        return f"({self.i},{self.j})"

class Piece(ABC):
    """
    Abstract class to subclass all the pieces from.
    """

    def __init__(self, color: Color, location: Location) -> None:
        if (not isinstance(color, Color)) and (color not in (Color.BLACK, Color.WHITE)):
            raise TypeError(f"Invalid color: {color}")
        if (not isinstance(location, Location)):
            raise TypeError(f"Invalid location: {location}")
        self.color = color
        self.loc = location
        self.has_moved = False

    @staticmethod
    def trim_los_to_board(los):
        valid_range = range(0,config.BOARD_SIZE)
        return list(filter(lambda x: x.i in valid_range and x.j in valid_range, los))

class BoundMoveMixin:
    """
    Mixin Class to generate moves for pieces that move in straight lines.
    Applicable Pieces: Rook, Bishop, Queen.
    """

    PARALLEL_DIRECTIONS = [(-1,0), (0,-1), (1,0), (0,1)]
    DIAGONAL_DIRECTIONS = [(-1,-1), (1,-1), (-1,1), (1,1)]
    bound_move_variation = BoundMoveVariationFlag(0)
    bound_move_step_limit = 0

    def generate_moves(self: Union[Piece, 'BoundMoveMixin'], board):
        """
        Generates a list of moves physically possible for the piece on the given board.
        """
        can_move_parallelly = BoundMoveVariationFlag.PARALLEL in self.bound_move_variation
        can_move_diagonally = BoundMoveVariationFlag.DIAGONAL in self.bound_move_variation
        directions = (
            (self.PARALLEL_DIRECTIONS if can_move_parallelly else [])
            +(self.DIAGONAL_DIRECTIONS if can_move_diagonally else [])
        )
        locs = []
        for direction in directions:
            step = 1
            while (
                step <= self.bound_move_step_limit
                and (i_hat := self.loc.i+(direction[0]*step)) in (valid_range := range(0, config.BOARD_SIZE))
                and (j_hat := self.loc.j+(direction[1]*step)) in valid_range
                and board.board[i_hat][j_hat] is None
            ):
                #TODO: Implement Attack + Optimize / Readibility
                step+=1
                locs.append(Location(i_hat, j_hat))
        return locs


class Pawn(Piece):
    def generate_moves(self) -> list[Location]:
        """
        Generates a list of moves physically possible for the pawn on the given board.
        """
        los = []
        #TODO: Capure/Attack Logic
        if self.color == Color.WHITE:
            los = [Location(self.loc.i+1, self.loc.j+d) for d in (-1, 0 , 1)]
            if not self.has_moved:
                los.append(Location(self.loc.i+2, self.loc.j))
        if self.color == Color.BLACK:
            los = [Location(self.loc.i-1, self.loc.j+d) for d in (-1, 0 , 1)]
            if not self.has_moved:
                los.append(Location(self.loc.i-2, self.loc.j))
        return self.trim_los_to_board(los)

    def __str__(self) -> str:
        return config.UNICODE_PAWN[self.color.value]

class Knight(Piece):
    def generate_moves(self) -> list[Location]:
        """
        Generates a list of moves physically possible for the knight on the given board.
        """
        locs = []
        for delta_i in [-2, -1, 1, 2]:
            for delta_j in [-2, -1, 1, 2]:
                if (
                    abs(delta_i) != abs(delta_j)
                    and (i_hat := self.loc.i+delta_i) in (valid_range := range(0, config.BOARD_SIZE))
                    and (j_hat :=  self.loc.j+delta_j) in valid_range
                ):
                    locs.append(Location(i_hat, j_hat))
        return locs

    def __str__(self) -> str:
        return config.UNICODE_KNIGHT[self.color.value]

class Bishop(Piece, BoundMoveMixin):

    bound_move_variation = BoundMoveVariationFlag.DIAGONAL
    bound_move_step_limit = float('inf')
    
    def __str__(self) -> str:
        return config.UNICODE_BISHOP[self.color.value]

class Rook(Piece, BoundMoveMixin):

    bound_move_variation = BoundMoveVariationFlag.PARALLEL
    bound_move_step_limit = float('inf')

    def __str__(self) -> str:
        return config.UNICODE_ROOK[self.color.value]

class Queen(Piece, BoundMoveMixin):

    bound_move_variation = BoundMoveVariationFlag.PARALLEL | BoundMoveVariationFlag.DIAGONAL
    bound_move_step_limit = float('inf')

    def __str__(self) -> str:
        return config.UNICODE_QUEEN[self.color.value]


class King(Piece, BoundMoveMixin):

    bound_move_variation = BoundMoveVariationFlag.PARALLEL | BoundMoveVariationFlag.DIAGONAL
    bound_move_step_limit = 1

    def __str__(self) -> str:
        return config.UNICODE_KING[self.color.value]


if __name__ == "__main__":
    some_bishop = Bishop(Color.BLACK, Location(0,0))
    some_pawn = Pawn(Color.WHITE, Location(1,0))