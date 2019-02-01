"""
Module that makes equipment
"""


class Equipment(object):
    """
    Creates an Equipment object that keeps track of all of its stats.
    """
    def __init__(self, item):
        self.equipment_info = item
        self.ID = self.equipment_info['ID']
        self.Faction_Type = self.equipment_info['Faction_Type']
        self.Equipment_Type = self.equipment_info['Equipment_Type']
        self.Name = self.equipment_info['Name']
        self.Equipment_Stats = {}
        if 'Damage' in self.equipment_info:
            self.Equipment_Stats['Damage'] = self.equipment_info['Damage']
        if 'Armor' in self.equipment_info:
            self.Equipment_Stats['Armor'] = self.equipment_info['Armor']
        if 'Range' in self.equipment_info:
            self.Equipment_Stats['Range'] = self.equipment_info['Range']
        if 'Stamina' in self.equipment_info:
            self.Equipment_Stats['Stamina'] = self.equipment_info['Stamina']
        self.Abilities = None

    def print_info(self):
        print('Name', self.Name)
        print('Type:', self.Faction_Type, self.Equipment_Type)
        for i in self.Equipment_Stats:
            print(i, self.Equipment_Stats[i], sep=': ')


