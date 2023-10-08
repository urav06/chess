"""
Game Class
"""
from __future__ import annotations

from functools import partial
from itertools import chain
from typing import Generator, Optional

import numpy as np

from engine.board import Board, PieceLocation
from engine.constants import BOARD_SIZE
from engine.pieces import PIECE_LOGIC_MAP
from engine.types import (
    Color, Direction, Location, Move, MoveType, Piece,
    CAPTURE,  # MoveTypes
    KING, ROOK, QUEEN,  # PieceTypes
    WHITE,  # Colors
)

class Game:
    """
    Game is a match of chess between Black and White.
    This class provides an interface between the players and the game.
    """
    def __init__(self) -> None:
        self.board = Board()
        self.active_color = Color.WHITE

    def reset(self) -> None:
        self.board.clear()
        self.active_color = Color.WHITE

    def execute_move(self, move: Move) -> None:
        match move:
            case Move(start, end, MoveType.PASSING):
                self.board.move_piece(start, end)

            case Move(start, end, MoveType.CAPTURE, target=_):
                self.board.remove_piece(end)
                self.board.move_piece(start, end)

            case Move(start, end, MoveType.CASTLE, castle_type=castle_type):
                rook_start = (start.i, (BOARD_SIZE-1 if castle_type is KING else 0))
                rook_dest = end + (Direction.W if castle_type is KING else Direction.E)
                self.board.move_piece(start, end)
                self.board.move_piece(rook_start, rook_dest)

            case Move(start, end, MoveType.PROMOTION, promotion_rank=rank) if rank:
                self.board.move_piece(start, end)
                self.board.promote_piece(end, rank)

            case Move(start, end, MoveType.CAPTURE_AND_PROMOTION, promotion_rank=rank) if rank:
                self.board.remove_piece(end)
                self.board.move_piece(start, end)
                self.board.promote_piece(end, rank)

            case _:
                raise ValueError(f'Invalid Move: {move}')

    def seek_move(self, move: Move) -> Game:
        game_copy = Game()
        np.copyto(game_copy.board.board, self.board.board)
        game_copy.active_color = self.active_color

        game_copy.execute_move(move)
        game_copy.active_color = ~game_copy.active_color
        return game_copy

    def is_in_check(self, color: Color) -> bool:
        return any(
            CAPTURE in move.type and move.target == KING
            for move in self.legal_moves(unsafe=True, color=~color)
        )

    def square_attacked(self, square: tuple[int, int], color: Color) -> bool:
        return any(
            move.end == square for move in self.legal_moves(unsafe=True, color=color)
        )

    def is_in_checkmate(self, color: Color) -> bool:
        return not any(self.legal_moves(color=color)) and self.is_in_check(color=color)

    def is_in_stalemate(self, color: Color) -> bool:
        return not any(self.legal_moves(color=color)) and not self.is_in_check(color=color)

    def legal_moves(
        self,
        color: Optional[Color] = None,
        piece: Optional[PieceLocation] = None,
        unsafe: bool = False
    ) -> Generator[Move, None, None]:
        """
        Generate all legal moves for the selected pieces.

        :param color: Color of the pieces to generate moves for. Defaults to `self.active_color`
        :param PieceLocation piece: The selected piece to generate moves for. Optional.
        :param unsafe: A flag to ignore depth 2 checks.
        """
        color = color or self.active_color
        pieces = {piece} if piece else self.board.get_pieces(color=color)
        piece_move_generator = chain.from_iterable(
            PIECE_LOGIC_MAP[p[0][1]](self.board, p[1], p[0][0]) for p in pieces
        )
        if unsafe:
            yield from piece_move_generator
        else:
            yield from filter(partial(self.is_move_safe, color), piece_move_generator)
            yield from self.castling_moves(color)

    def castling_moves(self, color: Optional[Color] = None) -> Generator[Move, None, None]:
        color = color or self.active_color
        pieces = self.board.get_pieces(color)
        row = BOARD_SIZE-1 if color is WHITE else 0
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
        return not self.seek_move(move).is_in_check(color=color)
