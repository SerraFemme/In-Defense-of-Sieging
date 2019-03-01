import sys
import pygame
from pygame.locals import *
from src.ReadGameData import SubListManager
from src.CONSTANTS import CONSTANTS
from src.Unit import Enemy, Player
from src.TeamPhases import PlayerMaker, HordeMaker
from src.BattleMap import MapInator, Movement
from src.GamePhases import BattlePhase

pygame.font.init()

max_team_size = CONSTANTS.MAX_PLAYERS
diff_list = CONSTANTS.DIFFICULTY_LIST

default_font = CONSTANTS.FONT_DICT['sans_bold']
small_text = pygame.font.Font(default_font, 20)
icon_text = pygame.font.Font(default_font, 16)

black = CONSTANTS.COLORS['black']
bright_red = CONSTANTS.COLORS['red']
red = CONSTANTS.COLORS['dark_red']
orange_red = CONSTANTS.COLORS['orange_red']
dark_orange = CONSTANTS.COLORS['dark_orange']
green_yellow = CONSTANTS.COLORS['green_yellow']
bright_green = CONSTANTS.COLORS['green']
medium_green = CONSTANTS.COLORS['medium_green']
grey = CONSTANTS.COLORS['grey']
blue = CONSTANTS.COLORS['blue']
pale_turquoise = CONSTANTS.COLORS['pale_turquoise']

bg_color = pale_turquoise
title_color = dark_orange
selected_color = orange_red
unselected_color = dark_orange

window_width = CONSTANTS.WINWIDTH
window_width_half = CONSTANTS.HALF_WINWIDTH
window_width_quarter = CONSTANTS.QUARTER_WINWIDTH
window_height = CONSTANTS.WINHEIGHT
window_height_half = CONSTANTS.HALF_WINHEIGHT
button_size = CONSTANTS.STANDARD_BUTTON_SIZE
tile_size = CONSTANTS.TILE_SIZE
cam_move_speed = CONSTANTS.CAM_MOVE_SPEED
fps = CONSTANTS.FPS


class StartScreen(object):  # TODO: assimilate start_screen
    def __init__(self, master_list, image_dict):
        self.master_list = master_list
        self.image_dict = image_dict

    def start(self, DISPLAYSURF, FPSCLOCK):
        """
        Display the start screen (which has the title and instructions)
        until the player presses a key. Returns None.
        """
        title = 'In Defense of Sieging'
        title_font = pygame.font.Font(default_font, 60)

        titleSurf = title_font.render(title, True, title_color)
        titleRect = titleSurf.get_rect()
        topCoord = 150  # topCoord tracks where to position the top of the text
        titleRect.top = topCoord
        titleRect.centerx = window_width_half
        topCoord += titleRect.height

        title_text_info = ['By Russell Buckner',
                           'Copyright 2019, All rights reserved.',
                           '',
                           'Press any key to continue']

        DISPLAYSURF.fill(bg_color)  # Start with drawing a blank color to the entire window:
        DISPLAYSURF.blit(titleSurf, titleRect)  # Draw the title image to the window:

        # Position and draw the text.
        for i in range(len(title_text_info)):
            instSurf = small_text.render(title_text_info[i], 1, dark_orange)
            instRect = instSurf.get_rect()
            topCoord += 10  # 10 pixels will go in between each line of text.
            instRect.top = topCoord
            instRect.centerx = window_width_half
            topCoord += instRect.height  # Adjust for the height of the line.
            DISPLAYSURF.blit(instSurf, instRect)

        while True:  # Main loop for the start screen.
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.__terminate()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.__terminate()
                    else:
                        mm = MainMenu(self.master_list, self.image_dict)
                        mm.start(DISPLAYSURF, FPSCLOCK)

            pygame.display.update()
            FPSCLOCK.tick()

    def __text_object(self, text, font):
        text_surface = font.render(text, True, black)
        return text_surface, text_surface.get_rect()

    def __terminate(self):
        pygame.quit()
        sys.exit()


class MainMenu(object):
    def __init__(self, master_list, image_dict):
        self.master_list = master_list
        self.image_dict = image_dict

    def start(self, DISPLAYSURF, FPSCLOCK):  # TODO: assimilate main_menu
        title = 'In Defense of Sieging'
        title_font = pygame.font.Font(default_font, 40)

        titleSurf = title_font.render(title, True, title_color)
        titleRect = titleSurf.get_rect()
        topCoord = 50  # topCoord tracks where to position the top of the text
        titleRect.top = topCoord
        titleRect.centerx = window_width_half
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
                    self.__terminate()
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
                            self.__terminate()
                        elif selected == 0:
                            ct = CreateTeam(self.master_list, self.image_dict)
                            ct.start(DISPLAYSURF, FPSCLOCK)
                            # run_battle()

            # Start Button
            if selected == 0:
                start_color = bright_green
                start_text = '<START>'
            else:
                start_color = medium_green
                start_text = 'START'

            start_button = pygame.draw.rect(DISPLAYSURF, start_color,
                                            (window_width_half - button_center[0],
                                             start_top_coordinate,
                                             button_size[0],
                                             button_size[1]))

            text_surface, text_rect = self.__text_object(start_text, small_text)
            text_rect.center = (start_button.centerx, start_button.centery)
            DISPLAYSURF.blit(text_surface, text_rect)

            # FIXME: "Exit" word shifts slightly when selected
            if selected == 1:
                exit_color = bright_red
                exit_text = '<EXIT>'
            else:
                exit_color = red
                exit_text = 'EXIT'

            exit_button = pygame.draw.rect(DISPLAYSURF, exit_color,
                                           (window_width_half - button_center[0],
                                            exit_top_coordinate,
                                            button_size[0],
                                            button_size[1]))

            text_surface, text_rect = self.__text_object(exit_text, small_text)
            text_rect.center = (exit_button.centerx, exit_button.centery)
            DISPLAYSURF.blit(text_surface, text_rect)

            pygame.display.update()
            FPSCLOCK.tick()

    def __text_object(self, text, font):
        text_surface = font.render(text, True, black)
        return text_surface, text_surface.get_rect()

    def __terminate(self):
        pygame.quit()
        sys.exit()


class CreateTeam(object):
    """
    Creates the player team
    """

    def __init__(self, master_list, image_dict):
        self.image_dict = image_dict
        self.master_list = master_list
        self.class_list = SubListManager(master_list.get_list('Class'))
        self.equipment_list = SubListManager(master_list.get_list('Equipment'))
        self.starting_equipment = SubListManager(master_list.get_list('Starting Equipment'))
        self.card_library = SubListManager(master_list.get_list('Card'))
        self.starting_deck = SubListManager(master_list.get_list('Starting Deck'))
        self.column_selected = 0
        self.class_selected = 0
        self.player_selected = 0
        self.next_player = 0
        self.player_reset = False
        self.reset_number = -1
        self.number_of_options = 1
        self.option_selected = 0
        self.max_classes_displayed = None
        self.top_displayed = 0
        self.team_size = 0
        self.player_list = []
        self.available_list = []
        self.player_team = None

    def start(self, DISPLAYSURF, fps_clock):
        available_classes = self.class_list.get_list()

        for i in available_classes:
            self.available_list.append(i['ID'])

        for i in range(max_team_size):
            player_dict = dict(name='Player ' + str(i + 1), number=i + 1, ID=None)
            self.player_list.append(player_dict)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.__terminate()
                elif event.type == KEYDOWN:
                    if self.column_selected == 0:
                        self.__cycle_classes(event)
                    elif self.column_selected == 1:
                        self.__cycle_players(event)
                    elif self.column_selected == 2:
                        self.__cycle_options(event, DISPLAYSURF, fps_clock)

            self.__draw_screen(DISPLAYSURF)

            pygame.display.update()
            fps_clock.tick()

    def __draw_screen(self, DISPLAYSURF):
        pygame.font.init()
        small_text = pygame.font.Font(default_font, 20)

        title = 'Player Team Creation'
        title_font = pygame.font.Font(default_font, 30)

        titleSurf = title_font.render(title, True, black)
        titleRect = titleSurf.get_rect()
        topCoord = 30
        titleRect.top = topCoord
        titleRect.centerx = window_width_half
        topCoord += titleRect.height + 20

        DISPLAYSURF.fill(bg_color)
        DISPLAYSURF.blit(titleSurf, titleRect)

        class_top_coordinate = topCoord
        player_top_coordinate = topCoord
        option_top_coordinate = topCoord

        class_button_size = button_size
        class_button_center = (class_button_size[0] / 2, class_button_size[1] / 2)

        player_button_size = (button_size[0], button_size[1] + 20)
        player_button_center = (player_button_size[0] / 2, player_button_size[1] / 2)

        option_button_size = button_size
        option_button_center = (option_button_size[0] / 2, option_button_size[1] / 2)

        quarter_width = int(window_width_half / 2)

        if self.max_classes_displayed is None:
            v = window_height - topCoord
            s = class_button_size[1] + 10
            self.max_classes_displayed = int(v / s)

        # Available Classes
        if self.max_classes_displayed <= len(self.available_list):
            bottom = self.max_classes_displayed
        else:
            bottom = len(self.available_list)

        if self.top_displayed + bottom > len(self.available_list):
            self.top_displayed -= 1

        for j in range(self.top_displayed, self.top_displayed + bottom):
            display_string = self.available_list[j]
            if j == self.class_selected and self.column_selected == 0:  # cursor on class
                button_color = orange_red
            elif self.team_size == max_team_size and self.player_reset is False:  # team full
                button_color = grey
            else:  # cursor can be on class
                button_color = dark_orange
            class_button = pygame.draw.rect(DISPLAYSURF, button_color,
                                            (quarter_width - class_button_center[0],
                                             class_top_coordinate,
                                             class_button_size[0],
                                             class_button_size[1]))

            text_surface, text_rect = self.__text_object(display_string, small_text)
            text_rect.center = (quarter_width, class_button.centery)
            DISPLAYSURF.blit(text_surface, text_rect)

            class_top_coordinate += class_button_size[1] + 10

        # class_top_coordinate = topCoord

        # Players
        for i in self.player_list:
            player_name = i['name']
            player_class = i['ID']
            if i['number'] - 1 == self.player_selected and self.column_selected == 1:  # cursor on player
                button_color = orange_red
            elif i['number'] - 1 == self.reset_number and self.player_reset:  # player being reset
                button_color = blue
            elif i['number'] - 1 != self.reset_number and self.player_reset:
                button_color = grey
            elif i['number'] - 1 == self.next_player and self.team_size < max_team_size:  # next empty player
                button_color = medium_green
            else:
                button_color = dark_orange  # can have cursor on player
            player_button = pygame.draw.rect(DISPLAYSURF, button_color,
                                             (window_width_half - player_button_center[0],
                                              player_top_coordinate,
                                              player_button_size[0],
                                              player_button_size[1]))

            text_surface, text_rect = self.__text_object(player_name, small_text)
            text_rect.center = (window_width_half, player_button.centery - int(player_button_size[1] / 4))
            DISPLAYSURF.blit(text_surface, text_rect)

            if player_class is None:
                class_string = 'Empty'
            else:
                class_string = player_class
            text_surface, text_rect = self.__text_object(class_string, small_text)
            text_rect.center = (window_width_half, player_button.centery + int(player_button_size[1] / 4))
            DISPLAYSURF.blit(text_surface, text_rect)

            player_top_coordinate += player_button_size[1] + 10

        # player_top_coordinate = topCoord

        # options selection
        option_color = dark_orange
        if self.team_size < max_team_size or self.player_reset:
            option_color = grey
        elif self.column_selected == 2:
            option_color = orange_red
        display_string = 'Encounter -->'
        mission_select = pygame.draw.rect(DISPLAYSURF, option_color,
                                          (3 * quarter_width - option_button_center[0],
                                           option_top_coordinate,
                                           option_button_size[0],
                                           option_button_size[1]))

        text_surface, text_rect = self.__text_object(display_string, small_text)
        text_rect.center = (3 * quarter_width, mission_select.centery)
        DISPLAYSURF.blit(text_surface, text_rect)

    def __cycle_classes(self, event):
        if event.key == K_w or event.key == K_UP:
            if self.class_selected == self.top_displayed + 1:
                if self.class_selected != 0:
                    self.class_selected -= 1
                if self.top_displayed != 0:
                    self.top_displayed -= 1
            else:
                if self.class_selected != 0:
                    self.class_selected -= 1
        elif event.key == K_s or event.key == K_DOWN:
            if self.class_selected < self.top_displayed + self.max_classes_displayed - 2:
                if self.class_selected < len(self.available_list) - 1:
                    self.class_selected += 1
            elif self.class_selected == self.top_displayed + self.max_classes_displayed - 1 and \
                    self.top_displayed + self.max_classes_displayed != len(self.available_list):
                if self.top_displayed + self.max_classes_displayed < len(self.available_list):
                    self.top_displayed += 1
            else:
                if self.class_selected < len(self.available_list) - 1:
                    self.class_selected += 1
                if self.top_displayed + self.max_classes_displayed < len(self.available_list):
                    self.top_displayed += 1

        elif event.key == K_d or event.key == K_RIGHT:
            if self.team_size > 0 and self.player_reset is False:
                self.column_selected = 1

        elif event.key == K_e or event.key == K_RETURN:
            if self.player_reset:
                c = self.available_list.pop(self.class_selected)
                player = self.player_list[self.reset_number]
                player['ID'] = c

                self.player_reset = False
                self.reset_number = -1

                if self.team_size == max_team_size:
                    self.column_selected = 1

            elif self.team_size < max_team_size:
                c = self.available_list.pop(self.class_selected)
                player = self.player_list[self.next_player]
                player['ID'] = c

                if self.next_player < max_team_size:
                    self.next_player += 1

                if self.class_selected > 0:
                    self.class_selected -= 1

                self.team_size += 1

                if self.team_size == max_team_size:
                    self.column_selected = 2

    def __cycle_players(self, event):
        if event.key == K_w or event.key == K_UP:
            if self.player_selected > 0:
                self.player_selected -= 1

        elif event.key == K_s or event.key == K_DOWN:
            if self.player_selected < self.team_size - 1:
                self.player_selected += 1

        elif event.key == K_d or event.key == K_RIGHT:
            if self.team_size == max_team_size and self.player_reset is False:
                self.column_selected = 2
        elif event.key == K_a or event.key == K_LEFT:
            if self.team_size < max_team_size:
                self.column_selected = 0

        # TODO: reselect class for player, take current class and put at top of available class list
        elif event.key == K_e or event.key == K_RETURN:
            self.player_reset = True
            player = self.player_list[self.player_selected]
            self.available_list.insert(0, player['ID'])
            player['ID'] = None
            self.class_selected = 0
            self.column_selected = 0
            self.reset_number = self.player_selected

    def __cycle_options(self, event, DISPLAYSURF, fps_clock):
        if event.key == K_w or event.key == K_UP:
            if self.option_selected > 0:
                self.option_selected -= 1
        elif event.key == K_s or event.key == K_DOWN:
            if self.option_selected < self.number_of_options - 1:
                self.option_selected += 1
        elif event.key == K_a or event.key == K_LEFT:
            self.column_selected = 1
        elif event.key == K_e or event.key == K_RETURN:
            if self.option_selected == 0 and self.player_team is None:
                self.player_team = self.__finalize_team()
                es = EncounterSelect(self.master_list, self.image_dict, self.player_team)
                es.start(DISPLAYSURF, fps_clock)
            # TODO: add team reset option

    def __finalize_team(self):
        self.player_team = []
        pm = PlayerMaker(self.class_list, self.starting_equipment, self.equipment_list,
                         self.starting_deck, self.card_library)
        for p in self.player_list:
            player = pm.create_player(p['name'], p['number'], p['ID'])
            self.player_team.append(player)

        return self.player_team

    def __text_object(self, text, font):
        text_surface = font.render(text, True, black)
        return text_surface, text_surface.get_rect()

    def __terminate(self):
        pygame.quit()
        sys.exit()


class EncounterSelect(object):
    """
    Select difficulty
    Select encounter
    """

    def __init__(self, master_list, image_dict, player_team):
        self.master_list = master_list
        self.image_dict = image_dict
        self.player_team = player_team
        self.enemy_team = None
        self.encounter_list = SubListManager(master_list.get_list('Encounter'))
        self.races = SubListManager(master_list.get_list('Enemy Race'))
        self.roles = SubListManager(master_list.get_list('Enemy Role'))
        self.equipment_list = SubListManager(master_list.get_list('Equipment'))
        self.category_selected = 0
        self.tribe_selected = 0
        self.diff_selected = 0
        self.encounter_selected = 0
        self.number_of_options = 1
        self.option_selected = 0
        self.tribe_list = []
        self.tribe_dict = {}
        self.chosen_encounter = None  # TODO: rename
        self.enemy_team = []
        self.top_displayed = 0
        self.max_displayed = None
        self.displayed_encounters = []
        self.change_displayed = False
        self.preview_encounter = False

    def start(self, DISPLAYSURF, fps_clock):
        self.__parse_encounter_list()

        tribe = self.tribe_dict[self.tribe_list[self.tribe_selected]]
        encounter_dict = tribe[diff_list[self.diff_selected]]
        for key in encounter_dict:
            encounter = encounter_dict[key]
            self.displayed_encounters.append(encounter)

        while True:  # Main loop for the start screen.
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.__terminate()
                elif event.type == KEYDOWN:
                    if self.category_selected == 0:
                        self.__cycle_tribes(event)
                    elif self.category_selected == 1:
                        self.__cycle_encounters(event)
                    elif self.category_selected == 2:
                        self.__cycle_options(event, DISPLAYSURF, fps_clock)

            if self.preview_encounter:
                self.__draw_preview(DISPLAYSURF)
            else:
                self.__draw_screen(DISPLAYSURF)

            pygame.display.update()
            fps_clock.tick()

    def __draw_screen(self, DISPLAYSURF):
        pygame.font.init()
        small_text = pygame.font.Font(default_font, 20)

        title = 'Encounter Selection'
        title_font = pygame.font.Font(default_font, 30)

        titleSurf = title_font.render(title, True, black)
        titleRect = titleSurf.get_rect()
        topCoord = 30
        titleRect.top = topCoord
        titleRect.centerx = window_width_half
        topCoord += titleRect.height + 20

        DISPLAYSURF.fill(bg_color)
        DISPLAYSURF.blit(titleSurf, titleRect)

        # Print Tribe Label
        arrow_box_size = (60, 30)
        arrow_box_center = (int(arrow_box_size[0] / 2), int(arrow_box_size[1] / 2))
        arrow_color = green_yellow

        tribe_button_size = button_size
        tribe_button_center = (int(tribe_button_size[0] / 2), int(tribe_button_size[1] / 2))

        tribe_top = topCoord

        if self.tribe_selected > 0:
            right_arrow = '<--'
            right_box = pygame.draw.rect(DISPLAYSURF, arrow_color,
                                         (window_width_quarter - arrow_box_center[0],
                                          tribe_top,
                                          arrow_box_size[0],
                                          arrow_box_size[1]))

            text_surface, text_rect = self.__text_object(right_arrow, small_text)
            text_rect.center = (right_box.centerx, right_box.centery)
            DISPLAYSURF.blit(text_surface, text_rect)

        tribe_name = self.tribe_list[self.tribe_selected]

        if self.category_selected == 0:  # cursor on tribe
            button_color = selected_color
        else:  # cursor can be on button
            button_color = unselected_color

        tribe_button = pygame.draw.rect(DISPLAYSURF, button_color,
                                        (window_width_half - tribe_button_center[0],
                                         tribe_top,
                                         tribe_button_size[0],
                                         tribe_button_size[1]))

        text_surface, text_rect = self.__text_object(tribe_name, small_text)
        text_rect.center = (tribe_button.centerx, tribe_button.centery)
        DISPLAYSURF.blit(text_surface, text_rect)

        if self.tribe_selected < len(self.tribe_list) - 1:
            left_arrow = '-->'
            left_box = pygame.draw.rect(DISPLAYSURF, arrow_color,
                                        (3 * window_width_quarter - arrow_box_center[0],
                                         tribe_top,
                                         arrow_box_size[0],
                                         arrow_box_size[1]))

            text_surface, text_rect = self.__text_object(left_arrow, small_text)
            text_rect.center = (left_box.centerx, left_box.centery)
            DISPLAYSURF.blit(text_surface, text_rect)

        # Print Difficulty Label
        diff_top = tribe_top + tribe_button_size[1] + 10

        diff_button_size = (button_size[0] - 40, button_size[1])
        diff_button_center = (int(diff_button_size[0] / 2), int(diff_button_size[1] / 2))

        if self.diff_selected > 0:
            right_arrow = '<--'
            right_box = pygame.draw.rect(DISPLAYSURF, arrow_color,
                                         (window_width_quarter - arrow_box_center[0],
                                          diff_top,
                                          arrow_box_size[0],
                                          arrow_box_size[1]))

            text_surface, text_rect = self.__text_object(right_arrow, small_text)
            text_rect.center = (right_box.centerx, right_box.centery)
            DISPLAYSURF.blit(text_surface, text_rect)

        button_color = green_yellow
        diff_box = pygame.draw.rect(DISPLAYSURF, button_color,
                                    (window_width_half - diff_button_center[0],
                                     diff_top,
                                     diff_button_size[0],
                                     diff_button_size[1]))

        text_surface, text_rect = self.__text_object(diff_list[self.diff_selected], small_text)
        text_rect.center = (diff_box.centerx, diff_box.centery)
        DISPLAYSURF.blit(text_surface, text_rect)

        if self.diff_selected < len(diff_list) - 1:
            left_arrow = '-->'
            left_box = pygame.draw.rect(DISPLAYSURF, arrow_color,
                                        (3 * window_width_quarter - arrow_box_center[0],
                                         diff_top,
                                         arrow_box_size[0],
                                         arrow_box_size[1]))

            text_surface, text_rect = self.__text_object(left_arrow, small_text)
            text_rect.center = (left_box.centerx, left_box.centery)
            DISPLAYSURF.blit(text_surface, text_rect)

        # TODO: Print Encounters to screen
        encounter_top = diff_top + diff_button_size[1] + 10

        encounter_box_size = (400, 50)
        encounter_box_center = (int(encounter_box_size[0] / 2), int(encounter_box_size[1] / 2))

        # Update encounter_list
        if self.change_displayed:
            self.displayed_encounters.clear()
            tribe = self.tribe_dict[self.tribe_list[self.tribe_selected]]
            encounter_dict = tribe[diff_list[self.diff_selected]]
            for key in encounter_dict:
                encounter = encounter_dict[key]
                self.displayed_encounters.append(encounter)
            self.change_displayed = False

        # Setup and Update top_displayed and max_displayed
        if self.max_displayed is None:
            v = window_height - encounter_top
            s = encounter_box_size[1] + 10
            self.max_displayed = int(v / s)

        if len(self.displayed_encounters) > 0:
            if self.max_displayed <= len(self.displayed_encounters):
                bottom = self.max_displayed
            else:
                bottom = len(self.displayed_encounters)

            if self.top_displayed + bottom > len(self.displayed_encounters):
                self.top_displayed -= 1

            # Print Encounters
            for i in range(self.top_displayed, self.top_displayed + bottom):
                if self.encounter_selected == i and self.category_selected == 1:  # cursor on tribe
                    button_color = orange_red
                # elif self.column_selected != 0:
                #     button_color = grey
                else:  # cursor can be on button
                    button_color = dark_orange

                encounter = self.displayed_encounters[i]
                encounter_text = encounter['Name']
                encounter_box = pygame.draw.rect(DISPLAYSURF, button_color,
                                                 (window_width_half - encounter_box_center[0],
                                                  encounter_top,
                                                  encounter_box_size[0],
                                                  encounter_box_size[1]))

                text_surface, text_rect = self.__text_object(encounter_text, small_text)
                text_rect.center = (encounter_box.centerx, encounter_box.centery)
                DISPLAYSURF.blit(text_surface, text_rect)

                encounter_top += encounter_box_size[1] + 10
        else:
            encounter_box = pygame.draw.rect(DISPLAYSURF, grey,
                                             (window_width_half - encounter_box_center[0],
                                              encounter_top,
                                              encounter_box_size[0],
                                              encounter_box_size[1]))

            text_surface, text_rect = self.__text_object('None', small_text)
            text_rect.center = (encounter_box.centerx, encounter_box.centery)
            DISPLAYSURF.blit(text_surface, text_rect)

    def __draw_preview(self, DISPLAYSURF):
        pygame.font.init()
        small_text = pygame.font.Font(default_font, 20)

        title = 'Encounter Preview'
        title_font = pygame.font.Font(default_font, 30)

        titleSurf = title_font.render(title, True, black)
        titleRect = titleSurf.get_rect()
        topCoord = 30
        titleRect.top = topCoord
        titleRect.centerx = window_width_half
        topCoord += titleRect.height + 20

        DISPLAYSURF.fill(bg_color)
        DISPLAYSURF.blit(titleSurf, titleRect)

        # Print Encounter Name
        name_box_size = (260, 50)
        name_box_center = (int(name_box_size[0] / 2), int(name_box_size[1] / 2))
        name_box_color = green_yellow

        selected = self.chosen_encounter
        encounter_name = selected['Name']
        encounter_name_box = pygame.draw.rect(DISPLAYSURF, name_box_color,
                                              (window_width_half - name_box_center[0],
                                               topCoord,
                                               name_box_size[0],
                                               name_box_size[1]))

        text_surface, text_rect = self.__text_object(encounter_name, small_text)
        text_rect.center = (encounter_name_box.centerx, encounter_name_box.centery)
        DISPLAYSURF.blit(text_surface, text_rect)

        # Print Back
        back_box_size = (60, 50)
        back_box_center = (int(back_box_size[0] / 2), int(back_box_size[1] / 2))

        if self.option_selected == 0:
            back_box_color = selected_color
        else:
            back_box_color = unselected_color

        back = 'Back'
        back_box = pygame.draw.rect(DISPLAYSURF, back_box_color,
                                    (window_width_quarter - back_box_center[0],
                                     topCoord,
                                     back_box_size[0],
                                     back_box_size[1]))

        text_surface, text_rect = self.__text_object(back, small_text)
        text_rect.center = (back_box.centerx, back_box.centery)
        DISPLAYSURF.blit(text_surface, text_rect)

        # Print Start Battle
        start_box_size = (130, 50)
        start_box_center = (int(start_box_size[0] / 2), int(start_box_size[1] / 2))

        if self.option_selected == 1:
            start_box_color = selected_color
        else:
            start_box_color = unselected_color

        start = 'Start Battle'
        start_box = pygame.draw.rect(DISPLAYSURF, start_box_color,
                                     (3 * window_width_quarter + 20 - start_box_center[0],
                                      topCoord,
                                      start_box_size[0],
                                      start_box_size[1]))

        text_surface, text_rect = self.__text_object(start, small_text)
        text_rect.center = (start_box.centerx, start_box.centery)
        DISPLAYSURF.blit(text_surface, text_rect)

        topCoord += name_box_size[1] + 20

        # Print Enemies

    def __cycle_tribes(self, event):
        if event.key == K_d or event.key == K_RIGHT:
            if self.tribe_selected < len(self.tribe_dict) - 1:
                self.tribe_selected += 1
                self.change_displayed = True

        elif event.key == K_a or event.key == K_LEFT:

            if self.tribe_selected > 0:
                self.tribe_selected -= 1
                self.change_displayed = True

        elif event.key == K_e or event.key == K_RETURN:
            self.category_selected = 1

    def __cycle_encounters(self, event):
        # Cycle Encounters
        if event.key == K_d or event.key == K_RIGHT:
            if self.diff_selected < len(diff_list) - 1:
                self.diff_selected += 1
                self.change_displayed = True

        elif event.key == K_a or event.key == K_LEFT:
            if self.diff_selected > 0:
                self.diff_selected -= 1
                self.change_displayed = True

        elif event.key == K_q or event.key == K_BACKSPACE:
            self.category_selected = 0

        # Cycle Encounters
        elif event.key == K_w or event.key == K_UP:
            if self.encounter_selected == self.top_displayed + 1:
                if self.encounter_selected != 0:
                    self.encounter_selected -= 1
                if self.top_displayed != 0:
                    self.top_displayed -= 1
            else:
                if self.encounter_selected != 0:
                    self.encounter_selected -= 1
        elif event.key == K_s or event.key == K_DOWN:
            if self.encounter_selected < self.top_displayed + self.max_displayed - 2:
                if self.encounter_selected < len(self.displayed_encounters) - 1:
                    self.encounter_selected += 1
            elif self.encounter_selected == self.top_displayed + self.max_displayed - 1 and \
                    self.top_displayed + self.max_displayed != len(self.displayed_encounters):
                if self.top_displayed + self.max_displayed < len(self.displayed_encounters):
                    self.top_displayed += 1
            else:
                if self.encounter_selected < len(self.displayed_encounters) - 1:
                    self.encounter_selected += 1
                if self.top_displayed + self.max_displayed < len(self.displayed_encounters):
                    self.top_displayed += 1

        elif event.key == K_e or event.key == K_RETURN:
            self.chosen_encounter = self.displayed_encounters[self.encounter_selected]
            self.category_selected = 2
            self.preview_encounter = True

    def __cycle_options(self, event, DISPLAYSURF, fps_clock):
        if event.key == K_d or event.key == K_RIGHT:
            self.option_selected = 1
        elif event.key == K_a or event.key == K_LEFT:
            self.option_selected = 0

        elif event.key == K_e or event.key == K_RETURN:
            if self.option_selected == 0:  # Reset Encounter
                self.chosen_encounter = None
                self.category_selected = 1
                self.preview_encounter = False
            elif self.option_selected == 1:  # Start Battle
                self.__finalize_encounter()
                bi = BattleSimulation(self.master_list, self.image_dict, self.player_team, self.enemy_team)
                bi.start(DISPLAYSURF, fps_clock)

    def __finalize_encounter(self):
        hm = HordeMaker(self.races, self.roles, self.equipment_list, len(self.player_team))
        self.enemy_team = hm.create_enemy_team(self.chosen_encounter)

    def __parse_encounter_list(self):
        e_l = self.encounter_list.get_list()
        for i in range(len(e_l)):
            encounter = e_l[i]
            t = encounter['Tribe']
            d = encounter['Difficulty']
            ID = encounter['ID']

            if t in self.tribe_dict:
                v = self.tribe_dict[t]  # get named tribe
                diff = v[d]  # get listed difficulty
                diff[ID] = encounter
            else:
                self.tribe_list.append(t)
                self.tribe_dict[t] = self.__make_diff_dict()
                tribe = self.tribe_dict[t]
                diff = tribe[d]
                diff[ID] = encounter

    def __make_diff_dict(self):
        diff_dict = {}
        for i in diff_list:
            diff_dict[i] = {}
        return diff_dict

    def __text_object(self, text, font):
        text_surface = font.render(text, True, black)
        return text_surface, text_surface.get_rect()

    def __terminate(self):
        pygame.quit()
        sys.exit()


class BattleSimulation(object):
    """
    Create map, size based on player team size
    auto-place enemy team
    players select starting position
    go to run_battle()
    """

    def __init__(self, master_list, image_dict, player_team, enemy_team):
        self.master_list = master_list
        self.image_dict = image_dict
        self.terrain_list = SubListManager(master_list.get_list('Terrain'))
        self.player_team = player_team
        self.enemy_team = enemy_team
        self.initiate = True
        self.battle_map = MapInator(self.terrain_list)
        self.map_size = self.battle_map.map_size
        self.map_display_size = (self.map_size[0] * tile_size[0], self.map_size[1] * tile_size[1])
        self.MAX_CAM_PAN = (abs(window_width_half - int(self.map_display_size[0] / 2)) + tile_size[0],
                            abs(window_width_half - int(self.map_display_size[1] / 2)) + tile_size[1])
        self.redraw_map = True
        self.camera_moving = False
        self.camera_offset_x = 0
        self.camera_offset_y = 0
        self.camera_up = False
        self.camera_down = False
        self.camera_left = False
        self.camera_right = False

    def start(self, DISPLAYSURF, fps_clock):
        movement = Movement(self.battle_map)
        movement.place_enemy_team_random(self.enemy_team)

        while True:  # Main loop for the start screen.
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.__terminate()
                elif event.type == KEYDOWN:
                    self.__camera_start_move(event)
                    self.redraw_map = True
                elif event.type == KEYUP:
                    self.__camera_stop(event)

            if self.redraw_map or self.camera_moving:
                mapSurf = self.__drawMap(DISPLAYSURF, self.battle_map)
                self.redraw_map = False

            self.__camera_move()

            mapSurfRect = mapSurf.get_rect()
            mapSurfRect.center = (window_width_half + self.camera_offset_x,
                                  window_height_half + self.camera_offset_y)

            DISPLAYSURF.blit(mapSurf, mapSurfRect)

            pygame.display.update()
            fps_clock.tick(fps)

    def run_battle(self, DISPLAYSURF, fps_clock, battle_map):  # TODO: Remove
        pass
        # while True:
        #     cursor_move = None
        #     key_pressed = False
        #
        #     for event in pygame.event.get():
        #         if event.type == QUIT:
        #             self.__terminate()
        #         elif event.type == KEYDOWN:
        #             # Handle key presses
        #             keyPressed = True
        #             # if event.key == K_w:
        #             #     playerMoveTo = UP
        #             # elif event.key == K_s:
        #             #     playerMoveTo = DOWN
        #             # elif event.key == K_a:
        #             #     playerMoveTo = LEFT
        #             # elif event.key == K_d:
        #             #     playerMoveTo = RIGHT
        #
        #             if event.key == K_q:
        #                 pass  # Cancel
        #             elif event.key == K_e:
        #                 pass  # Select
        #

        #
        #             elif event.key == K_ESCAPE:
        #                 pass  # Menu, implement later

    def __camera_start_move(self, event):
        self.camera_moving = True

        if event.key == K_UP:
            self.camera_up = True
        elif event.key == K_DOWN:
            self.camera_down = True
        elif event.key == K_LEFT:
            self.camera_left = True
        elif event.key == K_RIGHT:
            self.camera_right = True
        elif event.key == K_z:
            self.camera_offset_x = 0
            self.camera_offset_y = 0

    def __camera_move(self):
        if self.camera_up and self.camera_offset_y < self.MAX_CAM_PAN[0]:
            self.camera_offset_y += cam_move_speed
        elif self.camera_down and self.camera_offset_y > -self.MAX_CAM_PAN[0]:
            self.camera_offset_y -= cam_move_speed

        if self.camera_left and self.camera_offset_x < self.MAX_CAM_PAN[1]:
            self.camera_offset_x += cam_move_speed
        elif self.camera_right and self.camera_offset_x > -self.MAX_CAM_PAN[1]:
            self.camera_offset_x -= cam_move_speed

    def __camera_stop(self, event):
        self.camera_moving = True

        if event.key == K_UP:
            self.camera_up = False
        elif event.key == K_DOWN:
            self.camera_down = False
        elif event.key == K_LEFT:
            self.camera_left = False
        elif event.key == K_RIGHT:
            self.camera_right = False

    def __drawMap(self, DISPLAYSURF, battle_map):
        """
        Draws the map based on the tiles and their contents.
        """

        DISPLAYSURF.fill(bg_color)

        map_size = battle_map.map_size
        mapSurfWidth = map_size[0] * tile_size[0]
        mapSurfHeight = map_size[1] * tile_size[1]
        mapSurf = pygame.Surface((mapSurfWidth, mapSurfHeight))
        mapSurf.fill(bg_color)

        # Draw the tile sprites onto this surface.
        for x in range(map_size[0]):
            for y in range(map_size[1]):  #
                y_invert = map_size[1] - 1 - y
                spaceRect = pygame.Rect((x * tile_size[0], y_invert * tile_size[1],
                                         tile_size[0], tile_size[1]))
                tile = battle_map.get_tile(x, y)
                unit = tile.unit
                terrain_type = tile.get_terrain_type()
                baseTile = self.image_dict[terrain_type]

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

                # TODO: draw units on tiles
                if unit is not None:
                    if unit != 'Invalid':
                        if isinstance(unit, Player):
                            mapSurf.blit(self.image_dict['player_token'], spaceRect)
                        elif isinstance(unit, Enemy):
                            mapSurf.blit(self.image_dict['enemy_token'], spaceRect)
                        text_surface, text_rect = self.__text_object(unit.Icon, icon_text)
                        text_rect.center = (spaceRect.centerx, spaceRect.centery)
                        mapSurf.blit(text_surface, text_rect)

        return mapSurf

    def __text_object(self, text, font):
        text_surface = font.render(text, True, black)
        return text_surface, text_surface.get_rect()

    def __terminate(self):
        pygame.quit()
        sys.exit()
