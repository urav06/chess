from itertools import chain
from typing import List, Tuple, Generator

from engine.board import Board
from engine.types import Piece, Location, Color, Move, MoveType
from engine.pieces import PIECE_LOGIC_MAP


class Game:

    def __init__(self) -> None:
        self.board = Board()
        self.active_pieces: List[Tuple[Piece, Location]] = []
        self.active_color = Color.WHITE

    @property
    def active_color_pieces(self) -> List[Tuple[Piece, Location]]:
        return list(filter(lambda x: x[0].color is self.active_color, self.active_pieces))

    def reset(self) -> None:
        self.board.clear()
        self.active_pieces.clear()
        self.active_color = Color.WHITE

    def execute_move(self, move: Move) -> None:
        if move.type is MoveType.PASSING:
            self.board[move.end] = self.board[move.start]
            self.board[move.start] = 0

        elif move.type is MoveType.CAPTURE:
            captured = self.board.get_square(move.end)
            self.board[move.end] = self.board[move.start]
            self.board[move.start] = 0
            self.active_pieces.remove((captured, move.end))

        elif move.type is MoveType.CASTLE:
            pass
        elif move.type is MoveType.PROMOTION:
            pass
        else:
            raise ValueError(f'Unknown move type: {move.type}')
        self.board[move.end.i, move.end.j, 2] = 1  # Set piece_has_moved

    def legal_moves(self) -> Generator[Move, None, None]:
        yield from chain.from_iterable(
            PIECE_LOGIC_MAP[p[0].type](self.board, p[1], self.active_color) for p in self.active_color_pieces
        )
