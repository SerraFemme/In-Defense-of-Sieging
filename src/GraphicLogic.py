import sys
import pygame
from pygame.locals import *
from src.ReadGameData import SubListManager
from src.CONSTANTS import CONSTANTS
from src.Unit import Enemy, Player
from src.TeamPhases import PlayerMaker, HordeMaker
from src.BattleMap import MapCreator, Movement

pygame.font.init()

max_team_size = CONSTANTS.MAX_PLAYERS
diff_list = CONSTANTS.DIFFICULTY_LIST
direction_dict = CONSTANTS.DIRECTION_DICT

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
light_grey = CONSTANTS.COLORS['light_grey']
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
tile_size = CONSTANTS.TILE_SIZE
cam_move_speed = CONSTANTS.CAM_MOVE_SPEED
fps = CONSTANTS.FPS

standard_button_size = (160, 40)
standard_button_center = (int(standard_button_size[0] / 2), int(standard_button_size[1] / 2))


class Graphics(object):
    def __init__(self, master_list, image_dict, display, fps_clock):
        self.master_list = master_list
        self.image_dict = image_dict
        self.display_surface = display
        self.fps_clock = fps_clock

    # TODO: Make box size dynamically adjust with text length

    def make_title(self):  # TODO: rename, finish
        pass

    def background(self, color_in):  # TODO: finish
        pass

    def box_with_text(self, text, box_color, position, size):
        box = self.draw_box(box_color, position, size)
        self.write_text(text, box)

    def draw_box(self, box_color, position, size):
        return pygame.draw.rect(self.display_surface, box_color,
                                (position[0], position[1], size[0], size[1]))

    def draw_bordered_box(self, box_color, position, size, border_color=black, border_size=1):
        box = self.draw_box(box_color, position, size)
        pygame.draw.rect(self.display_surface, border_color,
                         (position[0], position[1], size[0], size[1]), border_size)
        return box

    def write_text(self, text, box, text_writer=small_text, surface=None):
        text_surface, text_rect = self.__text_object(text, text_writer)
        if isinstance(box, Rect):
            text_rect.center = (box.centerx, box.centery)
        elif isinstance(box, tuple):
            text_rect.center = (box[0], box[1])
        if surface is None:
            self.display_surface.blit(text_surface, text_rect)
        else:
            surface.blit(text_surface, text_rect)

    def write_fraction(self, top_number, bottom_number, position):
        dash_offset = position[0] - 8
        dash_width = 16 + 4 * int(bottom_number / 10)
        dash_box_size = (dash_width, 1)

        top_string = str(top_number)
        bottom_string = str(bottom_number)

        self.write_text(top_string, (position[0], position[1] - 10))

        self.write_text(bottom_string, (position[0], position[1] + 10))

        self.draw_box(black, (dash_offset, position[1] - 2), dash_box_size)

    def __text_object(self, text, font):
        text_surface = font.render(text, True, black)
        return text_surface, text_surface.get_rect()

    def __calculate_box_size(self):
        pass

    def terminate(self):
        pygame.quit()
        sys.exit()


# class ValuedList(object):
#     def __init__(self, given_list):
#         self.value = 0
#         self.item_list = given_list
#
#     def increment(self):
#         self.value += 1
#         if self.value >= len(self.item_list):
#             self.value = 0
#
#     def item(self):
#         return self.item_list[self.value]


class StartScreen(object):
    def __init__(self, graphics):
        self.graphics = graphics

    def start(self):
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

        self.graphics.display_surface.fill(bg_color)  # Start with drawing a blank color to the entire window:
        self.graphics.display_surface.blit(titleSurf, titleRect)  # Draw the title image to the window:

        # Position and draw the text.
        for i in range(len(title_text_info)):
            instSurf = small_text.render(title_text_info[i], 1, dark_orange)
            instRect = instSurf.get_rect()
            topCoord += 10  # 10 pixels will go in between each line of text.
            instRect.top = topCoord
            instRect.centerx = window_width_half
            topCoord += instRect.height  # Adjust for the height of the line.
            self.graphics.display_surface.blit(instSurf, instRect)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.graphics.terminate()
                elif event.type == KEYDOWN:
                    mm = MainMenu(self.graphics)
                    mm.start()

            pygame.display.update()
            self.graphics.fps_clock.tick()


class MainMenu(object):
    def __init__(self, graphics):
        self.graphics = graphics

    def start(self):
        title = 'In Defense of Sieging'
        title_font = pygame.font.Font(default_font, 40)

        titleSurf = title_font.render(title, True, title_color)
        titleRect = titleSurf.get_rect()
        topCoord = 50  # topCoord tracks where to position the top of the text
        titleRect.top = topCoord
        titleRect.centerx = window_width_half
        topCoord += titleRect.height

        self.graphics.display_surface.fill(bg_color)  # Start with drawing a blank color to the entire window:
        self.graphics.display_surface.blit(titleSurf, titleRect)  # Draw the title image to the window:

        button_size = (120, 50)
        button_center = (button_size[0] / 2, button_size[1] / 2)

        start_top_coordinate = topCoord + button_center[1]
        exit_top_coordinate = start_top_coordinate + button_size[1] + 20

        selected = 0

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.graphics.terminate()
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
                            self.graphics.terminate()
                        elif selected == 0:
                            ct = CreateTeam(self.graphics)
                            ct.start()

            # Start Button
            if selected == 0:
                start_color = bright_green
                start_text = '<START>'
            else:
                start_color = medium_green
                start_text = 'START'

            start_button = self.graphics.draw_box(start_color,
                                                  (window_width_half - button_center[0],
                                                   start_top_coordinate),
                                                  button_size)

            self.graphics.write_text(start_text, start_button)

            # FIXME: "Exit" word shifts slightly when selected
            if selected == 1:
                exit_color = bright_red
                exit_text = '<EXIT>'
            else:
                exit_color = red
                exit_text = 'EXIT'

            exit_button = self.graphics.draw_box(exit_color,
                                                 (window_width_half - button_center[0],
                                                  exit_top_coordinate),
                                                 button_size)

            self.graphics.write_text(exit_text, exit_button)

            pygame.display.update()
            self.graphics.fps_clock.tick()


class CreateTeam(object):
    """
    Creates the player team
    """

    def __init__(self, graphics):
        self.graphics = graphics
        self.class_list = SubListManager(graphics.master_list.get_list('Class'))
        self.equipment_list = SubListManager(graphics.master_list.get_list('Equipment'))
        self.starting_equipment = SubListManager(graphics.master_list.get_list('Starting Equipment'))
        self.card_library = SubListManager(graphics.master_list.get_list('Card'))
        self.starting_deck = SubListManager(graphics.master_list.get_list('Starting Deck'))
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

    def start(self):
        available_classes = self.class_list.get_list()

        for i in available_classes:
            self.available_list.append(i['ID'])

        for i in range(max_team_size):
            player_dict = dict(name='Player ' + str(i + 1), number=i + 1, ID=None)
            self.player_list.append(player_dict)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.graphics.terminate()
                elif event.type == KEYDOWN:
                    if self.column_selected == 0:
                        self.__cycle_classes(event)
                    elif self.column_selected == 1:
                        self.__cycle_players(event)
                    elif self.column_selected == 2:
                        self.__cycle_options(event)

            self.__draw_screen()

            pygame.display.update()
            self.graphics.fps_clock.tick()

    def __draw_screen(self):
        pygame.font.init()

        title = 'Player Team Creation'
        title_font = pygame.font.Font(default_font, 30)

        titleSurf = title_font.render(title, True, black)
        titleRect = titleSurf.get_rect()
        topCoord = 30
        titleRect.top = topCoord
        titleRect.centerx = window_width_half
        topCoord += titleRect.height + 20

        self.graphics.display_surface.fill(bg_color)
        self.graphics.display_surface.blit(titleSurf, titleRect)

        class_top_coordinate = topCoord
        player_top_coordinate = topCoord
        option_top_coordinate = topCoord

        class_button_size = standard_button_size
        class_button_center = standard_button_center

        player_button_size = (standard_button_size[0], standard_button_size[1] + 20)
        player_button_center = (int(player_button_size[0] / 2), int(player_button_size[1] / 2))

        option_button_size = standard_button_size
        option_button_center = standard_button_center

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

            class_button = self.graphics.draw_box(button_color,
                                                  (quarter_width - class_button_center[0],
                                                   class_top_coordinate),
                                                  class_button_size)

            self.graphics.write_text(display_string, class_button)

            class_top_coordinate += class_button_size[1] + 10

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

            player_button = self.graphics.draw_box(button_color,
                                                   (window_width_half - player_button_center[0],
                                                    player_top_coordinate),
                                                   player_button_size)

            self.graphics.write_text(player_name,
                                     (window_width_half, player_button.centery - int(player_button_size[1] / 4)))

            if player_class is None:
                class_string = 'Empty'
            else:
                class_string = player_class

            self.graphics.write_text(class_string,
                                     (window_width_half,
                                      player_button.centery + int(player_button_size[1] / 4)))

            player_top_coordinate += player_button_size[1] + 10

        # options selection
        option_color = dark_orange
        if self.team_size < max_team_size or self.player_reset:
            option_color = grey
        elif self.column_selected == 2:
            option_color = orange_red
        display_string = 'Encounter -->'

        mission_select = self.graphics.draw_box(option_color,
                                                (3 * quarter_width - option_button_center[0],
                                                 option_top_coordinate),
                                                option_button_size)

        self.graphics.write_text(display_string, mission_select)

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

        elif event.key == K_e or event.key == K_RETURN:
            self.player_reset = True
            player = self.player_list[self.player_selected]
            self.available_list.insert(0, player['ID'])
            player['ID'] = None
            self.class_selected = 0
            self.column_selected = 0
            self.reset_number = self.player_selected

    def __cycle_options(self, event):
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
                es = EncounterSelect(self.graphics, self.player_team)
                es.start()
            # TODO: add team reset option

    def __finalize_team(self):
        self.player_team = []
        pm = PlayerMaker(self.class_list, self.starting_equipment, self.equipment_list,
                         self.starting_deck, self.card_library)
        for p in self.player_list:
            player = pm.create_player(p['name'], p['number'], p['ID'])
            self.player_team.append(player)

        return self.player_team


class EncounterSelect(object):
    """
    Select difficulty
    Select encounter
    """

    def __init__(self, graphics, player_team):
        self.graphics = graphics
        self.player_team = player_team
        self.enemy_team = None
        self.encounter_list = SubListManager(graphics.master_list.get_list('Encounter'))
        self.races = SubListManager(graphics.master_list.get_list('Enemy Race'))
        self.roles = SubListManager(graphics.master_list.get_list('Enemy Role'))
        self.equipment_list = SubListManager(graphics.master_list.get_list('Equipment'))
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

    def start(self):
        self.__parse_encounter_list()

        tribe = self.tribe_dict[self.tribe_list[self.tribe_selected]]
        encounter_dict = tribe[diff_list[self.diff_selected]]
        for key in encounter_dict:
            encounter = encounter_dict[key]
            self.displayed_encounters.append(encounter)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.graphics.terminate()
                elif event.type == KEYDOWN:
                    if self.category_selected == 0:
                        self.__cycle_tribes(event)
                    elif self.category_selected == 1:
                        self.__cycle_encounters(event)
                    elif self.category_selected == 2:
                        self.__cycle_options(event)

            if self.preview_encounter:
                self.__draw_preview()
            else:
                self.__draw_screen()

            pygame.display.update()
            self.graphics.fps_clock.tick()

    def __draw_screen(self):
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

        self.graphics.display_surface.fill(bg_color)
        self.graphics.display_surface.blit(titleSurf, titleRect)

        # Print Tribe Label
        arrow_box_size = (60, 30)
        arrow_box_center = (int(arrow_box_size[0] / 2), int(arrow_box_size[1] / 2))
        arrow_color = green_yellow

        tribe_button_size = standard_button_size
        tribe_button_center = standard_button_center

        tribe_top = topCoord

        if self.tribe_selected > 0:
            self.__left_arrow(arrow_color,
                              (window_width_quarter - arrow_box_center[0],
                               tribe_top),
                              arrow_box_size)

        tribe_name = self.tribe_list[self.tribe_selected]

        if self.category_selected == 0:  # cursor on tribe
            button_color = selected_color
        else:  # cursor can be on button
            button_color = unselected_color

        self.graphics.box_with_text(tribe_name, button_color,
                                    (window_width_half - tribe_button_center[0],
                                     tribe_top),
                                    tribe_button_size)

        if self.tribe_selected < len(self.tribe_list) - 1:
            self.__right_arrow(arrow_color,
                               (3 * window_width_quarter - arrow_box_center[0],
                                tribe_top),
                               arrow_box_size)

        # Print Difficulty Label
        diff_top = tribe_top + tribe_button_size[1] + 10

        diff_button_size = (standard_button_size[0] - 40, standard_button_size[1])
        diff_button_center = (int(diff_button_size[0] / 2), int(diff_button_size[1] / 2))

        if self.diff_selected > 0:
            self.__left_arrow(arrow_color,
                              (window_width_quarter - arrow_box_center[0],
                               diff_top),
                              arrow_box_size)

        button_color = green_yellow
        self.graphics.box_with_text(diff_list[self.diff_selected], button_color,
                                    (window_width_half - diff_button_center[0],
                                     diff_top),
                                    diff_button_size)

        if self.diff_selected < len(diff_list) - 1:
            self.__right_arrow(arrow_color,
                               (3 * window_width_quarter - arrow_box_center[0],
                                diff_top),
                               arrow_box_size)

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
                self.graphics.box_with_text(encounter_text, button_color,
                                            (window_width_half - encounter_box_center[0],
                                             encounter_top),
                                            encounter_box_size)

                encounter_top += encounter_box_size[1] + 10
        else:
            self.graphics.box_with_text('None', grey,
                                        (window_width_half - encounter_box_center[0],
                                         encounter_top),
                                        encounter_box_size)

    def __draw_preview(self):
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

        self.graphics.display_surface.fill(bg_color)
        self.graphics.display_surface.blit(titleSurf, titleRect)

        # Print Encounter Name
        name_box_size = (260, 50)
        name_box_center = (int(name_box_size[0] / 2), int(name_box_size[1] / 2))
        name_box_color = green_yellow

        selected = self.chosen_encounter
        encounter_name = selected['Name']
        self.graphics.box_with_text(encounter_name, name_box_color,
                                    (window_width_half - name_box_center[0],
                                     topCoord),
                                    name_box_size)

        # Print Back
        back_box_size = (60, 50)
        back_box_center = (int(back_box_size[0] / 2), int(back_box_size[1] / 2))

        if self.option_selected == 0:
            back_box_color = selected_color
        else:
            back_box_color = unselected_color

        back = 'Back'
        self.graphics.box_with_text(back, back_box_color,
                                    (window_width_quarter - back_box_center[0],
                                     topCoord),
                                    back_box_size)

        # Print Start Battle
        start_box_size = (130, 50)
        start_box_center = (int(start_box_size[0] / 2), int(start_box_size[1] / 2))

        if self.option_selected == 1:
            start_box_color = selected_color
        else:
            start_box_color = unselected_color

        start = 'Start Battle'
        self.graphics.box_with_text(start, start_box_color,
                                    (3 * window_width_quarter + 20 - start_box_center[0],
                                     topCoord),
                                    start_box_size)

        topCoord += name_box_size[1] + 20

        # Print Enemies

    def __left_arrow(self, arrow_color, position, size):
        left_arrow = '<--'
        self.graphics.box_with_text(left_arrow, arrow_color, position, size)

    def __right_arrow(self, arrow_color, position, size):
        right_arrow = '-->'
        self.graphics.box_with_text(right_arrow, arrow_color, position, size)

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

        elif event.key == K_e or event.key == K_RETURN:  # FIXME: breaks when chosen encounter is None?
            self.chosen_encounter = self.displayed_encounters[self.encounter_selected]
            self.category_selected = 2
            self.preview_encounter = True

    def __cycle_options(self, event):
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
                bi = BattleSimulation(self.graphics, self.player_team, self.enemy_team)
                bi.start()

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


class BattleSimulation(object):  # TODO: strip out game logic and leave only graphical logic
    """
    Create map, size based on player team size
    auto-place enemy team
    players select starting position
    go to run_battle()
    """

    def __init__(self, graphics, player_team, enemy_team):
        self.graphics = graphics
        self.image_dict = graphics.image_dict
        self.terrain_list = SubListManager(graphics.master_list.get_list('Terrain'))
        self.player_team = player_team
        self.enemy_team = enemy_team
        self.battle_map = MapCreator(self.terrain_list)
        self.map_size = self.battle_map.map_size
        self.movement = None
        self.map_display_size = (self.map_size[0] * tile_size[0], self.map_size[1] * tile_size[1])
        self.redraw_map = True

        # TODO: Adjust MAX_CAM_PAN, take into account the info boxes
        self.MAX_CAM_PAN = (abs(window_width_half - int(self.map_display_size[0] / 2)) + tile_size[0],
                            abs(window_width_half - int(self.map_display_size[1] / 2)) + tile_size[1])
        self.camera_moving = False
        self.camera_offset_x = 0
        self.camera_offset_y = 0
        self.camera_up = False
        self.camera_down = False
        self.camera_left = False
        self.camera_right = False

        self.initiate = True
        self.tile_selected = None
        self.adjacent_tiles = None  # TODO: Delete, being moved to BattleMap.Tile

        self.turn_counter = 1

        self.active_team = 0
        self.team_turn = ['Player Team',
                          'Enemy Team']

        self.active_player_number = 0
        self.active_player = None
        self.player_mode = 0
        self.mode_list = ['Cursor',
                          'Movement',
                          'Action']

        self.active_enemy_number = 0
        self.active_enemy = None
        self.enemy_mode = 0
        self.enemy_mode_list = ['Movement',
                                'Action']

        self.option_selected = 0
        self.option_list = ['Hand',
                            'Passive',
                            'Enchantments',  # TODO: rename
                            'Player Info',
                            'End Turn']

    def start(self):
        if self.movement is None:
            self.movement = Movement(self.battle_map)
            self.movement.place_enemy_team_random(self.enemy_team)

        if self.tile_selected is None:
            x = int(self.map_size[0] / 2)
            y = int(self.battle_map.starting_range / 2)
            self.tile_selected = (x, y)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.graphics.terminate()
                elif event.type == KEYDOWN:
                    self.__camera_start_move(event)
                    self.__player_input(event)
                    self.redraw_map = True
                elif event.type == KEYUP:
                    self.__camera_stop(event)

            if self.active_player_number >= len(self.player_team) and self.initiate:  # Start Battle
                self.__next_player_turn()

            if self.redraw_map or self.camera_moving:
                mapSurf = self.__draw_map()
                self.redraw_map = False

            self.__camera_move()

            mapSurfRect = mapSurf.get_rect()
            mapSurfRect.center = (window_width_half + self.camera_offset_x,
                                  window_height_half + self.camera_offset_y)

            self.graphics.display_surface.blit(mapSurf, mapSurfRect)

            self.__draw_title()
            if self.initiate is False and self.active_team == 0:
                if self.player_mode == 2:
                    self.__draw_action_bar()
                else:
                    self.__draw_unit_info()
            elif self.active_team == 1:  # Enemy Turn
                pass

            pygame.display.update()
            self.graphics.fps_clock.tick(fps)

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

    def __player_input(self, event):
        if self.player_mode == 0:  # Cursor
            self.__cursor_mode(event)
        elif self.player_mode == 1:  # Movement
            self.__movement_cursor(event)
        elif self.player_mode == 2:  # Action
            self.__action_mode(event)

    def __cursor_mode(self, event):
        if event.key == K_w:  # Up
            if self.initiate:
                if self.tile_selected[1] < self.battle_map.starting_range:
                    self.tile_selected = (self.tile_selected[0], self.tile_selected[1] + 1)
            elif self.tile_selected[1] < self.map_size[0] - 1:
                self.tile_selected = (self.tile_selected[0], self.tile_selected[1] + 1)
        elif event.key == K_s:  # Down
            if self.tile_selected[1] > 0:
                self.tile_selected = (self.tile_selected[0], self.tile_selected[1] - 1)
        elif event.key == K_d:  # Right
            if self.tile_selected[0] < self.map_size[0] - 1:
                self.tile_selected = (self.tile_selected[0] + 1, self.tile_selected[1])
        elif event.key == K_a:  # Left
            if self.tile_selected[0] > 0:
                self.tile_selected = (self.tile_selected[0] - 1, self.tile_selected[1])
        elif event.key == K_e or event.key == K_RETURN:
            if self.initiate:
                self.__place_player()

        elif event.key == K_SPACE:
            if self.initiate is False:
                self.player_mode = 1
                self.adjacent_tiles = self.__calculate_adjacent_tiles(self.active_player.Position)
                self.tile_selected = self.active_player.Position

    def __movement_cursor(self, event):
        if event.key == K_w and 'up' in self.adjacent_tiles:
            self.tile_selected = self.adjacent_tiles['up']
        elif event.key == K_s and 'down' in self.adjacent_tiles:
            self.tile_selected = self.adjacent_tiles['down']
        elif event.key == K_d and 'right' in self.adjacent_tiles:
            self.tile_selected = self.adjacent_tiles['right']
        elif event.key == K_a and 'left' in self.adjacent_tiles:
            self.tile_selected = self.adjacent_tiles['left']
        elif event.key == K_e or event.key == K_RETURN:
            self.movement.move_unit(self.active_player, self.tile_selected)
            self.adjacent_tiles = self.__calculate_adjacent_tiles(self.active_player.Position)
        elif event.key == K_SPACE:
            self.player_mode = 2

    def __action_mode(self, event):
        if event.key == K_w:  # Up
            if self.option_selected > 0:
                self.option_selected -= 1
            else:
                self.option_selected = len(self.option_list) - 1
        elif event.key == K_s:  # Down
            if self.option_selected < len(self.option_list) - 1:
                self.option_selected += 1
            else:
                self.option_selected = 0
        elif event.key == K_d:  # Right
            if self.option_selected == 0:
                pass  # TODO: cycle card selected
            elif self.option_selected == 1:
                pass  # TODO: cycle passive button selected
            elif self.option_selected == 2:
                pass  # TODO: cycle enchantments
            elif self.option_selected == 3:
                pass  # TODO: cycle info tab
        elif event.key == K_a:  # Left
            if self.option_selected == 0:
                pass  # TODO: cycle card selected
            elif self.option_selected == 1:
                pass  # TODO: cycle passive button selected
            elif self.option_selected == 2:
                pass  # TODO: cycle enchantments
            elif self.option_selected == 3:
                pass  # TODO: cycle info tab

        elif event.key == K_e or event.key == K_RETURN:
            if self.option_selected == 0:
                pass  # TODO: use selected card
            elif self.option_selected == 1:
                pass  # TODO: use selected passive button
            elif self.option_selected == 2:
                pass  # TODO: use selected enchantment enchantments
            elif self.option_selected == 3:
                pass  # TODO: info tab action?
            elif self.option_selected == 4:  # Pass Turn
                self.__next_player_turn()

        elif event.key == K_SPACE:
            self.player_mode = 0

    def __draw_map(self):
        """
        Draws the map based on the tiles and their contents.
        """

        self.graphics.display_surface.fill(bg_color)

        mapSurfWidth = self.map_size[0] * tile_size[0]
        mapSurfHeight = self.map_size[1] * tile_size[1]
        mapSurf = pygame.Surface((mapSurfWidth, mapSurfHeight))
        mapSurf.fill(bg_color)

        for x in range(self.map_size[0]):
            for y in range(self.map_size[1]):
                y_invert = self.map_size[1] - 1 - y
                spaceRect = pygame.Rect((x * tile_size[0], y_invert * tile_size[1],
                                         tile_size[0], tile_size[1]))
                tile = self.battle_map.get_tile(x, y)
                unit = tile.unit

                terrain_type = tile.get_terrain_type()
                tile_image = self.image_dict[terrain_type]

                mapSurf.blit(tile_image, spaceRect)

                if self.initiate and tile.coordinate[1] <= self.battle_map.starting_range:
                    if unit is None:  # Tile Empty
                        mapSurf.blit(self.image_dict['valid_move_tile'], spaceRect)
                    else:  # Tile Occupied
                        mapSurf.blit(self.image_dict['invalid_move_tile'], spaceRect)
                elif self.player_mode == 1:  # Movement Mode
                    for i in self.adjacent_tiles:
                        if tile.coordinate == self.adjacent_tiles[i]:
                            if tile.get_terrain_movement_cost() is not None:
                                # if tile.get_terrain_movement_cost() > self.active_player.Stamina.points:
                                if self.active_player.Stamina.can_spend(tile.get_terrain_movement_cost()) is False:
                                    mapSurf.blit(self.image_dict['insuf_stam_tile'], spaceRect)
                                elif unit is None:  # Tile Empty
                                    mapSurf.blit(self.image_dict['valid_move_tile'], spaceRect)
                                else:  # Tile Occupied
                                    mapSurf.blit(self.image_dict['invalid_move_tile'], spaceRect)
                            else:  # Tile Occupied
                                mapSurf.blit(self.image_dict['invalid_move_tile'], spaceRect)

                if self.tile_selected is not None and self.player_mode != 2:
                    if self.tile_selected[0] == x and self.tile_selected[1] == y:
                        mapSurf.blit(self.image_dict['cursor'], spaceRect)

                if unit is not None:
                    if unit != 'Invalid':
                        text = icon_text
                        if isinstance(unit, Player):
                            mapSurf.blit(self.image_dict['player_token'], spaceRect)
                            text = small_text
                            if self.initiate is False and unit.Player_Number == self.active_player_number + 1:
                                mapSurf.blit(self.image_dict['active_player'], spaceRect)

                        elif isinstance(unit, Enemy):
                            mapSurf.blit(self.image_dict['enemy_token'], spaceRect)
                        self.graphics.write_text(unit.Icon, spaceRect, text, mapSurf)

        return mapSurf

    def __draw_title(self):
        topCoord = 0
        box_color = green_yellow
        boxes = None
        team = self.team_turn[self.active_team]
        if self.active_team == 0:
            player = self.player_team[self.active_player_number]
        elif self.active_team == 1:
            enemy = self.enemy_team[self.active_enemy_number]
        if self.initiate:
            boxes = [{'text': 'Select Starting Position',
                      'size': (260, 30)},
                     {'text': player.Player_Name + ': ' + player.Class_Name,
                      'size': (180, 30)}]
        elif self.active_team == 0:  # Player Team Turn
            if self.player_mode == 0:  # Cursor
                boxes = [{'text': 'Mode: Cursor',
                          'size': (144, 30)}]
            elif self.player_mode == 1:  # Movement
                boxes = [{'text': 'Mode: Movement',
                          'size': (180, 30)}]
            elif self.player_mode == 2:  # Action Mode
                boxes = [{'text': 'Mode: Action',
                          'size': (150, 30)}]
            boxes.insert(0, {'text': player.Player_Name + ': ' + player.Class_Name,
                             'size': (180, 30)})
            boxes.insert(0, {'text': team + ': Turn ' + str(self.turn_counter),
                             'size': (230, 30)})

        elif self.active_team == 1:  # Enemy Team Turn
            boxes = [{'text': team + ': Turn ' + str(self.turn_counter),
                      'size': (230, 30)},
                     {'text': enemy.get_name(),
                      'size': (200, 30)}]

        for box in boxes:
            text = box['text']
            size = box['size']

            box_one_center = (int(size[0] / 2), int(size[1] / 2))
            self.graphics.box_with_text(text, box_color,
                                        (window_width_half - box_one_center[0],
                                         topCoord),
                                        size)

            topCoord += size[1] + 5

    def __draw_unit_info(self, top_coordinate=None):  # TODO: Clean Up
        info_box_height = 50
        if top_coordinate is None:
            top_coordinate = window_height - info_box_height
        else:
            top_coordinate -= info_box_height
        info_box_color = light_grey
        info_box_size = (window_width, info_box_height)
        info_box_center = (int(info_box_size[0] / 2), int(info_box_size[1] / 2))

        info_box = self.graphics.draw_bordered_box(info_box_color,
                                                   (window_width_half - info_box_center[0],
                                                    top_coordinate),
                                                   info_box_size)

        # TODO: make values dynamic based on text length
        health_x = 50
        health_value_x = health_x + 60
        stamina_x = health_value_x + 76
        stamina_fraction_x = stamina_x + 56
        weapon_x = stamina_fraction_x + 110
        weapon_value_x = weapon_x + 100
        range_x = weapon_value_x + 90
        range_value_x = range_x + 85
        armor_x = range_value_x + 60
        armor_value_x = armor_x + 50
        cards_x = armor_value_x + 60
        cards_value_x = cards_x + 60

        # Health
        text = 'Health:'
        self.graphics.write_text(text, (health_x, info_box.centery))

        text = 'N/A'
        self.graphics.write_text(text, (health_value_x, info_box.centery))

        # Stamina
        text = 'Stamina:'
        self.graphics.write_text(text, (stamina_x, info_box.centery))

        top_number = self.active_player.Stamina.points
        bottom_number = self.active_player.Stamina.get_pool_size()
        self.graphics.write_fraction(top_number, bottom_number, (stamina_fraction_x, info_box.centery))

        # Weapon Damage
        text = 'Weapon Damage:'
        self.graphics.write_text(text, (weapon_x, info_box.centery))

        damage_number = self.active_player.Weapon_Damage.value
        self.graphics.write_text(str(damage_number), (weapon_value_x, info_box.centery))

        # Bonus Range
        text = 'Bonus Range:'
        self.graphics.write_text(text, (range_x, info_box.centery))

        range_number = self.active_player.Bonus_Range.value
        self.graphics.write_text(str(range_number), (range_value_x, info_box.centery))

        # Armor
        text = 'Armor:'
        self.graphics.write_text(text, (armor_x, info_box.centery))

        armor_number = self.active_player.Armor.value
        self.graphics.write_text(str(armor_number), (armor_value_x, info_box.centery))

        if self.active_team == 0:
            # Number of Cards in Hand
            text = 'Cards:'
            self.graphics.write_text(text, (cards_x, info_box.centery))

            cards_number = 'N/A'  # TODO: get hand size
            self.graphics.write_text(cards_number, (cards_value_x, info_box.centery))

    def __draw_action_bar(self):
        action_bar_height = 150
        top_coordinate = window_height - action_bar_height
        action_bar_color = light_grey
        action_bar_size = (window_width, action_bar_height)
        action_bar_center = (int(action_bar_size[0] / 2), int(action_bar_size[1] / 2))

        self.graphics.draw_bordered_box(action_bar_color,
                                        (window_width_half - action_bar_center[0],
                                         top_coordinate),
                                        action_bar_size)

        if self.option_selected != 3:  # If not player info selected
            self.__draw_unit_info(top_coordinate)

        option_box_size = (160, 30)
        option_box_center = (int(option_box_size[0] / 2), int(option_box_size[1] / 2))
        option_coordinate = top_coordinate
        for option in self.option_list:
            if option == self.option_list[self.option_selected]:
                action_color = selected_color
            else:
                action_color = unselected_color
            action_box = self.graphics.draw_bordered_box(action_color, (0, option_coordinate), option_box_size)
            self.graphics.write_text(option, action_box)
            option_coordinate += option_box_size[1]

        if self.option_selected == 0:  # TODO: print cards to screen when hand selected
            self.__draw_hand()

        elif self.option_selected == 1:  # TODO: print passive to screen
            self.__draw_passive()

        elif self.option_selected == 2:  # TODO: print enchantments when selected
            self.__draw_enchantment()

        elif self.option_selected == 3:  # TODO: print info tabs and info when selected
            self.__draw_information_tabs()

        elif self.option_selected == 4:  # TODO: print "end of turn" effects
            pass

    def __draw_hand(self):
        # TODO: print cards in hand, make scrollable
        pass

    def __draw_passive(self):
        # TODO: print class passive, either text, bonuses given, and/or buttons
        pass

    def __draw_enchantment(self):
        # TODO: print buffs then debuffs, includes buttons of enchantments
        pass

    def __draw_information_tabs(self):
        # TODO: draw full character info divided into multiple tabs
        pass

    def __draw_tile_info_bar(self):
        # TODO: print tile info

        # TODO: print unit info
        pass

    def __place_player(self):
        if self.active_player_number < len(self.player_team):
            tile = self.battle_map.get_tile(self.tile_selected[0], self.tile_selected[1])
            if tile.unit is None:
                player = self.player_team[self.active_player_number]
                tile.unit = player
                player.Position = self.tile_selected
                self.active_player_number += 1

    def __calculate_adjacent_tiles(self, location):  # TODO: move to BattleMap.Tile
        adjacent_dict = {}
        for i in direction_dict:
            coordinate = direction_dict[i]
            x = location[0] + coordinate[0]
            y = location[1] + coordinate[1]
            if 0 <= x < self.map_size[0] and 0 <= y < self.map_size[1]:
                adjacent_dict[i] = (x, y)

        return adjacent_dict

    def __next_player_turn(self):  # TODO: Clean Up
        if self.initiate:
            if self.active_player_number >= len(self.player_team):
                self.initiate = False
                self.__cycle_players(0)
                self.tile_selected = self.active_player.Position
        else:
            if self.active_player_number == len(self.player_team) - 1:
                self.__cycle_players(0)
                self.active_team = 1
            else:  # Change to Enemy Team
                self.__cycle_players(self.active_player_number + 1)
                player = self.player_team[self.active_player_number]
                self.tile_selected = player.Position
                self.player_mode = 0
                self.option_selected = 0

    def __cycle_players(self, number):
        self.active_player_number = number
        self.active_player = self.player_team[self.active_player_number]
        self.active_player.turn_beginning()

    def __next_enemy_turn(self):
        if self.active_enemy_number == len(self.enemy_team) - 1:  # Change to Player Team
            self.__cycle_enemies(0)
            self.active_team = 0
        else:
            self.__cycle_enemies(self.active_enemy_number + 1)
            enemy = self.enemy_team[self.active_enemy_number]
            self.tile_selected = enemy.Position

    def __cycle_enemies(self, number):
        self.active_enemy_number = number
        self.active_enemy = self.enemy_team[self.active_enemy_number]
        self.active_enemy.turn_beginning()
