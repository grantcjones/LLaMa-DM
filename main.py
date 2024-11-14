#--------------------------------------------------------------------------------------------------------------
#   MAIN.PY
#--------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------
#   Glossary
#--------------------------------------------------------------------------------------------------------------

    # Dependencies
        # 1 - Outside dependencies
        # 2 - Entities
        # 3 - AI
        # 4 - Simplicities

    # Main Function

#--------------------------------------------------------------------------------------------------------------
#   Outside dependancies
#--------------------------------------------------------------------------------------------------------------

import random
import json

#--------------------------------------------------------------------------------------------------------------
#   Entities
#--------------------------------------------------------------------------------------------------------------
import Modules.entity as entity

#--------------------------------------------------------------------------------------------------------------
#   Loading Screen
#--------------------------------------------------------------------------------------------------------------
from Modules.loading import LoadingScreen
loading = LoadingScreen()

#--------------------------------------------------------------------------------------------------------------
#   AI
#--------------------------------------------------------------------------------------------------------------
from Modules.ai import AI
ai = AI()

#--------------------------------------------------------------------------------------------------------------
#   Simplicities
#--------------------------------------------------------------------------------------------------------------
from Modules.simplify import wait
from Modules.simplify import clear
from Modules.simplify import show_cursor
from Modules.simplify import hide_cursor

#--------------------------------------------------------------------------------------------------------------
#   Main Function
#--------------------------------------------------------------------------------------------------------------

def test_delay():
    while True:
        clear()
        options = [
            'begin'
        ]
        user_input = ai.ask('Are you ready to start the game?', options)

        print(f'Average: {ai.total_time/ai.tries}')
        if user_input in options:
            wait(1.5)
            print(f'Success: {user_input}')
        else:
            print(user_input)

def main():
    player = entity.Player()
    while True:
        clear()
        options = [
            'begin'
        ]
        user_input = ai.ask('Are you ready to start the game?', options, True)
        print(f'Average: {ai.total_time/ai.tries}')
        if user_input in options:
            wait(1.5)
            print(f'Success: {user_input}')
        else:
            print(user_input)

if __name__ == '__main__':
    main()