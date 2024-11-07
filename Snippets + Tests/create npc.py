import ollama

# TODO: update to real Modelfile values
npc = ollama.copy('llama3.2', 'NPCs/edward')

edward='''
FROM llama3.2
SYSTEM Your name is Kaelyn (you're male). You have only the knowledge a medieval blacksmith would, and you exist in a dark fantasy context."
'''

for response in ollama.create(model='Kaelyn', modelfile=edward, stream=True):
  print(response)

