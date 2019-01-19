import json
import os

class ReadJSONList(object):
    """
    Generic class for reading JSON list.
    New Intention: Read and keep ALL json lists in memory
    Then pass only the list or very specific data

    Pass by object reference?
    """

    TEST_LIST_1 = [1, 2, 3]

    TEST_DICT = {'one': TEST_LIST_1}


    def __init__(self, jsonFile):
        self.listFileName = jsonFile

    def _read_file(self):
        try:
            path = os.path.abspath('JSON Files')
            os.chdir(path)
        except:
            print("Can't change the Current Working Directory") 

        with open(jsonFile) as jsonList:
            data = json.load(jsonList)

        return data

    def get_list(self):
        return self.TEST_LIST_1

    def get_list_from_dict(self):
        return self.TEST_DICT['one']

    def get_item(self, item):
        data = self._read_file()
        for i in data:
            if i['ID']==item:
                itemBlock = i['ID']
                break # valid?
         
        return itemBlock