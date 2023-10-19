# first-advantage-demo

Demonstration code to illustrate possibilities during planned First Advantage workshop.

# Installation

To install, download the repo:

    git clone https://github.com/break-free/first-advantage-demo
    cd first-advantage-demo

Setup and activate a Python virtual environment:

    pip -m venv .venv-first-advantage-demo
    source .venv-first-advantage-demo/bin/activate

Run the demonstration:

    python demo.py

> [!NOTE]
> Currently, the only option that works is conversation mode. The load matrix mode simply prints
> to screen that the function needs to be completed.

# TODO

- [ ] Build a document store using the `parser.py` file.
- [ ] Get the chat interface and document store linked up.

# Completed TODO's

- [x] Template files loaded to repo.

Note that the files originate from this repo:
[breakfree-dk-with-openai-chat](https://github.com/break-free/breakfree-dk-with-openai-chat/tree/main)

- [x] Build a chat interface using the `chat.py` file.

Basic functionality added so queries are sent and answers received from OpenAI.
