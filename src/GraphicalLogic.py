import sys
import pygame
from pygame.locals import *
from src.ReadGameData import SubListManager
from src.CONSTANTS import CONSTANTS
from src.TeamPhases import PlayerMaker

max_team_size = CONSTANTS.MAX_PLAYERS
diff_list = CONSTANTS.DIFFICULTY_LIST

default_font = CONSTANTS.FONT_DICT['sans_bold']
black = CONSTANTS.COLORS['black']
orange_red = CONSTANTS.COLORS['orange_red']
dark_orange = CONSTANTS.COLORS['dark_orange']
green_yellow = CONSTANTS.COLORS['green_yellow']
medium_green = CONSTANTS.COLORS['medium_green']
grey = CONSTANTS.COLORS['grey']
blue = CONSTANTS.COLORS['blue']

window_width = CONSTANTS.WINWIDTH
window_width_half = CONSTANTS.HALF_WINWIDTH
window_width_quarter = int(window_width_half / 2)
window_height = CONSTANTS.WINHEIGHT
button_size = CONSTANTS.STANDARD_BUTTON_SIZE


# TODO: move start screen to here

# TODO: move menu to here


class CreateTeam(object):
    """
    Creates the player team
    """

    def __init__(self, master_list):
        self.master_list = master_list
        self.terrain_list = SubListManager(master_list.get_list('Terrain'))
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

    def start(self, DISPLAYSURF, bg_color, HALF_WINWIDTH, fps_clock):
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
                        self.__cycle_options(event, DISPLAYSURF, bg_color, HALF_WINWIDTH, fps_clock)

            self.__draw_screen(DISPLAYSURF, bg_color, HALF_WINWIDTH)

            pygame.display.update()
            fps_clock.tick()

    def __draw_screen(self, DISPLAYSURF, bg_color, HALF_WINWIDTH):
        pygame.font.init()
        small_text = pygame.font.Font(default_font, 20)

        title = 'Player Team Creation'
        title_font = pygame.font.Font(default_font, 30)

        titleSurf = title_font.render(title, True, black)
        titleRect = titleSurf.get_rect()
        topCoord = 30
        titleRect.top = topCoord
        titleRect.centerx = HALF_WINWIDTH
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

        quarter_width = int(HALF_WINWIDTH / 2)

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
                                             (HALF_WINWIDTH - player_button_center[0],
                                              player_top_coordinate,
                                              player_button_size[0],
                                              player_button_size[1]))

            text_surface, text_rect = self.__text_object(player_name, small_text)
            text_rect.center = (HALF_WINWIDTH, player_button.centery - int(player_button_size[1] / 4))
            DISPLAYSURF.blit(text_surface, text_rect)

            if player_class is None:
                class_string = 'Empty'
            else:
                class_string = player_class
            text_surface, text_rect = self.__text_object(class_string, small_text)
            text_rect.center = (HALF_WINWIDTH, player_button.centery + int(player_button_size[1] / 4))
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
        # Handle key presses
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

    def __cycle_options(self, event, DISPLAYSURF, bg_color, HALF_WINWIDTH, fps_clock):
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
                es = EncounterSelect(self.master_list, self.player_team)
                es.start(DISPLAYSURF, bg_color, HALF_WINWIDTH, fps_clock)
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

    def __init__(self, master_list, player_team):
        self.master_list = master_list
        self.player_team = player_team
        self.enemy_team = None
        self.encounter_list = SubListManager(master_list.get_list('Encounter'))
        self.races = SubListManager(master_list.get_list('Enemy Race'))
        self.roles = SubListManager(master_list.get_list('Enemy Role'))
        self.column_selected = 0
        self.tribe_selected = 0
        self.diff_selected = 0
        self.number_of_options = 1
        self.option_selected = 0
        self.tribe_list = []
        self.tribe_dict = {}
        self.selected_encounter = None
        self.enemy_team = []

    def start(self, DISPLAYSURF, bg_color, HALF_WINWIDTH, fps_clock):
        self.__parse_encounter_list()

        while True:  # Main loop for the start screen.
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.__terminate()
                elif event.type == KEYDOWN:
                    if self.column_selected == 0:
                        self.__cycle_tribes(event)
                    elif self.column_selected == 1:
                        self.__cycle_difficulties(event)
                    elif self.column_selected == 2:
                        self.__cycle_encounters(event)
                    elif self.column_selected == 3:
                        self.__cycle_options(event)

            self.__draw_screen(DISPLAYSURF, bg_color, HALF_WINWIDTH)

            pygame.display.update()
            fps_clock.tick()

    def __draw_screen(self, DISPLAYSURF, bg_color, HALF_WINWIDTH):
        pygame.font.init()
        small_text = pygame.font.Font(default_font, 20)

        title = 'Encounter Selection'
        title_font = pygame.font.Font(default_font, 30)

        titleSurf = title_font.render(title, True, black)
        titleRect = titleSurf.get_rect()
        topCoord = 30
        titleRect.top = topCoord
        titleRect.centerx = HALF_WINWIDTH
        topCoord += titleRect.height + 20

        DISPLAYSURF.fill(bg_color)
        DISPLAYSURF.blit(titleSurf, titleRect)

        window_number = len(self.tribe_dict) + 1

        # Print Tribes
        tribe_division = window_width / window_number

        tribe_button_size = button_size
        tribe_button_center = (int(tribe_button_size[0] / 2), int(tribe_button_size[1] / 2))

        tribe_top = topCoord

        for i in range(len(self.tribe_list)):
            display_string = self.tribe_list[i]
            if i == self.tribe_selected and self.column_selected == 0:  # cursor on tribe
                button_color = orange_red
            # elif self.column_selected != 0:
            #     button_color = grey
            else:  # cursor can be on button
                button_color = dark_orange
            tribe_button = pygame.draw.rect(DISPLAYSURF, button_color,
                                            (tribe_division * (1 + i) - tribe_button_center[0],
                                             tribe_top,
                                             tribe_button_size[0],
                                             tribe_button_size[1]))

            text_surface, text_rect = self.__text_object(display_string, small_text)
            text_rect.center = (tribe_division * (1 + i), tribe_button.centery)
            DISPLAYSURF.blit(text_surface, text_rect)

        # Print Difficulties
        diff_top = tribe_top + tribe_button_size[1] + 10

        diff_button_size = (button_size[0] - 40, button_size[1])
        diff_button_center = (int(diff_button_size[0] / 2), int(diff_button_size[1] / 2))

        arrow_box_size = (60, 30)
        arrow_box_center = (int(arrow_box_size[0] / 2), int(arrow_box_size[1] / 2))
        arrow_color = green_yellow
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
        # encounter_top = diff_top + diff_button_size[1] + 10

        encounter_box_size = (400, 50)
        encounter_box_center = (int(encounter_box_size[0] / 2), int(encounter_box_size[1] / 2))

        # for i in range(len(diff_list)):
        #     diff_button = pygame.draw.rect(DISPLAYSURF, button_color,
        #                                    (diff_division * (1 + i) - diff_button_center[0],
        #                                     diff_top,
        #                                     diff_button_size[0],
        #                                     diff_button_size[1]))
        #
        #     text_surface, text_rect = self.__text_object(diff_list[i], small_text)
        #     text_rect.center = (diff_division * (1 + i), diff_button.centery)
        #     DISPLAYSURF.blit(text_surface, text_rect)




    def __cycle_tribes(self, event):
        if event.key == K_d or event.key == K_RIGHT:
            if self.tribe_selected < len(self.tribe_list) - 1:
                self.tribe_selected += 1

        elif event.key == K_a or event.key == K_LEFT:
            if self.tribe_selected > 0:
                self.tribe_selected -= 1

        elif event.key == K_e or event.key == K_RETURN:
            self.column_selected = 1

    def __cycle_difficulties(self, event):
        if event.key == K_d or event.key == K_RIGHT:
            if self.diff_selected < len(diff_list) - 1:
                self.diff_selected += 1

        elif event.key == K_a or event.key == K_LEFT:
            if self.diff_selected > 0:
                self.diff_selected -= 1

        elif event.key == K_q or event.key == K_BACKSPACE:
            self.column_selected = 0

    def __cycle_encounters(self, event):
        pass

    def __cycle_options(self, event):
        if event.key == K_w or event.key == K_UP:
            if self.option_selected > 0:
                self.option_selected -= 1
        elif event.key == K_s or event.key == K_DOWN:
            if self.option_selected < self.number_of_options - 1:
                self.option_selected += 1
        elif event.key == K_e or event.key == K_RETURN:
            if self.option_selected == 0 and self.selected_encounter is not None:  # Start Battle
                self.__finalize_encounter()
                # bi = BattleInitialization(self.player_team, self.enemy_team)
                # bi.start(DISPLAYSURF, bg_color, HALF_WINWIDTH, fps_clock)
                pass
            elif self.option_selected == 1:  # Reset Encounter
                if self.selected_encounter is not None:
                    self.selected_encounter = None

    def __finalize_encounter(self):
        # TODO: make enemy team
        pass

    def __parse_encounter_list(self):
        e_l = self.encounter_list.get_list()
        for e in e_l:
            t = e['Tribe']
            # TODO: parse difficulty of encounters
            # d = e['Difficulty']
            # if d not in self.difficulty_list:
            #     self.difficulty_list.append(d)
            if t in self.tribe_dict:
                v = self.tribe_dict[t]
                v.append(e)
            else:
                v = []
                v.append(e)
                self.tribe_dict[t] = v
                self.tribe_list.append(t)

    def __text_object(self, text, font):
        text_surface = font.render(text, True, black)
        return text_surface, text_surface.get_rect()

    def __terminate(self):
        pygame.quit()
        sys.exit()


class BattleInitialization(object):
    """
    Create map, size based on player team size
    auto-place enemy team
    players select starting position
    go to run_battle()
    """

    def __init__(self, master_list, player_team, enemy_team):
        self.master_list = master_list
        self.player_team = player_team
        self.enemy_team = enemy_team
        # terrain list

    def start(self, DISPLAYSURF, bg_color, HALF_WINWIDTH, fps_clock):
        while True:  # Main loop for the start screen.
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.__terminate()

            pygame.display.update()
            fps_clock.tick()

    def __terminate(self):
        pygame.quit()
        sys.exit()

# TODO: move BattleEngine to here

# TODO: move DrawMap to here
