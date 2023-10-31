"""First Advantage Demonstration script

Runs the demonstration for First Advantage (to be used during the workshop).
"""

import os
import select
import subprocess
import sys
import time
import AzureBlobUtil

_BLOB_FILE_NAME = "simple-example-matrix.csv"
_CONTAINER_NAME = "fa-test-container"
_AZURE_UTIL_INSTANCE = AzureBlobUtil.AzureBlobUtil()
# the below function pulls the file from blob storage on azure and writes it locally for loading and use
AzureBlobUtil.getFileFromBlob(_AZURE_UTIL_INSTANCE, _CONTAINER_NAME, _BLOB_FILE_NAME)

if "OPENAI_API_KEY" not in os.environ:
  print("You must set an OPENAI_API_KEY environment variable.", file=sys.stderr)
else:
  print("== First Advantage Demonstration ==")
  print ("You have five seconds to select an option")
  print()
  print("1: File statistics\n2: Query the client matrix via chat\n> ", end="")
  
  # var to account for clear vs cls depending on the OS; defaults to Unix-like clear 
  clearCommand = "clear"

  if sys.platform == 'win32':
      # windows does not support select() for anything except sockets
      # https://docs.python.org/3.11/library/select.html
      i = sys.stdin
      o = []
      e = []
      clearCommand = "cls"
  else:
    i, o, e = select.select( [sys.stdin], [], [], 10 )
  print()
  
  if (i):
    choice = sys.stdin.readline().strip()
    time.sleep(0.5)
    os.system(clearCommand)
    if choice == "1":
      print("FILE STATISTICS")
      import parser
      parser.statistics(file_name=_BLOB_FILE_NAME, raw=True)
    elif choice == "2":
      print("CONVERSATION MODE")
      import chat
      chat.chat(_BLOB_FILE_NAME)
  sys.exit()
