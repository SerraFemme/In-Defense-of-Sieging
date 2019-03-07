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
