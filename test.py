from attack_weapon import AttackWeapon
from defense_weapon import DefenseWeapon
from enemy import Enemy
#! Ensure to 'from/import' every class needed in a file like above



#! Generate Enemy
room_enemy = Enemy('enemy name', room_level = 'easy')

print("Player attack test.")
print(f'Enemy health: ', room_enemy.getHealth)
print("player attack")

#* Initialize the object 'weapon_one', then 
weapon_one = AttackWeapon("The Throngler") # attack weapon
#* Use the weapon's 'applyDamage' function to lower the enemy's health (applyDamage args: (time it took to answer the question, total time given to answer question))
room_enemy.takeDamage(weapon_one.applyDamage(12, 24))

print(f'Enemy health: ', room_enemy.getHealth)

print("Enemy attack test")

player_health = 100
weapon_two = DefenseWeapon("Buckler")

print(f'Player Health: ', player_health)

#! This is assuming the player has failed the math problem
enemy_attack = room_enemy.getAttack

print('enemy attack')
player_health -= enemy_attack - weapon_two.applyDamage()

print("Player health: ", player_health)

