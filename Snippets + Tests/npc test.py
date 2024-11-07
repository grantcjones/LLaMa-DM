import ollama
import json
import os

# edward='''
# FROM llama3.2
# You are a helpful assistant.
# '''

# npc = ollama.create('llama3.2', modelfile=edward)
# print(npc)


def clear():
    print("\033[H\033[J")

def talk_to_npc(name):
    context = []
    exit = False
    output = ''

    if os.path.isfile(f"{name}_context.json"):
        with open(f'{name}_context.json') as context_file:
            try:
                context = json.load(context_file)
            except:
                ""

    while exit == False:
        user_input = input()
        if user_input != "exit":
            clear()
            stream = ollama.generate(
                model=f'NPCs/{name}',
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
                model=f'NPCs/{name}',
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
    with open(f'{name}_context.json', 'w') as f:
        json.dump(context, f)

talk_to_npc('Kaelin')
        


  

