"""
Board Class
"""

from itertools import product
from typing import Optional, Tuple, Union, overload

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

    def place_piece(self, piece: Piece, location: Tuple[int, int]) -> None:
        if self[location[0], location[1], 3] != 0:
            raise ValueError(f"{location} already occupied.")
        self[location] = np.array([piece.color, piece.type, 0, 1], dtype=np.int8)

    def update_rank(self, location: Tuple[int, int], rank: Optional[PieceType]) -> None:
        # Remove optional
        if rank:
            self[location[0], location[1], 1] = rank

    @overload
    def is_occupied(self, arg1: Tuple[int, int]) -> bool: ...
    @overload
    def is_occupied(self, arg1: int, arg2: int) -> bool: ...
    def is_occupied(self, arg1: Union[Tuple[int, int], int], arg2: Optional[int] = None) -> bool:
        i, j = self.__unpack_index_args(arg1, arg2)
        return int(self[i, j, 3]) != 0

    @overload
    def get_piece(self, arg1: Tuple[int, int]) -> Piece: ...
    @overload
    def get_piece(self, arg1: int, arg2: int) -> Piece: ...
    def get_piece(self, arg1: Union[Tuple[int, int], int], arg2: Optional[int] = None) -> Piece:
        i, j = self.__unpack_index_args(arg1, arg2)
        if self[i, j, 3] == 0:
            raise ValueError(f"No piece at {(i, j)}")
        return Piece(Color(int(self[i, j, 0])), PieceType(int(self[i, j, 1])))

    def clear(self) -> None:
        self.board.fill(0)

    @staticmethod
    def is_in_bounds(location: Tuple[int, int]) -> bool:
        return 0 <= location[0] < BOARD_SIZE and 0 <= location[1] < BOARD_SIZE

    @overload
    def __getitem__(self, index: Tuple[int, int]) -> npt.NDArray[np.int8]: ...
    @overload
    def __getitem__(self, index: Tuple[int, int, int]) -> npt.NDArray[np.int8]: ...
    def __getitem__(
        self, index: Union[Tuple[int, int], Tuple[int, int ,int]]
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

    @staticmethod
    def __unpack_index_args(
        arg1: Union[Tuple[int, int], int], arg2: Optional[int] = None
    ) -> Tuple[int, int]:
        if isinstance(arg1, int) and isinstance(arg2, int):
            return arg1, arg2
        if isinstance(arg1, tuple):
            return arg1
        raise IndexError(f"Invalid index {(arg1, arg2)} for Board.")

    def __str__(self) -> str:
        visual: str = ""
        for i, j in product(range(BOARD_SIZE), range(BOARD_SIZE)):
            if self.is_occupied(i, j):
                piece = self.get_piece(i, j)
                visual += f" {UNICODE_PIECES[piece.type][piece.color]} "
            else:
                square_color = Color.BLACK if (i % 2 == 0) ^ (j % 2 == 0) else Color.WHITE
                visual += f" {UNICODE_SQUARE[square_color]} "
            if j == BOARD_SIZE - 1:
                visual += "\n"
        return visual

    __repr__ = __str__
