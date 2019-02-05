"""
Module containing ALL passives for players and enemies
"""


class ActivatedPassive(object):
    """
    Can only be used on the player's turn and only once per turn.
    Resets at the beginning of the player's turn
    """
    def __init__(self):
        self.unused = True

    def activate(self):
        if self.unused:
            # Stuff
            self.unused = False

    def reset(self):
        self.unused = True


class DynamicPassive(object):
    """
    A passive that gives a bonus based on the state of a specific condition.
    Always in effect even if a bonus is not given.
    """
    pass


class TriggeredPassive(object):
    """
    A passive that happens when a condition is met.
    Can only happen once per condition met.
    """
    pass


class Knight(ActivatedPassive):
    """
    Once per turn, you may move onto an adjacent tile for free.
    This does not count as movement for cards or effects.
    Effects on the tile moved onto still trigger as normal.
    """
    pass


class Monk(DynamicPassive):
    """
    +1 weapon damage for every 12 cards in your health deck.
    """
    pass
