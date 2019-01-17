import Stamina

class Player(object):
    """Primary class that stores and calculates all Player info"""

    NameOfClass = 'Paladin' # temporary

    def __init__(self, NameOfClass):
        if ReadClassList(NameOfClass) is not None: # may need to change
            PlayerClass = ReadJSONList(NameOfClass)
            self.className = PlayerClass['ID'] # redundant?
            self.Stamina = Stamina(PlayerClass['Stamina_Pool'])
            #self.WeaponDamage = WeaponDamage() # Starts at 0, then Starting Equipment affects it
            #self.Armor = Armor() # Starts at 0, then Starting Equipment affects it
            #self.HandSize = HandSize(PlayerClass['Hand_Size'])
            #self.PlayerDeck = Starting Deck
            #self.Equipment = Starting Equipment

        else:
            print(NameOfClass, "does not exist")