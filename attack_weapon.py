from weapon_item import Weapon
import random

class AttackWeapon(Weapon):
    '''Specifically weapons for attacking an enemy entity.'''
    def __init__(self, name):
        super().__init__(name)  # Initialize the base Weapon class
        self.crit_chance = self.getDamage() * ((random.randrange(8, 26)) / 100)  # Critical hit chance (8-25%)
        self.crit_mult = random.uniform(1.2, 1.5)  # Damage multiplier for critical hits

    def rollToCrit(self) -> bool:
        
        '''Roll for a critical hit and return whether it was successful.
        Only implemented within this class, ignore this method.'''
        roll = random.randint(1, 100)
        return roll <= self.crit_chance

    def applyDamage(self, completion_time: float, total_time: float) -> int:
        '''Takes the time the player answered the question in and compares it to the total time they 
        had to complete the question, and if they answer it within half the time given, they get a flat damage
        bonus. Returns and integer for how much damage is applied'''
        if completion_time <= (total_time / 2):
            self.damage += self.modifier
        if self.rollToCrit():
            self.damage += int(self.crit_mult * self.damage)
        return self.damage
