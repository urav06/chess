"""
Game Class
"""
from __future__ import annotations

from functools import partial, wraps
from itertools import chain
from typing import Any, Callable, Generator, Set, Tuple, TypeVar

import numpy as np

from engine.board import Board
from engine.pieces import PIECE_LOGIC_MAP
from engine.types import Color, Location, Move, MoveType, Piece, PieceType

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
    def add_piece(self, location: Location, piece: Piece, **kwds: Any) -> None:
        board: Board = kwds["board"]
        pieces: Set[Tuple[Piece, Location]] = kwds["pieces"]

        board.place_piece(piece, location)
        pieces.add((piece, location))

    @seekable
    def remove_piece(self, location: Location, **kwds: Any) -> None:
        board: Board = kwds["board"]
        pieces: Set[Tuple[Piece, Location]] = kwds["pieces"]

        piece = board.get_piece(location)
        board[location] = 0
        pieces.remove((piece, location))

    @seekable
    def move_piece(self, source: Location, destination: Location, **kwds: Any) -> None:
        board: Board = kwds["board"]
        pieces: Set[Tuple[Piece, Location]] = kwds["pieces"]

        piece = board.get_piece(source)
        board[destination] = board[source]
        board[source] = 0
        board[destination.i, destination.j, 2] = 1 # Set piece_has_moved
        pieces.remove((piece, source))
        pieces.add((piece, destination))

    def reset(self) -> None:
        self.board.clear()
        self.active_pieces.clear()

        self.seek_board.clear()
        self.seek_board_pieces.clear()

        self.active_color = Color.WHITE

    def execute_move(self, move: Move, seek: bool = False) -> None:
        if seek:
            # Refresh Seek Board Data
            np.copyto(self.seek_board.board, self.board.board)
            self.seek_board_pieces = self.active_pieces.copy()

        if move.type is MoveType.PASSING:
            self.move_piece(move.start, move.end, seek=seek)

        elif move.type is MoveType.CAPTURE:
            self.remove_piece(move.end, seek=seek)
            self.move_piece(move.start, move.end, seek=seek)

        elif move.type is MoveType.CASTLE:
            pass
        elif move.type is MoveType.PROMOTION:
            pass
        else:
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
