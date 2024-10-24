import ollama
import random
import time

defaultEasyHealth = 15

enemyPick = {'name': 'rusty emotionless robot', 'room': 'floor with dirt, rust and bolts'}
enemyDesc = "In the forsaken chamber of corroded steel and forgotten dreams, \"Kalthok, the Cogheart\" stood motionless, its very existence a blasphemy against the soul, as if rusted gears and wires had supplanted the fire of life, leaving only an abyssal void where warmth once dwelled."
enemyName = "Kalthok, the Cogheart".replace(",","")
print(enemyName)

enemyHealth = round(defaultEasyHealth * random.random())
print(enemyHealth)

currentEnemy = {
    'name':enemyName,
    'maxHealth':enemyHealth,
    'health':enemyHealth
}

def generateEventDescription(event, enemy, chance, threshhold, damage=0):
    description = "Blank"
    if event == "missed":
        # Summon Llama 3.2 3B for a description.
        print("Generating Description for Miss")
        description = ollama.generate('llama3.2:3b', f"Generate a short description for what just happened in second person - just one sentence. The player attacked {enemy['name']} and missed, with a roll of {chance} out of {threshhold}. Give it a dark fantasy atmostphere, and only include the description and nothing else. Leave out numbers in your response, instead dramaticizing the agony of close hits and the defeat of sure misses.")
        print("Done")
    if event == "hit":
        print("Generating Description for Hit")
        description = ollama.generate('llama3.2:3b', f"Generate a short description for what just happened in second person - just one sentence. The player attacked {enemy['name']} and hit with a roll of {chance} with the minimum hit thresshold being {threshhold}. {enemy['name']} has {enemy['health']} health and the player did {damage} damage. Remember - this is an attack, not a kill. Give it a dark fantasy atmostphere, and only include the description and nothing else. Leave out numbers in your response, instead dramaticizing the thril of near misses and the bravado of sure hits. Make sure to add in the enemy's reaction (no dialog) to the hit.")
        print("Done")
    return description['response']

equipped = "Darkslayer Blade"
equippedMaxDamage = 10

# misses = 0

# while misses <= 3:
#     hitChance = random.random()
#     if hitChance > 0.2: # 80% chance
#         # I'm not doing math problems, I'm giving a random chance for suceeding the saving throw for now.
#         solveChance = random.random()
#         if solveChance > 0.3: # 70% chance
#             damage = equippedMaxDamage * random.random()
#         else:
#             print(generateEventDescription("missed", enemyName, solveChance * 100, 70))
#             misses += 1
#             time.sleep(3)
#             print()
#     else:
#         print(generateEventDescription("missed", enemyName, hitChance * 100, 80))
#         misses += 1
#         time.sleep(3)
#         print()

hitChance = random.random()
for i in range(4):
    damage = equippedMaxDamage * random.random()
    # What happened. The current enemy. The hit chance. What the minimum roll was. Optionally how much damage was dealt.
    print(generateEventDescription("hit", currentEnemy, hitChance * 100, 70, damage))
    print()

# def describeRoom(difficulty="easy"):
#     # Easy by default. Otherwise, it checks for "medium" and "hard".
#     enemyPick = enemyPick = easyDiff[random.randint(0, len(easyDiff)-1)]
#     if difficulty == "medium":
#         enemyPick = medDiff[random.randint(0, len(medDiff)-1)]
#     elif difficulty == "hard":
#         enemyPick = hardDiff[random.randint(0, len(hardDiff)-1)]
        
#     if debug == True:
#         print(enemyPick)
#     # Generate the description.
#     descriptiveOutput = ollama.generate('llama3.2:3b', f"Create a short description for an enemy described simply as \"{enemyPick['name']}\" in a room described as \"{enemyPick['room']}\" with a more flowery and foreboding atmosphere in just one sentence. Take on as much creative liberty as you would like, but make sure to name the enemy directly so as to not leave it ambiguous for the player what they're fighting. You can change the adjectives for it, just not the noun.")
#     enemyName = ollama.generate('llama3.2:3b', f"Extract the enemy name from the following, with no commas or additional text: [{descriptiveOutput}]")
#     # Completely accidental side effect: the AI gives the enemy a name.
#     return descriptiveOutput['response'], enemyName







