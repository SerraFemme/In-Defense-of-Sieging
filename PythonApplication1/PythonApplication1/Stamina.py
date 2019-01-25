import UnitStat


class Stamina(UnitStat):
    """Used by Units to keep track of Stamina Points, Pool, and effects"""

    def __init__(self, value=10):
        self.pool = value  # Pool Capacity
        self.points = value  # Unspent Stamina
        # self.PoolEffects = [] # List of effects affecting Pool Capacity

    # Stamina Point Functions
    def get_stamina_points(self):
        return self.points

    def gain_stamina_points(self, value):
        self.points += value

    def spend_stamina_points(self, value):
        if self.can_spend(value):  # may be redundant?
            self.points -= value
        else:
            self.points = 0  # may need to change later

    def reset_stamina_points(self):
        self.points = self.pool

    def can_spend(self, value):
        if value > self.points:
            return False
        else:
            return True

    # Stamina Pool Functions
    # Implements UnitStat class
