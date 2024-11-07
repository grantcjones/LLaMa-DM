import ollama
import json
import os

def clear():
    print("\033[H\033[J")

npc_context = {}

with open(f'npc_context.json') as context_file:
    try:
        npc_context = json.load(context_file)
    except:
        ""

def talk_to_npc(name):
    context = []
    exit = False
    output = ''
    try:
        context = npc_context[f'{name}']
    except:
        npc_context[f'{name}'] = []
    

    while exit == False:
        user_input = input()
        if user_input != "exit":
            clear()
            stream = ollama.generate(
                model=f'{name}',
                prompt=user_input,
                stream=True,
                context=context
            )
            
            for chunk in stream:
                print(chunk['response'], end='', flush=True)
                try:
                    context = chunk['context']
                except:
                    ""
            print("\n")
        else:
            stream = ollama.generate(
                model=f'{name}',
                prompt='Say goodbye to the user',
                stream=True,
                context=context,
                keep_alive=0
            )
            for chunk in stream:
                print(chunk['response'], end='', flush=True)
                try:
                    context = chunk['context']
                except:
                    ""
            exit = True
    npc_context[f'{name}'] = context
    with open('npc_context.json', 'w') as f:
        json.dump(npc_context, f)


talk_to_npc('Kaelyn')
        


  

