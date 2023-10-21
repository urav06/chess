"""
Module defining the Base Bot.
"""
from abc import ABC, abstractmethod
from typing import Optional

from engine import Color, Game, Move


class BaseBot(ABC):
    """
    Base class for all bots. To be used as an interface.
    """
    def __init__(self, color: Color) -> None:
        self.color = color
        self.name = f"{color.name.capitalize()}_{self.__class__.__name__}"
        self.total_time = 0

    @abstractmethod
    def select_move(self, game: Game) -> Optional[Move]:
        """
        Selects a move that this bot will play from the given game.
        """
        if game.active_color != self.color:
            raise RuntimeError(f"It's not my turn yet. I'm playing as {str(self.color).lower()}.")

    def display_time_taken(self) -> None:
        print(f"{self.name} took {round(self.total_time, 5)}s.")
