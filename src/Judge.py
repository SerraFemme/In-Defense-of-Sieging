"""
Module containing all Judge Classes
"""


class CombatJudge(object):
    """
    Resolves combat between an Attacker and a Defender
    """

    # Attacker
    # Defender
    # Card/Effect being used

    # Check for any valid Interrupts, Interrupt_Judge()
    # If !Interrupted
    # Damage = Damage_Given(Attacker, Attack)
    # Total_Damage = Damage_Received(Defender, Damage)

    # Else
    # Break

    # If Defender==Player
    # Player.mill(Total_Damage)

    # Else If Defender==Enemy
    # Defender.set_Health(Defender.get_Health()-Total_Damage)

    # Else
    # Throw Error

    # Do any additional effects
    # Ex: Splash damage: in affected area, call Damage_Received(Defender, Splash_Damage)


class InterruptJudge(object):
    """
    Determines if a card/effect gets interrupted
    """

    # Interrupt card/effect
    # Target of the interrupt

    # if interrupt is effective
    # Return True
    # Else
    # Return False
