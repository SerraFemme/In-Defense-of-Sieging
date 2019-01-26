import json
import os

MASTER_DICT = {'Card': 'CardLibrary.json',
               'Class': 'ClassLibrary.json',
               'Enemy Race': 'EnemyRaceLibrary.json',
               'Enemy Role': 'EnemyRoleLibrary.json',
               'Equipment': 'EquipmentLibrary.json',
               'Terrain': 'MapTerrain.json',
               'Starting Equipment': 'StartingEquipmentLibrary.json'}


class MasterListManager(object):
    """
    Reads all valid files in Game Data then stores into MASTER_LIST
    Returns a specific list when needed
    """

    TEST_LIST_1 = [1, 2, 3]

    TEST_DICT = {'one': TEST_LIST_1}

    MASTER_LIST = []

    def __init__(self):
        # global MASTER_DICT
        # print()

        for i in MASTER_DICT.values():
            self.MASTER_LIST.append(self._read_file(i))

    # @property?
    def _read_file(self, filename):
        try:
            path = os.path.abspath('Game Data')
            if os.path.exists(path):
                os.chdir(path)

        except OSError:
            print("Can't change the Current Working Directory to:", path)

        with open(filename) as jsonList:
            data = json.load(jsonList)

        return data

    def get_list(self, item):
        itemblock = None
        for i in self.MASTER_LIST:
            for j in i:
                if j == item:
                    itemblock = i

        return itemblock

    # def get_list(self):
    #     return self.TEST_LIST_1
    #
    # def get_list_from_dict(self):
    #     return self.TEST_DICT['one']


class SubListManager(object):
    """
    Is given a specific list when called
    Either checks and returns a boolean or searches and returns a specific set of data
    """

    def __init__(self, listname):
        self.sublist = listname

    def get_item(self, item):
        for i in self.sublist.values():  # fix?
            for j in i:
                if j['ID'] == item:
                    itemblock = j

        return itemblock

    def has_item(self, item):
        for i in self.sublist.values():
            if i['ID'] == item:
                return True

        return False
