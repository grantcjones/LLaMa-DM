import ollama

# TODO: update to real Modelfile values
npc = ollama.copy('llama3.1', 'NPCs/edward')

edward='''
FROM llama3.2
SYSTEM Your name is Edward. You have only the knowledge a medieval peasant would, and you exist in a dark fantasy context."
'''

for response in ollama.create(model='NPCs/edward', modelfile=edward, stream=True):
  print(response)

