from src.py_classes.imports import *

def getOptionalArgs(accessor, algorithm):
    if algorithm in accessor['optionInfo'].OPTIONS['has_extra_args']:
        items = accessor['optionInfo'].callbacks[algorithm]()
        return map(lambda x : str(x), items)

def lfg_params():
    op_char = InputHandler.getItemFromListFromInput("Operator (*, +, -, ^): ", ['*', '+', '-', '^'])
    j = -1
    while not (j > 0):
        j = InputHandler.getIntFromInput("J Value: ")
        if not j > 0:
            print('Value must be greater than 0')
    k = -1
    while not (k > 0 and k != j):
        k = InputHandler.getIntFromInput("K Value: ")
        if not k > 0:
            print('Value must be greater than 0')
        if k == j:
            print('K and J must be different values')
    
    return [op_char, j, k]

def bbs_params():
    blum_prime_examples = "TODO"
    p = InputHandler.getIntFromInput("P Value (Blum Prime): ")
    while not isBlumPrime(p):
        print("Invalid Input -- P Value must be a Blum Prime.\n Examples: " + blum_prime_examples + ".")
        p = InputHandler.getIntFromInput("P Value (Blum Prime): ")
    q = InputHandler.getIntFromInput("Q Value (Blum Prime): ")
    while not isBlumPrime(q):
        print("Invalid Input -- Q Value must be a Blum Prime.\n Examples: " + blum_prime_examples + ".")
        q = InputHandler.getIntFromInput("Q Value (Blum Prime): ")
    return [p, q]

# checks if a number is a Blum Prime
def isBlumPrime(n):
    if n <= 1:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return n % 4 == 3

