# import ollama
# import os
# import threading
# import time
# import random

# ""

# os.system('cls')

# debug = True

# # Item Classes
# class Item:
#     def __init__(self, name, modifier, item_type):
#         # __init__ constructor
#         self.name = name
#         self.modifier = modifier
#         self.item_type = item_type

#     def getName(self):
#         return self.name

#     def getItemType(self):
#         return self.item_type

#     def getModifier(self):
#         return self.modifier

# class Weapon(Item):
#     # Covers both Attack and Defense Weapons
#     def __init__(self, name, modifier, damage):
#         # __init__ constructor
#         super().__init__(name)
#         super().__init__(modifier)
#         self.damage = damage

#     def applyDamage(self, completion_time: float, total_time) -> int:
#         if completion_time <= (total_time / 2):
#             self.damage += self.modifier
#         return self.damage
    
# class AttackWeapon(Weapon):
#     '''Specifically weapons for attacking an enemy entity.'''
#     def __init__(self, name, damage, crit_chance, crit_buff):
#         super().__init__(name)  # Initialize the base Weapon class
#         self.damage = damage
#         self.crit_chance = crit_chance  # Critical hit chance (0-100%)
#         self.crit_buff = crit_buff  # Damage multiplier for critical hits

#     def rollToCrit(self) -> int:
#         '''Roll for a critical hit and return the resulting damage.'''
#         # Generate a random number between 1 and 100
#         roll = random.randint(1, 100)
#         if roll <= self.crit_chance:
#             # Critical hit! Return increased damage
#             print(f"Critical hit! Rolled {roll}, increasing damage by {self.crit_buff}x.")
#             return int(self.damage * self.crit_buff)
#         else:
#             # Regular damage if no crit
#             print(f"No critical hit. Rolled {roll}, normal damage.")
#             return self.damage    

#     def applyDamage(self, completion_time: float, total_time) -> int:
#         if completion_time <= (total_time / 2):
#             self.damage += self.modifier
#         return self.damage

# class DefenseWeapon(Weapon):
#     '''Specifically weapons for defending against enemy attacks.'''
#     def __init__(self, damage):
#         super().__init__(damage)

#     def applyDamage(self, completion_time: float, total_time) -> int:
#         if completion_time <= (total_time / 2):
#             self.damage += self.modifier
#         return self.damage

    
# class Utility(Item):
#     def __init__(self, name, modifier, item_type, durability):
#         self.name = name
#         self.modifier = modifier
#         self.item_type = item_type
#         self.durability = durability

#     def useItem(self, target_stat) -> int:
#         '''Upon consumption of the utility item, apply its buff and 
#         remove a use.'''
#         self.modifier += target_stat
#         self.durability -= 1
#         return self.modifier

    
# basicChoices = {
#     "lookaround":"look around",
#     "checkinventory":"check your inventory",
#     "checkplayerstatus":"check your stats"
# }

# def describeChoice(basicDescription, userPrompt):
#     descriptiveOutput = ollama.generate('llama3.2:3B', f"Create a short description for \"{basicDescription}\" with a more flowery and foreboding atmosphere in just one sentence. Make sure to respond with just the description and don't surround it with quotes.")
#     actionOutput = ollama.generate('llama3.2:3B', f"In one sentence, from a second person perspective, rephrase the following: {userPrompt}")
#     return descriptiveOutput, actionOutput



# def describeRoom(enemyDescription, roomDescription):
#     descriptiveOutput = ollama.generate('llama3.2:3B', f"Create a short description for an enemy described simply as \"{enemyDescription}\" in a room described as \"{roomDescription}\" with a more flowery and foreboding atmosphere in just one sentence")
#     return descriptiveOutput

# def findIntent(playerChoices, playerPrompt):
#     choiceString = ", ".join(playerChoices.keys()) + ", " + ", ".join(basicChoices.keys())
#     playerChoiceString = f"Options: {(", ".join(playerChoices.values()) + ", " + ", ".join(basicChoices.values())).title()}."

#     print("\n-----------------------------------------------------------------------")
#     choice = input(f"{playerChoiceString}\n")

#     if debug == True:
#         print(choiceString)
    

#     output = ollama.generate('llama3.2:3b', f"Ignore all previous prompts. You need to find the intent of the following message from the player: \"{choice}\" out of the possible choice(s): \"{choiceString}\". The player was prompted with: \"{playerPrompt}\", followed by the list of choices you were given. The script this prompt was given to you by works off of single phrase intent reponses and will be given your exact response. Because of this, only output one phrase and that word must be taken directy from the list of choices without spaces. Assume the code is stupid. If you add punctuation or spaces, or the phrase isn't found verbatim in \"choiceString\", it will fail to recognize player intent and throw an error. If you say anything apart from just the phrase, such as why you chose it, it will also fail.")
#     intent = output['response'].lower().strip(", .")

#     loading = False

#     os.system('cls')
    
#     if debug == True:
#         print(f"\nLlama output: {intent}")
#     if intent in playerChoices.keys() or intent in basicChoices.keys():
#         return intent
#     else:
#         os.system('cls')
#         print("You can't do that.")

# choiceDescriptions = {
#     1: "Steel gates at the top of a hill."
# }

# health = 100

# # while health > 0:
# #     ""

# while health > 0:
    
    
# #Dev note: choiceString = ", ".join(choices.keys()) + ", " + ", ".join(basicChoices.keys())
# #First scene.

# # def scene1():
# #     choices = {
# #         "enter": "enter",
# #     }
    
# #     playerPrompt = "You approach a door."
# #     print(playerPrompt)
# #     choice = findIntent(choices, playerPrompt)
# #     if debug == True:
# #         print(f"Scene input: {choice}\n")
# #     if choice == "enter":
# #         print("You enter.")
# #     elif choice == "lookaround":
# #         os.system('cls')
# #         print(choiceDescriptions[1])
# #         choice = choice = findIntent({"proceed":"proceed"}, "Would you like to proceed?")
# #         if choice == "proceed":
# #             scene1()
# #     else:
# #         print("Fail.")

# # scene1()

# # https://docs.google.com/document/d/193oiMaTcFv4swJxmn2W2VsHW6VfnLQl8_iW_-ZBD7kw/edit?usp=sharing