import ollama
# import random

class Enemy:
    ''''''

    def __init__(self, name: str, room_level: str):
        self.name = name
        self.room_level = room_level

        if room_level.lower() == "hard":
            self.health = 100
            self.attack = 25

        elif room_level.lower() == "medium":
            self.health = 50
            self.attack = 15

        else:
            self.health = 25
            self.attack = 10

    def getAttack(self) -> int:
        return self.attack
    
    def getHealth(self) -> int:
        return self.health

    def takeDamage(self, dmg: int) -> None:
        self.health -= dmg