"""
Questions: When to double divine damage to an undead unit
"""


class DealDamage(object):
    """
    Takes the information of the Attacker and calculates a final number that
    represents the damage being dealt to the defender.
    """
    print('ATTACK!')
    # Receive Base Damage, Damage Multiplier, Misc. Damage Additions, DamageType
    # Multiply Base Damage by Damage Multiplier
    # Add Misc. Damage Additions
    # Return Tuple of Final Damage and Damage Type


class ReceiveDamage(object):
    """
    Takes the information of the Defender and the incoming damage and
    calculates a final number that represents the damage being received
    then callig a funtion to change the health of the Defender to an
    appropriate value
    """
    print('DEFEND!')
    # Receive Tuple of Incoming Damage and Damage Type
    # Do Misc Calculations Based on Damage Type (Ignore Armor, etc.)
    # Based on previous results, add any Misc. Damage Additions
    # Unit.take_damage(final_damage)


