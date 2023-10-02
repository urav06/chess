"""
Game Class
"""
from __future__ import annotations

from functools import partial, wraps
from itertools import chain
from typing import Any, Callable, Generator, TypeVar, ParamSpec, cast

import numpy as np

from engine.board import Board
from engine.constants import BOARD_SIZE
from engine.pieces import PIECE_LOGIC_MAP
from engine.types import (
    Color, Direction, Location, Move, MoveType, Piece, PieceType,
    CAPTURE,  # MoveTypes
    KING, ROOK, QUEEN,  # PieceTypes
    WHITE,  # Colors
)

R = TypeVar('R')
P = ParamSpec('P')
GamePieceInfo = tuple[Piece, Location]


class Game:
    """
    Game is a match of chess between Black and White.
    This class provides an interface between the players and the game.
    """
    def __init__(self) -> None:
        self.board = Board()
        self.active_color = Color.WHITE

        self.seek_board = Board()

    @staticmethod
    def seekable(wrapped: Callable[P, R]) -> Callable[P, R]:
        """
        Decorator to select the board, and color to use for a method.
        """
        @wraps(wrapped)
        def wrapper(*args: P.args, **kwds: P.kwargs) -> R:
            self: Game = cast(Game, args[0])
            seek: bool = cast(bool, kwds.setdefault("seek", False))
            if seek:
                kwds["board"] = kwds.get("board") or self.seek_board
            else:
                kwds["board"] = kwds.get("board") or self.board
            kwds["color"] = kwds.get("color") or self.active_color
            return wrapped(*args, **kwds)
        return wrapper

    @seekable
    def add_piece(
        self, location: tuple[int, int], piece: tuple[Color, PieceType], **kwds: Any
    ) -> GamePieceInfo:
        board: Board = kwds["board"]

        board.place_piece(piece, location)
        return (Piece(*piece), Location(*location))

    @seekable
    def remove_piece(self, location: tuple[int, int], **kwds: Any) -> None:
        board: Board = kwds["board"]

        board.board[location] = 0

    @seekable
    def promote_piece(self, location: tuple[int, int], rank: PieceType, **kwds: Any) -> None:
        board: Board = kwds["board"]

        board.board[location[0], location[1], 1] = rank

    @seekable
    def move_piece(
        self, source: tuple[int, int], destination: tuple[int, int], **kwds: Any
    ) -> None:
        board: Board = kwds["board"]

        board.board[destination] = board.board[source]
        board.board[source] = 0
        board.board[destination[0], destination[1], 2] = 1  # Piece has moved

    def reset(self) -> None:
        self.board.clear()
        self.seek_board.clear()


    def execute_move(self, move: Move, seek: bool = False) -> None:
        if seek:
            # Refresh Seek Board Data
            np.copyto(self.seek_board.board, self.board.board)

        match move:
            case Move(start, end, MoveType.PASSING):
                self.move_piece(start, end, seek=seek)

            case Move(start, end, MoveType.CAPTURE, target=_):
                self.remove_piece(end, seek=seek)
                self.move_piece(start, end, seek=seek)

            case Move(start, end, MoveType.CASTLE, castle_type=castle_type):
                castling_kingside: bool = castle_type is KING
                rook_start = (start.i, (BOARD_SIZE-1 if castling_kingside else 0))
                rook_dest = end + (Direction.W if castling_kingside else Direction.E)
                self.move_piece(start, end, seek=seek)
                self.move_piece(rook_start, rook_dest, seek=seek)

            case Move(start, end, MoveType.PROMOTION, promotion_rank=rank) if rank:
                self.move_piece(start, end, seek=seek)
                self.promote_piece(end, rank, seek=seek)

            case Move(start, end, MoveType.CAPTURE_AND_PROMOTION, promotion_rank=rank) if rank:
                self.remove_piece(end, seek=seek)
                self.move_piece(start, end, seek=seek)
                self.promote_piece(end, rank, seek=seek)

            case _:
                raise ValueError(f'Invalid Move: {move}')

    @seekable
    def is_in_check(self, **kwds: Any) -> bool:
        color = kwds["color"]
        kwds["color"] = ~color
        return any(
            CAPTURE in move.type and move.target == KING
            for move in self.legal_moves(unsafe=True, **kwds)
        )

    def square_attacked(self, square: tuple[int, int], color: Color) -> bool:
        return any(
            move.end == square for move in self.legal_moves(unsafe=True, color=color)
        )

    def is_in_checkmate(self, color: Color) -> bool:
        return not any(self.legal_moves(color=color)) and self.is_in_check(color=color)

    def is_in_stalemate(self, color: Color) -> bool:
        return not any(self.legal_moves(color=color)) and not self.is_in_check(color=color)

    @seekable
    def legal_moves(self, unsafe: bool = False, **kwds: Any) -> Generator[Move, None, None]:
        """
        Generate all legal moves for the selected pieces.

        :param Color color: Color of the pieces to generate moves for.
        :param bool seek: Whether to use the seek board and pieces.
        :param set[GamePieceInfo] pieces: Set of pieces to generate moves for.
        """
        if kwds.get("piece"):
            pieces = {kwds["piece"]}
        else:
            pieces = self.board.get_pieces(kwds.get("color", self.active_color))
        piece_move_generator = chain.from_iterable(
            PIECE_LOGIC_MAP[p[0][1]](kwds["board"], Location(*p[1]), p[0][0]) for p in pieces
        )
        if kwds["seek"] or unsafe:
            yield from piece_move_generator
        else:
            yield from filter(partial(self.is_move_safe, kwds["color"]), piece_move_generator)
            yield from self.castling_moves(**kwds)

    @seekable
    def castling_moves(self, **kwds: Any) -> Generator[Move, None, None]:
        pieces = self.board.get_pieces(kwds.get("color", self.active_color))
        color = kwds["color"]
        row = BOARD_SIZE-1 if kwds["color"] is WHITE else 0
        king_loc = Location(row, 4)
        if all((
            (Piece(color, KING), king_loc) in pieces,
            (Piece(color, ROOK), Location(row, BOARD_SIZE-1)) in pieces,
            self.board.board[row, 4, 2] == 0,  # King has not moved
            self.board.board[row, BOARD_SIZE-1, 2] == 0,  # Kingside Rook has not moved
            not np.any(self.board.board[row, 4+1:BOARD_SIZE-1, 3]),  # No pieces in between
            not any(self.square_attacked((row, col), ~color) for col in range(4, 4+2)),
                # King doesn't pass through check
        )):
            yield Move(
                king_loc,
                Location(row, 4+2),
                type=MoveType.CASTLE,
                castle_type=KING
            )
        if all((
            (Piece(color, KING), king_loc) in pieces,
            (Piece(color, ROOK), Location(row, 0)) in pieces,
            self.board.board[row, 4, 2] == 0,  # King has not moved
            self.board.board[row, 0, 2] == 0,  # Queenside Rook has not moved
            not np.any(self.board.board[row, 1:4, 3]),  # No pieces in between
            not any(self.square_attacked((row, col), ~color) for col in range(4-2, 4+1)),
                # King doesn't pass through check
        )):
            yield Move(
                king_loc,
                Location(row, 4-2),
                type=MoveType.CASTLE,
                castle_type=QUEEN
            )

    def is_move_safe(self, color: Color, move: Move) -> bool:
        self.execute_move(move, seek=True)
        return not self.is_in_check(color=color, seek=True)
