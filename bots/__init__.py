"""
This package contains the bots for the game.
"""

from bots.random.bot import RandomBot
from bots.min_max.bot import MinMaxBot
from bots.min_max_pro import  MinMaxProBot
from bots.basebot import BaseBot

__all__ = ["RandomBot", "MinMaxBot", "MinMaxProBot", "BaseBot"]
