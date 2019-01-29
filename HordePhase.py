"""
Module that sets up the enemy horde and controls their turn
"""

from ReadGameData import SubListManager
from Enemy import Enemy
from Equipment import Equipment


class HordeMaker(object):
    """
    Creates an enemy horde based on the encounter list then puts them on the map
    """
    def __init__(self, battle_map, movement, encounter_list, races, roles, equipment_list, n):
        self.battle_map = battle_map
        self.movement = movement
        self.number_of_players = n
        self.encounter_list = SubListManager(encounter_list)
        self.race_list = SubListManager(races)
        self.role_list = SubListManager(roles)
        self.equipment_list = SubListManager(equipment_list)

    def create_enemy_horde(self):
        encounter = self.__select_encounter()
        enemy_horde = []
        enemy_list = encounter['Enemies']

        print('Encounter Selection Phase:')
        for i in enemy_list:
            if isinstance(i['Number'], int):
                for j in range(i['Number']):
                    race = self.race_list.get_item(i['Race'])
                    role = self.role_list.get_item(i['Role'])
                    enemy = Enemy(race, role, j+1)
                    for e in i['Equipment']:
                        equipment = self.equipment_list.get_item(e)
                        enemy.add_equipment(Equipment(equipment))
                    enemy_horde.append(enemy)
            else:  # Numbers is a string
                for j in range(self.number_of_players):
                    race = self.race_list.get_item(i['Race'])
                    role = self.role_list.get_item(i['Role'])
                    enemy = Enemy(race, role, j+1)
                    for e in i['Equipment']:
                        equipment = self.equipment_list.get_item(e)
                        enemy.add_equipment(Equipment(equipment))
                    enemy_horde.append(enemy)

        self.__put_horde_on_map(enemy_horde)

        return enemy_horde

    def __select_encounter(self):  # ask player team which encounter they would like to play
        available_difficulties = ['Easy']
        while True:
            try:
                print('\n' + '0: Easy')
                # print('1: Medium')
                # print('2: Hard')
                value = int(input('Enter selection for difficulty: '))
            except ValueError:
                print('Invalid input, try again')
            else:
                if 0 <= value < len(available_difficulties):
                    break
                else:
                    print('Improper selection, try again')

        full_list = self.encounter_list.get_list()
        selected_list = []
        print('')
        for i in full_list:
            if i['Difficulty'] == available_difficulties[value]:
                selected_list.append(i)

        while True:
            try:
                k = 0
                for j in selected_list:
                    print(k, j['Name'], sep=': ')
                    k += 1
                v = int(input('Enter selection for encounter: '))
            except ValueError:
                print('Invalid input, try again')
            else:
                if 0 <= v < len(selected_list):
                    break
                else:
                    print('Improper selection, try again')

        return selected_list[v]

    def __put_horde_on_map(self, horde):  # puts enemies on their side of the map
        for i in horde:
            self.movement.place_enemy_random(i)


class EnemyTurn(object):
    """
    Controls the enemy during their phase
    """
    def enemy_turn_loop(self):
        pass

