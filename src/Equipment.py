"""
Module that makes equipment
"""


class Equipment(object):
    """
    Creates an Equipment object that keeps track of all of its stats.
    """
    def __init__(self, item):
        self.ID = item['ID']
        self.Faction_Type = item['Faction_Type']
        self.Equipment_Type = item['Equipment_Type']
        self.Name = item['Name']
        self.Equipment_Stats = {}
        if 'Stats' in item:
            stats = item['Stats']
            for key in stats:
                self.Equipment_Stats[key] = stats[key]
        self.Abilities = None

    def print_info(self):
        print('Name', self.Name)
        print('Type:', self.Faction_Type, self.Equipment_Type)
        if len(self.Equipment_Stats) > 0:
            for i in self.Equipment_Stats:
                print(i, self.Equipment_Stats[i], sep=': ')
