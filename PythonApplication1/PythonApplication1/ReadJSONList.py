import json
import os

class ReadJSONList():
    """Generic class for reading JSON list, then either returning the entire list or a single item as a dict."""


    #Base function which allows the class to know which json file to use
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

        return data # returns a 'dict' type

    def find_item(self, item):
        data = self._read_file()
        for i in data:
            if i['ID']==item:
                itemBlock = i['ID']
                break # valid?
         
        return itemBlock