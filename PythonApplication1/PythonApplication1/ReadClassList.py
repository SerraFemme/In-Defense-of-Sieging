import json # allows Python to use JSON
import os


class ReadClassList():
    """Class for reading ClassList.json then returning the entire list as a dict."""

    #function to return whole list
    def __init__(self):
        data = self.read_file()
        return data # returns whole list as a 'dict' type


    #function to return specific terrain
    def __init__(self, className):
        data = self.read_file()
        for i in data:
            if i['Class_Name']==className:
                classData = i['Class_Name']
         
        #Either returns a selected class as a 'dict' type or None
        return classData

    def read_file(self):
        try:
            #Change directory to the one needed, later change to be adaptive
            os.chdir("D:\\3 My New Game\\PythonGameCode\\PythonApplication1\\PythonApplication1\\JSON Files")

        except:
            print("Can't change the Current Working Directory") 

        #get Map Terrain List
        with open('ClassList.json') as ClassL:
            data = json.load(ClassL)

        return data # returns a 'dict' type

    #def has_class(self, className):
