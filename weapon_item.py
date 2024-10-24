from item import Item
import random

class Weapon(Item):
    # Covers both Attack and Defense Weapons
    def __init__(self, name):
        # Call the parent (Item) constructor with both name and modifier
        super().__init__(name)
        self.damage = random.randrange(6, 13)

    def getDamage(self) -> int:
        return self.damage

    def applyDamage(self, completion_time: float, total_time: float) -> int:
        if completion_time <= (total_time / 2):
            self.damage += self.modifier
        return self.damage
