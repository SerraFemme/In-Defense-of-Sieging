
import json # allows Python to use JSON
import os

class ReadTerrainList():
    """Class for reading MapTerrain.json returning the entire list as a dict.  May add functionality to return a specific item"""

    #methor to return whole list

    #method to return specific item

    try:
        #Change directory to the one needed, later change to be adaptive
        os.chdir("D:\\3 My New Game\\PythonGameCode\\PythonApplication1\\PythonApplication1\\JSON Files")

    except:
        print("Can't change the Current Working Directory") 

    #get Map Terrain List
    with open('MapTerrain.json') as Terrain:
        data = json.load(Terrain)
    #print(json.dumps(data, indent=4))

    #return data