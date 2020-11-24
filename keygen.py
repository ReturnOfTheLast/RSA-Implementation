import random as __rnd
import math as __math

def GenerateKeyPair():
    n, p, q = __Internal_GenerateN()

    print(str(p) + " " + str(q) + " " + str(n) + " ")

def __Internal_GenerateN():
    # Read file and extract prime numbers
    f = open("primenums.txt", "r")
    lines = f.readlines()
    f.close()

    primes = list()

    # Strip newlines
    for line in lines:
        primes.append(int(line.strip()))

    p, q = __rnd.sample(primes, k=2)

    return p * q, p, q

if __name__ == "__main__":
    GenerateKeyPair()