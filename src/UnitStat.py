class StatTracker(object):
    """
    Class used for keeping track of a list of effects and their values.
    Used primarily by Stamina, Weapon Damage, Armor, and Hand Size.
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

    def __set_value(self, new_value):
        self.value = new_value

    def __add_value(self, new_value):
        self.value += new_value

    def __subtract_value(self, new_value):
        self.value -= new_value

    # EffectList functions
    def get_effect_list(self):
        return self.EffectList

    def get_effect(self, effect_name):
        for item in self.EffectList:
            if item[0] == effect_name:
                return item

    def add_effect(self, effect_name, value):
        self.EffectList.append((effect_name, value))
        self.__add_value(value)

    def remove_effect(self, effect_name):
        deleted = self.get_effect(effect_name)
        self.__subtract_value(deleted[1])
        self.EffectList.remove(deleted)

    def has_effect(self, effect_name):
        b = False
        for item in self.EffectList:
            if item[0] == effect_name:
                b = True
        return b


class Stamina(object):
    """
    Used by Units to keep track of Stamina Points, Pool, and effects
    """

    def __init__(self, value=10):
        self.pool = StatTracker(value)  # Pool Capacity
        self.points = value  # Unspent Stamina

    # Stamina Point Functions
    def gain_stamina_points(self, value):
        self.points += value

    def spend_stamina_points(self, value):  # TODO: Clean Up
        if self.can_spend(value):  # may be redundant?
            self.points -= value
        else:
            self.points = 0  # may need to change later

    def reset_stamina_points(self):
        self.points = self.pool.value

    def can_spend(self, value):
        if value > self.points:
            return False
        else:
            return True

    # Stamina Pool Functions
    def get_pool_size(self):
        return self.pool.value

    def add_effect(self, effect_name, value):
        self.pool.add_effect(effect_name, value)

    def remove_effect(self, effect):
        if self.pool.has_effect(effect):
            self.pool.remove_effect(effect)
        else:
            print(effect, 'is not listed')


class UnitAbilities(object):
    """
    Stores and runs ALL passives and abilities granted by the unit or their
    equipment.
    """
    def __init__(self):
        self.button_abilities = []
        self.triggered_abilities = []
        self.dynamic_abilities = []

    def list_buttons(self):
        for i in self.button_abilities:
            pass
