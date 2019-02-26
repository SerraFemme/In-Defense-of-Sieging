import os
import pygame
from src.CONSTANTS import CONSTANTS
from src.ReadGameData import MasterListManager
from src.GraphicalLogic import StartScreen

# Window Constants
WINWIDTH = CONSTANTS.WINWIDTH
WINHEIGHT = CONSTANTS.WINHEIGHT

# Colors
dark_orange = CONSTANTS.COLORS['dark_orange']
pale_turquoise = CONSTANTS.COLORS['pale_turquoise']

png_dict = CONSTANTS.IMAGE_DICTIONARY


def main():
    home = os.getcwd()
    image_dict = {}

    for key in png_dict:
        image_dict[key] = __read_file(png_dict[key])

    os.chdir(home)
    direct = os.path.abspath('..')
    os.chdir(direct)

    master_list = MasterListManager()

    pygame.init()
    FPSCLOCK = pygame.time.Clock()

    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))

    pygame.display.set_caption('In Defense of Sieging')

    start_screen = StartScreen(master_list, image_dict)
    start_screen.start(DISPLAYSURF, FPSCLOCK)


def __read_file(filename):  # TODO: clean up
    try:
        p = os.path.abspath('..')
        path = os.path.join(p, 'data\\images')
        if os.path.exists(path):
            os.chdir(path)

    except OSError:
        print("Can't change the Current Working Directory to:", path)

    with open(filename):
        data = pygame.image.load(filename)

    return data


if __name__ == '__main__':
    main()
