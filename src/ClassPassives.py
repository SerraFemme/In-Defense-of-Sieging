"""
Module containing ALL passives for all player classes
"""
from src.PassiveTypes import *


class Knight(ActivatedPassive):
    """
    Once per turn, you may move onto an adjacent tile for free.
    This does not count as movement for cards or effects.
    Effects on the tile moved onto still trigger as normal.
    """
    def __init__(self):
        super().__init__()

    def activate(self):
        # Stuff
        super().use()


class Monk(DynamicPassive):
    """
    +1 weapon damage for every 12 cards in your health deck.
    """
    pass
