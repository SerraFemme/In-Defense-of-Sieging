"""
Contains all functions needed for either side to make their team and take
their turns.
"""

from src.Unit import Player, Enemy
from src.Equipment import Equipment


class PlayerMaker(object):
    """
    Creates the player.
    """

    def __init__(self, c, se, e, sd, card):
        self.class_list = c
        self.s_equipment = se  # Starting Equipment
        self.equipment_list = e
        self.s_deck = sd  # Starting Deck
        self.card_library = card

    def create_player(self, player_name, player_number, selected_class):
        player = Player(self.class_list.get_item(selected_class), player_name, player_number)
        self.__equip_s_equipment(player,
                                 self.s_equipment.get_item(selected_class),
                                 self.equipment_list)
        # player.Passive = getattribute(src.ClassPassives, selected_class)
        # TODO: give player starting deck
        # self.add_s_deck(player, self.s_deck.get_item(selected_class, self.card_library)
        # self.add_s_deck(player, self.s_deck.get_item("Test", self.card_library)
        return player

    def __equip_s_equipment(self, player, s_equip, equip_list):
        s_list = s_equip['Starting_Equipment']
        for i in s_list:
            e = Equipment(equip_list.get_item(i))
            player.add_equipment(e)


class HordeMaker(object):
    """
    Creates an enemy horde based on the encounter list then puts them on the map
    """

    def __init__(self, races, roles, equipment_list, n):
        self.number_of_players = n
        self.race_list = races
        self.role_list = roles
        self.equipment_list = equipment_list

    def create_enemy_team(self, encounter):
        enemy_horde = []
        enemy_list = encounter['Enemies']

        for i in enemy_list:
            if isinstance(i['Number'], int):
                for j in range(i['Number']):
                    race = self.race_list.get_item(i['Race'])
                    role = self.role_list.get_item(i['Role'])
                    enemy = Enemy(race, role, j + 1)
                    for e in i['Equipment']:
                        equipment = self.equipment_list.get_item(e)
                        enemy.add_equipment(Equipment(equipment))
                    enemy_horde.append(enemy)
            else:  # Numbers is a string
                for j in range(self.number_of_players):
                    race = self.race_list.get_item(i['Race'])
                    role = self.role_list.get_item(i['Role'])
                    enemy = Enemy(race, role, j + 1)
                    for e in i['Equipment']:
                        equipment = self.equipment_list.get_item(e)
                        enemy.add_equipment(Equipment(equipment))
                    enemy_horde.append(enemy)

        return enemy_horde



