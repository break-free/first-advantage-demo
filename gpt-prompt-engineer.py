from prettytable import PrettyTable
import json
import openai
import os
import sys
import time

# openai.api_key = "ADD YOUR KEY HERE" # enter your OpenAI API key here
if "OPENAI_API_KEY" not in os.environ:
    print("You must set an OPENAI_API_KEY environment variable.", file=sys.stderr)

def generate_candidate_prompts(description, test_cases, context,
                               expected_results, number_of_prompts):
    outputs = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[
            {
                "role": "system",
                "content": f"Your job is to generate system prompts for GPT-4, given a description of the use-case and some test cases.\n\nThe prompts you will be generating will be determining the answers to a series of questions. The answer permitted for each question must be one of the following: {expected_results} .\n\nIn your generated prompt, you should describe how the AI should behave in plain English. Include what it will see, and what it's allowed to output. Be creative in with prompts to get the best possible results. The AI knows it's an AI -- you don't need to tell it this.\n\nYou will be graded based on the performance of your prompt... but don't cheat! You cannot include specifics about the test cases in your prompt. Any prompts with examples will be disqualified.\n\nMost importantly, output NOTHING but the prompt. Do not include anything else in your message."},
            {
                "role": "user",
                "content": f"Here is the description of the use-case:\n\n`{description.strip()}`\n\nHere are some test cases:\n\n`{test_cases}`\n\nHere is the employers eligibility matrix (provided as comma separated values):\n\n`{context}`\n\nRespond with your prompt, and nothing else. Be creative."
            }
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
    table.field_names = ["Question", "Expected"] + [f"Prompt {i+1}-{j+1}" for j, prompt in enumerate(prompts) for i in range(prompts.count(prompt))]

    # Wrap the text in the "Question" and "Prompt" columns
    table.max_width["Question"] = 100
    table.max_width["Prompt"] = 100

    num_test_cases = len(test_cases)
    count_test_case = 1
    for test_case in test_cases:
        print(f"Test Case no. {count_test_case} of {num_test_cases} total test cases.")
        num_prompts = len(prompts)
        count_prompt = 1
        row = [test_case['question'], test_case['result']]
        for prompt in prompts:
            print(f"Prompt no. {count_prompt} of {num_prompts} total prompts in Test Case no. {count_test_case}")
            x = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": f"{test_case['question']}"}
                    ],
                max_tokens=200,
                temperature=0,
                ).choices[0].message.content

            status = f"✅ {x}" if x == test_case['result'] else f"❌ {x}"
            row.append(status)

            # Update model results
            if x == test_case['result']:
                prompt_results[prompt]['correct'] += 1
            prompt_results[prompt]['total'] += 1

            count_prompt = count_prompt + 1

        table.add_row(row)
        count_test_case = count_test_case + 1
        # add delay to prevent time-outs
        time.sleep(30)

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

# describe the classification task clearly
description = "Decide if an applicant is eligible using an employers eligibility matrix."
# choose how many prompts you want to generate and test
number_of_prompts = 1

with open('test_cases.json') as f_test_cases:
    file_test_cases = json.load(f_test_cases)

# build adjudication test cases
test_cases = []
expected_results = set()
for test_case in file_test_cases["adjudication test cases"]:
    # pull data from the `test_cases.json` file
    state = test_case["state"]
    charge = test_case["charge category"]
    level = test_case["charge level"]
    result = test_case["result"]
    # build and store the question and result
    question = f"""If I live in {state} and have a {level} {charge} offence, am I eligible, decisional, or ineligible?"""
    test_cases.append({"question": question, "result": result})
    expected_results.add(result)

# provide context from a file
with open(file_test_cases["client matrix"]) as f_context:
    context = f_context.read()

candidate_prompts = generate_candidate_prompts(description,
                                               test_cases,
                                               context,
                                               str(expected_results),
                                               number_of_prompts)
test_candidate_prompts(test_cases,
                       candidate_prompts)
