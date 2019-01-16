#
#DECOMMISSION
#


# testing how to use json in python
import json # allows Python to use JSON
import os


class ReadEquipmentList():
    """Class for reading ClassList.json then returning the entire list as a dict."""

    #function to return whole list
    def __init__(self):
        data = self.read_file()
        return data # returns whole list as a 'dict' type


    #function to return specific terrain
    def __init__(self, equipName):
        data = self.read_file()
        for i in data:
            if i['ID']==equipName:
                equipData = i['ID']
                break # valid?
                
        #Either returns a selected equip as a 'dict' type or None
        return equipData

    def read_file(self):
        try:
            #Change directory to the one needed, later change to be adaptive
            os.chdir("D:\\3 My New Game\\PythonGameCode\\PythonApplication1\\PythonApplication1\\JSON Files")

        except:
            print("Can't change the Current Working Directory") 

        #get Equipment List
        with open('EquipmentLibrary.json') as EquipL:
            data = json.load(EquipL)

        return data # returns a 'dict' type
