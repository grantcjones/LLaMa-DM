import ollama
import time

LEVELS = ['basic', 'intermediate', 'advanced', 'sat']

def generate_problem(difficulty):
    """Generates a math problem using AI based on the given difficulty."""
    if difficulty in ['easy', 'intermediate']:
        prompt = ollama.generate(
            "llama3.2:3b",
            f"Create a {difficulty} math problem without text. Provide the problem in the first section labeled 'Problem', "
            f"the correct answer as numbers only with no sign in the second section labeled 'Correct Answer', and a step-by-step explanation last section labeled 'explanation'."
        )
    else:
        prompt = ollama.generate(
            "llama3.2:3b",
            f"Create a {difficulty} math problem. Provide the problem in the first section labeled 'Problem', "
            f"the correct answer as numbers only with no sign in the second section labeled 'Correct Answer', and a step-by-step explanation last section labeled 'explanation'."
        )

    response = prompt['response']
    return parse_response(response)

def parse_response(response):
    """Parses the AI response into problem, answer, explanation, and tips."""
    print(response)
    lines = response.split('\n')
    print(lines)
    problem, answer, explanation= '', '', ''
    section = None

    for line in lines:
        if line in ['Problem', '**Problem**']:
            section = 'problem'
            continue  # Move to the next line
        elif line in ['Correct Answer:', '**Correct Answer:**']:
            section = 'answer'
            continue
        elif line in ['Explanation:', '**Explanation:**']:
            section = 'explanation'
            continue

        # Append lines to the appropriate section
        if section == 'problem':
            problem += line.strip() + ' '
            # print(problem)
        elif section == 'answer':
            answer += line.strip() + ' '
            # print(answer)
        elif section == 'explanation':
            explanation += line.strip() + ' '
            # print(explanation)

    return problem, answer, explanation

def adjust_level(current_level, problems_attempted, problems_solved, total_time):
    """Adjusts the difficulty level based on performance and timing."""
    success_rate = problems_solved / problems_attempted if problems_attempted else 0
    average_time = total_time / problems_attempted if problems_attempted else float('inf')

    if success_rate >= 0.7 and average_time < 300:
        next_index = min(LEVELS.index(current_level) + 1, len(LEVELS) - 1)
        new_level = LEVELS[next_index]
    elif success_rate < 0.4 or average_time > 600:
        prev_index = max(LEVELS.index(current_level) - 1, 0)
        new_level = LEVELS[prev_index]
    else:
        new_level = current_level

    return new_level