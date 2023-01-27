from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum, Flag, auto
from typing import ClassVar, Union, NamedTuple, Optional

from config import BOARD_SIZE, UNICODE_PIECES, UNICODE_SQUARE


class Color(Enum):
    """
    The two colors in chess: black and white.
    """
    BLACK = auto()
    WHITE = auto()


class SlidingVariation(Flag):
    """
    Denotes parallel movement & diagonal movement of pieces.
    """
    PARALLEL = auto()
    DIAGONAL = auto()


class MoveType(Enum):
    """
    Denotes the type of moves.

    PASSING: A piece moves without capturing.
    CAPTURE: A piece captures an opponent piece.
    CASTLE: Castling move.
    """
    PASSING = auto()
    CAPTURE = auto()
    CASTLE = auto()


class Direction(Enum):
    """
    Denotes the 8 eight directions on the chess board
    """
    NORTH = N = (-1, 0)
    SOUTH = S = (1, 0)
    EAST = E = (0, 1)
    WEST = W = (0, -1)
    NORTHEAST = NE = (-1, 1)
    NORTHWEST = NW = (-1, -1)
    SOUTHEAST = SE = (1, 1)
    SOUTHWEST = SW = (1, -1)


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
    ) -> Optional[Location]:
        """
        Returns a location in a particular direction relative to this point.
        Direction is absolute in reference to the board and indepndent of color.
        If the relative location is out of bounds, None is returned.
        """
        if type(direction) is Direction:
            direction_val: tuple[int, int] = direction.value
        elif type(direction) is tuple:
            direction_val = direction

        rel = Location(self.i+direction_val[0]*step, self.j+direction_val[1]*step)

        return rel if rel.is_in_bounds() else None

    def __repr__(self) -> str:
        return f"({self.i},{self.j})"


class Piece(ABC):
    """
    Abstract class to subclass all the pieces from.
    """

    name: str = "PIECE"
    color: Color
    loc: Location
    has_moved: bool

    def __init__(self, color: Color, location: Location) -> None:
        if not (isinstance(color, Color) or color in (Color.BLACK.value, Color.WHITE.value)):
            raise TypeError(f"Invalid color: {color}")
        if not isinstance(location, Location):
            raise TypeError(f"Invalid location: {location}")
        if not location.is_in_bounds():
            raise ValueError(f"Location out of bounds: {location}")
        self.color: Color = color
        self.loc: Location = location
        self.has_moved: bool = False

    def is_on(self, board: Board) -> bool:
        return board[self.loc] == self

    def is_opponent(self, another_piece: Piece) -> bool:
        return self.color != another_piece.color

    @abstractmethod
    def generate_moves(self, board: Board) -> list[Move]:
        pass

    def __str__(self) -> str:
        return UNICODE_PIECES[self.name][self.color.name]


class Board:

    size: ClassVar[int] = BOARD_SIZE
    board: list[list[Optional[Piece]]]
    white_graveyard: list[Piece]
    black_graveyard: list[Piece]

    def __init__(self) -> None:
        self.board = [[None for _ in range(self.size)] for __ in range(self.size)]

    def place_new_piece(
        self,
        piece_type: type[Piece],
        color: Color,
        location: Union[Location, tuple[int, int]]
    ) -> Piece:
        if type(location) is not Location:
            location = Location(*location)
        if not location.is_in_bounds():
            raise ValueError(f"Invalid location: {location}")
        if (existing_piece := self[location]):
            raise ValueError(f"A {existing_piece.name} already exists at {location}")
        new_pice: Piece = piece_type(color=color, location=location)
        self[location] = new_pice
        return new_pice

    def visualize(self) -> None:
        visual: str = ""
        for i in range(self.size):
            for j in range(self.size):
                piece: Optional[Piece] = self[Location(i, j)]
                square_color: Color = Color.BLACK if (i % 2 == 0) ^ (j % 2 == 0) else Color.WHITE
                square: str = UNICODE_SQUARE[square_color.name]
                visual += f" {piece} " if piece else f" {square} "
            visual += "\n"
        print(visual)

    def __getitem__(self, location: Location) -> Optional[Piece]:
        if not location.is_in_bounds():
            raise ValueError(f"Invalid location: {location}")
        return self.board[location.i][location.j]

    def __setitem__(self, location: Location, piece: Optional[Piece]) -> None:
        if not location.is_in_bounds():
            raise ValueError(f"Invalid location: {location}")
        self.board[location.i][location.j] = piece


class Move:
    """
    A class to represent a possible move for a given piece.

    piece: The piece that will make this move.
    type: The type of move. Passing, Capture or Castle.
    destination: The resulting location of the piece after the move is made.
    target_piece: The opponent piece being captured or the friendly rook in the case of castling.

    CASTLING: The move is only generated for the king. The rook is the target_piece.
        upon execution, both the pieces move.
    """

    piece: Piece
    type: MoveType
    destination: Location
    target_piece: Optional[Piece]

    def __init__(
        self,
        piece: Piece,
        type: MoveType,
        destination: Location,
        target_piece: Optional[Piece] = None
    ) -> None:
        if type in (MoveType.CAPTURE, MoveType.CASTLE) and target_piece is None:
            raise ValueError(f"Target piece not provided for {MoveType.CASTLE.name} move")

        if type == MoveType.CAPTURE and target_piece and destination != target_piece.loc:
            raise ValueError(
                f"Target not at the destination. {destination} != {target_piece.loc}"
            )

        self.piece = piece
        self.type = type
        self.destination = destination
        self.target_piece = target_piece

    def execute(self, board: Board) -> None:
        if not self.piece.is_on(board):
            raise ValueError(
                f"This {self.piece.color.name} {self.piece.name} is not on the board: {board}"
            )
        if self.target_piece and not self.target_piece.is_on(board):
            raise ValueError(
                f"Target {self.piece.color.name} {self.piece.name} is not on the board: {board}"
            )

        old_location = self.piece.loc
        match self.type:
            case MoveType.PASSING:
                self.piece.loc = self.destination
                board[old_location] = None
                board[self.destination] = self.piece

            case MoveType.CAPTURE:
                pass
            case MoveType.CASTLE:
                pass
            case _:
                raise ValueError(f"Invalid Move Type: {self.type}")

        self.piece.has_moved = True

    def __repr__(self) -> str:
        if self.type is MoveType.PASSING:
            return f"<{self.type.name}: {self.destination}>"
        else:
            return f"<{self.type.name} ({self.target_piece}): {self.destination}>"


class SlidingMixin(Piece):
    # TODO: AVOID INHERTANCE FROM PIECE.
    """
    Mixin Class to generate moves for pieces that move in straight lines.
    Applicable Pieces: Rook, Bishop, Queen.
    """

    PARALLEL_DIRECTIONS: ClassVar[list[Direction]] = (
        [Direction.N, Direction.S, Direction.E, Direction.W]
    )
    DIAGONAL_DIRECTIONS: ClassVar[list[Direction]] = (
        [Direction.NE, Direction.NW, Direction.SE, Direction.SW]
    )
    slidng_variation: SlidingVariation = SlidingVariation(0)
    sliding_step_limit: Union[int, float] = 0

    def generate_moves(self, board: Board) -> list[Move]:
        """
        Generates a list of moves physically possible for the piece on the given board.
        """
        can_move_parallelly = SlidingVariation.PARALLEL in self.slidng_variation
        can_move_diagonally = SlidingVariation.DIAGONAL in self.slidng_variation
        directions = (
            (self.PARALLEL_DIRECTIONS if can_move_parallelly else [])
            + (self.DIAGONAL_DIRECTIONS if can_move_diagonally else [])
        )
        moves: list[Move] = []
        for direction in directions:
            step: int = 1
            while (
                step <= self.sliding_step_limit
                and (dest := self.loc.get_relative(direction, step))
            ):
                target: Union[Piece, None] = board[dest]
                if target is None:
                    step += 1
                    moves.append(Move(self, MoveType.PASSING, dest))
                elif self.is_opponent(target):
                    moves.append(Move(self, MoveType.CAPTURE, dest, target))
                    break
                elif not self.is_opponent(target):
                    break
        return moves


class Pawn(Piece):

    name = "PAWN"

    def generate_moves(self, board: Board) -> list[Move]:
        """
        Generates a list of moves physically possible for the pawn on the given board.
        """
        moves: list[Move] = []
        front: Direction = Direction.N if self.color == Color.WHITE else Direction.S
        front_left: Direction = Direction.NW if self.color == Color.WHITE else Direction.SE
        front_right: Direction = Direction.NE if self.color == Color.WHITE else Direction.SW
        one_ahead: Optional[Location] = self.loc.get_relative(front)
        two_ahead: Optional[Location] = self.loc.get_relative(front, 2)
        attacking_diagonals: tuple[Optional[Location], Optional[Location]] = (
            self.loc.get_relative(front_left), self.loc.get_relative(front_right)
        )

        if one_ahead and board[one_ahead] is None:
            moves.append(Move(self, MoveType.PASSING, one_ahead))
            if not self.has_moved and two_ahead and board[two_ahead] is None:
                moves.append(Move(self, MoveType.PASSING, two_ahead))

        for dest in attacking_diagonals:
            if dest and (target := board[dest]) is not None and self.is_opponent(target):
                moves.append(Move(self, MoveType.CAPTURE, dest, target))

        return moves


class Knight(Piece):

    name = "KNIGHT"

    def generate_moves(self, board: Board) -> list[Move]:
        """
        Generates a list of moves physically possible for the knight on the given board.
        """
        moves: list[Move] = []
        for delta_i in [-2, -1, 1, 2]:
            for delta_j in [-2, -1, 1, 2]:
                if (
                    abs(delta_i) != abs(delta_j)
                    and (dest := self.loc.get_relative((delta_i, delta_j)))
                ):
                    if (target := board[dest]) is None:
                        moves.append(Move(self, MoveType.PASSING, dest))
                    elif target.color != self.color:
                        moves.append(Move(self, MoveType.CAPTURE, dest, target))
        return moves


class Bishop(SlidingMixin, Piece):

    slidng_variation = SlidingVariation.DIAGONAL
    sliding_step_limit = float('inf')
    name = "BISHOP"


class Rook(SlidingMixin, Piece):

    slidng_variation = SlidingVariation.PARALLEL
    sliding_step_limit = float('inf')
    name = "ROOK"


class Queen(SlidingMixin, Piece):

    slidng_variation = SlidingVariation.PARALLEL | SlidingVariation.DIAGONAL
    sliding_step_limit = float('inf')
    name = "QUEEN"


class King(SlidingMixin, Piece):

    slidng_variation = SlidingVariation.PARALLEL | SlidingVariation.DIAGONAL
    sliding_step_limit = 1
    name: str = "KING"
