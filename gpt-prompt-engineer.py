from prettytable import PrettyTable
import openai
import os
import sys
import time

# openai.api_key = "ADD YOUR KEY HERE" # enter your OpenAI API key here
if "OPENAI_API_KEY" not in os.environ:
  print("You must set an OPENAI_API_KEY environment variable.", file=sys.stderr)

def generate_candidate_prompts(description, test_cases, number_of_prompts):
  outputs = openai.ChatCompletion.create(
      model='gpt-4',
      messages=[
          {"role": "system", "content": """Your job is to generate system prompts for GPT-4, given a description of the use-case and some test cases.

The prompts you will be generating will be for classifiers, with 'true' and 'false' being the only possible outputs.

In your generated prompt, you should describe how the AI should behave in plain English. Include what it will see, and what it's allowed to output. Be creative in with prompts to get the best possible results. The AI knows it's an AI -- you don't need to tell it this.

You will be graded based on the performance of your prompt... but don't cheat! You cannot include specifics about the test cases in your prompt. Any prompts with examples will be disqualified.

Most importantly, output NOTHING but the prompt. Do not include anything else in your message."""},
          {"role": "user", "content": f"Here are some test cases:`{test_cases}`\n\nHere is the description of the use-case: `{description.strip()}`\n\nRespond with your prompt, and nothing else. Be creative."}
          ],
      temperature=.9,
      n=number_of_prompts)

  prompts = []

  for i in outputs.choices:
    prompts.append(i.message.content)
  return prompts

def test_candidate_prompts(test_cases, prompts):
  prompt_results = {prompt: {'correct': 0, 'total': 0} for prompt in prompts}

  # Initialize the table
  table = PrettyTable()
  table.field_names = ["Prompt", "Expected"] + [f"Prompt {i+1}-{j+1}" for j, prompt in enumerate(prompts) for i in range(prompts.count(prompt))]


  # Wrap the text in the "Prompt" column
  table.max_width["Prompt"] = 100

  num_test_cases = len(test_cases)
  count_test_case = 1
  for test_case in test_cases:
      print(f"Test Case no. {count_test_case} of {num_test_cases} total test cases.")
      num_prompts = len(prompts)
      count_prompt = 1
      row = [test_case['prompt'], test_case['answer']]
      for prompt in prompts:
          print(f"Prompt no. {count_prompt} of {num_prompts} total prompts in Test Case no. {count_test_case}")
          x = openai.ChatCompletion.create(
              model='gpt-3.5-turbo',
              messages=[
                  {"role": "system", "content": prompt},
                  {"role": "user", "content": f"{test_case['prompt']}"}
              ],
              logit_bias={
                  '1904': 100,  # 'true' token
                  '3934': 100,  # 'false' token
              },
              max_tokens=1,
              temperature=0,
          ).choices[0].message.content


          status = "✅" if x == test_case['answer'] else "❌"
          row.append(status)

          # Update model results
          if x == test_case['answer']:
              prompt_results[prompt]['correct'] += 1
          prompt_results[prompt]['total'] += 1
          count_prompt = count_prompt + 1

      table.add_row(row)
      count_test_case = count_test_case + 1

  print(table)

  # Calculate and print the percentage of correct answers and average time for each model
  best_prompt = None
  best_percentage = 0
  for i, prompt in enumerate(prompts):
      correct = prompt_results[prompt]['correct']
      total = prompt_results[prompt]['total']
      percentage = (correct / total) * 100
      print(f"Prompt {i+1} got {percentage:.2f}% correct.")
      if percentage > best_percentage:
          best_percentage = percentage
          best_prompt = prompt

  print(f"The best prompt was '{best_prompt}' with a correctness of {best_percentage:.2f}%.")

test_cases = [
    {
        'prompt': 'Find the best contact email on this site.',
        'answer': 'true'
    },
    {
        'prompt': 'who is the current president?',
        'answer': 'true'
    },
    {
        'prompt': 'order me a pizza',
        'answer': 'false'
    },
    {
        'prompt': 'what are some ways a doctor could use an assistant?',
        'answer': 'true'
    },
    {
        'prompt': 'write a speech on the danger of cults',
        'answer': 'false'
    },
    {
        'prompt': 'Make a reservation at The Accent for 9pm',
        'answer': 'false'
    },
    {
        'prompt': 'organize my google drive',
        'answer': 'false'
    },
    {
        'prompt': 'Find the highest-rated Italian restaurant near me.',
        'answer': 'true'
    },
    {
        'prompt': 'Explain the theory of relativity.',
        'answer': 'true'
    },
    {
        'prompt': 'What are the main differences between Python and Java programming languages?',
        'answer': 'true'
    },
    {
        'prompt': 'Translate the following English sentence to Spanish: "The weather today is great."',
        'answer': 'false'
    },
    {
        'prompt': 'Create a new event on my calendar for tomorrow at 2 pm.',
        'answer': 'false'
    },
    {
        'prompt': 'Write a short story about a lonely cowboy.',
        'answer': 'false'
    },
    {
        'prompt': 'Design a logo for a startup.',
        'answer': 'false'
    },
    {
        'prompt': 'Compose a catchy jingle for a new soda brand.',
        'answer': 'false'
    },
    {
        'prompt': 'Calculate the square root of 1999.',
        'answer': 'false'
    },
    {
        'prompt': 'What are the health benefits of yoga?',
        'answer': 'true'
    },
    {
        'prompt': 'find me a source of meat that can be shipped to canada',
        'answer': 'true'
    },
    {
        'prompt': 'Find the best-selling book of all time.',
        'answer': 'true'
    },
    {
        'prompt': 'What are the top 5 tourist attractions in Brazil?',
        'answer': 'true'
    },
    {
        'prompt': 'List the main ingredients in a traditional lasagna recipe.',
        'answer': 'true'
    },
    {
        'prompt': 'How does photosynthesis work in plants?',
        'answer': 'true'
    },
    {
        'prompt': 'Write a Python program to reverse a string.',
        'answer': 'false'
    },
    {
        'prompt': 'Create a workout routine for a beginner.',
        'answer': 'false'
    },
    {
        'prompt': 'Edit my resume to highlight my project management skills.',
        'answer': 'false'
    },
    {
        'prompt': 'Draft an email to a client to discuss a new proposal.',
        'answer': 'false'
    },
    {
        'prompt': 'Plan a surprise birthday party for my best friend.',
        'answer': 'false'
}]


description = "Decide if a task is research-heavy." # describe the classification task clearly
number_of_prompts = 3 # choose how many prompts you want to generate and test



candidate_prompts = generate_candidate_prompts(description, test_cases, number_of_prompts)
test_candidate_prompts(test_cases, candidate_prompts)
