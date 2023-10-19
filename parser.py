# TODO: Update this function to parse a Microsoft Excel file using an available document
#       loader.
def parse():
  print("Parse some data ... eventually. TODO!")


# trainingData = list(Path("training/facts/").glob("**/*.txt"))
#
#   #check there is data in the trainingData folder
#
#   if len(trainingData) < 1:
#     print("The folder training/facts should be populated with at least one .txt file.", file=sys.stderr)
#     return
#
#   data = []
#   for training in trainingData:
#     with open(training) as f:
#       print(f"Add {f.name} to dataset")
#       data.append(f.read())
#
#   textSplitter = CharacterTextSplitter(chunk_size=2000, separator="\n")
#
#   docs = []
#   for sets in data:
#     docs.extend(textSplitter.split_text(sets))
#
#   store = FAISS.from_texts(docs, OpenAIEmbeddings())
#   faiss.write_index(store.index, "training.index")
#   store.index = None
#
#   with open("faiss.pkl", "wb") as f:
#     pickle.dump(store, f)
