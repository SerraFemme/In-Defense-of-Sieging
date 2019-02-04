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
    # If Interrupted
    #     If Card:
    #         Put card into proper place
    # Break

    # Else
    #     Damage = Damage_Given(Attacker, Attack)
    #     Total_Damage = Damage_Received(Defender, Damage)

    #

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
