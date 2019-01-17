class UnitStat(object):
    """Primarily used for Stats for Units including Stamina and Armor"""


    def __init__(self, value):
        self.value = value
        self.EffectList = []

    
    #Value functions
    def get_value():
        return self.value

    def set_value(self, newValue):
        self.value = newValue

    def increase_value(self, newValue):
        self.value =+ newValue

    def decrease_value(self, newValue):
        self.value =- newValue


    #EffectList functions
