from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import Prompt

def chat():

  # Import Document Store

  #TODO: Need to import from a local document store containing a representative-client matrix.

  # Setup and start chat

  with open("master.prompt", "r") as f:
    promptTemplate = f.read()

  prompt = Prompt(template=promptTemplate, input_variables=["history", "question"])

  llmChain = LLMChain(prompt=prompt, llm=OpenAI(temperature=0.25))

  def onMessage(question, history):
    #TODO: Need to search through a document store.
    #TODO: Need to update the `master.prompt` file with a "context" input variable.

    answer = llmChain.predict(question=question, history=history)
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
