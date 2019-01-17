import json
import os

class ReadJSONList(object):
    """
    Generic class for reading JSON list.
    Either returns the entire list or a single item as a dict.
    """


    def __init__(self, jsonFile):
        self.listFileName = jsonFile

    def _read_file(self):
        try:
            path = os.path.abspath('.\\JSON Files')
            os.chdir(path)
        except:
            print("Can't change the Current Working Directory") 

        with open(self.listFileName) as jsonList:
            data = json.load(jsonList)

        return data

    def get_item(self, item):
        data = self._read_file()
        for i in data:
            if i['ID']==item:
                itemBlock = i['ID']
                break # valid?
         
        return itemBlock