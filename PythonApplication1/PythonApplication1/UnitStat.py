class UnitStat(object):
    """Primarily used for Stats for Units including Stamina and Armor"""

    def __init__(self, value):
        self.value = value
        self.EffectList = []

    # Value functions
    def get_value(self):
        return self.value

    def set_value(self, newValue):
        self.value = newValue

    def change_value(self, newValue):
        self.value = + newValue  # should increase or decrease if value is pos or neg

    # EffectList functions
    def get_effect_list(self):
        return self.EffectDict

    def add_effect(self, effect_name, value):
        self.EffectList.append((effect_name, value))

    def remove_effect(self, effect_name):
        pass

    def has_effect(self, value):
        v = False
        for item in self.EffectList:
            if item[0] == value:
                v = True
        return v
