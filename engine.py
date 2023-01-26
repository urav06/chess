from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum, Flag, auto
from typing import ClassVar, Union, NamedTuple, Optional

from config import BOARD_SIZE, UNICODE_PIECES, UNICODE_SQUARE


class Color(Enum):
    BLACK = "black"
    WHITE = "white"


class BoundMoveVariationFlag(Flag):
    """
    Denotes parallel movement & diagonal movement
    """
    PARALLEL = auto()
    DIAGONAL = auto()


class MoveType(Enum):
    PASSING = auto()
    CAPTURE = auto()
    CASTLE = auto()


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

    def __repr__(self) -> str:
        return f"({self.i},{self.j})"


class Piece(ABC):
    """
    Abstract class to subclass all the pieces from.
    """

    name = ""

    def __init__(self, color: Color, location: Location) -> None:
        if (not isinstance(color, Color)) and (color not in (Color.BLACK.value, Color.WHITE.value)):
            raise TypeError(f"Invalid color: {color}")
        if (not isinstance(location, Location)):
            raise TypeError(f"Invalid location: {location}")
        self.color: Color = color
        self.loc: Location = location
        self.has_moved: bool = False

    def is_on(self, board: Board) -> bool:
        return board.board[self.loc.i][self.loc.j] == self

    @staticmethod
    def trim_los_to_board(los: list[Location]) -> list[Location]:
        valid_range = range(0, BOARD_SIZE)
        return list(filter(lambda x: x.i in valid_range and x.j in valid_range, los))

    @abstractmethod
    def generate_moves(self, board: Board) -> list[Move]:
        pass

    def __str__(self) -> str:
        return UNICODE_PIECES[self.name][self.color.value]


class Board:

    size: ClassVar[int] = BOARD_SIZE

    def __init__(self) -> None:
        self.board: list[list[Union[Piece, None]]] = (
            [[None for _ in range(self.size)] for __ in range(self.size)]
        )

    def place_new_piece(self, piece_type: type[Piece], color: Color, location: Location) -> Piece:
        if (existing_piece := self.board[location.i][location.j]) is not None:
            raise ValueError(f"A {existing_piece.name} already exists at {location}")
        new_pice: Piece = piece_type(color=color, location=location)
        self.board[location.i][location.j] = new_pice
        return new_pice

    def visualize(self) -> None:
        visual: str = ""
        for i in range(self.size):
            for j in range(self.size):
                piece: Union[Piece, None] = self.board[i][j]
                square_color: Color = Color.BLACK if (i % 2 == 0) ^ (j % 2 == 0) else Color.WHITE
                square: str = UNICODE_SQUARE[square_color.value]
                visual += f" {piece} " if piece else f" {square} "
            visual += "\n"
        print(visual)


class Move:
    def __init__(self, piece: Piece, type: MoveType, loc: Location, target_piece: Union[Piece, None] = None) -> None:
        if type in (MoveType.CAPTURE, MoveType.CASTLE) and target_piece is None:
            raise ValueError(f"Target piece not provided for {MoveType.CASTLE.name} move")

        if type == MoveType.CAPTURE and target_piece and loc != target_piece.loc:
            raise ValueError(f"Target {target_piece.name} not at the location. {loc} != {target_piece.loc}")

        self.piece = piece
        self.type = type
        self.loc = loc
        self.target_piece = target_piece

    def execute(self, board: Board) -> None:
        if not self.piece.is_on(board):
            raise ValueError(f"This {self.piece.color.value} {self.piece.name} is not on the board: {board}")
        if self.target_piece and not self.target_piece.is_on(board):
            raise ValueError(f"This target {self.piece.color.value} {self.piece.name} is not on the board: {board}")

        match self.type:
            case MoveType.PASSING:
                board.board[self.piece.loc.i][self.piece.loc.j] = None
                board.board[self.loc.i][self.loc.j] = self.piece
                self.piece.loc = self.loc

            case MoveType.CAPTURE:
                pass
            case MoveType.CASTLE:
                pass
            case _:
                raise ValueError(f"Invalid Move Type: {self.type}")

        self.piece.has_moved = True


class BoundMoveMixin:
    """
    Mixin Class to generate moves for pieces that move in straight lines.
    Applicable Pieces: Rook, Bishop, Queen.
    """

    PARALLEL_DIRECTIONS = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    DIAGONAL_DIRECTIONS = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
    bound_move_variation = BoundMoveVariationFlag(0)
    bound_move_step_limit: Union[int, float] = 0
    loc: Location
    color: Color

    def generate_moves(self, board: Board) -> list[Move]:
        """
        Generates a list of moves physically possible for the piece on the given board.
        """
        can_move_parallelly = BoundMoveVariationFlag.PARALLEL in self.bound_move_variation
        can_move_diagonally = BoundMoveVariationFlag.DIAGONAL in self.bound_move_variation
        directions = (
            (self.PARALLEL_DIRECTIONS if can_move_parallelly else [])
            + (self.DIAGONAL_DIRECTIONS if can_move_diagonally else [])
        )
        moves = []
        for direction in directions:
            step = 1
            while (
                step <= self.bound_move_step_limit
                and (i_hat := self.loc.i+(direction[0]*step)) in (valid_range := range(0, BOARD_SIZE))
                and (j_hat := self.loc.j+(direction[1]*step)) in valid_range
            ):
                target: Union[Piece, None] = board.board[i_hat][j_hat]
                if target is None:
                    step += 1
                    moves.append(Move(self, MoveType.PASSING, Location(i_hat, j_hat)))
                elif target.color != self.color:
                    moves.append(Move(self, MoveType.CAPTURE, Location(i_hat, j_hat), target))
                    break
                elif target.color == self.color:
                    break
        return moves


class Pawn(Piece):

    name = "pawn"

    def generate_moves(self, board: Board) -> list[Move]:
        """
        Generates a list of moves physically possible for the pawn on the given board.
        """
        moves = []

        if self.color == Color.WHITE:
            one_ahead = Location(self.loc.i+1, self.loc.j)
            two_ahead = Location(self.loc.i+2, self.loc.j)
            left_diagonal = Location(self.loc.i+1, self.loc.j-1)
            right_diagonal = Location(self.loc.i+1, self.loc.j+1)
        if self.color == Color.BLACK:
            one_ahead = Location(self.loc.i-1, self.loc.j)
            two_ahead = Location(self.loc.i-2, self.loc.j)
            left_diagonal = Location(self.loc.i-1, self.loc.j+1)
            right_diagonal = Location(self.loc.i-1, self.loc.j-1)

        if one_ahead.is_in_bounds():
            target = board.board[one_ahead.i][one_ahead.j]
            if target is None:
                moves.append(Move(self, MoveType.PASSING, one_ahead))
                if not self.has_moved and two_ahead.is_in_bounds():
                    target_2 = board.board[two_ahead.i][two_ahead.j]
                    if target_2 is None:
                        moves.append(Move(self, MoveType.PASSING, two_ahead))

        for dest in (left_diagonal, right_diagonal):
            if dest.is_in_bounds():
                target: Optional[Piece] = board.board[dest.i][dest.j]
                if target is not None:
                    if target.color != self.color:
                        moves.append(Move(self, MoveType.CAPTURE, dest, target))

        return moves


class Knight(Piece):

    name = "knight"

    def generate_moves(self, board: Board) -> list[Move]:
        """
        Generates a list of moves physically possible for the knight on the given board.
        """
        moves = []
        for delta_i in [-2, -1, 1, 2]:
            for delta_j in [-2, -1, 1, 2]:
                dest = Location(self.loc.i+delta_i, self.loc.j+delta_j)
                if (
                    abs(delta_i) != abs(delta_j)
                    and dest.is_in_bounds()
                ):
                    target: Optional[Piece] = board.board[dest.i][dest.j]
                    if target is None:
                        moves.append(Move(self, MoveType.PASSING, dest))
                    elif target.color != self.color:
                        moves.append(Move(self, MoveType.CAPTURE, dest, target))
        return moves


class Bishop(BoundMoveMixin, Piece):

    bound_move_variation: BoundMoveVariationFlag = BoundMoveVariationFlag.DIAGONAL
    bound_move_step_limit = float('inf')
    name = "bishop"


class Rook(BoundMoveMixin, Piece):

    bound_move_variation: BoundMoveVariationFlag = BoundMoveVariationFlag.PARALLEL
    bound_move_step_limit = float('inf')
    name = "rook"


class Queen(BoundMoveMixin, Piece):

    bound_move_variation = BoundMoveVariationFlag.PARALLEL | BoundMoveVariationFlag.DIAGONAL
    bound_move_step_limit = float('inf')
    name = "queen"


class King(BoundMoveMixin, Piece):

    bound_move_variation = BoundMoveVariationFlag.PARALLEL | BoundMoveVariationFlag.DIAGONAL
    bound_move_step_limit = 1
    name = "king"


if __name__ == "__main__":
    some_bishop = Bishop(Color.BLACK, Location(0, 0))
    some_pawn = Pawn(Color.WHITE, Location(1, 0))
