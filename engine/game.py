"""
Game Class
"""

from itertools import chain
from typing import Set, Tuple, Generator

from engine.board import Board
from engine.types import Piece, Location, Color, Move, MoveType
from engine.pieces import PIECE_LOGIC_MAP


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
        _, pieces = self.process_seek_flag(seek)
        return set(filter(lambda x: x[0].color is color, pieces))

    def add_piece(self, location: Location, piece: Piece, seek: bool = False) -> None:
        board, pieces = self.process_seek_flag(seek)
        board.place_piece(piece, location)
        pieces.add((piece, location))

    def remove_piece(self, location: Location, seek: bool = False) -> None:
        board, pieces = self.process_seek_flag(seek)
        piece = board.get_piece(location)
        board[location] = 0
        pieces.remove((piece, location))

    def move_piece(
        self, source: Location, destination: Location, seek: bool = False
    ) -> None:
        board, pieces = self.process_seek_flag(seek)
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
        if move.type is MoveType.PASSING:
            self.move_piece(move.start, move.end, seek)

        elif move.type is MoveType.CAPTURE:
            self.remove_piece(move.end, seek)
            self.move_piece(move.start, move.end, seek)

        elif move.type is MoveType.CASTLE:
            pass
        elif move.type is MoveType.PROMOTION:
            pass
        else:
            raise ValueError(f'Unknown move type: {move.type}')

    def legal_moves(self, color: Color) -> Generator[Move, None, None]:
        pieces = self.filter_color_pieces(color)
        yield from chain.from_iterable(
            PIECE_LOGIC_MAP[p[0].type](self.board, p[1], self.active_color) for p in pieces
        )

    def process_seek_flag(self, seek: bool) -> Tuple[Board, Set[Tuple[Piece, Location]]]:
        # TODO: This whole logic and its usage should be a decorator
        if seek:
            return self.seek_board, self.seek_board_pieces
        return self.board, self.active_pieces
