import sys
import os
import pygame
from pygame.locals import *
from src.BattleMap import MapInator
from src.ReadGameData import MasterListManager

FPS = 30
WINWIDTH = 800
WINHEIGHT = 600
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)

# Tile Constants
TILEWIDTH = 50
TILEHEIGHT = 50

CAM_MOVE_SPEED = 10

WHITE = (255, 255, 255)
bright_blue = (0, 170, 255)
pale_turquoise = (175, 238, 238)
orange_red = (255, 69, 0)
dark_orange = (255, 140, 0)
BGCOLOR = pale_turquoise
TEXTCOLOR = dark_orange
title_color = dark_orange

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

png_dict = {'Grass': 'GRASS.png',
            'Hill': 'HILL.png',
            'Mountain': 'MOUNTAIN.png',
            'cursor': 'CURSOR.png',
            'selected_cursor': 'SELECTED.png',
            'targeting_tile': 'TARGETING_TILE.png',
            'player_token': 'PLAYER.png',
            'enemy_token': 'ENEMY.png'}


def main():
    global FPSCLOCK, DISPLAYSURF, image_dict, BASICFONT,  png_dict

    home = os.getcwd()

    pygame.init()
    FPSCLOCK = pygame.time.Clock()

    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))

    pygame.display.set_caption('In Defense of Sieging')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    # basic_font = pygame.font.Font('', 18)

    image_dict = {}

    for key in png_dict:
        image_dict[key] = __read_file(png_dict[key])

    start_screen()

    os.chdir(home)
    direct = os.path.abspath('..')
    os.chdir(direct)

    r = MasterListManager()
    terrain_list = r.get_list('Terrain')

    while True:  # main game loop
        run_battle(terrain_list)


def __read_file(filename):  # clean up
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


def run_battle(terrain_list):
    # Game Logic
    battle_map = MapInator(terrain_list)
    map_size = battle_map.map_size

    # Display Logic
    mapWidth = map_size[0] * TILEWIDTH
    mapHeight = map_size[1] * TILEHEIGHT
    MAX_CAM_X_PAN = abs(HALF_WINHEIGHT - int(mapHeight / 2)) + TILEWIDTH
    MAX_CAM_Y_PAN = abs(HALF_WINWIDTH - int(mapWidth / 2)) + TILEHEIGHT
    redraw_map = True

    cameraOffsetX = 0
    cameraOffsetY = 0

    cameraUp = False
    cameraDown = False
    cameraLeft = False
    cameraRight = False

    while True:
        cursor_move = None
        key_pressed = False

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                # Handle key presses
                keyPressed = True
                if event.key == K_w:
                    playerMoveTo = UP
                elif event.key == K_s:
                    playerMoveTo = DOWN
                elif event.key == K_a:
                    playerMoveTo = LEFT
                elif event.key == K_d:
                    playerMoveTo = RIGHT

                elif event.key == K_q:
                    pass  # Cancel
                elif event.key == K_e:
                    pass  # Select

                # Set the camera move mode.
                elif event.key == K_UP:
                    cameraUp = True
                elif event.key == K_DOWN:
                    cameraDown = True
                elif event.key == K_LEFT:
                    cameraLeft = True
                elif event.key == K_RIGHT:
                    cameraRight = True
                elif event.key == K_z:
                    cameraOffsetX = 0
                    cameraOffsetY = 0

                elif event.key == K_ESCAPE:
                    pass  # Menu, implement later

            elif event.type == KEYUP:
                # Unset the camera move mode.
                if event.key == K_UP:
                    cameraUp = False
                elif event.key == K_DOWN:
                    cameraDown = False
                elif event.key == K_LEFT:
                    cameraLeft = False
                elif event.key == K_RIGHT:
                    cameraRight = False


        DISPLAYSURF.fill(BGCOLOR)

        if redraw_map:
            mapSurf = drawMap(battle_map)
            redraw_map = False

        if cameraUp and cameraOffsetY < MAX_CAM_X_PAN:
            cameraOffsetY += CAM_MOVE_SPEED
        elif cameraDown and cameraOffsetY > -MAX_CAM_X_PAN:
            cameraOffsetY -= CAM_MOVE_SPEED
        if cameraLeft and cameraOffsetX < MAX_CAM_Y_PAN:
            cameraOffsetX += CAM_MOVE_SPEED
        elif cameraRight and cameraOffsetX > -MAX_CAM_Y_PAN:
            cameraOffsetX -= CAM_MOVE_SPEED

        mapSurfRect = mapSurf.get_rect()
        mapSurfRect.center = (HALF_WINWIDTH + cameraOffsetX, HALF_WINHEIGHT + cameraOffsetY)

        DISPLAYSURF.blit(mapSurf, mapSurfRect)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def start_screen():
    """
    Display the start screen (which has the title and instructions)
    until the player presses a key. Returns None.
    """
    global title_color

    title = 'In Defense of Sieging'
    title_font = pygame.font.Font('freesansbold.ttf', 60)

    titleSurf = title_font.render(title, True, title_color)
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


def drawMap(battle_map):  # Assimilate, convert mapOdj to Battle Map
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
    mapSurfHeight = map_size[1] * TILEHEIGHT
    mapSurf = pygame.Surface((mapSurfWidth, mapSurfHeight))
    mapSurf.fill(BGCOLOR)  # start with a blank color on the surface.

    # Draw the tile sprites onto this surface.
    for x in range(map_size[0]):
        for y in range(map_size[1]):
            spaceRect = pygame.Rect((x * TILEWIDTH, y * TILEHEIGHT,
                                     TILEWIDTH, TILEHEIGHT))
            tile = battle_map.get_tile(x, y)
            terrain_type = tile.get_terrain_type()
            baseTile = image_dict[terrain_type]

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

            # if tile.unit != 'Invalid':
            #     char = tile.unit.char
            #     if isinstance(char, int):
            #         mapSurf.blit(UNITIMAGES['P'], spaceRect)
            #     else:
            #         mapSurf.blit(UNITIMAGES[char], spaceRect)

    return mapSurf


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
