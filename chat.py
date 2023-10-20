"""Chat Interface

Starts a simple chat interface in the console. It uses a Large Language Model to interpret the
queries and respond back to the user, using an attached document store as a reference.

This file can be imported as a module and contains the following functions:

    * chat: Loads a document store and starts a chat interface to query it.
"""
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import Prompt

def chat(file_name: str):
  """ Load a document store and start a chat.

  Parameters
  ---
  file_name: str
    The name of the file.
  """

  # Import document(s) for context
  contents = ""
  with open(file_name, "r") as f:
    contents = f.read()

  # Setup and start chat

  with open("master.prompt", "r") as f:
    promptTemplate = f.read()

  prompt = Prompt(template=promptTemplate, input_variables=["question", "context", "history"])

  llmChain = LLMChain(prompt=prompt, llm=ChatOpenAI(temperature=0.1, model_name="gpt-4"))

  def onMessage(question, history):
    #TODO: Need to update the `master.prompt` file with a "context" input variable.

    answer = llmChain.predict(question=question, context=contents, history=history)
    return answer

  history = []
  while True:
    question = input("Ask a question > ")
    if question in ['exit', 'q', 'quit']:
        break
    answer = onMessage(question, history)
    print(f"Bot: {answer}")
    history.append(f"Human: {question}")
    history.append(f"Bot: {answer}")
