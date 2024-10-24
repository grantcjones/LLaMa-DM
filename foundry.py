import ollama
from item import Item
from weapon_item import Weapon
from attack_weapon import AttackWeapon
from defense_weapon import DefenseWeapon
from utility_item import Utility

LLAMA = 'llama3.2:3B'

prompt = 'Generate a cool RPG sword name in just two words. Make sure you say nothing else but those two words.'







def createAttackWeapon():
    raw_output = ollama.generate(LLAMA, prompt)
    name = raw_output['response']

    # dmg_output

    
    new_weapon = AttackWeapon(name, )
    # return ouput['response']