from src.UnitStat import *


class Enemy(object):
    """
    Primary class that stores and calculates all Player info
    """

    def __init__(self, race, role, number):
        self.race_info = race
        self.role_info = role
        self.Race_Name = self.race_info['ID']
        self.Role_Name = self.role_info['ID']
        self.Char = self.role_info['Char']
        self.Enemy_Number = number
        self.Position = None
        self.Alive = True
        self.AT = None  # Aggression Token, only used by Elites
        self.Health_Points = self.race_info['Base_Health'] + self.role_info['Bonus_Health']
        self.Stamina = Stamina(self.race_info['Stamina_Pool'] + self.role_info['Bonus_SP'])
        self.Weapon_Damage = StatTracker(self.role_info['Bonus_Damage'])
        self.Armor = StatTracker(self.race_info['Base_Armor'] + self.role_info['Bonus_Armor'])
        self.Bonus_Range = StatTracker()
        self.Equipment = []  # Restrict to 3 items
        self.Passive = None

    def turn_beginning(self):
        self.Stamina.reset_stamina_points()
        # upkeep

    def print_info(self):  # fix: prints None at end?
        print('\n' + self.Race_Name, self.Role_Name)
        print('Position:', self.Position)
        print('Health:', self.Health_Points)
        print('Stamina Pool:', self.Stamina.get_pool_size())
        print('Remaining Stamina:', self.Stamina.points)
        print('Weapon Damage:', self.Weapon_Damage.value)
        print('Bonus Range:', self.Bonus_Range.value)
        print('Armor:', self.Armor.value)

    def get_name(self):
        return self.Race_Name + ' ' + self.Role_Name

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

    def heal(self, value):
        self.Health_Points += value

    def take_damage(self, value):
        if value >= self.Health_Points:
            self.Health_Points = 0
            self.Alive = False
        else:
            self.Health_Points -= value

