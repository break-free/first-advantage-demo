"""Parser Functions

Contains functions for creating and manipulating a document store using First Advantage client
matrices.

This file can be imported as a module and contains the following functions:

    * parse: accepts a Microsoft Excel file and returns a document store.
"""

from langchain.document_loaders import UnstructuredExcelLoader

# TODO: Update this function to parse a Microsoft Excel file using an available document
#       loader.
def parse(file_name: str):
  """ Returns a document store from a Microsoft Excel file.

  Parameters:
  ---
  file_name: str
    File name of the Excel file.

  Returns:
  ---
  ???
  """
  print("Parsing Excel file ...")

  docs = []

  with open(file_name, "r"):
    loader = UnstructuredExcelLoader(file_name, mode="elements")
    docs = loader.load()

  print(f"No. of document: {len(docs)}")
  count = 0
  while count < len(docs):
    print(f"\n\nDocument no. {count}\n\n{docs[count]}")
    count += 20

  print("Parsing complete!")


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
