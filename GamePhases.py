"""
Module for all of the primary phases of the game
Reward and Hub Town phases to be added later on
"""


class BattlePhase(object):
    """
    Creates the Battle Map, populates it with enemies then players, then starts the battle
    """
    def __init__(self, player_phase):
        self.player_phase = player_phase

    def loop(self):
        global keep_playing
        keep_playing = True
        while keep_playing:
            keep_playing = self.player_phase.player_turn_loop()
            if keep_playing is False:
                break

            print('')
            print('Enemy Turn: N/A')
            print('')
