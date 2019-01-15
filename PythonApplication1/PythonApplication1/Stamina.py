class Stamina(object):
    """Used by Units to keep track of Stamina Points, Pool, and effects"""

    
    def __init__(self, value=10):
        self.pool = value # Pool Capacity
        self.points = value # Unspent Stamina
        #self.PoolEffects = [] # List of effects affecting Pool Capacity

    
    #Stamina Point Functions
    def get_stamina_points(self):
        return self.points
    
    def gain_stamina_points(self, value):
        self.points += value

    def spend_stamina_points(self, value):
        if self.can_spend(value):
            self.points -= value
        else:
            self.points = 0 # may need to change later

    def reset_stamina_points(self):
        self.points = self.pool

    def can_spend(self, value):
        if value > self.points:
            return false
        else:
            return true


    #Stamina Pool Functions
        #Implements Tuple_List





    # Use add to add an item to the stack
    def add(self, dataval):
        if dataval not in self.stack:
            self.stack.append(dataval) # Use list append method to add element
            return True
        else:
            return False

    # Use peek to look at the top of the stack
    def peek(self):     
        return self.stack[0]

    # Use list pop method to remove element
    def remove(self):
        if len(self.stack) <= 0:
            return ("No element in the Stack")
        else:
            return self.stack.pop()
