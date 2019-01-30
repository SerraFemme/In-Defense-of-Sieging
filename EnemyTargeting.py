"""
Controls which player the enemy will move and attack during their turn
"""


class TargetNearest(object):
    """

    """
    pass


class TargetAT(object):
    """
    Special targeting that only Elites use.
    Creates an Aggression Token and "gives" it to the Player which
    fulfills its targeting restriction.
    If an Elite already has an Aggression Token in effect, it uses it instead of creating a new one.
    """
    pass


class AggressionToken(object):
    """
    Object which links an Elite to a Player based on a predefined condition
    A player can have any number of Aggression Tokens, but an Elite can only have one
    Aggression Token at a time.

    """
    pass
