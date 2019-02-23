import sys
import os
import pygame
from pygame.locals import *
from src.CONSTANTS import CONSTANTS
from src.ReadGameData import MasterListManager
from src.GraphicalLogic import CreateTeam
from src.BattleMap import MapInator
from src.GamePhases import BattlePhase

# Window Constants
FPS = CONSTANTS.FPS
WINWIDTH = CONSTANTS.WINWIDTH
WINHEIGHT = CONSTANTS.WINHEIGHT
HALF_WINWIDTH = CONSTANTS.HALF_WINWIDTH
HALF_WINHEIGHT = CONSTANTS.HALF_WINHEIGHT
third_window_width = CONSTANTS.THIRD_WINDOW_WIDTH

# Tile Constants
TILEWIDTH = 50
TILEHEIGHT = 50

CAM_MOVE_SPEED = CONSTANTS.CAM_MOVE_SPEED

# Colors
black = CONSTANTS.COLORS['black']
bright_red = CONSTANTS.COLORS['red']
red = CONSTANTS.COLORS['dark_red']
orange_red = CONSTANTS.COLORS['orange_red']
dark_orange = CONSTANTS.COLORS['dark_orange']
green = CONSTANTS.COLORS['medium_green']
bright_green = CONSTANTS.COLORS['green']
pale_turquoise = CONSTANTS.COLORS['pale_turquoise']

bg_color = pale_turquoise
title_color = dark_orange

# Fonts
default_font = CONSTANTS.FONT_DICT['sans_bold']

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
    # Graphics Variables
    global FPSCLOCK, DISPLAYSURF, BASICFONT, small_text, png_dict, image_dict

    # Logic Variables
    global terrain_list, class_list, equipment_list, starting_equipment, \
        starting_deck, card_library, encounter_list, races, roles

    home = os.getcwd()

    pygame.init()
    FPSCLOCK = pygame.time.Clock()

    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))

    pygame.display.set_caption('In Defense of Sieging')
    BASICFONT = pygame.font.Font(default_font, 18)
    small_text = pygame.font.Font(default_font, 20)

    image_dict = {}

    for key in png_dict:
        image_dict[key] = __read_file(png_dict[key])

    start_screen()

    os.chdir(home)
    direct = os.path.abspath('..')
    os.chdir(direct)

    master_list = MasterListManager()

    ct = CreateTeam(master_list)

    while True:  # main menu loop
        for event in pygame.event.get():
            if event.type == QUIT:
                __terminate()

        main_menu(ct)


def start_screen():
    """
    Display the start screen (which has the title and instructions)
    until the player presses a key. Returns None.
    """
    global title_color

    title = 'In Defense of Sieging'
    title_font = pygame.font.Font(default_font, 60)

    titleSurf = title_font.render(title, True, title_color)
    titleRect = titleSurf.get_rect()
    topCoord = 150  # topCoord tracks where to position the top of the text
    titleRect.top = topCoord
    titleRect.centerx = HALF_WINWIDTH
    topCoord += titleRect.height

    title_text_info = ['By Russell Buckner',
                       'Copyright 2019, All rights reserved.',
                       '',
                       'Press any key to continue']

    DISPLAYSURF.fill(bg_color)  # Start with drawing a blank color to the entire window:
    DISPLAYSURF.blit(titleSurf, titleRect)  # Draw the title image to the window:

    # Position and draw the text.
    for i in range(len(title_text_info)):
        instSurf = BASICFONT.render(title_text_info[i], 1, dark_orange)
        instRect = instSurf.get_rect()
        topCoord += 10  # 10 pixels will go in between each line of text.
        instRect.top = topCoord
        instRect.centerx = HALF_WINWIDTH
        topCoord += instRect.height  # Adjust for the height of the line.
        DISPLAYSURF.blit(instSurf, instRect)

    while True:  # Main loop for the start screen.
        for event in pygame.event.get():
            if event.type == QUIT:
                __terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    __terminate()
                return  # user has pressed a key, so return.

        # Display the DISPLAYSURF contents to the actual screen.
        pygame.display.update()
        FPSCLOCK.tick()


def main_menu(ct):
    global title_color, FPSCLOCK
    title = 'In Defense of Sieging'
    title_font = pygame.font.Font(default_font, 40)

    titleSurf = title_font.render(title, True, title_color)
    titleRect = titleSurf.get_rect()
    topCoord = 50  # topCoord tracks where to position the top of the text
    titleRect.top = topCoord
    titleRect.centerx = HALF_WINWIDTH
    topCoord += titleRect.height

    DISPLAYSURF.fill(bg_color)  # Start with drawing a blank color to the entire window:
    DISPLAYSURF.blit(titleSurf, titleRect)  # Draw the title image to the window:

    button_size = (120, 50)
    button_center = (button_size[0] / 2, button_size[1] / 2)

    start_top_coordinate = topCoord + button_center[1]
    exit_top_coordinate = start_top_coordinate + button_size[1] + 20

    selected = 0

    while True:  # Main loop for the start screen.
        for event in pygame.event.get():
            if event.type == QUIT:
                __terminate()
            elif event.type == KEYDOWN:
                # Handle key presses
                if event.key == K_w or event.key == K_UP:
                    selected += 1
                    if selected > 1:
                        selected = 0
                elif event.key == K_s or event.key == K_DOWN:
                    selected -= 1
                    if selected < 0:
                        selected = 1
                elif event.key == K_e or event.key == K_RETURN:
                    if selected == 1:
                        __terminate()
                    elif selected == 0:
                        ct.start(DISPLAYSURF, FPSCLOCK)
                        # run_battle()

        # Start Button
        if selected == 0:
            start_color = bright_green
            start_text = '<START>'
        else:
            start_color = green
            start_text = 'START'

        start_button = pygame.draw.rect(DISPLAYSURF, start_color,
                                        (HALF_WINWIDTH - button_center[0],
                                         start_top_coordinate,
                                         button_size[0],
                                         button_size[1]))

        text_surface, text_rect = __text_object(start_text, small_text)
        text_rect.center = (start_button.centex, start_button.centery)
        DISPLAYSURF.blit(text_surface, text_rect)

        # FIXME: "Exit" word shifts slightly when selected
        if selected == 1:
            exit_color = bright_red
            exit_text = '<EXIT>'
        else:
            exit_color = red
            exit_text = 'EXIT'

        exit_button = pygame.draw.rect(DISPLAYSURF, exit_color,
                                       (HALF_WINWIDTH - button_center[0],
                                        exit_top_coordinate,
                                        button_size[0],
                                        button_size[1]))

        text_surface, text_rect = __text_object(exit_text, small_text)
        text_rect.center = (exit_button.centerx, exit_button.centery)
        DISPLAYSURF.blit(text_surface, text_rect)

        pygame.display.update()
        FPSCLOCK.tick()


def run_battle():
    global terrain_list
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
                __terminate()
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

        DISPLAYSURF.fill(bg_color)

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


def drawMap(battle_map):
    """
    Draws the map based on the tiles and their contents.
    """

    map_size = battle_map.map_size
    mapSurfWidth = map_size[0] * TILEWIDTH
    mapSurfHeight = map_size[1] * TILEHEIGHT
    mapSurf = pygame.Surface((mapSurfWidth, mapSurfHeight))
    mapSurf.fill(bg_color)

    # Draw the tile sprites onto this surface.
    for x in range(map_size[0]):
        for y in range(map_size[1]):
            spaceRect = pygame.Rect((x * TILEWIDTH, y * TILEHEIGHT,
                                     TILEWIDTH, TILEHEIGHT))
            tile = battle_map.get_tile(x, y)
            terrain_type = tile.get_terrain_type()
            baseTile = image_dict[terrain_type]

            mapSurf.blit(baseTile, spaceRect)

            # TODO: draw units on tiles
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


def __text_object(text, font):
    text_surface = font.render(text, True, black)
    return text_surface, text_surface.get_rect()


def __terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
