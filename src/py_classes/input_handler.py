from src.py_classes.imports import *

# static class
class InputHandler:
    def getIntFromInput(message):
        while True: 
            try:
                x = int(input(message))
                if (x >= 1):
                    return x
                else:
                    print("Invalid Input -- Must be >= 1")
            except ValueError:
                print("Invalid Input -- Must be Integer")


    # validates yes/no (boolean) input from standard input
    def getBoolFromInput(message):
        while True:
            answer = input(message).lower()
            if (answer == 'y' or answer == 'yes'):
                return True
            elif (answer == 'n' or answer == 'no'):
                return False
            else:
                print("Invalid Input -- Must be Yes/No or Y/N")

    # validates positive float input from standard input
    def getFloatFromInput(message):
        while True: 
            try:
                x = float(input(message))
                if (x > 0.0):
                    return x
                else:
                    print("Invalid Input -- Must be > 0.0")
            except ValueError:
                print("Invalid Input -- Must be > 0.0")

    def getItemFromListFromInput(message, list, secondaryList = []):
        while True: 
            x = input(message)
            if (x in map(lambda x : str(x), list)):
                return x
            else:
                if len(secondaryList) == 0:
                    print("Invalid Input -- Must be in list:\n\t" + ", ".join(list))
                else:
                    print("Invalid Input -- Must be in list:\n\t" + ", ".join(secondaryList))
    