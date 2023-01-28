from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Union, Optional, Dict

from engine_types import (
    Color, SlidingVariation, MoveType, Direction, Location,
    PARALLEL_DIRECTIONS, DIAGONAL_DIRECTIONS
)
from config import BOARD_SIZE, UNICODE_PIECES, UNICODE_SQUARE


class Piece(ABC):
    """
    Abstract class to subclass all the pieces from.
    """

    name: str = "PIECE"
    color: Color
    loc: Location
    has_moved: bool
    is_captured: bool

    def __init__(self, color: Color, location: Location) -> None:
        self.color = color
        self.loc = location
        self.has_moved = False
        self.is_captured = False

    def is_opponent(self, another_piece: Piece) -> bool:
        return self.color != another_piece.color

    @abstractmethod
    def generate_moves(self, board: Board) -> list[Move]:
        pass

    def __str__(self) -> str:
        return UNICODE_PIECES[self.name][self.color.name]


class Board:

    board: list[list[Optional[Piece]]]
    graveyard: Dict[Color, list[Piece]]

    def __init__(self) -> None:
        self.board = [[None for _ in range(BOARD_SIZE)] for __ in range(BOARD_SIZE)]
        self.graveyard = {Color.BLACK: [], Color.WHITE: []}

    def place_new(self, piece_type: type[Piece], color: Color, location: Location) -> Piece:
        if self[location] is not None:
            raise ValueError(f"Location {location} is not vacant: {self[location]}")
        new_pice: Piece = piece_type(color=color, location=location)
        self[location] = new_pice
        return new_pice

    def execute_move(self, move: Move) -> None:
        match move.type:
            case MoveType.PASSING:
                self._move_piece(move.piece, move.destination)
            case MoveType.CAPTURE:
                assert move.target_piece is not None
                assert move.target_piece.loc == move.destination
                self._capture_piece(move.target_piece)
                self._move_piece(move.piece, move.destination)
            case MoveType.CASTLE:
                pass

    def _capture_piece(self, piece: Piece) -> None:
        self[piece.loc] = None
        piece.is_captured = True
        self.graveyard[piece.color].append(piece)

    def _move_piece(self, piece: Piece, destination: Location) -> None:
        self[piece.loc] = None
        piece.loc = destination
        self[destination] = piece
        piece.has_moved = True

    def __str__(self) -> str:
        visual: str = ""
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                piece: Optional[Piece] = self[Location(i, j)]
                square_color: Color = Color.BLACK if (i % 2 == 0) ^ (j % 2 == 0) else Color.WHITE
                square_repr: str = UNICODE_SQUARE[square_color.name]
                visual += f" {piece} " if piece else f" {square_repr} "
            visual += "\n"
        return visual

    def __getitem__(self, location: Location) -> Optional[Piece]:
        if not location.is_in_bounds():
            raise ValueError(f"Location is out of bounds: {location}")
        return self.board[location.i][location.j]

    def __setitem__(self, location: Location, piece: Optional[Piece]) -> None:
        if not location.is_in_bounds():
            raise ValueError(f"Location is out of bounds: {location}")
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
        self, piece: Piece,
        type: MoveType,
        destination: Location,
        target_piece: Optional[Piece] = None
    ) -> None:
        if type in (MoveType.CAPTURE, MoveType.CASTLE) and target_piece is None:
            raise ValueError(f"Target piece not provided for {type.name} move")

        if type == MoveType.CAPTURE and target_piece and destination != target_piece.loc:
            raise ValueError(
                f"Target not at the destination. {destination} != {target_piece.loc}"
            )

        self.piece = piece
        self.type = type
        self.destination = destination
        self.target_piece = target_piece

    def __repr__(self) -> str:
        if self.type is MoveType.PASSING:
            return f"<{self.type.name}: {self.destination}>"
        else:
            return f"<{self.type.name} ({self.target_piece}): {self.destination}>"


class SlidingPiece(Piece):
    """
    Mixin Class to generate moves for pieces that move in straight lines.
    Applicable Pieces: Rook, Bishop, Queen.
    """

    slidng_variation: SlidingVariation = SlidingVariation(0)
    sliding_step_limit: Union[int, float] = 0

    def generate_moves(self, board: Board) -> list[Move]:
        """
        Generates a list of moves physically possible for the sliding piece on the given board.
        """
        can_move_parallelly: bool = SlidingVariation.PARALLEL in self.slidng_variation
        can_move_diagonally: bool = SlidingVariation.DIAGONAL in self.slidng_variation
        directions = (
            (PARALLEL_DIRECTIONS if can_move_parallelly else [])
            + (DIAGONAL_DIRECTIONS if can_move_diagonally else [])
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


class Bishop(SlidingPiece):

    slidng_variation = SlidingVariation.DIAGONAL
    sliding_step_limit = float('inf')
    name = "BISHOP"


class Rook(SlidingPiece):

    slidng_variation = SlidingVariation.PARALLEL
    sliding_step_limit = float('inf')
    name = "ROOK"


class Queen(SlidingPiece):

    slidng_variation = SlidingVariation.PARALLEL | SlidingVariation.DIAGONAL
    sliding_step_limit = float('inf')
    name = "QUEEN"


class King(SlidingPiece):

    slidng_variation = SlidingVariation.PARALLEL | SlidingVariation.DIAGONAL
    sliding_step_limit = 1
    name: str = "KING"
