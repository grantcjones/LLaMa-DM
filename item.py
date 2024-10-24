import random

class Item:
    def __init__(self, name):
        # __init__ constructor
        self.name = name
        self.modifier = random.randrange(1, 6)

    def getName(self):
        return self.name

    def getModifier(self):
        return self.modifier

    

