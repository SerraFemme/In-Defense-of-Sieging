from ReadGameData import SubListManager


class Player(object):
    """
    Primary class that stores and calculates all Player info
    """

    def __init__(self, classitem, selectedClass):
        self.classlist = SubListManager(classitem)
        self.classinfo = self.classlist.get_item(selectedClass)
        self.className = self.classinfo['ID']
        self.position = None
        # self.Stamina = Stamina(self.classinfo['Stamina_Pool'])
        # self.WeaponDamage = WeaponDamage() # Starts at 0, then Starting Equipment affects it
        # self.Armor = Armor() # Starts at 0, then Starting Equipment affects it
        # self.HandSize = HandSize(PlayerClass['Hand_Size'])
        # self.PlayerDeck = Starting Deck
        # self.Equipment = Starting Equipment

    def get_class_name(self):
        return self.className

    def get_position(self):
        return self.position

    def set_position(self, coordinates):
        self.position = coordinates

    # Stamina stuff

    # Weapon Stuff

    # Armor Stuff

    # Hand Size Stuff

    # Player Deck Stuff

    # Equipment Stuff
