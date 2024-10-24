import ollama
import os
import time
import random
import json
from attack_weapon import AttackWeapon
from defense_weapon import DefenseWeapon
from enemy import Enemy
from Math_problems import generate_problem
from Math_problems import adjust_level
#from foundry import createAttackWeapon
VERSION = 'llama3.2:3B'

os.system('cls')

debug = True
easyEnemyMaxHealth = 15

"https://drive.google.com/drive/folders/1nwtzyt7ICeFlUcNEoMvSp6rMQI3ZTdQJ?usp=drive_link"

#--------------------------------------------------------------------------------------------------------------
#   Glossary
#--------------------------------------------------------------------------------------------------------------

# 1 Player stats
# 2 Descriptions (Makes poetic description from a basic one)
# 3 Choice description (Describes both a setting and a choice the player has, outputing each individually.)
# 4 Enemy Information + Room Randomizer (Stores all the basic enemies and the system that uses it to generate rooms.)
# 5 Intent recognition (Matches player input to a pre-made list of options)
# 6 Event descriptions (In combat, this describes events like misses and hits)
# 7 And finally: the game itself.

#--------------------------------------------------------------------------------------------------------------
#   1 - Player stats (to be incorporated with classes later)
#--------------------------------------------------------------------------------------------------------------

equipped = "Darkslayer Blade"
equippedMaxDamage = 10
health = 100

#--------------------------------------------------------------------------------------------------------------
#   2 - Simple description
#--------------------------------------------------------------------------------------------------------------

#The AI is given a basic description and beautifies it.

def describe(basicDescription):
    descriptiveOutput = ollama.generate(VERSION, f"Create a short description for \"{basicDescription}\" with a more flowery and foreboding atmosphere in just one sentence. Make sure to respond with just the description and don't surround it with quotes.")
    return descriptiveOutput


#--------------------------------------------------------------------------------------------------------------
# @   3 - Choice description
#--------------------------------------------------------------------------------------------------------------

# This is given two inputs: a basic description of an area, and the prompt the player should be given.
# It generates an elaborate version of the basic decription.
# It then generates an elabotate version of the prompt the player is given.
# Finally, it returns both individually.

def describeChoice(basicDescription, userPrompt):
    descriptiveOutput = describe(basicDescription)
    actionOutput = ollama.generate(VERSION, f"In one sentence, from a second person perspective, rephrase the following: {userPrompt}")
    return descriptiveOutput['response'], actionOutput['response']

#--------------------------------------------------------------------------------------------------------------
#   4 - Enemy Information + Room Randomizer
#--------------------------------------------------------------------------------------------------------------

with open('data.json', 'r') as file:
    enemy_data = json.load(file)

easyDiff = enemy_data['enemies']['easy']
medDiff = enemy_data['enemies']['medium']
hardDiff = enemy_data['enemies']['hard']

# Based on the difficulty, this picks a random enemy from the enemy pool.
# Each enemy is paired with a room description.
# The AI is given both the enemy and room descriptions and told to make it descriptive.
# The function then returns the AI's response.

def describeRoom(difficulty="easy"):
    # Easy by default. Otherwise, it checks for "medium" and "hard".
    enemyPick = enemyPick = easyDiff[random.randint(0, len(easyDiff)-1)]
    if difficulty == "medium":
        enemyPick = medDiff[random.randint(0, len(medDiff)-1)]
    elif difficulty == "hard":
        enemyPick = hardDiff[random.randint(0, len(hardDiff)-1)]
        
    if debug == True:
        print(enemyPick)

    # Generate the description.
    descriptiveOutput = ollama.generate(VERSION, f"Create a short description for an enemy described simply as \"{enemyPick['name']}\" in a room described as \"{enemyPick['room']}\" with a more flowery and foreboding atmosphere in just one sentence. Make sure it's in second person. Take on as much creative liberty as you would like, but make sure to name the enemy directly so as to not leave it ambiguous for the player what they're fighting. You can change the adjectives for it, just not the noun.")
    enemyName = ollama.generate(VERSION, f"Extract the enemy name from the following, with no commas or additional text: [{descriptiveOutput}]")
    # Completely accidental side effect: the AI gives the enemy a name.
    return descriptiveOutput['response'], enemyName['response']

#--------------------------------------------------------------------------------------------------------------
#   5 - Intent Recognition
#--------------------------------------------------------------------------------------------------------------

# This stores all the built-in choices.
    # To do: adjust this for combat.

basicChoices = {
    "check_inventory":"check your inventory",
    "check_player_status":"check your stats"
}

#This finds player intent
def findIntent(playerChoices, playerPrompt):
    while True:
        choiceString = ", ".join(playerChoices.keys()) + ", " + ", ".join(basicChoices.keys())
        playerChoiceString = f"Options: {(", ".join(playerChoices.values()) + ", " + ", ".join(basicChoices.values())).title()}."

        print("\n-----------------------------------------------------------------------")
        choice = input(f"{playerChoiceString}\n")

        if debug == True:
            print(choiceString)

        #loadingState.start()

        output = ollama.generate(VERSION, f"You need to find the intent of the following message from the player: \"{choice}\" out of the possible choice(s): \"{choiceString}\". The player was prompted with: \"{playerPrompt}\", followed by the list of choices you were given. The script this prompt was given to you by works off of single phrase intent reponses and will be given your exact response. Because of this, only output one phrase and that word must be taken directy from the list of choices without spaces. Assume the code is stupid. If you add punctuation or spaces, or the phrase isn't found verbatim in \"{choiceString}\", it will fail to recognize player intent and throw an error. If you say anything apart from just the phrase, such as why you chose it, it will also fail.")
        # Oh, all the silly things I have to do to regulate it. Removing commas, periods, spaces, and quotes. Fun stuff.
        intent = output['response'].lower().strip(", .").strip('"')
        
        if debug == True:
            print(f"\nLlama output: [{intent}]")

        if intent in playerChoices.keys() or intent in basicChoices.keys():
            return intent
    

#--------------------------------------------------------------------------------------------------------------
#   6 - Event Descriptions
#--------------------------------------------------------------------------------------------------------------

def generateEventDescription(event, enemy, chance, threshold, damage=0):
    description = "Blank"
    if event.lower() == "miss":
        print("Loading...")
        # Summon Llama 3.2 3B for a description.
        description = ollama.generate(VERSION, f"Generate a short description for what just happened in second person - just one sentence. The player attacked {enemy['name']} and hit with a roll of {chance} with the minimum hit thresshold being {threshold}. {enemy['name']} has {enemy['health']} health and the player did {damage} damage. Remember - this is an attack, not a kill. Give it a dark fantasy atmostphere, and only include the description and nothing else. Leave out numbers in your response, instead dramaticizing the thril of near misses and the bravado of sure hits. Make sure to add in the enemy's reaction (no dialog) to the hit.")
    if event == "hit":
        print("Loading...")
        description = ollama.generate(VERSION, f"You need to generate a short, flowery summarization of current events in second person perspective using the following details. There should be no dialog. The player attacked {enemy['name']}, with the attack getting them down to {enemy['health']/enemy['maxHealth']*100}%. The player has a health of {(health/100)*100}%. The player had a {100 - threshold} chance of making contact with their sword and passed. Make sure to give it a foreboding fantasy vibe and make it dramatic based on the details you were given. Do this all in a single sentence.")
        os.system('cls')
    else:
        print("Error: event not found")
    return description['response']

#--------------------------------------------------------------------------------------------------------------
#   7 - Main Loop
#--------------------------------------------------------------------------------------------------------------

equippedName = ""
equippedAttackDamage = 0
skills = 50



def engageCombat(room, enemy):
    global skills
    death = False
    print(room)
    while enemy['health'] > 0:
        #os.system('cls')
        choices = {
            "attack_enemy":"attack",
        }
        intent = findIntent(choices, "Would you like to attack the enemy?")
        if intent == "attack_enemy":
            print("attacking enemy")
            hitChance = random.random()
            if hitChance > -1:
                enemy['health'] -= equippedAttackDamage
                event = describe(f"The player landed a hit on {enemy['name']}. In the style of dark fantasy, summarize the action.")
                os.system('cls')
                print(event['response'])
                print(f"You did {equippedMaxDamage} damage.")
            else:
                current_level = 'intermediate'
                problems_attempted=0
                problems_solved = 0
                total_time = 0.0
                problem, correct_answer, explanation = generate_problem(current_level)
                print(f'Problem: {problem}')
                start_time = time.time()
                user_input = input("Your answer: ").strip()
                end_time = time.time()
                problems_attempted +=1
                total_time += (end_time - start_time)
                if user_input == correct_answer:
                    print("Correct! You landed your attack.")
                    enemy['health'] -= equippedAttackDamage
                    skills += 5
                else:
                    skills -= 5
                    print(f"Incorrect. The correct answer was: {correct_answer}")
                    print(f"Explanation: {explanation}")
                if problems_attempted % 3 == 0:
                    current_level = adjust_level(current_level, problems_attempted, problems_solved, total_time)
                    problems_attempted, problems_solved, total_time = 0, 0, 0.0
    return

def newRoom():
    global equippedName
    global equippedAttackDamage

    easyRooms = 0
    medRooms = 0
    hardRooms = 0
    
    if easyRooms < 3:
        # Picking up weapon
        os.system('cls')
        weaponName = ollama.generate('llama3.2:3b', "Generate a cool RPG sword name in just two words. Make sure you say nothing else but those two words.")
        weaponDamage = random.randrange(8, 12)
        playerPrompt = f"You have come across a sword: the {weaponName['response']}. It does {weaponDamage} damage. Would you like to pick it up?"
        print(playerPrompt)
        choices = {
            "pickup":"pickup",
            "yes":"yes"
        }
        intent = findIntent(choices, playerPrompt)
        if intent == "pickup" or intent == "yes":
            equippedName = weaponName
            equippedAttackDamage = weaponDamage
        os.system('cls')
        # Moving forward
        room, enemyName = describeRoom("easy")
        health = random.randint(5, 10)
        enemy = {
            "name":enemyName,
            "maxHealth":health,
            "health":health
        }
        engageCombat(room, enemy)
    elif easyRooms > 3 and medRooms < 3:
        choices = {
            "attack":"attack enemy",
        }
        room, enemy = describeRoom("medium")
        os.system('cls')
        print(room)
        intent = findIntent(choices, "What would you like to do? ")
        if intent == "attack":
            engageCombat()
    elif medRooms > 3 and hardRooms < 3:
        choices = {
            "attack":"attack enemy",
        }
        room, enemy = describeRoom("hard")
        os.system('cls')
        print(room)
        intent = findIntent(choices, "What would you like to do? ")
        if intent == "attack":
            engageCombat()

def main():

    # Intro to the game for the player.
    # Format: Developers give a basic description of the setting.
    # Format: Developers give a basic choice for the player.
    # Output: enhanced description, enhanced choice. The flowery versions.
    description = "Steel gates at the top of a hill."
    choice = "Would you like to enter? (keep it in question form)"
    enhancedDesc, enhancedChoice = describeChoice(description, choice)
    print(enhancedDesc)
    userInput = input(enhancedChoice + "\n")

    while True:
        #*Main Loop
        player_hp = 100
        newRoom()
        # Weapon Generation

        #* Exit requirement.
        if player_hp <= 100:
            break
        print("while loop ended")

if __name__ == "__main__":
    main()