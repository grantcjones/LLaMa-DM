from item import Item

class Utility(Item):
    def __init__(self, name, modifier):
        super().__init__(name, modifier)

    def useItem(self) -> int:
        '''Upon consumption, add amount to player health.'''
        return self.modifier
