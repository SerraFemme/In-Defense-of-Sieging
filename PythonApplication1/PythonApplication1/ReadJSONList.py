import json # allows Python to use JSON
import os

class ReadCardList():
    """Generic class for reading JSON list then either returning the entire list or a single item as a dict."""

    #function to return whole list
    def __init__(self):
        data = self.read_file()
        return data # returns whole list as a 'dict' type


    #function to return specific terrain
    def __init__(self, item):
        data = self.read_file()
        for i in data:
            if i['ID']==item:
                itemBlock = i['ID']
                break # valid?
         
        #Either returns a selected class as a 'dict' type or None
        return itemBlock

    def read_file(self):
        # set listFileName
        
        try:
            #Change directory to the one needed, later change to be adaptive
            os.chdir("D:\\3 My New Game\\PythonGameCode\\PythonApplication1\\PythonApplication1\\JSON Files")

        except:
            print("Can't change the Current Working Directory") 

        #get Map Terrain List
        with open(listFileName) as jsonList:
            data = json.load(jsonList)

        return data # returns a 'dict' type