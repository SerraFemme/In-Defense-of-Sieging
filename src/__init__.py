import sys
import os
import pygame
from pygame.locals import *
from src.ReadGameData import MasterListManager, SubListManager
from src.BattleMap import MapInator
from src.GamePhases import BattlePhase
from src.TeamPhases import PlayerMaker, HordeMaker

# Window Constants
FPS = 30
WINWIDTH = 800
WINHEIGHT = 600
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)
third_window_width = int(WINWIDTH / 3)

# Tile Constants
TILEWIDTH = 50
TILEHEIGHT = 50

CAM_MOVE_SPEED = 10

WHITE = (255, 255, 255)
black = (0, 0, 0)
bright_blue = (0, 170, 255)
pale_turquoise = (175, 238, 238)
orange_red = (255, 69, 0)
dark_orange = (255, 140, 0)
red = (180, 0, 0)
bright_red = (255, 0, 0)
green = (0, 200, 0)
bright_green = (0, 255, 0)
BGCOLOR = pale_turquoise
TEXTCOLOR = dark_orange
title_color = dark_orange

default_font = 'freesansbold.ttf'

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

max_team_size = 4  # Change later
player_team = []
enemy_team = []


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

    r = MasterListManager()
    terrain_list = SubListManager(r.get_list('Terrain'))
    class_list = SubListManager(r.get_list('Class'))
    equipment_list = SubListManager(r.get_list('Equipment'))
    starting_equipment = SubListManager(r.get_list('Starting Equipment'))
    starting_deck = SubListManager(r.get_list('Starting Deck'))
    card_library = SubListManager(r.get_list('Card'))
    encounter_list = SubListManager(r.get_list('Encounter'))
    races = SubListManager(r.get_list('Enemy Race'))
    roles = SubListManager(r.get_list('Enemy Role'))

    while True:  # main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                __terminate()

        main_menu()  # menu


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

    DISPLAYSURF.fill(BGCOLOR)  # Start with drawing a blank color to the entire window:
    DISPLAYSURF.blit(titleSurf, titleRect)  # Draw the title image to the window:

    # Position and draw the text.
    for i in range(len(title_text_info)):
        instSurf = BASICFONT.render(title_text_info[i], 1, TEXTCOLOR)
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


def main_menu():
    global title_color
    title = 'In Defense of Sieging'
    title_font = pygame.font.Font(default_font, 40)

    titleSurf = title_font.render(title, True, title_color)
    titleRect = titleSurf.get_rect()
    topCoord = 50  # topCoord tracks where to position the top of the text
    titleRect.top = topCoord
    titleRect.centerx = HALF_WINWIDTH
    topCoord += titleRect.height

    DISPLAYSURF.fill(BGCOLOR)  # Start with drawing a blank color to the entire window:
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
                        create_player_team()
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
        text_rect.center = (HALF_WINWIDTH, start_button.centery)
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
        text_rect.center = (HALF_WINWIDTH, exit_button.centery)
        DISPLAYSURF.blit(text_surface, text_rect)

        pygame.display.update()
        FPSCLOCK.tick()


def create_player_team():
    global terrain_list, class_list, equipment_list, starting_equipment, \
        starting_deck, card_library, encounter_list, races, roles
    global max_team_size, player_team
    title = 'Player Team Creation'
    title_font = pygame.font.Font(default_font, 30)

    titleSurf = title_font.render(title, True, black)
    titleRect = titleSurf.get_rect()
    topCoord = 30
    titleRect.top = topCoord
    titleRect.centerx = HALF_WINWIDTH
    topCoord += titleRect.height + 20

    DISPLAYSURF.fill(BGCOLOR)
    DISPLAYSURF.blit(titleSurf, titleRect)

    class_selected = 0
    player_selected = 0
    max_displayed = 8
    top_displayed = 0
    class_top_coordinate = topCoord
    player_top_coordinate = topCoord

    available_classes = class_list.get_list()
    pm = PlayerMaker(class_list, starting_equipment, equipment_list,
                     starting_deck, card_library)

    class_button_size = (180, 50)
    class_button_center = (class_button_size[0] / 2, class_button_size[1] / 2)

    player_button_size = (180, 80)
    player_button_center = (player_button_size[0] / 2, player_button_size[1] / 2)

    quarter_width = int(HALF_WINWIDTH / 2)

    while True:  # Main loop for the start screen.
        for event in pygame.event.get():
            if event.type == QUIT:
                __terminate()
            elif event.type == KEYDOWN:
                # Handle key presses
                if event.key == K_w or event.key == K_UP:
                    if class_selected == top_displayed + 1:
                        if class_selected != 0:
                            class_selected -= 1
                        if top_displayed != 0:
                            top_displayed -= 1
                    else:
                        if class_selected != 0:
                            class_selected -= 1
                elif event.key == K_s or event.key == K_DOWN:
                    if class_selected < top_displayed + max_displayed - 2:
                        if class_selected < len(available_classes) - 1:
                            class_selected += 1
                    elif class_selected == top_displayed + max_displayed - 1 and top_displayed + max_displayed != len(
                            available_classes):
                        if top_displayed + max_displayed < len(available_classes):
                            top_displayed += 1
                    else:
                        if class_selected < len(available_classes) - 1:
                            class_selected += 1
                        if top_displayed + max_displayed < len(available_classes):
                            top_displayed += 1
                    # if class_selected == top_displayed + max_displayed - 1:
                    #     if class_selected < top_displayed + max_displayed - 2:
                    #         class_selected += 1
                    #     if top_displayed + max_displayed - 1 < len(display_list):
                    #         top_displayed += 1
                    # else:
                    #     if class_selected != top_displayed + max_displayed - 1:
                    #         class_selected += 1

                elif event.key == K_e or event.key == K_RETURN:
                    if len(player_team) < max_team_size:
                        c = available_classes.pop(class_selected)
                        number = str(len(player_team) + 1)
                        name = 'Player ' + number
                        player = pm.create_player(name, number, c)
                        player_team.append(player)
                        if class_selected > 0:
                            class_selected -= 1

        if max_displayed <= len(available_classes):
            bottom = max_displayed
        else:
            bottom = len(available_classes)

        if top_displayed + bottom > len(available_classes):
            top_displayed -= 1

        # FIXME: prints last class repeatedly if len(available_classes) < max_displayed
        for j in range(top_displayed, top_displayed + bottom):
            display_class = available_classes[j]
            display_string = display_class['ID']
            if j == class_selected:
                button_color = orange_red
            else:
                button_color = dark_orange
            class_button = pygame.draw.rect(DISPLAYSURF, button_color,
                                            (quarter_width - class_button_center[0],
                                             class_top_coordinate,
                                             class_button_size[0],
                                             class_button_size[1]))

            text_surface, text_rect = __text_object(display_string, small_text)
            text_rect.center = (quarter_width, class_button.centery)
            DISPLAYSURF.blit(text_surface, text_rect)

            class_top_coordinate += class_button_size[1] + 10

        class_top_coordinate = topCoord

        if len(player_team) > 0:
            for p in range(len(player_team)):
                player_name = player_team[p].Player_Name
                player_class = player_team[p].Class_Name
                button_color = orange_red
                player_button = pygame.draw.rect(DISPLAYSURF, button_color,
                                                 (3 * quarter_width - player_button_center[0],
                                                  player_top_coordinate,
                                                  player_button_size[0],
                                                  player_button_size[1]))

                text_surface, text_rect = __text_object(player_name, small_text)
                text_rect.center = (3 * quarter_width, player_button.centery - int(player_button_size[1] / 4))
                DISPLAYSURF.blit(text_surface, text_rect)

                text_surface, text_rect = __text_object(player_class, small_text)
                text_rect.center = (3 * quarter_width, player_button.centery + int(player_button_size[1] / 4))
                DISPLAYSURF.blit(text_surface, text_rect)

                player_top_coordinate += player_button_size[1] + 10

            player_top_coordinate = topCoord

        if len(available_classes) > 0:
            # TODO: Go to encounter maker button
            pass

        pygame.display.update()
        FPSCLOCK.tick()


def mission_select():  # TODO: enemy encounters
    # Select difficulty
    # Select encounter
    while True:  # Main loop for the start screen.
        for event in pygame.event.get():
            if event.type == QUIT:
                __terminate()

        pygame.display.update()
        FPSCLOCK.tick()


def battle_initialization():  # TODO: place ALL units on battle_map
    # create map, size based on player team size
    # auto-place enemy team
    # players select starting position
    # go to run_battle()
    while True:  # Main loop for the start screen.
        for event in pygame.event.get():
            if event.type == QUIT:
                __terminate()

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


def drawMap(battle_map):
    """
    Draws the map based on the tiles and their contents.
    """

    map_size = battle_map.map_size
    mapSurfWidth = map_size[0] * TILEWIDTH
    mapSurfHeight = map_size[1] * TILEHEIGHT
    mapSurf = pygame.Surface((mapSurfWidth, mapSurfHeight))
    mapSurf.fill(BGCOLOR)

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
