import random as __rnd
import math as __math
import numpy as __np
from decimal import Decimal as __Deci

def GenerateKeyPair(keysize):
    print("Generating p, q and n")
    n, p, q = __Internal_GenerateN(int(__Deci((2 ** keysize) - 1).sqrt()))
    print("n = " + str(n) + " (" + str(n.bit_length()) + " bits)")
    
    print("")
    
    print("Calculating λ(n) = lcm(p - 1, q - 1)")
    tot = __Internal_FindLeastCommonMultiple(p - 1, q - 1)
    print("λ(n) = " + str(tot) + " (" + str(tot.bit_length()) + " bits)")

    print("")

    print("Generating public key")
    e = __Internal_GeneratePublicKey(tot, keysize)
    print("pub = " + str(e) + " (" + str(e.bit_length()) + " bits)")

def __Internal_GenerateN(limit):
    
    p = __Internal_GetPrime(limit)
    print("p = " + str(p) + " (" + str(p.bit_length()) + " bits)")
    q = __Internal_GetPrime(limit)
    print("q = " + str(q) + " (" + str(q.bit_length()) + " bits)")

    return p * q, p, q

def __Internal_GetPrime(limit):
    num = 0
    while True:
        num = __rnd.randint(0, limit)
        print(str(hex(num)), end="\r")
        if __Internal_IsPrime(num): break
    
    return num

def __Internal_IsPrime(num):
    if num < 2: return False
    if num == 2: return True
    if num & 0x01 == 0: return False
    n = int(num ** 0.5)
    for i in range(3, n, 2):
        if num % i == 0:
            return False
    
    return True

def __Internal_FindLeastCommonMultiple(num1, num2):
    lcm = int((num1 * num2) / __math.gcd(num1, num2))
    return lcm

def __Internal_GeneratePublicKey(tot, keysize):    
    while True:
        e = __rnd.randint(2, tot - 1)
        print(str(hex(e)), end="\r")
        if __math.gcd(e, tot) == 1:
            break
    return e

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="RSA keygen")
    parser.add_argument('--bits', '-b', dest='keysize', default=1024)
    args = parser.parse_args()
    GenerateKeyPair(int(args.keysize))