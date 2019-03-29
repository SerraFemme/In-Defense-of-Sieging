"""
Contains all classes used for storing various unit info
"""
from src.UnitStat import StatTracker, Stamina


class Player(object):
    """
    Primary class that stores and calculates all Player info
    """

    def __init__(self, selected_class, name, number):
        self.Player_Name = name
        self.Player_Number = number
        self.Icon = 'P' + str(number)
        self.Conscious = True
        self.Position = None
        self.AT = []  # Aggression Tokens
        self.Class_Name = selected_class['ID']
        self.Full_Name = self.Player_Name + ': ' + self.Class_Name
        self.Faction_Restriction = selected_class['Allowed_Faction']
        self.Equipment_Restriction = selected_class['Allowed_Equipment']
        self.Stamina = Stamina(selected_class['Stamina_Pool'])
        self.Weapon_Damage = StatTracker()
        self.Armor = StatTracker()
        self.Bonus_Range = StatTracker()
        self.HandSize = StatTracker(selected_class['Hand_Size'])
        self.Deck = None
        self.mulligan_phase = False
        self.discard_phase = False
        self.Equipment = []  # Restrict to 3 items
        self.Abilities = None  # Stores passives and other misc abilities
        # TODO: convert Stats to a dict
        # self.Stats = {
        #     "Stamina": Stamina(selected_class['Stamina_Pool']),
        #     "Armor": StatTracker(),
        #     "Range": StatTracker(),
        #     "Hand": StatTracker(selected_class['Hand_Size'])}

    def turn_beginning(self):
        self.Stamina.reset_stamina_points()
        self.mulligan_phase = True

    def upkeep(self):
        self.Deck.end_mulligan()
        self.mulligan_phase = False
        # upkeep step

    def turn_ending(self):
        # end step effects
        # self.discard_phase = True
        # discard step
        pass

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

    def add_equipment(self, item):  # TODO: Make Dynamic, "for key in dict"
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
            self.HandSize.add_effect(item.Name, item.Equipment_Stats['Hand'])
        # for key in item.Equipment_Stats:
        #     if key in self.Stats:
        #         self.Stats[key].add_effect(key, item.Equipment_Stats[key])

    # Deck Stuff
    def take_damage(self, value):  # Redo later
        self.Deck.mill(value)
        if len(self.Deck.current_health()) == 0:
            self.Conscious = False

    def heal(self, value):  # Redo later
        self.Deck.heal(value)


class Enemy(object):
    """
    Primary class that stores and calculates all Enemy info
    """

    def __init__(self, race, role, number):
        self.race_info = race
        self.role_info = role
        self.Race_Name = self.race_info['ID']
        self.Role_Name = self.role_info['ID']
        self.Icon = self.race_info['Char'] + self.role_info['Char'] + str(number)
        self.Enemy_Number = number
        self.Full_Name = self.Race_Name + ' ' + self.Role_Name + ' ' + str(number)
        self.Position = None
        self.Alive = True
        self.AT = None  # Aggression Token, only used by Elites
        self.Health_Points = self.race_info['Base_Health'] + self.role_info['Bonus_Health']
        self.Stamina = Stamina(self.race_info['Stamina_Pool'] + self.role_info['Bonus_SP'])
        self.Weapon_Damage = StatTracker(self.role_info['Bonus_Damage'])
        self.Armor = StatTracker(self.race_info['Base_Armor'] + self.role_info['Bonus_Armor'])
        self.Bonus_Range = StatTracker()
        self.Equipment = []  # Restrict to 3 items
        self.Abilities = None  # Stores passives and other misc. abilities
        # TODO: convert Stats to a dict
        # self.Stats = {
        #     "Stamina": Stamina(),
        #     "Armor": StatTracker(),
        #     "Range": StatTracker()}

    def turn_beginning(self):
        self.Stamina.reset_stamina_points()
        self.upkeep()

    def upkeep(self):
        # upkeep
        pass

    def turn_ending(self):
        # end step effects
        pass

    def get_name(self):
        return self.Race_Name + ' ' + self.Role_Name + ' ' + str(self.Enemy_Number)

    # Equipment Stuff
    def get_equipped_list(self):  # Needed?
        return self.Equipment

    def get_equipped_item(self, item):  # Needed?
        for i in self.Equipment:
            if i.Name == item:
                return i

    def add_equipment(self, item):
        self.Equipment.append(item)
        if 'Damage' in item.Equipment_Stats:
            self.Weapon_Damage.add_effect(item.Name, item.Equipment_Stats['Damage'])
        if 'Armor' in item.Equipment_Stats:
            self.Armor.add_effect(item.Name, item.Equipment_Stats['Armor'])
        if 'Range' in item.Equipment_Stats:
            self.Bonus_Range.add_effect(item.Name, item.Equipment_Stats['Range'])
        if 'Stamina' in item.Equipment_Stats:
            self.Stamina.add_effect(item.Name, item.Equipment_Stats['Stamina'])
        # for key in item.Equipment_Stats:
        #     if key in self.Stats:
        #         self.Stats[key].add_effect(key, item.Equipment_Stats[key])

    def heal(self, value):
        self.Health_Points += value

    def take_damage(self, value):
        if value >= self.Health_Points:
            self.Health_Points = 0
            self.Alive = False
        else:
            self.Health_Points -= value
