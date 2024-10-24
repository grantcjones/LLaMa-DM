import ollama
import random

debug = True

# Easy enemies
easyDiff = [
{"name": "large angry wolf", "room": "cave floor with bones and fur"},
{"name": "giant hungry rat", "room": "small bones and fur on nasty floor"},
{"name": "sneaky greedy goblin", "room": "disorganized room with cooking pot"},
{"name": "rusty emotionless robot", "room": "floor with dirt, rust and bolts"},
{"name": "giant chaotic frog", "room": "floor with eggs and saliva dripping"},
{"name": "giant spider with large fangs", "room": "floor and ceiling with eggs in cave"},
{"name": "giant fast beetle", "room": "hiding under dirt with stink"},
{"name": "giant slimy worm", "room": "digs out from under dusty floor"},
{"name": "group of vampire bats", "room": "smelly room with bones on floor"}
]

# Medium difficulty enemies
medDiff = [
{"name": "angry wailing ghost", "room": "room with puddles of tears on floor"},
{"name": "fast viscous basilisk", "room": "room with dead rats"},
{"name": "screeching furious harpy", "room": "room with talon marks on walls"},
{"name": "emotionless fire elemental", "room": "room with scorched rocks"},
{"name": "gluttonous ooze", "room": "room covered in green sticky ooze"},
{"name": "undead knight", "room": "empty, windy room with dead goblins"},
{"name": "giant cobra", "room": "cave ground, dripping venom"},
{"name": "prideful genie", "room": "inside a bottle"},
{"name": "dnd mimic monster", "room": "lying on cave ground"}
]

# Hard enemies
hardDiff = [
{"name": "angry dumb cave troll", "room": "cave cooking meat and eating"},
{"name": "hydra with eight heads", "room": "crumbling stone walls around"},
{"name": "proud minotaur with club and axe", "room": "refined well-made room"},
{"name": "purple sturdy crystal golem", "room": "room made of purple crystal"},
{"name": "sneaky fastidious vampire", "room": "haunted house with large dining room"},
{"name": "animated lion skeleton", "room": "emerges from large pile of bones"},
{"name": "giant emotionless scorpion", "room": "asleep on floor cooling off"},
{"name": "vicious vain gorgon", "room": "stone small animals around on floor"},
{"name": "powerful instinctual chimera", "room": "eating a small meal it caught"}
]

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
    descriptiveOutput = ollama.generate('llama3.2:3b', f"Create a short description for an enemy described simply as \"{enemyPick['name']}\" in a room described as \"{enemyPick['room']}\" with a more flowery and foreboding atmosphere in just one sentence. Take on as much creative liberty as you would like, but make sure to name the enemy directly so as to not leave it ambiguous for the player what they're fighting. You can change the adjectives for it, just not the noun.")
    # Completely accidental side effect: the AI gives the enemy a name.
    return descriptiveOutput['response']

room = describeRoom("easy")
print(room)

#description = describeRoom("Large angry wolf", "Cave floor with bones and fur")
    