import json
import os
from src.CONSTANTS import CONSTANTS
# from pathlib import Path

MASTER_DICT = CONSTANTS.JSON_DICT


class MasterListManager(object):
    """
    Reads all listed files in MASTER_DICT from the data folder then stores
    into MASTER_LIST.
    Returns a specific list when needed.
    """

    # TODO: implement pathlib?

    MASTER_LIST = []

    def __init__(self):
        for i in MASTER_DICT.values():
            self.MASTER_LIST.append(self.__read_file(i))

    # def __init__(self):
    #     json_dir = Path('/In Defense of Sieging/data/JSON Files')
    #     if json_dir.is_dir():
    #         for i in MASTER_DICT.values():
    #             self.MASTER_LIST.append(self.__read_file(json_dir, i))

    # TODO: @property?
    def __read_file(self, filename):
        try:
            path = os.path.abspath('data/JSON files')  # convert to pathlib?
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
                    break
            if item_block is not None:
                break

        return item_block

    # def __read_file(self, path, filename):
    #     try:
    #         path.resolve(strict=True)
    #
    #     except FileNotFoundError:
    #         print("Can't change the Current Working Directory to:", path)
    #
    #     with open(filename) as jsonList:
    #         data = json.load(jsonList)
    #
    #     return data

    # def get_list(self, item):
    #     item_block = None
    #     for i in self.MASTER_LIST:
    #         for j in i:
    #             if j == item:
    #                 item_block = i
    #                 break
    #         if item_block is not None:
    #             break
    #
    #     return item_block


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
