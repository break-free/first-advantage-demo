# first-advantage-demo

Demonstration code to illustrate possibilities during planned First Advantage workshop.

# Installation

To install, download the repo:

    git clone https://github.com/break-free/first-advantage-demo
    cd first-advantage-demo

Setup and activate a Python virtual environment:

    pip -m venv .venv-first-advantage-demo
    source .venv-first-advantage-demo/bin/activate
    pip install -r requirements.txt

Run the demonstration:

    python demo.py

# TODO

- [ ] Improve prompts so that the used CSV files are better interpreted by the LLM.
    - Perhaps use the LLM to work out the correct prompt...?
    - `promptfoo` is a project we could also use; [linked here](https://github.com/promptfoo/promptfoo).
    - Another is LangSmith, which we should ask for from the LangChain team.
- [ ] Build a document store using the `parser.py` file.

# Completed TODO's

- [x] Template files loaded to repo.

Note that the files originate from this repo:
[breakfree-dk-with-openai-chat](https://github.com/break-free/breakfree-dk-with-openai-chat/tree/main)

- [x] Build a chat interface using the `chat.py` file.

Basic functionality added so queries are sent and answers received from OpenAI.

- [x] Get the chat interface and document store linked up.

Completed using a CSV file and passing the entire file to ChatGPT v4 to answer questions. The
parser file is not being used.
