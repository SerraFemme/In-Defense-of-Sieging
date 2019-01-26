from ReadGameData import SubListManager
from Player import Player

"""
Module that asks the Player which class they would like to play, then creates
    a Player object with the proper info.
"""


class TeamMaker(object):
    def __init__(self, c, e):
        self.class_list = SubListManager(c)
        self.equipment_list = SubListManager(e)
        self.player_list = []

    def team_init(self):
        for i in range(4):
            selected_class = self.__select_class()
            class_info = self.class_list.get_item(selected_Class)
            player = Player(class_info)
            # give player starting equipment
            # give player starting deck
        return self.player_list

    def __select_class(self):
        # print list of classes
        # ask for selection as int
        # get class name as string
        return selection
