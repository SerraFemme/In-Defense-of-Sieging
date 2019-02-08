"""
Module containing ALL keywords as classes

List of other keywords used by the game:
-Draw X
-Discard X
-Interrupt
-Trigger
-Scar X
"""


class Inline(object):
    """
    In-Line.
    Restricts range of targeting to orthogonal tiles only.
    Cannot be removed.
    CAN be overridden by Close
    """


class Close(object):
    """
    Restricts range of targeting to the nearest unit (either ally or enemy) in
    a given orthogonal direction.
    If the nearest target in a given direction is not within the given range of
    a card or effect, then the target (and thus the direction) is invalid.
    Cannot be removed.
    Cannot be overridden by In-Line
    """


class Heal(object):
    """
    Player specific keyword.
    Player takes the top X cards of their wound pile and puts them on the
    bottom of their health deck.
    """


class Regen(object):
    """
    Player specific keyword.
    When a card with this keyword is drawn, the owner Heals X.
    """


class Push(object):
    """
    Requires In-Line or Close to be in effect.
    The defender is moved away from the attacker by X tiles unoccupied tiles.
    If there are not enough unoccupied tiles for the defender to move, then the
    defender stops on the last unoccupied tile.
    """


class Pull(object):
    """
    Requires In-Line or Close to be in effect.
    The defender is moved toward the attacker by X tiles unoccupied tiles.
    If there are not enough unoccupied tiles for the defender to move, then the
    defender stops on the last unoccupied tile.
    """


class Recoil(object):
    """
    Requires In-Line or Close to be in effect.
    The attacker is moved away from the defender by X tiles unoccupied tiles.
    If there are not enough unoccupied tiles for the attacker to move, then the
    attacker stops on the last unoccupied tile.
    Instances of Recoil are additive.
    """


class Bludgeon(object):
    """
    Weapon specific keyword.
    When you resolve an attack card against a target, reduce that target's armor
    by X until the end of your turn.
    May change duration to the end of the Player Phase.
    """


class Splash(object):
    """
    Deal weapon damage to all units in a radius X around the target.
    Instances of Splash are additive. (adds to the radius)
    """


class Unique(object):
    """
    Buff and Debuff specific keyword.
    Cannot have more than 1 of the named cards attached to the same unit,
    regardless of the source. (Unless noted otherwise)
    """


class Fabricated(object):
    """
    Fabricated cards are purely temporary.
    If they would be put into either the wound or scar pile, they are DELETED
    instead.
    """
