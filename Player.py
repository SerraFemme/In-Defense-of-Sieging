from UnitStat import *


class Player(object):
    """
    Primary class that stores and calculates all Player info
    """

    def __init__(self, selected_class, name):
        self.class_info = selected_class
        self.conscious = True
        self.Player_Name = name
        self.Class_Name = self.class_info['ID']
        self.Position = None
        self.Faction_Restriction = self.class_info['Allowed_Faction']
        self.Equipment_Restriction = self.class_info['Allowed_Equipment']
        self.Stamina = Stamina(self.class_info['Stamina_Pool'])
        self.Weapon_Damage = StatTracker()
        self.Armor = StatTracker()
        self.Range_Bonus = StatTracker()
        self.HandSize = StatTracker(self.class_info['Hand_Size'])
        # self.PlayerDeck = Starting Deck
        self.Equipment = []  # Starting Equipment
        # self.Passive

    def turn_beginning(self):
        self.Stamina.reset_stamina_points()
        # mulligan phase
        # upkeep

    def print_info(self):  # fix: prints None at end
        print('\n' + 'Class:', self.Class_Name)
        print('Position:', self.Position)
        print('Stamina Pool:', self.Stamina.get_pool_size())
        print('Remaining Stamina:', self.Stamina.get_stamina_points())
        print('Weapon Damage:', self.Weapon_Damage.value)
        print('Armor:', self.Armor.value)
        print('Hand Size:', self.HandSize.value)

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
