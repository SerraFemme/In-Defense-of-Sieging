"""
Module containing ALL passive types
"""


class ActivatedPassive(object):
    """
    Can only be used on the player's turn and only once per turn.
    Resets at the beginning of the player's turn
    """
    def __init__(self):
        self.unused = True

    def use(self):
        if self.unused:
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
