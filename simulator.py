# Driver program for site clearing simulation
# Author: Shahram Kalantari
# July 19, 2020

#!/usr/bin/python

import sys

from core.site_map import SiteMap
from core.bulldozer import Bulldozer

def help():
  """
  Provides a short description on how to run the program.
  Will be called whenever the program is called in an incorrect way
  """
  print("Please run the simulator according to the following insruction: ")
  print("python3 simulator.py <Path-to-sitemap-file>")

def readNextCommand():
  """
  Reads the user command. Accepts both lowercase and uppercase
  """
  command = input("(l)eft, (r)ight, (a)dvance <n>, (q)uit: ")
  return command.lower()

def isValid(commandStr):
  """
  Checks if the entered command is valid
  Returns True if the command is valid, Flase if invalid
  :param commandStr(str): entered command
  :rtype: bool
  """
  validCommands = ['left', 'l', 'right', 'r', 'quit', 'q']
  validMultipartCommands = ['advance', 'a']
  if commandStr in validCommands:
    return True
  for command in validMultipartCommands:
    # Only advance command is a two-part command
    if commandStr.startswith(command) and len(commandStr.split()) == 2:
      try:
        squares = int(commandStr.split()[1])
        # Number of advancement steps cannot be less than 1
        if squares <= 0:
          return False
        return True
      except ValueError:
        return False
  return False

# The main simulation process:
if __name__ == "__main__":
  if len(sys.argv) != 2:
    help()
    exit(1)

  # Read site map from the input file
  siteMapFile = sys.argv[1]
  try:
    siteMap = SiteMap(siteMapFile)
  except Exception as e:
    print(str(e))
    exit(1)

  # Create a bulldozer object on the created siteMap
  bulldozer = Bulldozer(siteMap)

  print("\nWelcome to the Aconex site clearing simulator. This is a map of the site:\n")
  bulldozer.siteMap.show()
  print("\nThe bulldozer is currently located at the Northern edge of the site, immediately to the West of the site, and facing East.\n")

  # While the user enters a non-quit command and bulldozer can accept commands, read the command
  command = readNextCommand()
  while True:
    # Check if the command is valid
    if isValid(command):
      try:
        # Apply the command on the bulldozer
        bulldozer.applyCommand(command)
      except Exception as e:
        # If the bulldozer moves out of the site, or moves on a protected tree, or enters the quit command
        # terminate the simulation by generating a report of command history and expenses
        print(str(e))
        print("The final status of the site is shown below: \n")
        bulldozer.siteMap.show()
        bulldozer.generateReport()
        break
    else:
      # Don't exit the program if the command is not valid, ask for a valid command instead
      print("{} is not an acceptable command, please try again.\n".format(command))

    # After each command, update the site map and show the progress to the user
    # The cleared area will be shown by '*' character
    bulldozer.siteMap.show()
    command = readNextCommand()

  print("\nThank you for using the Aconex site clearing simulator.\n")
