"""
Module containing ALL keywords as classes
"""


class Inline(object):
    """
    Restricts range of targeting to orthogonal tiles only.
    """
    pass


class Close(object):
    """
    Restricts range of targeting to the nearest unit (either ally or enemy) in
    a given orthogonal direction.
    If the nearest target in a given direction is not within the given range of
    a card or effect, then the target is invalid.
    """


class Heal(object):
    """

    """


class Regen(object):
    """

    """


class Push(object):
    """

    """


class Pull(object):
    """

    """


class Recoil(object):
    """

    """
