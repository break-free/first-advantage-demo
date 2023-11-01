"""Chat Interface

Starts a simple chat interface in the console. It uses a Large Language Model to interpret the
queries and respond back to the user, using an attached document store as a reference.

This file can be imported as a module and contains the following functions:

    * chat: Loads a document store and starts a chat interface to query it.
"""
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import Prompt

def test_single_file(file_name: str):
  """ Load a document store and test it using expected questions.

  Parameters
  ---
  file_name: str
    The name of the file.
  """

  # Import document(s) for context
  contents = ""
  with open(file_name, "r") as f:
    contents = f.read()

  # Setup
  with open("master.prompt", "r") as f:
    promptTemplate = f.read()
  prompt = Prompt(template=promptTemplate, input_variables=["question", "context", "history"])
  llmChain = LLMChain(prompt=prompt, llm=ChatOpenAI(temperature=0.1, model_name="gpt-4"))

  # Testing
  history = []
  _list_of_states = ["Wisconsin",
                     "New York"]
  _list_of_offences = ["Alcohol",
                       "Public Nuisance",
                       "Injury",
                       "Child Endangerment",
                       "Gambling"]
  results = {}
  for state in _list_of_states:
    for offence in _list_of_offences:
      question = (
          f"""If I live in {state} and have an {offence}, am I eligible, decisional, """
          f"""ineligible, or something else?"""
          )
      answer = llmChain.predict(question=question, context=contents, history=history)
      results[f"""{offence} in {state}"""] = answer

  # Print results
  for key, value in results.items():
      print(f"""{key} : {value}""")
