import json
import os

MASTER_DICT = {'Terrain': 'MapTerrain.json',
               'Class': 'ClassLibrary.json',
               'Enemy Race': 'EnemyRaceLibrary.json',
               'Enemy Role': 'EnemyRoleLibrary.json',
               'Encounter': 'Encounter.json',
               'Equipment': 'EquipmentLibrary.json',
               'Starting Equipment': 'StartingEquipmentLibrary.json',
               'Card': 'CardLibrary.json',
               'Starting Deck': 'StartingDeck.json'}


class MasterListManager(object):
    """
    Reads all listed files in MASTER_DICT from the data folder then stores
    into MASTER_LIST.
    Returns a specific list when needed.
    """

    MASTER_LIST = []

    def __init__(self):
        for i in MASTER_DICT.values():
            self.MASTER_LIST.append(self._read_file(i))

    # @property?
    def _read_file(self, filename):
        try:
            path = os.path.abspath('data')
            if os.path.exists(path):
                os.chdir(path)

        except OSError:
            print("Can't change the Current Working Directory to:", path)

        with open(filename) as jsonList:
            data = json.load(jsonList)

        return data

    def get_list(self, item):
        item_block = None
        for i in self.MASTER_LIST:
            for j in i:
                if j == item:
                    item_block = i

        return item_block


class SubListManager(object):
    """
    Is given a specific list when called
    Either checks and returns a boolean or searches and returns a specific set of data
    """

    def __init__(self, list_name):
        self.sublist = list_name

    def get_item(self, item):
        item_block = None
        for i in self.sublist.values():
            for j in i:
                if j['ID'] == item:
                    item_block = j

        return item_block

    def has_item(self, item):
        for i in self.sublist.values():
            if i['ID'] == item:
                return True

        return False

    def get_list(self):
        item_list = []
        for i in self.sublist.values():
            for j in i:
                item_list.append(j)
        return item_list
