"""
Module that sets up the enemy horde and controls their turn
"""

from ReadGameData import SubListManager
from Player import Player
from Equipment import Equipment


class HordeMaker(object):
    def __init__(self, encounter_list, races, roles, equipment_list):
        self.encounter_list = SubListManager(encounter_list)
        self.race_list = SubListManager(races)
        self.role_list = SubListManager(roles)
        self.equipment_list = SubListManager(equipment_list)


class EnemyTurn(object):
    pass

