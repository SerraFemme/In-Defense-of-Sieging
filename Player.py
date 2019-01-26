from ReadGameData import SubListManager
from UnitStat import *


class Player(object):
    """
    Primary class that stores and calculates all Player info
    """

    def __init__(self, classitem, selectedClass):
        self.classlist = SubListManager(classitem)
        self.classinfo = self.classlist.get_item(selectedClass)
        # self.Player_Name =
        # self.Player_Number =
        self.Class_Name = self.classinfo['ID']
        self.Position = None
        self.FactionRestriction = self.classinfo['Allowed_Faction']
        self.EquipmentRestriction = self.classinfo['Allowed_Equipment']
        self.Stamina = Stamina(self.classinfo['Stamina_Pool'])
        self.WeaponDamage = StatTracker()
        self.Armor = StatTracker()
        self.Range_Bonus = StatTracker()
        self.HandSize = StatTracker(self.classinfo['Hand_Size'])
        # self.PlayerDeck = Starting Deck
        self.Equipment = []  # Starting Equipment
        # self.Passive

    def turn_beginning(self):
        self.Stamina.reset_stamina_points()
        # mulligan phase
        # upkeep

    def print_info(self):  # fix: prints None at end
        print('')
        print('Class:', self.get_class_name())
        print('Position:', self.get_position())
        print('Stamina Pool:', self.Stamina.get_pool_size())
        print('Remaining Stamina:', self.Stamina.get_stamina_points())
        print('Weapon Damage:', self.WeaponDamage.get_value())
        print('Armor:', self.Armor.get_value())
        print('Hand Size:', self.HandSize.get_value())

    def get_class_name(self):
        return self.Class_Name

    def get_position(self):
        return self.Position

    def set_position(self, coordinates):
        self.Position = coordinates

    # Faction Restrictions

    # Equipment Restrictions

    # Stamina stuff

    # Weapon Stuff

    # Armor Stuff

    # Hand Size Stuff

    # Player Deck Stuff

    # Equipment Stuff
    # def get_all_equipped(self):
    #     return self.Equipment

    # def get_equipped_item(self, item):

    # def add_equipment(self, item):

    # def remove_equipment(self, item):

    # def has_equipped(self, item):
    #     for i in self.Equipment:
    #         pass
