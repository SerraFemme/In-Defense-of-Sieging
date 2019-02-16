class CONSTANTS(object):
    """
    Contains miscellaneous constants that may be used throughout the program.
    The intention is to have a "catalogue" of variables set up before they're needed.
    """

    MAX_PLAYERS = 4

    COLORS = {'white': (255, 255, 255),
              'black': (0, 0, 0),
              'light_grey': (211, 211, 211),
              'grey': (128, 128, 128),
              'slate_grey': (112, 128, 144),
              'red': (255, 0, 0),
              'dark_red': (160, 0, 0),
              'maroon': (128, 0, 0),
              'dark_orange': (255, 140, 0),
              'orange_red': (255, 69, 0),
              'yellow': (255, 255, 0),
              'green': (0, 255, 0),
              'medium_green': (0, 140, 0),
              'green_yellow': (173, 255, 47),
              'blue': (0, 0, 255),
              'cyan': (0, 255, 255),
              'pale_turquoise': (175, 238, 238),
              'turquoise': (64, 224, 208),
              'teal': (0, 128, 128),
              'magenta': (255, 0, 255),
              'purple': (128, 0, 128),
              'indigo': (75, 0, 130),
              'hot_pink': (255, 20, 147),
              'deep_pink': (255, 20, 147),
              'tan': (210, 180, 140),
              'golden_rod': (218, 165, 32),
              'saddle_brown': (139, 69, 19)}

    FONT_DICT = {'sans_bold': 'freesansbold.ttf'}
