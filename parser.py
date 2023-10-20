"""Parser Functions

Contains functions for creating and manipulating a document store using First Advantage client
matrices.

This file can be imported as a module and contains the following functions:

    * parse: accepts a Microsoft Excel file and returns a document store.
"""

import os
import sys
import tiktoken
from langchain.document_loaders import CSVLoader
from langchain.document_loaders import UnstructuredExcelLoader

def parse(file_name: str):
  """ Returns a document store from a Microsoft Excel or CSV file.

  Parameters:
  ---
  file_name: str
    The name of the file.

  Returns:
  ---
  docs: list
    List of documents retrieved from file.
  """
  print("Parsing Excel file ...")
  docs = _load_file_to_list(file_name)
  while count < len(docs):
    print(f"\n\nDocument no. {count}\n\n{docs[count]}")
    count += 1
  print("Parsing complete!")
  return docs

def statistics(file_name: str, raw: bool=False):
  """Print relevant statistics for a file.

  Parameters:
  ---
  file_name: str
    The name of the file.
  raw: bool=False
    Whether to load using a document loader or raw (i.e., not parsed).
  """
  total_tokens = 0
  encoding = tiktoken.get_encoding("cl100k_base")
  if not raw:
    docs = _load_file_to_list(file_name)
    print(f"No. of document: {len(docs)}")
    for doc in docs:
      total_tokens = len(encoding.encode(doc))
      print(f"Average tokens per document: {total_tokens/len(docs)}")
  else:
    with open(file_name, "r") as f:
      contents = f.read()
      total_tokens = len(encoding.encode(contents))
  print(f"Total tokens: {total_tokens}")

def _load_file_to_list(file_name: str) -> list:
  """Loads a file using either a Excel of CSV document loader and returns a list.

  Parameters
  ---
  file_name: str
    The name of the file.

  Returns:
  ---
  docs: list
    List of documents retrieved from file.
  """
  docs = []
  file_extension =  os.path.splitext(file_name)[1]
  if file_extension in [".xls", ".xlsx"]:
    loader = UnstructuredExcelLoader(file_name, mode="elements")
  elif file_extension == ".csv":
    loader = CSVLoader(
      file_path=file_name,
      csv_args={
          "delimiter": ',',
          "quotechar": '"',
        },
      )
  else:
    print(f"File '{file_name}' is not supported.")
    sys.exit(0)
  docs = loader.load()
  return docs
