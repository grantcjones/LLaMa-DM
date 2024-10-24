import ollama
import os

debug = True

basicChoices = {
    "checkinventory":"check your inventory",
    "checkplayerstatus":"check your stats"
}

#This finds player intent
def findIntent(playerChoices, playerPrompt):
    choiceString = ", ".join(playerChoices.keys()) + ", " + ", ".join(basicChoices.keys())
    playerChoiceString = f"Options: {(", ".join(playerChoices.values()) + ", " + ", ".join(basicChoices.values())).title()}."

    print("\n-----------------------------------------------------------------------")
    choice = input(f"{playerChoiceString}\n")

    if debug == True:
        print(choiceString)

    #loadingState.start()

    output = ollama.generate('llama3.2:3b', f"You need to find the intent of the following message from the player: \"{choice}\" out of the possible choice(s): \"{choiceString}\". The player was prompted with: \"{playerPrompt}\", followed by the list of choices you were given. The script this prompt was given to you by works off of single phrase intent reponses and will be given your exact response. Because of this, only output one phrase and that word must be taken directy from the list of choices without spaces. Assume the code is stupid. If you add punctuation or spaces, or the phrase isn't found verbatim in \"choiceString\", it will fail to recognize player intent and throw an error. If you say anything apart from just the phrase, such as why you chose it, it will also fail.")
    intent = output['response'].lower().strip(", .").strip()
    
    if debug == True:
        print(f"\nLlama output: {intent}")
    if intent in playerChoices.keys() or intent in basicChoices.keys():
        return intent
    else:
        print("You can't do that.")

playerChoices = {
    "attackenemy":"attack enemy",
}

intent = findIntent(playerChoices, "Would you like to attack?")

