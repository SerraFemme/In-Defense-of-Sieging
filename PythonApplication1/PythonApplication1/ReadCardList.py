#
#DECOMMISSION
#

# testing how to use json in python
import json # allows Python to use JSON
import os

class ReadCardList():

    #function to return whole list
    def __init__(self):
        data = self.read_file()
        return data # returns whole list as a 'dict' type


    #function to return specific card
    def __init__(self, className):
        data = self.read_file()
        for i in data:
            if i['ID']==className:
                classData = i['ID']
                break # valid?
         
        #Either returns a selected class as a 'dict' type or None
        return classData

    try:
        #Change directory to the one I need to
        os.chdir("D:\\3 My New Game\\PythonGameCode\\PythonApplication1\\PythonApplication1\\JSON Files")

    except:
        print("Can't change the Current Working Directory") 

    #test line of code
    #with open('EquipmentLibrary.json') as EquipL: data = json.load(EquipL)

    #get Equipment Library and print to screen
    with open('CardLibrary.json') as CardL:
        data = json.load(CardL)
    print(json.dumps(data, indent=4))