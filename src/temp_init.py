import pygame
import sys
from pygame.locals import *
from pathlib import Path
import os

FPS = 30
WINWIDTH = 800
WINHEIGHT = 600
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)

# Tile Constants
TILEWIDTH = 50
TILEHEIGHT = 50

CAM_MOVE_SPEED = 5

WHITE = (255, 255, 255)
BRIGHTBLUE = (0, 170, 255)
pale_turquoise = (175, 238, 238)
orange_red = (255, 69, 0)
BGCOLOR = BRIGHTBLUE
TEXTCOLOR = WHITE
title_color = orange_red

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

image_dict = {'grass': 'GRASS.png',
              'hill': 'HILL.png',
              'mountain': 'MOUNTAIN.png',
              'cursor': 'CURSOR',
              'targeting_tile': 'TARGETING_TILE.png',
              'princess': 'princess.png',
              'boy': 'boy.png',
              'catgirl': 'catgirl.png',
              'horngirl': 'horngirl.png',
              'pinkgirl': 'pinkgirl.png',
              'rock': 'Rock.png',
              'short tree': 'Tree_Short.png',
              'tall tree': 'Tree_Tall.png',
              'ugly tree': 'Tree_Ugly.png'}

# path = Path().cwd()  # / 'data/Images'
# image_folder = path.parents[0] / 'data/Images'

# if Path('data/Images').exists():
#     image_folder = Path('data/Images')

# src = Path().cwd()
# home = src.parents[0]
# image_folder = home / 'data' / 'Images'


def main():
    global FPSCLOCK, DISPLAYSURF, IMAGESDICT, TILEMAPPING, OUTSIDEDECOMAPPING,\
        BASICFONT, UNITIMAGES, currentImage, image_dict

    pygame.init()
    FPSCLOCK = pygame.time.Clock()

    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))

    pygame.display.set_caption('In Defense of Sieging')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    # basic_font = pygame.font.Font('', 18)

    # with open(image_folder):
    #     IMAGESDICT = {'grass': pygame.image.load('GRASS.png'),
    #                   'hill': pygame.image.load('HILL.png'),
    #                   'mountain': pygame.image.load('MOUNTAIN.png'),
    #                   'cursor': pygame.image.load('CURSOR'),
    #                   'targeting_tile': pygame.image.load('TARGETING_TILE.png'),
    #                   'princess': pygame.image.load('princess.png'),
    #                   'boy': pygame.image.load('boy.png'),
    #                   'catgirl': pygame.image.load('catgirl.png'),
    #                   'horngirl': pygame.image.load('horngirl.png'),
    #                   'pinkgirl': pygame.image.load('pinkgirl.png'),
    #                   'rock': pygame.image.load('Rock.png'),
    #                   'short tree': pygame.image.load('Tree_Short.png'),
    #                   'tall tree': pygame.image.load('Tree_Tall.png'),
    #                   'ugly tree': pygame.image.load('Tree_Ugly.png')}

    IMAGESDICT = {}

    for key in image_dict:
        IMAGESDICT[key] = pygame.image.load(__read_file(image_dict[key]))

    TILEMAPPING = {'&': IMAGESDICT['mountain'],
                   '~': IMAGESDICT['hill'],
                   '.': IMAGESDICT['grass']}
    OUTSIDEDECOMAPPING = {'1': IMAGESDICT['rock'],
                          '2': IMAGESDICT['short tree'],
                          '3': IMAGESDICT['tall tree'],
                          '4': IMAGESDICT['ugly tree']}

    UNITIMAGES = {'P': IMAGESDICT['boy'],
                  'G': IMAGESDICT['pinkgirl'],
                  'C': IMAGESDICT['horngirl'],
                  'M': IMAGESDICT['catgirl']}

    start_screen()

    while True:  # main game loop
        DISPLAYSURF.fill(WHITE)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            pygame.display.update()
            FPSCLOCK.tick(FPS)

def __read_file(filename):
    try:
        path = os.path.abspath('data/Images')  # convert to pathlib?
        if os.path.exists(path):
            os.chdir(path)

    except OSError:
        print("Can't change the Current Working Directory to:", path)

    with open(filename) as image:
        data = pygame.image.load(image)

    return data

def start_screen():
    """
    Display the start screen (which has the title and instructions)
    until the player presses a key. Returns None.
    """
    global title_color

    TITLE = 'In Defense of Sieging'
    TITLEFONT = pygame.font.Font('freesansbold.ttf', 60)

    # Position the title image.
    # titleRect = IMAGESDICT['title'].get_rect()
    titleSurf = TITLEFONT.render(TITLE, True, title_color)
    titleRect = titleSurf.get_rect()
    topCoord = 150  # topCoord tracks where to position the top of the text
    titleRect.top = topCoord
    titleRect.centerx = HALF_WINWIDTH
    topCoord += titleRect.height

    # Unfortunately, Pygame's font & text system only shows one line at
    # a time, so we can't use strings with \n newline characters in them.
    # So we will use a list with each line in it.
    instruction_text = ['By Russell Buckner',
                        'Copyright 2019, All rights reserved.',
                        '',
                        'Press any key to continue']

    # Start with drawing a blank color to the entire window:
    DISPLAYSURF.fill(BGCOLOR)

    # Draw the title image to the window:
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Position and draw the text.
    for i in range(len(instruction_text)):
        instSurf = BASICFONT.render(instruction_text[i], 1, TEXTCOLOR)
        instRect = instSurf.get_rect()
        topCoord += 10  # 10 pixels will go in between each line of text.
        instRect.top = topCoord
        instRect.centerx = HALF_WINWIDTH
        topCoord += instRect.height  # Adjust for the height of the line.
        DISPLAYSURF.blit(instSurf, instRect)

    while True:  # Main loop for the start screen.
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return  # user has pressed a key, so return.

        # Display the DISPLAYSURF contents to the actual screen.
        pygame.display.update()
        FPSCLOCK.tick()


def drawMap(battle_map, gameStateObj, goals):  # Assimilate, convert mapOdj to Battle Map
    """
    Draws the map to a Surface object, including the player and stars.
    This function does NOT call pygame.display.update(), nor does it draw the
    "Level" and "Steps" text in the corner.
    """

    # mapSurf will be the single Surface object that the tiles are drawn
    # on, so that it is easy to position the entire map on the DISPLAYSURF
    # Surface object. First, the width and height must be calculated.
    map_size = battle_map.map_size
    mapSurfWidth = map_size[0] * TILEWIDTH
    mapSurfHeight = (map_size[1]) * TILEHEIGHT
    mapSurf = pygame.Surface((mapSurfWidth, mapSurfHeight))
    mapSurf.fill(BGCOLOR)  # start with a blank color on the surface.

    # Draw the tile sprites onto this surface.
    for x in range(map_size[0]):
        for y in range(map_size[1]):
            spaceRect = pygame.Rect((x * TILEWIDTH, y * TILEHEIGHT,
                                     TILEWIDTH, TILEHEIGHT))
            tile = battle_map.get_tile(x, y)
            char = tile.get_terrain_char()
            baseTile = TILEMAPPING[char]

            # First draw the base ground/wall tile.
            mapSurf.blit(baseTile, spaceRect)

            # if mapObj[x][y] in OUTSIDEDECOMAPPING:
            #     # Draw any tree/rock decorations that are on this tile.
            #     mapSurf.blit(OUTSIDEDECOMAPPING[mapObj[x][y]], spaceRect)
            # elif (x, y) in gameStateObj['stars']:
            #     if (x, y) in goals:
            #         # A goal AND star are on this space, draw goal first.
            #         mapSurf.blit(IMAGESDICT['covered goal'], spaceRect)
            #     # Then draw the star sprite.
            #     mapSurf.blit(IMAGESDICT['star'], spaceRect)
            # elif (x, y) in goals:
            #     # Draw a goal without a star on it.
            #     mapSurf.blit(IMAGESDICT['uncovered goal'], spaceRect)

            # Last draw the player on the board.
            # if (x, y) == gameStateObj['player']:
            #     # Note: The value "currentImage" refers
            #     # to a key in "PLAYERIMAGES" which has the
            #     # specific player image we want to show.
            #     mapSurf.blit(PLAYERIMAGES[currentImage], spaceRect)

            if tile.unit != 'Invalid':
                char = tile.unit.char
                if isinstance(char, int):
                    mapSurf.blit(UNITIMAGES['P'], spaceRect)
                else:
                    mapSurf.blit(UNITIMAGES[char], spaceRect)

    return mapSurf


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
