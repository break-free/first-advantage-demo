# TODO: This whole file.
import ???

# Import Document Store

index = faiss.read_index("training.index")

  with open("faiss.pkl", "rb") as f:
    store = pickle.load(f)

  store.index = index

# Setup and start chat

  with open("training/master.txt", "r") as f:
    promptTemplate = f.read()

  prompt = Prompt(template=promptTemplate, input_variables=["history", "context", "question"])

  llmChain = LLMChain(prompt=prompt, llm=OpenAI(temperature=0.25))

  def onMessage(question, history):
    docs = store.similarity_search(question)
    contexts = []
    for i, doc in enumerate(docs):
      contexts.append(f"Context {i}:\n{doc.page_content}")
      answer = llmChain.predict(question=question, context="\n\n".join(contexts), history=history)
    return answer

  history = []
  while True:
    question = input("Ask a question > ")
    answer = onMessage(question, history)
    print(f"Bot: {answer}")
    history.append(f"Human: {question}")
    history.append(f"Bot: {answer}")
