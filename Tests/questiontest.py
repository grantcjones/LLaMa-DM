import ollama
import time
VERSION = 'llama3.2:3B'

for i in range(15):
    question = ollama.generate(VERSION,"Generate just a simple math problem for someone with a high school sophomore math knowledge. Just output the operation.")
    answer = ollama.generate(VERSION, f"Tell me the answer to \"{question['response']}\"  with zero text or added input. Just the number.")
    print("--------------------------------------------------------------------------------")
    print(i)
    print(f"Question: {question['response']}")
    print(f"Answer: {answer['response']}")
    print("--------------------------------------------------------------------------------")
    print()
    time.sleep(0.5)


