#--------------------------------------------------------------------------------------------------------------
#   REWRITE 11/13/2024
#   The purpose is to lessen how many global variables are used and simplify what inputs/outputs are used in
#   and improve the flow between functions, but also learn classes at the same time.
#--------------------------------------------------------------------------------------------------------------

import ollama
import time
import random
import threading
import json
import sys

#--------------------------------------------------------------------------------------------------------------
#   Glossary
#--------------------------------------------------------------------------------------------------------------

    # 0 - Clear screen + other niceities
    # 1 - Basic classes (player, weapon, etc)
    # 2 - Loading Screen
    # 3 - Enemy Data + Class
    # 4 - AI Class
    #     Main Function

#--------------------------------------------------------------------------------------------------------------
#   0 - Clear screen, hide cursor, show cursor + bonus niceties
#--------------------------------------------------------------------------------------------------------------

def wait(duration=0.1):
    time.sleep(duration)

def clear():
    print("\033[H\033[J")

def hide_cursor():
    sys.stdout.write("\033[?25l")

def show_cursor():
    sys.stdout.write("\033[?25h")

#--------------------------------------------------------------------------------------------------------------
#   1 - Basic classes (weapons, living beings (hashealth), player
#--------------------------------------------------------------------------------------------------------------

class Weapon:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage

class Entity:
    def __init__(self, max_health):
        self.health = max_health
        self.max_health = max_health
        self.dead = False

    def damage(self, damage):
        self.health -= damage
        if self.health - damage <= 0:
            self.dead = True

class Player(Entity):
    def __init__(self):
        super().__init__(20)
        self.equipped = Weapon('Gregorator', 5)
        
player = Player()

#--------------------------------------------------------------------------------------------------------------
#   2 - Loading Screen (methods: start, stop)
#--------------------------------------------------------------------------------------------------------------

class LoadingScreen:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoadingScreen, cls).__new__(cls)
        return cls._instance

    def __init__(self, reason="loading"):
    #  Load stopped means that the load function has announced it's finished.
    #  Stop loading tells the load function to stop.
        self.load_stopped = threading.Event()
        self.stop_loading = threading.Event()
    
    def load(self, reason):
        hide_cursor()
        clear()
        animation = ["\\", "|", "/", "-"]
        index = 0
        while not self.stop_loading.is_set():
            clear()
            print(f"{reason.title()}... {animation[index]}")
            index = (index + 1) % len(animation)
            wait(0.1)
        self.load_stopped.set()
        show_cursor()
        clear()
    
    def stop(self):
    #  Tell the load function to stop, and wait for it to say it's done stopping.
        self.stop_loading.set()
        self.load_stopped.wait()

    def start(self, reason='loading'):
    #  Set up load_stopped and stop_loading.
        self.load_stopped.clear()
        self.stop_loading.clear()
        threading.Thread(target=self.load, args=(reason,)).start()

loading = LoadingScreen()

#--------------------------------------------------------------------------------------------------------------
#   3 - Enemy data + Class
#--------------------------------------------------------------------------------------------------------------

# Initialize enemy table
with open('enemies.json', 'r') as file:
    enemy_data = json.load(file)
ENEMIES = {
    'easy_dif':enemy_data['enemies']['easy'],
    'med_dif':enemy_data['enemies']['medium'],
    'hard_dif':enemy_data['enemies']['hard']
}  

easy='easy'
med='med'
hard='hard'

class NewEnemy(Entity):
    def __init__(self, difficulty=easy):
        enemy = random.choice(ENEMIES[f'{difficulty}_diff'])
        super().__init__(20)
        self.difficulty = difficulty
        self.description = enemy['name']
        self.room = enemy['room']

#--------------------------------------------------------------------------------------------------------------
#   4 - AI Functions/Class (methods: describe, ask, intent*)
#--------------------------------------------------------------------------------------------------------------


class AI():
    def __init__(self):
    #  Settings
        self.refresh = 3
        self.votes = 3
        self.basic_choices = {'check inventory'}
        self.version = 'llama3.2:latest'
        self.situation_context = []

    #  Statistics
        self.total_time = 0
        self.tries = 0
#  Ask a question and get the intent
    def ask(self, query, options):
        loading.start('Generating question')
        prompt = f'Make a forboding version of "{query}" in the absolute shortest way possible in question form. It should be in second person and not be encapsolated in quotation marks. Do not include any additional information in your output.'
        rephrase = ollama.generate(self.version, prompt)['response']
        loading.stop()
        return self.intent(input(rephrase + ' '), query, options)
#  Retrieve intent from a text.
    def intent(self, text, query, options, context=None, basic_options=False):
        refresh = 0
        intent_found = False
        start = time.time()
        while refresh < self.refresh:
            refresh += 1
            self.tries += 1
            loading.start('Grabbing intent')
        
        #  Assemble the options string
            if basic_options != False:
                basic_options = ['check inventory']
                options += basic_options
            option_string = f", ".join(list(options)) + f", ".join(list(basic_options)) if basic_options else ", ".join(options)

        #  Start grabbing intent votes
            prompt = f'Get user intention from the following text: "{text}" from the following context: "{query}" out of the following options: "{option_string}". Your output must STRICTLY be from the list of options. Explain your reasoning on a new line.'
            compilation = ''
            for i in range(self.votes):
                compilation += f'{ollama.generate(self.version, prompt)['response']},/n'
            loading.stop()

        #  Tally the vote
            loading.start('Analyzing')
            prompt = f"Look at the following and ONLY output the most commonly picked choice, NOT any kind of reasoning, punctuation, or list: [\n{compilation}]."
            outcome = ollama.generate(self.version, prompt)['response']

        #  Stop loading and return the outcome of the vote
            loading.stop()
            if outcome.lower().strip(', ."') in options:
                self.total_time += time.time()-start
                return outcome.lower().strip(', ."')
            print(f'{refresh}/{self.refresh}')
        print("Intent not found.")
    
ai = AI()

#--------------------------------------------------------------------------------------------------------------
#   Main Function
#--------------------------------------------------------------------------------------------------------------

def main():
    while True:
        clear()
        options = [
            'begin'
        ]
        user_input = ai.ask('Are you ready to start?', options)
        print(f'Average: {ai.total_time/ai.tries}')
        if user_input in options:
            wait(1.5)
            print(f'Success: {user_input}')
        else:
            print(user_input)
main()