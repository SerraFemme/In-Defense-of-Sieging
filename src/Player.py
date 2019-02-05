from src.UnitStat import *


class Player(object):
    """
    Primary class that stores and calculates all Player info
    """

    def __init__(self, selected_class, name, number):
        self.class_info = selected_class
        self.Player_Name = name
        self.Player_Number = number
        self.Conscious = True
        self.Position = None
        self.AT = []  # Aggression Tokens
        self.Class_Name = self.class_info['ID']
        self.Faction_Restriction = self.class_info['Allowed_Faction']
        self.Equipment_Restriction = self.class_info['Allowed_Equipment']
        self.Stamina = Stamina(self.class_info['Stamina_Pool'])
        self.Weapon_Damage = StatTracker()
        self.Armor = StatTracker()
        self.Bonus_Range = StatTracker()
        self.HandSize = StatTracker(self.class_info['Hand_Size'])
        self.Deck = None
        self.Equipment = []  # Restrict to 3 items
        self.Passive = None

    def turn_beginning(self):
        self.Stamina.reset_stamina_points()
        # self.Deck.mulligan()
        # upkeep

    def print_info(self):  # fix: prints None at end
        print('\n' + 'Class:', self.Class_Name)
        print('Position:', self.Position)
        print('Stamina Pool:', self.Stamina.get_pool_size())
        print('Remaining Stamina:', self.Stamina.points)
        print('Weapon Damage:', self.Weapon_Damage.value)
        print('Bonus Range:', self.Bonus_Range.value)
        print('Armor:', self.Armor.value)
        print('Hand Size:', self.HandSize.value)

    def get_name(self):
        return self.Player_Name + ': ' + self.Class_Name

    # Faction Restrictions

    # Equipment Restrictions

    # Equipment Stuff
    def get_equipped_list(self):  # Needed?
        return self.Equipment

    def get_equipped_item(self, item):  # Needed?
        for i in self.Equipment:
            if i.Name == item:
                return i

    def add_equipment(self, item):  # Make Dynamic
        self.Equipment.append(item)
        if 'Damage' in item.Equipment_Stats:
            self.Weapon_Damage.add_effect(item.Name, item.Equipment_Stats['Damage'])
        if 'Armor' in item.Equipment_Stats:
            self.Armor.add_effect(item.Name, item.Equipment_Stats['Armor'])
        if 'Range' in item.Equipment_Stats:
            self.Bonus_Range.add_effect(item.Name, item.Equipment_Stats['Range'])
        if 'Stamina' in item.Equipment_Stats:
            self.Stamina.add_effect(item.Name, item.Equipment_Stats['Stamina'])
        if 'Hand' in item.Equipment_Stats:
            self.HandSize.add_effect(item.name, item.Equipment_Stats['Hand'])

    # Deck Stuff
    def take_damage(self, value):  # Redo later
        self.Deck.mill(value)
        if len(self.Deck) == 0:
            self.Conscious = False

    def heal(self, value):  # Redo later
        self.Deck.heal(value)
