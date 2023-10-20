import sys, select, time, os, subprocess, sys

if "OPENAI_API_KEY" not in os.environ:
  print("You must set an OPENAI_API_KEY environment variable.", file=sys.stderr)
else:
  

  print("== First Advantage Demonstration ==")
  print ("You have five seconds to select an option")
  print()
  print("1: Load Matrix\n2: Talk to your Bot\n> ", end="")
  
  i, o, e = select.select( [sys.stdin], [], [], 10 )
  print()
  
  if (i):
    choice = sys.stdin.readline().strip()
    time.sleep(0.5)
    os.system('clear')
    if choice == "1":
      print("LOAD MATRIX MODE")
      import parser
      parser.parse("simple-example-matrix.xls")
    elif choice == "2":
      print("CONVERSATION MODE")
      import chat
      chat.chat()
  sys.exit()
