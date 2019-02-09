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
        if 'Stats' in self.equipment_info:
            stats = self.equipment_info['Stats']
            for key in stats:
                self.Equipment_Stats[key] = stats[key]
        self.Abilities = None

    def print_info(self):
        print('Name', self.Name)
        print('Type:', self.Faction_Type, self.Equipment_Type)
        for i in self.Equipment_Stats:
            print(i, self.Equipment_Stats[i], sep=': ')


