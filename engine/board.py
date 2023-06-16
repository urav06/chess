from itertools import product
from typing import Any, Optional, Tuple, Union

import numpy as np
import numpy.typing as npt

from config import BOARD_SIZE, UNICODE_PIECES, UNICODE_SQUARE
from engine.types import (
    Color, Location, Piece, PieceType
)


class Board:
    """
    Board.board is an 8x8 matrix of squares.
    Values stored in a square are:
        0: Piece Color
        1: Piece Type
        2: Whether the piece has moved
        3: Whether the square is occupied
    """
    def __init__(self) -> None:
        self.board: npt.NDArray[np.int8] = np.full(
            shape=(BOARD_SIZE, BOARD_SIZE, 4), fill_value=0, dtype=np.int8
        )

    def set_square(self, location: Location, piece: Optional[Piece]) -> None:
        """
        Places or removes a piece.

        :param piece: The piece to place. None to remove any piece.
        :param location: The location to place the piece.
        """
        if piece:
            if self[location.i, location.j, 3] == 1:
                raise ValueError(f"{location} already occupied.")
            self[location] = np.array([piece.color, piece.type, 0, 1], dtype=np.int8)
        elif self[location.i, location.j, 3] != 0:
            self[location] = 0

    def get_square(self, location: Location) -> Optional[Piece]:
        if self[location.i, location.j, 3] == 0:
            return None
        return Piece(
            Color(int(self[location.i, location.j, 0])),
            PieceType(int(self[location.i, location.j, 1]))
        )

    def clear(self) -> None:
        self.board.fill(0)

    @staticmethod
    def is_in_bounds(location: Union[Location, Tuple[int, int]]) -> bool:
        return 0 <= location[0] < BOARD_SIZE and 0 <= location[1] < BOARD_SIZE

    def __getitem__(self, *args: Any) -> npt.NDArray[np.int8]:
        # TODO: Improve further as a passover function
        if len(args[0]) == 2:
            return self.board[args[0][0], args[0][1], ...]
        if len(args[0]) == 3:
            return self.board[args[0][0], args[0][1], args[0][2], ...]
        raise Exception(f"Invalid index {args[0]} for Board.")

    def __setitem__(self, *args: Any) -> None:
        # TODO: Improve further as a passover function
        if len(args[0]) == 2:
            self.board[args[0][0], args[0][1]] = args[1]
        elif len(args[0]) == 3:
            self.board[args[0][0], args[0][1], args[0][2]] = args[1]
        else:
            raise Exception(f"Invalid index {args[0]} for Board.")

    def __str__(self) -> str:
        visual: str = ""
        for i, j in product(range(BOARD_SIZE), range(BOARD_SIZE)):
            if (piece := self.get_square(Location(i, j))):
                visual += f" {UNICODE_PIECES[piece.type.name][piece.color.name]} "
            else:
                square_color = Color.BLACK if (i % 2 == 0) ^ (j % 2 == 0) else Color.WHITE
                visual += f" {UNICODE_SQUARE[square_color.name]} "
            if j == BOARD_SIZE - 1:
                visual += "\n"
        return visual

    __repr__ = __str__
