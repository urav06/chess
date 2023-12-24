"""
Module defining the Base Bot.
"""
from abc import ABC, abstractmethod

import chess


class BaseBot(ABC):
    """
    Base class for all bots. To be used as an interface.
    """
    def __init__(self, color: chess.Color) -> None:
        self.color: chess.Color = color
        self.name: str = f"{'white' if color else 'black'}_{self.__class__.__name__}"
        self.clock: float = 0

    @abstractmethod
    def select_move(self, board: chess.Board) -> chess.Move:
        """
        Selects a move that this bot will play from the given game.
        """
        if board.turn != self.color:
            raise RuntimeError(f"It's not my turn yet. I'm playing as {str(self.color).lower()}.")
        return chess.Move.null()

    def display_time_taken(self) -> None:
        print(f"{self.name} took {round(self.clock, 5)}s.")
