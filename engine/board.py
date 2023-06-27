"""
Board Class
"""

from itertools import product
from typing import Tuple, Union, overload

import numpy as np
import numpy.typing as npt

from engine.constants import BOARD_SIZE, UNICODE_PIECES, UNICODE_SQUARE
from engine.types import Color, Piece, PieceType


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

    def place_piece(self, piece: Tuple[Color, PieceType], location: Tuple[int, int]) -> None:
        if self.board[location[0], location[1], 3] != 0:
            raise ValueError(f"{location} already occupied.")
        self.board[location] = np.array([piece[0], piece[1], 0, 1], dtype=np.int8)

    def get_piece(self, loc: Tuple[int, int]) -> Piece:
        if self.board[loc[0], loc[1], 3] == 0:
            raise ValueError(f"No piece at {(loc[0], loc[1])}")
        return Piece(
            Color(self.board[loc[0], loc[1], 0]),
            PieceType(self.board[loc[0], loc[1], 1])
        )

    def clear(self) -> None:
        self.board.fill(0)

    @staticmethod
    def is_in_bounds(location: Tuple[int, int]) -> bool:
        return 0 <= location[0] < BOARD_SIZE and 0 <= location[1] < BOARD_SIZE

    @overload
    def __getitem__(self, index: Tuple[int, int]) -> npt.NDArray[np.int8]: ...
    @overload
    def __getitem__(
        self, index: Tuple[Union[int, slice], Union[int, slice], int]
    ) -> npt.NDArray[np.int8]: ...
    def __getitem__(
        self,
        index: Union[Tuple[int, int], Tuple[Union[int, slice], Union[int, slice], int]]
    ) -> npt.NDArray[np.int8]:
        if 2 <= len(index) <= 3:
            return self.board.__getitem__((*index, Ellipsis))
        raise IndexError(f"Invalid index {index} for Board.")

    @overload
    def __setitem__(
        self, index: Tuple[int, int], value: Union[npt.NDArray[np.int8], int]
    ) -> None: ...
    @overload
    def __setitem__(self, index: Tuple[int, int, int], value: int) -> None: ...
    def __setitem__(
        self, index: Tuple[int, ...], value: Union[npt.NDArray[np.int8], int]
    ) -> None:
        if 2 <= len(index) <= 3:
            self.board.__setitem__(index, value)
        else:
            raise IndexError(f"Invalid index {index} for Board.")

    def __str__(self) -> str:
        visual: str = ""
        for i, j in product(range(BOARD_SIZE), range(BOARD_SIZE)):
            if self.board[i, j, 3]:
                piece = self.get_piece((i, j))
                visual += f" {UNICODE_PIECES[piece.type][piece.color]} "
            else:
                square_color = Color.BLACK if (i % 2 == 0) ^ (j % 2 == 0) else Color.WHITE
                visual += f" {UNICODE_SQUARE[square_color]} "
            if j == BOARD_SIZE - 1:
                visual += "\n"
        return visual

    __repr__ = __str__
