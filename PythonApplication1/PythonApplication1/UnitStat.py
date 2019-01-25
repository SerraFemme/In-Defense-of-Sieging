class StatTracker(object):
    """
    Class used for keeping track of a list of effects and their values.
    Used primarily by Stamina, Armor, and Hand Size.
    """

    def __init__(self, value=0):
        self.value = value
        self.EffectList = []

    # Value functions
    def get_value(self):
        if self.value < 0:
            return 0
        else:
            return self.value

    def set_value(self, newValue):
        self.value = newValue

    def add_value(self, newValue):
        self.value += newValue

    def subtract_value(self, newValue):
        self.value -= newValue

    # EffectList functions
    def get_effect_list(self):
        return self.EffectList

    def get_effect(self, effect_name):
        for item in self.EffectList:
            if item[0] == effect_name:
                return item

    def add_effect(self, effect_name, value):
        self.EffectList.append((effect_name, value))

    def remove_effect(self, effect_name):
        self.EffectList.remove(self.get_effect(effect_name))

    def has_effect(self, effect_name):
        v = False
        for item in self.EffectList:
            if item[0] == effect_name:
                v = True
        return v


class Stamina(object):
    """
    Used by Units to keep track of Stamina Points, Pool, and effects
    """

    def __init__(self, value=10):
        self.pool = StatTracker(value)  # Pool Capacity
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
    def get_pool_size(self):
        return self.pool.get_value()

    def add_pool_effect(self, effect_name, value):
        self.pool.add_effect(effect_name, value)
        self.pool.add_value(value)

    def remove_pool_effect(self, effect):
        if self.pool.has_effect(effect):
            value = self.pool.get_effect(effect)
            self.pool.remove_effect(effect)
            self.pool.subtract_value(value[1])
        else:
            print(effect, 'is not listed')
