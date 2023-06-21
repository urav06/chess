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

    def filter_color_pieces(self, color: Color) -> Set[Tuple[Piece, Location]]:
        return set(filter(lambda x: x[0].color is color, self.active_pieces))

    def put_piece(self, location: Location, piece: Piece) -> None:
        self.board.place_piece(piece, location)
        self.active_pieces.add((piece, location))

    def remove_piece(self, location: Location) -> None:
        piece = self.board.get_piece(location)
        self.board[location] = 0
        self.active_pieces.remove((piece, location))

    def move_piece(self, source: Location, destination: Location) -> None:
        piece = self.board.get_piece(source)
        self.board[destination] = self.board[source]
        self.board[source] = 0
        self.active_pieces.remove((piece, source))
        self.active_pieces.add((piece, destination))

    def reset(self) -> None:
        self.board.clear()
        self.active_pieces.clear()
        self.active_color = Color.WHITE

    def execute_move(self, move: Move) -> None:
        if move.type is MoveType.PASSING:
            self.move_piece(move.start, move.end)

        elif move.type is MoveType.CAPTURE:
            self.remove_piece(move.end)
            self.move_piece(move.start, move.end)

        elif move.type is MoveType.CASTLE:
            pass
        elif move.type is MoveType.PROMOTION:
            pass
        else:
            raise ValueError(f'Unknown move type: {move.type}')
        self.board[move.end.i, move.end.j, 2] = 1  # Set piece_has_moved

    def legal_moves(self, color: Color) -> Generator[Move, None, None]:
        pieces = self.filter_color_pieces(color)
        yield from chain.from_iterable(
            PIECE_LOGIC_MAP[p[0].type](self.board, p[1], self.active_color) for p in pieces
        )
