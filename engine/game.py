"""
Game Class
"""
from __future__ import annotations

from functools import partial, wraps
from itertools import chain
from typing import Any, Callable, Generator, TypeVar

import numpy as np

from engine.board import Board
from engine.constants import BOARD_SIZE
from engine.pieces import PIECE_LOGIC_MAP
from engine.types import (
    CastleType, Color, Direction, Location, Move, MoveType, Piece, PieceType,
    CAPTURE, CAPTURE_AND_PROMOTION, # MoveTypes
    KING, # PieceTypes
)

R = TypeVar('R')
GamePieceInfo = tuple[Piece, Location]

def seekable(wrapped: Callable[..., R]) -> Callable[..., R]:
    @wraps(wrapped)
    def wrapper(game: Game, *args: Any, **kwds: Any) -> Any:
        seek = kwds.setdefault("seek", False)
        if seek:
            kwds["board"] = kwds.get("board") or game.seek_board
            kwds["pieces"] = kwds.get("pieces") or game.seek_board_pieces
        else:
            kwds["board"] = kwds.get("board") or game.board
            kwds["pieces"] = kwds.get("pieces") or game.active_pieces
        kwds["color"] = kwds.get("color") or game.active_color
        return wrapped(game, *args, **kwds)
    return wrapper


class Game:
    """
    Game is a match of chess between Black and White.
    This class provides an interface between the players and the game.
    """
    def __init__(self) -> None:
        self.board = Board()
        self.active_pieces: set[GamePieceInfo] = set()
        self.active_color = Color.WHITE

        self.seek_board = Board()
        self.seek_board_pieces: set[GamePieceInfo] = set()

    @seekable
    def filter_color_pieces(self, color: Color, **kwds: Any) -> set[GamePieceInfo]:
        pieces = kwds["pieces"]
        return set(filter(lambda x: x[0].color is color, pieces))

    @seekable
    def add_piece(
        self, location: tuple[int, int], piece: tuple[Color, PieceType], **kwds: Any
    ) -> GamePieceInfo:
        board: Board = kwds["board"]
        pieces: set[GamePieceInfo] = kwds["pieces"]

        board.place_piece(piece, location)
        pieces.add((Piece(*piece), Location(*location)))
        return (Piece(*piece), Location(*location))

    @seekable
    def remove_piece(self, location: tuple[int, int], **kwds: Any) -> None:
        board: Board = kwds["board"]
        pieces: set[GamePieceInfo] = kwds["pieces"]

        piece = board.get_piece(location)
        board[location] = 0
        pieces.remove((piece, Location(*location)))

    @seekable
    def move_piece(
        self, source: tuple[int, int], destination: tuple[int, int], **kwds: Any
    ) -> None:
        board: Board = kwds["board"]
        pieces: set[GamePieceInfo] = kwds["pieces"]

        piece = board.get_piece(source)
        board[destination] = board[source]
        board[source] = 0
        board[destination[0], destination[1], 2] = 1 # Piece has moved
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

        match move:
            case Move(start, end, MoveType.PASSING):
                self.move_piece(start, end, seek=seek)

            case Move(start, end, MoveType.CAPTURE, target=_):
                self.remove_piece(end, seek=seek)
                self.move_piece(start, end, seek=seek)

            case Move(start, end, MoveType.CASTLE, castle_type=castle_type):
                castling_kingside: bool = castle_type is CastleType.KINGSIDE
                rook_start = (start.i, (BOARD_SIZE-1 if castling_kingside else 0))
                rook_dest = end + (Direction.W if castling_kingside else Direction.E)
                self.move_piece(start, end, seek=seek)
                self.move_piece(rook_start, rook_dest, seek=seek)

            case Move(start, end, MoveType.PROMOTION, promotion_rank=rank) if rank:
                self.move_piece(start, end, seek=seek)
                self.board.update_rank(end, rank)

            case Move(start, end, MoveType.CAPTURE_AND_PROMOTION, promotion_rank=rank) if rank:
                self.remove_piece(end, seek=seek)
                self.move_piece(start, end, seek=seek)
                self.board.update_rank(end, rank)

            case _:
                raise ValueError(f'Invalid Move: {move}')

    def is_in_check(self, color: Color, **kwds: Any) -> bool:
        # TODO: Improve capture and promote flagging
        return any(
            move.type in [CAPTURE, CAPTURE_AND_PROMOTION] and move.target == (color, KING)
            for move in self.legal_moves(color=~color, **kwds)
        )

    @seekable
    def legal_moves(self, **kwds: Any) -> Generator[Move, None, None]:
        pieces = self.filter_color_pieces(**kwds)
        piece_move_generator = chain.from_iterable(
            PIECE_LOGIC_MAP[p[0].type](kwds["board"], p[1], p[0].color) for p in pieces
        )
        if kwds["seek"]:
            yield from piece_move_generator
        else:
            yield from filter(partial(self.is_move_safe, kwds["color"]), piece_move_generator)

    def is_move_safe(self, color: Color, move: Move) -> bool:
        self.execute_move(move, seek=True)
        return not self.is_in_check(color, seek=True)
