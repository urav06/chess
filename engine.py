import numpy as np
import numpy.typing as npt
from typing import Generator, Optional

from engine_types import Location, Move, MoveType, Piece, Color, PieceType


class Board:

    def __init__(self) -> None:
        self.board: npt.NDArray[np.int8] = np.full(shape=(8, 8, 4), fill_value=0, dtype=np.int8)
        self.active_color = Color.WHITE

    def execute_move(self, move: Move) -> None:
        if move.type is MoveType.PASSING:
            self.board[move.end] = self.board[move.start]
            self.board[move.start] = 0

        elif move.type is MoveType.CAPTURE:
            pass
        elif move.type is MoveType.CASTLE:
            pass
        else:
            raise ValueError(f'Unknown move type: {move.type}')

    def place_new(self, piece: Piece, location: Location) -> None:
        """
        Places a new piece on the board.
        Values stored in the board are:
            0: Piece type
            1: Piece color
            2: Whether the piece has moved
            3: Whether the square is occupied

        :param piece: The piece to place.
        :param location: The location to place the piece.
        """
        if self.board[location][3] == 1:
            raise ValueError(f'Cannot place piece at {location} because it is already occupied.')
        self.board[location] = np.array([piece.type.value, piece.color.value, 0, 1])

    def get_piece(self, location: Location) -> Optional[Piece]:
        square: npt.NDArray[np.int8] = self.board[location]
        if square[3] == 0:  # Square Unoccupied
            return None
        else:  # Square Occupied
            return Piece(Color(square[1]), PieceType(square[0]))

    def get_legal_moves(self) -> list[Move]:
        # TODO: rename better + maybe this will be a generator + optimize
        return []

    def __getitem__(self, location: Location) -> npt.NDArray[np.int8]:
        return self.board[location.i, location.j, :]

    def __setitem__(self, location: Location, value: npt.NDArray[np.int8]) -> None:
        self.board[location.i, location.j] = value


def pawn_moves(board: Board, location: Location) -> Generator[Move, None, None]:
    color = board[location][0]  # TODO: find better way to abstract piece vector
    if color == 0:
        pass
    yield Move(Location(0, 0), Location(0, 0), MoveType.PASSING)


def knight_moves(board: Board, location: Location) -> Generator[Move, None, None]:
    yield Move(Location(0, 0), Location(0, 0), MoveType.PASSING)


def bishop_moves(board: Board, location: Location) -> Generator[Move, None, None]:
    yield Move(Location(0, 0), Location(0, 0), MoveType.PASSING)


def rook_moves(board: Board, location: Location) -> Generator[Move, None, None]:
    yield Move(Location(0, 0), Location(0, 0), MoveType.PASSING)


def queen_moves(board: Board, location: Location) -> Generator[Move, None, None]:
    yield Move(Location(0, 0), Location(0, 0), MoveType.PASSING)


def king_moves(board: Board, location: Location) -> Generator[Move, None, None]:
    yield Move(Location(0, 0), Location(0, 0), MoveType.PASSING)
