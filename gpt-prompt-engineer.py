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
                               expected_answers, number_of_prompts):
    outputs = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[
            {
                "role": "system",
                "content": f"Your job is to generate system prompts for GPT-4, given a description of the use-case and some test cases.\n\nThe prompts you will be generating will be determine the answers to a series of questions. The answer permitted for each question consists of only one of the following and no other text: {expected_answers}.\n\nIn your generated prompt, you should describe how the AI should behave in plain English. Include what it will see, and what it's allowed to output. Be creative when generating prompts to get the best possible answers.\n\nThe AI knows it's an AI -- you don't need to tell it this.\n\nYou will be graded based on the performance of your prompt... but don't cheat! You cannot include specifics about the test cases in your prompt. Any prompts with examples will be disqualified.\n\nMost importantly, output NOTHING but the prompt. Do not include anything else in your message."},
            {
                "role": "user",
                "content": f"Here is the description of the use-case:\n\n`{description.strip()}`\n\nHere is the employers eligibility matrix (provided as comma separated values) that must be included in your generated prompt (for reference):\n\n`{context}`\n\nHere are some test cases:\n\n`{test_cases}`\n\nRespond with your prompt, and nothing else. Be creative."
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
    table.max_width["Question"] = 50
    table.max_width["Prompt"] = 50

    num_test_cases = len(test_cases)
    count_test_case = 1
    for test_case in test_cases:
        print(f"Test Case no. {count_test_case} of {num_test_cases} total test cases.")
        num_prompts = len(prompts)
        count_prompt = 1
        row = [test_case['question'], test_case['answer']]
        for prompt in prompts:
            print(f"Prompt no. {count_prompt} of {num_prompts} total prompts in Test Case no. {count_test_case}")
            x = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": f"{test_case['question']}"}
                    ],
                max_tokens=500,
                temperature=0,
                ).choices[0].message.content

            status = f"✅ {x}" if x == test_case['answer'] else f"❌ {x}"
            row.append(status)

            # Update model results
            if x == test_case['answer']:
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
description = "Decide if a potential employee is eligible using an employer's eligibility matrix. The employer's eligibility matrix consists of at least one table, where the first column is a list of offences. The first row of each table (i.e., the headings) are possible eligibility statuses. A non-empty square in the table, e.q., an 'X', indicates that if a potential employee has this type of offence in their record, then the column heading is their eligibility status. Note that there is only one non-empty column in a row."
# choose how many prompts you want to generate and test
number_of_prompts = 2

with open('test_cases.json') as f_test_cases:
    file_test_cases = json.load(f_test_cases)

# build adjudication test cases
test_cases = []
expected_answers = set()
for test_case in file_test_cases["adjudication test cases"]:
    # pull data from the `test_cases.json` file
    state = test_case["state"]
    charge = test_case["charge category"]
    level = test_case["charge level"]
    answer = test_case["answer"]
    # build and store the question and answer
    question = f"""If I live in {state} and have a {charge} offence, am I eligible, decisional, or ineligible for a role?"""
    test_cases.append({"question": question, "answer": answer})
    expected_answers.add(answer)

# provide context from a file
with open(file_test_cases["client matrix"]) as f_context:
    context = f_context.read()

candidate_prompts = generate_candidate_prompts(description,
                                               test_cases,
                                               context,
                                               str(expected_answers),
                                               number_of_prompts)
test_candidate_prompts(test_cases,
                       candidate_prompts)