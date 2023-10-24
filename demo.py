"""First Advantage Demonstration script

Runs the demonstration for First Advantage (to be used during the workshop).
"""

import os
import select
import subprocess
import sys
import time

_file_name = "simple-example-matrix.csv"

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
      parser.statistics(file_name=_file_name, raw=True)
    elif choice == "2":
      print("CONVERSATION MODE")
      import chat
      chat.chat(_file_name)
  sys.exit()
