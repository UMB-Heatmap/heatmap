# gets / sanitizes extra arguments for algorithms that require them
def getAlgoArgs(algo):
    if algo not in HAS_EXTRA_ARGS:
        return []
    # IMPORTANT: add case for each algorithm that requires extra arguments
    elif algo == 'lfg':
        op_char = input("Operator (*, +, -, ^): ")
        while op_char not in ['*', '+', '-', '^']:
            op_char = input("Invalid Input -- Select From Operators (*, +, -, ^): ")
        j = -1
        while not (j > 0):
            j = getIntFromInput("J Value: ")
        k = -1
        while not (k > 0 and k != j):
            k = getIntFromInput("K Value: ")
        
        return [op_char, j, k]
    
    elif algo == "bbs":
        p = getIntFromInput("P Value (Blum Prime): ")
        while not isBlumPrime(p):
            p = getIntFromInput("Invalid Input -- P Value must be a Blum Prime: ")
        q = getIntFromInput("Q Value (Blum Prime): ")
        while not isBlumPrime(q):
            q = getIntFromInput("Invalid Input -- Q Value must be a Blum Prime: ")
        return [p, q]

# checks if a number is a Blum Prime
def isBlumPrime(n):
    if n <= 1:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return n % 4 == 3