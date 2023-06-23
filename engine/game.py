"""
Game Class
"""
from __future__ import annotations

from functools import partial, wraps
from itertools import chain
from typing import Any, Callable, Generator, Set, Tuple, TypeVar

import numpy as np

from engine.board import Board
from engine.constants import BOARD_SIZE
from engine.pieces import PIECE_LOGIC_MAP
from engine.types import (
    CastleType, Color, Direction, Location, Move,MoveType, Piece, PieceType
)

R = TypeVar('R')

def seekable(wrapped: Callable[..., R]) -> Callable[..., R]:
    @wraps(wrapped)
    def wrapper(game: Game, *args: Any, **kwds: Any) -> Any:
        seek = kwds.setdefault("seek", False)
        if seek:
            kwds.setdefault("board", game.seek_board)
            kwds.setdefault("pieces", game.seek_board_pieces)
        else:
            kwds.setdefault("board", game.board)
            kwds.setdefault("pieces", game.active_pieces)
        return wrapped(game, *args, **kwds)
    return wrapper


class Game:
    """
    Game is a match of chess between Black and White.
    This class provides an interface between the players and the game.
    """
    def __init__(self) -> None:
        self.board = Board()
        self.active_pieces: Set[Tuple[Piece, Location]] = set()
        self.active_color = Color.WHITE

        self.seek_board = Board()
        self.seek_board_pieces: Set[Tuple[Piece, Location]] = set()

    def filter_color_pieces(self, color: Color, seek: bool = False) -> Set[Tuple[Piece, Location]]:
        pieces = self.seek_board_pieces if seek else self.active_pieces
        return set(filter(lambda x: x[0].color is color, pieces))

    @seekable
    def add_piece(self, location: Tuple[int, int], piece: Piece, **kwds: Any) -> None:
        board: Board = kwds["board"]
        pieces: Set[Tuple[Piece, Location]] = kwds["pieces"]

        board.place_piece(piece, location)
        pieces.add((piece, Location(*location)))

    @seekable
    def remove_piece(self, location: Tuple[int, int], **kwds: Any) -> None:
        board: Board = kwds["board"]
        pieces: Set[Tuple[Piece, Location]] = kwds["pieces"]

        piece = board.get_piece(location)
        board[location] = 0
        pieces.remove((piece, Location(*location)))

    @seekable
    def move_piece(
        self, source: Tuple[int, int], destination: Tuple[int, int], **kwds: Any
    ) -> None:
        board: Board = kwds["board"]
        pieces: Set[Tuple[Piece, Location]] = kwds["pieces"]

        piece = board.get_piece(source)
        board[destination] = board[source]
        board[source] = 0
        board[destination[0], destination[1], 2] = 1 # Set piece_has_moved
        pieces.remove((piece, Location(*source)))
        pieces.add((piece, Location(*destination)))

    def reset(self) -> None:
        self.board.clear()
        self.active_pieces.clear()
        self.seek_board.clear()
        self.seek_board_pieces.clear()

    def execute_move(self, move: Move, seek: bool = False) -> None:
        if seek:
            # Refresh Seek Board Data
            np.copyto(self.seek_board.board, self.board.board)
            self.seek_board_pieces = self.active_pieces.copy()

        match move.type:
            case MoveType.PASSING:
                self.move_piece(move.start, move.end, seek=seek)

            case MoveType.CAPTURE:
                self.remove_piece(move.end, seek=seek)
                self.move_piece(move.start, move.end, seek=seek)

            case MoveType.CASTLE:
                castling_kingside: bool = move.castle_type is CastleType.KINGSIDE
                rook_start = (move.start.i, (BOARD_SIZE-1 if castling_kingside else 0))
                rook_dest = move.end + (Direction.W if castling_kingside else Direction.E)
                self.move_piece(move.start, move.end, seek=seek)
                self.move_piece(rook_start, rook_dest, seek=seek)

            case MoveType.PROMOTION:
                self.move_piece(move.start, move.end, seek=seek)
                self.board.update_rank(move.end, move.promotion_rank)

            case _:
                raise ValueError(f'Unknown move type: {move.type}')

    def is_in_check(self, color: Color, seek: bool = False) -> bool:
        for move in self.legal_moves(~color, seek=seek):
            if move.type is MoveType.CAPTURE and move.target == Piece(color, PieceType.KING):
                return True
        return False

    @seekable
    def legal_moves(self, color: Color, **kwds: Any) -> Generator[Move, None, None]:
        pieces = self.filter_color_pieces(color, seek=kwds["seek"])
        piece_move_generator = chain.from_iterable(
            PIECE_LOGIC_MAP[p[0].type](kwds["board"], p[1], color) for p in pieces
        )
        if kwds["seek"]:
            yield from filter(partial(self.is_move_safe, color), piece_move_generator)
        else:
            yield from piece_move_generator

    def is_move_safe(self, color: Color, move: Move) -> bool:
        self.execute_move(move, seek=True)
        return not self.is_in_check(color, seek=True)
