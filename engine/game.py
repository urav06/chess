from typing import List, Tuple

from engine.board import Board
from engine.types import Piece, Location, Color


class Game:

    def __init__(self) -> None:
        self.board = Board()
        self.active_pieces: List[Tuple[Piece, Location]] = []
        self.active_color = Color.WHITE