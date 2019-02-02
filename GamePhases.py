"""
Module for all of the primary phases of the game
Reward and Hub Town phases to be added later on
"""
# from ObserveEvents import Observable


class BattlePhase(object):
    """
    Creates the Battle Map, populates it with enemies then players, then starts the battle
    """
    def __init__(self, player_phase, enemy_phase):
        self.player_phase = player_phase
        self.enemy_phase = enemy_phase
        # Observable Class initiator

    def loop(self):  # optimize?
        global keep_playing
        keep_playing = True
        global i  # turn counter
        i = 1
        while keep_playing:
            print('\n' + 'Turn', i, '\n' + 'Player Phase')
            keep_playing = self.player_phase.player_turn_loop()
            if keep_playing is False:
                break

            print('\n' + 'Turn', i, '\n' + 'Enemy Phase')
            self.enemy_phase.enemy_turn_loop()

            i += 1
