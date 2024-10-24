from weapon_item import Weapon

class DefenseWeapon(Weapon):
    '''Specifically weapons for defending against enemy attacks.'''
    def __init__(self, name):
        super().__init__(name)

    def applyDamage(self) -> int:
        '''Subtract from incoming damage.'''
        return self.getDamage()
    
