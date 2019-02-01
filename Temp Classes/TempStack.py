class Stack(object):
    """Example Stack implementation, decomission later"""

    def __init__(self):
        self.stack = []  # May need changing

    # Use add to add an item to the stack
    def add(self, dataval):
        if dataval not in self.stack:
            self.stack.append(dataval)  # Use list append method to add element
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
