class Queue(object):
    """Default Queue implementation"""

    def __init__(self):
        self.queue = list() #May need changing

    def addtoq(self,dataval):
    # Insert method to add element
        if dataval not in self.queue:
            self.queue.insert(0,dataval)
            return True
        else:
            return False


    # Pop method to remove element
    def removefromq(self):
        if len(self.queue)>0:
            return self.queue.pop()
        else:
            return ("No elements in Queue!")

    def size(self):
        return len(self.queue)