from ReadGameData import SubListManager
from UnitStat import *


class Player(object):
    """
    Primary class that stores and calculates all Player info
    """

    def __init__(self, classitem, selectedClass):
        self.classlist = SubListManager(classitem)
        self.classinfo = self.classlist.get_item(selectedClass)
        self.className = self.classinfo['ID']
        self.position = None
        self.Stamina = Stamina(self.classinfo['Stamina_Pool'])
        # self.WeaponDamage = StatTracker()
        # self.Armor = StatTracker()
        # self.HandSize = StatTracker(PlayerClass['Hand_Size'])
        # self.PlayerDeck = Starting Deck
        # self.Equipment = Starting Equipment

    def turn_beginning(self):
        self.Stamina.reset_stamina_points()
        # mulligan phase
        # upkeep

    def print_info(self):
        print('Position:', self.get_position())
        print('Remaining Stamina:', self.Stamina.get_stamina_points())
        # print('Weapon Damage:', WeaponDamage.get_value())
        # print('Armor:', Armor.get_value())
        # print('Hand Size:', HandSize.get_value())

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
